"""三段式流水线：元数据 → 摘要 → 分类导出。

每一段都有落盘与断点续跑能力：
    阶段 1  列表页   1 个请求/年       -> raw/cvpr{年}_metadata.json
    阶段 2  详情页   N 个请求，多线程  -> raw/cvpr{年}_abstracts.jsonl（逐条 append，可中断续跑）
    阶段 3  分类     纯本地计算        -> by_topic/*.csv + 统计文件
"""

import csv
import json
import os
from collections import Counter, OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

from .net import BASE_URL, Fetcher
from .parser import parse_abstract, parse_list_page
from .topics import OTHER, TOPIC_NAMES, TopicClassifier

CSV_FIELDS = [
    "paper_id", "year", "primary_topic", "all_topics", "topic_score", "confidence",
    "title", "authors", "n_authors", "pages", "has_abstract",
    "pdf_url", "supp_url", "detail_url", "abstract", "bibtex",
]


# ---------------------------------------------------------------- 通用 IO

def save_json(data, filepath) -> None:
    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def save_csv(rows: List[dict], filepath, fields: List[str]) -> None:
    with open(filepath, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def list_url(year: int) -> str:
    return "%s/CVPR%s?day=all" % (BASE_URL, year)


# ---------------------------------------------------------------- 阶段 1

def crawl_metadata(years: List[int], fetcher: Fetcher, raw_dir) -> List[dict]:
    """爬取各年份列表页并解析元数据。"""
    all_papers = []
    for year in years:
        url = list_url(year)
        print("[1/3] 拉取 CVPR%s 列表页: %s" % (year, url))
        html = fetcher.get_text(url)
        if html is None:
            print("      拉取失败，跳过该年份")
            continue

        papers = parse_list_page(html, year)
        print("      解析到 %d 篇（pdf %d，supp %d，bibtex %d）" % (
            len(papers),
            sum(1 for p in papers if p["pdf_url"]),
            sum(1 for p in papers if p["supp_url"]),
            sum(1 for p in papers if p["bibtex"]),
        ))
        save_json(papers, os.path.join(raw_dir, "cvpr%s_metadata.json" % year))
        all_papers.extend(papers)

    return all_papers


# ---------------------------------------------------------------- 阶段 2

def _load_abstract_cache(path) -> Dict[str, str]:
    cache = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except ValueError:
                    continue
                if record.get("abstract"):
                    cache[record["paper_id"]] = record["abstract"]
    return cache


def _fetch_one(paper: dict, fetcher: Fetcher):
    html = fetcher.get_text(paper["detail_url"])
    return paper["paper_id"], (parse_abstract(html) if html else "")


def crawl_abstracts(papers: List[dict], fetcher: Fetcher, cache_path,
                    workers: int = 6, limit: Optional[int] = None) -> Dict[str, str]:
    """并发抓取摘要，结果逐条追加到 jsonl，支持中断续跑。"""
    cache = _load_abstract_cache(cache_path)
    todo = [p for p in papers if p["paper_id"] not in cache]
    if limit is not None:
        todo = todo[:limit]

    print("[2/3] 待抓摘要 %d 篇（已有缓存 %d 篇），%d 线程" % (len(todo), len(cache), workers))
    if not todo:
        return cache

    done = 0
    failed = 0
    with open(cache_path, "a", encoding="utf-8") as fh, \
            ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_fetch_one, p, fetcher): p for p in todo}
        for future in as_completed(futures):
            paper_id, abstract = future.result()
            done += 1
            if abstract:
                cache[paper_id] = abstract
                fh.write(json.dumps({"paper_id": paper_id, "abstract": abstract},
                                    ensure_ascii=False) + "\n")
                fh.flush()
            else:
                failed += 1
            if done % 200 == 0 or done == len(todo):
                print("      进度 %d/%d（失败 %d）" % (done, len(todo), failed))

    return cache


# ---------------------------------------------------------------- 阶段 3

def classify_papers(papers: List[dict], abstracts: Dict[str, str],
                    classifier: TopicClassifier) -> List[dict]:
    """给每篇论文打方向标签。"""
    labeled = []
    for paper in papers:
        abstract = abstracts.get(paper["paper_id"], "")
        primary, labels, score, confidence = classifier.classify(paper["title"], abstract)
        record = dict(paper)
        record["abstract"] = abstract
        record["has_abstract"] = bool(abstract)
        record["primary_topic"] = primary
        record["all_topics"] = "|".join(labels)
        record["topic_score"] = score
        record["confidence"] = confidence
        labeled.append(record)
    return labeled


def _topic_filename(index: int, name: str) -> str:
    return "%02d_%s.csv" % (index, name)


def export(labeled: List[dict], out_dir, stats_only: bool = False) -> dict:
    """按方向拆分成文件并输出统计。"""
    by_topic_dir = os.path.join(out_dir, "by_topic")
    os.makedirs(by_topic_dir, exist_ok=True)

    # 全量表（含方向列）
    save_csv(labeled, os.path.join(out_dir, "00_ALL_labeled.csv"), CSV_FIELDS)

    # 每个方向一个文件：多标签命中即收录，用 is_primary 区分主/次
    grouped = {name: [] for name in TOPIC_NAMES}
    for record in labeled:
        for topic in record["all_topics"].split("|"):
            grouped.setdefault(topic, []).append(record)

    per_topic_fields = CSV_FIELDS[:2] + ["is_primary"] + CSV_FIELDS[2:]
    topic_counts = OrderedDict()
    for index, name in enumerate(TOPIC_NAMES, start=1):
        rows = grouped.get(name, [])
        topic_counts[name] = len(rows)
        if rows:
            with open(os.path.join(by_topic_dir, _topic_filename(index, name)),
                      "w", newline="", encoding="utf-8-sig") as fh:
                writer = csv.DictWriter(fh, fieldnames=per_topic_fields, extrasaction="ignore")
                writer.writeheader()
                for record in rows:
                    row = dict(record)
                    row["is_primary"] = int(record["primary_topic"] == name)
                    writer.writerow(row)

    # 统计
    primary_counter = Counter(r["primary_topic"] for r in labeled)
    no_abstract = sum(1 for r in labeled if not r["has_abstract"])
    low_conf = sum(1 for r in labeled if r["confidence"] < 0.2)
    multi_label = sum(1 for r in labeled if len(r["all_topics"].split("|")) > 1)

    stats = OrderedDict()
    stats["total_papers"] = len(labeled)
    stats["years"] = sorted(set(r["year"] for r in labeled))
    stats["papers_with_abstract"] = len(labeled) - no_abstract
    stats["papers_without_abstract"] = no_abstract
    stats["multi_label_papers"] = multi_label
    stats["low_confidence_papers"] = low_conf
    stats["primary_distribution"] = OrderedDict(
        sorted(primary_counter.items(), key=lambda kv: -kv[1]))
    stats["label_distribution"] = OrderedDict(
        sorted(topic_counts.items(), key=lambda kv: -kv[1]))

    save_json(stats, os.path.join(out_dir, "topic_stats.json"))
    _write_stats_md(stats, os.path.join(out_dir, "topic_stats.md"))
    return stats


def _write_stats_md(stats: dict, filepath) -> None:
    total = max(stats["total_papers"], 1)
    lines = [
        "# CVPR 论文方向分布统计",
        "",
        "- 年份: %s" % ", ".join(str(y) for y in stats["years"]),
        "- 论文总数: %d" % stats["total_papers"],
        "- 有摘要: %d / 缺摘要: %d" % (stats["papers_with_abstract"], stats["papers_without_abstract"]),
        "- 多标签论文: %d" % stats["multi_label_papers"],
        "- 低置信度论文（主次方向分差 < 20%%，建议复核）: %d" % stats["low_confidence_papers"],
        "",
        "## 主方向分布（每篇只计一次）",
        "",
        "| 方向 | 论文数 | 占比 |",
        "| --- | ---: | ---: |",
    ]
    for name, count in stats["primary_distribution"].items():
        lines.append("| %s | %d | %.1f%% |" % (name, count, 100.0 * count / total))

    lines += [
        "",
        "## 标签命中分布（多标签，一篇可计入多个方向）",
        "",
        "| 方向 | 命中数 | 占比 |",
        "| --- | ---: | ---: |",
    ]
    for name, count in stats["label_distribution"].items():
        lines.append("| %s | %d | %.1f%% |" % (name, count, 100.0 * count / total))

    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------- 可选：下载 PDF

def download_pdfs(labeled: List[dict], fetcher: Fetcher, pdf_dir,
                  topics: Optional[List[str]] = None, limit: Optional[int] = None) -> int:
    """按方向筛选后下载 PDF。默认不调用（全量约 20-60GB）。"""
    os.makedirs(pdf_dir, exist_ok=True)
    selected = [r for r in labeled
                if (topics is None or r["primary_topic"] in topics) and r["pdf_url"]]
    if limit is not None:
        selected = selected[:limit]

    print("[PDF] 准备下载 %d 篇 -> %s" % (len(selected), pdf_dir))
    ok = 0
    for i, record in enumerate(selected, start=1):
        name = "".join(c if c not in '<>:"/\\|?*' else "_" for c in record["title"])[:120]
        filepath = os.path.join(pdf_dir, "%s_%s.pdf" % (record["year"], name))
        if fetcher.download(record["pdf_url"], filepath):
            ok += 1
        if i % 20 == 0:
            print("      进度 %d/%d（成功 %d）" % (i, len(selected), ok))
    return ok
