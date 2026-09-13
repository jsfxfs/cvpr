# -*- coding: utf-8 -*-
"""执行重命名(两阶段防冲突) + 同步更新文内相对链接 + 链接完整性检查(临时脚本)"""
import os, re, sys, json

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = r'e:/Work/yan1/early_explore/paper/06_Java全栈知识体系'
MAPF = r'e:/Work/yan1/early_explore/paper/_rename_map.json'

LINK = re.compile(r'(?<!!)\[([^\]]*)\]\(([^()\s]+)\)')


def resolve_link(src_rel, href):
    """把文件内相对链接解析为相对 ROOT 的绝对路径(旧名)"""
    base = href.split('#', 1)[0]
    if not base or '://' in base or base.startswith('mailto:'):
        return None
    d = os.path.dirname(src_rel)
    return os.path.normpath(os.path.join(d, base) if d else base).replace('\\', '/')


def scan_broken():
    broken = []
    for dirpath, _, files in os.walk(ROOT):
        for f in files:
            if not f.endswith('.md'):
                continue
            fp = os.path.join(dirpath, f)
            rel = os.path.relpath(fp, ROOT).replace('\\', '/')
            try:
                txt = open(fp, encoding='utf-8').read()
            except Exception:
                continue
            for m in LINK.finditer(txt):
                href = m.group(2)
                if not href.endswith('.md') and '.md#' not in href:
                    continue
                t = resolve_link(rel, href)
                if t and not os.path.exists(os.path.join(ROOT, t.replace('/', os.sep))):
                    broken.append((rel, href))
    return broken

# ---- 基线：重命名前的坏链数量 ----
base_broken = scan_broken()
print('BASELINE_BROKEN_LINKS:', len(base_broken))

plan = json.load(open(MAPF, encoding='utf-8'))
# 去掉变体选择符(如 ❤️ 的 U+FE0F),避免奇怪的不可见字符
for x in plan:
    x['new'] = x['new'].replace('\ufe0f', '')
old2new = {x['old']: x['new'] for x in plan}

# ---- 阶段1: 旧名 -> 临时名 ----
tmpmap = {}
for i, x in enumerate(plan):
    old_abs = os.path.join(ROOT, x['old'].replace('/', os.sep))
    tmp = old_abs + '.renametmp%d' % i
    os.rename(old_abs, tmp)
    tmpmap[x['old']] = tmp

# ---- 阶段2: 临时名 -> 中文名 ----
errs = []
for x in plan:
    new_abs = os.path.join(ROOT, x['new'].replace('/', os.sep))
    try:
        os.rename(tmpmap[x['old']], new_abs)
    except Exception as e:
        errs.append((x['old'], x['new'], str(e)))
        os.rename(tmpmap[x['old']], os.path.join(ROOT, x['old'].replace('/', os.sep)))
print('RENAME_ERRORS:', len(errs))
for e in errs[:20]:
    print('   ERR:', e)

# ---- 更新文内链接 ----
changed = 0
for x in plan:
    fp = os.path.join(ROOT, x['new'].replace('/', os.sep))
    if not os.path.exists(fp):
        continue
    txt = open(fp, encoding='utf-8').read()
    d = os.path.dirname(x['new'])

    def rep(m):
        label, href = m.group(1), m.group(2)
        if '://' in href or href.startswith(('mailto:', '#')):
            return m.group(0)
        base, sep, frag = href.partition('#')
        if not base:
            return m.group(0)
        abs_old = resolve_link(x['new'], href)
        tgt = old2new.get(abs_old)
        if not tgt:
            return m.group(0)
        rel = os.path.relpath(tgt, d if d else '.').replace('\\', '/')
        return '[%s](%s%s)' % (label, rel, (sep + frag) if sep else '')

    new_txt = LINK.sub(rep, txt)
    if new_txt != txt:
        open(fp, 'w', encoding='utf-8').write(new_txt)
        changed += 1
print('FILES_WITH_LINK_UPDATES:', changed)

# ---- 重命名后的坏链检查 ----
after_broken = scan_broken()
print('AFTER_BROKEN_LINKS:', len(after_broken))
new_breaks = [b for b in after_broken if b not in base_broken]
print('NEWLY_BROKEN_BY_RENAME:', len(new_breaks))
for b in new_breaks[:30]:
    print('   BROKEN:', b[0], '->', b[1])

cnt = sum(1 for dp, _, fs in os.walk(ROOT) for f in fs if f.endswith('.md'))
print('FINAL_MD_COUNT:', cnt)
