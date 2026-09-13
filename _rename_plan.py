# -*- coding: utf-8 -*-
"""重命名预演 v2: 按 H1 生成中文文件名方案, 处理重名/特殊符号, 输出报告(临时脚本)"""
import os, re, sys, json, collections

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = r'e:/Work/yan1/early_explore/paper/06_Java全栈知识体系'
REPORT = r'e:/Work/yan1/early_explore/paper/_rename_report.txt'
ILLEGAL = {'\\': '-', '/': '-', ':': '：', '*': '', '?': '？', '"': '',
           '<': '', '>': '', '|': '-',
           '▶': '-', '►': '-', '◆': '-', '■': '-', '●': '-', '▪': '-'}


def clean(name):
    for k, v in ILLEGAL.items():
        name = name.replace(k, v)
    name = name.replace('`', '').replace('**', '').replace('*', '')
    name = re.sub(r'\s+', ' ', name).strip().strip('.')
    name = re.sub(r'[-\s]+$', '', name)
    if len(name) > 80:
        name = name[:80].rstrip()
    return name


files = []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if f.lower().endswith('.md'):
            files.append(os.path.join(dp, f))
files.sort()

plan = []
for p in files:
    rel = os.path.relpath(p, ROOT).replace('\\', '/')
    first = ''
    with open(p, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if line.startswith('# '):
                first = line[2:].strip()
                break
    plan.append({'old': rel, 'title': first, 'new': None})

# 生成目标名(带重名去重)
used = set()
for x in plan:
    d = os.path.dirname(x['old'])
    if x['title']:
        base = clean(x['title'])
    else:
        base = os.path.splitext(os.path.basename(x['old']))[0]
    cand = base
    n = 2
    key = lambda nm: ((d + '/' + nm).casefold())
    while key(cand + '.md') in used:
        cand = '%s (%d)' % (base, n)
        n += 1
    used.add(key(cand + '.md'))
    x['new'] = ((d + '/' + cand + '.md') if d else cand + '.md')

rep = []
rep.append('TOTAL: %d' % len(plan))

dups = [k for k, v in collections.Counter(x['new'].casefold() for x in plan).items() if v > 1]
rep.append('FINAL_DUPLICATES: %d %s' % (len(dups), dups))

no_h1 = [x for x in plan if not x['title']]
rep.append('NO_H1 (keep old name): %d' % len(no_h1))
for x in no_h1:
    rep.append('   %s' % x['old'])

suffix2 = [x for x in plan if re.search(r' \(\d\)\.md$', x['new'])]
rep.append('DEDUP_SUFFIX (%d):' % len(suffix2))
for x in suffix2:
    rep.append('   %s -> %s   [title=%s]' % (x['old'], x['new'], x['title']))

same = [x for x in plan if x['old'] == x['new']]
rep.append('UNCHANGED: %d' % len(same))
for x in same:
    rep.append('   %s   [title=%s]' % (x['old'], x['title'][:70]))

long_names = [x for x in plan if len(os.path.basename(x['new'])) > 60]
rep.append('LONG_NAMES: %d' % len(long_names))
for x in long_names:
    rep.append('   %d chars: %s' % (len(os.path.basename(x['new'])), x['new']))

# 新名是否撞到"其他文件当前的旧名"
old_by_key = {x['old'].casefold(): x['old'] for x in plan}
clash = [x for x in plan
         if x['old'] != x['new'] and x['new'].casefold() in old_by_key
         and old_by_key[x['new'].casefold()] != x['old']]
rep.append('CLASH_WITH_OTHER_OLDNAME: %d' % len(clash))
for x in clash:
    rep.append('   %s -> %s' % (x['old'], x['new']))

nonascii = [x for x in plan if re.search(r'[^\x00-\x7f]', x['new'])]
rep.append('HAS_NON_ASCII(new name): %d / %d' % (len(nonascii), len(plan)))

rep.append('--- SAMPLE 25 ---')
for x in plan[:25]:
    rep.append('%s  ->  %s' % (x['old'], x['new']))

with open(REPORT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(rep))
with open(ROOT + '/../_rename_map.json', 'w', encoding='utf-8') as f:
    json.dump(plan, f, ensure_ascii=False, indent=1)

print('OK. report=%s map=_rename_map.json total=%d' % (REPORT, len(plan)))
print('DEDUP:', len(suffix2), 'NO_H1:', len(no_h1), 'UNCHANGED:', len(same),
      'CLASH:', len(clash), 'LONG:', len(long_names))
