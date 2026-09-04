"""CVPR 论文爬取 + 方向分类 入口。

用法：
    python run_cvpr.py                      # 全量跑 CVPR2026
    python run_cvpr.py --limit 30           # 只抓 30 篇摘要，快速试跑
    python run_cvpr.py --years 2025 2026    # 多年份
    python run_cvpr.py --workers 8 --delay 0.4
    python run_cvpr.py --skip-abstracts     # 只重跑分类（改完词表后用）
    python run_cvpr.py --pdf-topic Diffusion_Generative   # 只下某个方向的 PDF
"""

import argparse
import os
import random
import sys
from typing import List, Optional

from cvpr.net import Fetcher
from cvpr.pipeline import (crawl_abstracts, crawl_metadata, classify_papers,
                           download_pdfs, export)
from cvpr.topics import TopicClassifier

# ============ 配置区 ============
YEARS = [2026]          # 要爬的年份（CVPR2026 共 4042 篇）
OUTPUT_DIR = "./cvpr_papers"
WORKERS = 6             # 抓摘要的并发线程数
DELAY = 0.5             # 每线程每次请求后的基础延时（秒）
RETRIES = 4
SAMPLE = 15             # 结束时打印的抽查样例数
# ================================


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CVPR 论文爬取与方向分类")
    parser.add_argument("--years", type=int, nargs="+", default=YEARS)
    parser.add_argument("--out", default=OUTPUT_DIR)
    parser.add_argument("--workers", type=int, default=WORKERS)
    parser.add_argument("--delay", type=float, default=DELAY)
    parser.add_argument("--limit", type=int, default=None,
                        help="只抓前 N 篇摘要，用于试跑")
    parser.add_argument("--skip-abstracts", action="store_true",
                        help="跳过抓取，直接用缓存重跑分类")
    parser.add_argument("--sample", type=int, default=SAMPLE)
    parser.add_argument("--pdf-topic", nargs="+", default=None,
                        help="只下载指定方向的 PDF")
    parser.add_argument("--pdf-limit", type=int, default=None)
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    out_dir = os.path.abspath(args.out)
    raw_dir = os.path.join(out_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)

    fetcher = Fetcher(delay=args.delay, retries=RETRIES)
    year_tag = "_".join(str(y) for y in args.years)
    abstracts_path = os.path.join(raw_dir, "cvpr%s_abstracts.jsonl" % year_tag)

    # ---------- 阶段 1：元数据 ----------
    metadata_path = os.path.join(raw_dir, "cvpr%s_metadata.json" % year_tag)
    if os.path.exists(metadata_path) and args.skip_abstracts:
        import json
        with open(metadata_path, "r", encoding="utf-8") as fh:
            papers = json.load(fh)
        print("[1/3] 复用已缓存元数据 %d 篇" % len(papers))
    else:
        papers = crawl_metadata(args.years, fetcher, raw_dir)
        if not papers:
            print("未获取到任何论文，终止。")
            return 1
        import json
        with open(metadata_path, "w", encoding="utf-8") as fh:
            json.dump(papers, fh, ensure_ascii=False, indent=2)

    # ---------- 阶段 2：摘要 ----------
    if args.skip_abstracts:
        from cvpr.pipeline import _load_abstract_cache
        abstracts = _load_abstract_cache(abstracts_path)
        print("[2/3] 复用已缓存摘要 %d 篇" % len(abstracts))
    else:
        abstracts = crawl_abstracts(papers, fetcher, abstracts_path,
                                    workers=args.workers, limit=args.limit)

    # ---------- 阶段 3：分类 + 导出 ----------
    print("[3/3] 分类并导出 ...")
    classifier = TopicClassifier()
    labeled = classify_papers(papers, abstracts, classifier)
    stats = export(labeled, out_dir)

    # ---------- 抽查 ----------
    if args.sample > 0 and labeled:
        print("\n抽查 %d 篇（主方向 / 置信度 / 标题）：" % args.sample)
        pool = [r for r in labeled if r["has_abstract"]] or labeled
        for record in random.sample(pool, min(args.sample, len(pool))):
            print("  [%-30s] c=%.2f  %s" % (
                record["primary_topic"], record["confidence"], record["title"][:88]))

    print("\n完成。共 %d 篇，输出目录: %s" % (stats["total_papers"], out_dir))
    print("  全量表 : %s" % os.path.join(out_dir, "00_ALL_labeled.csv"))
    print("  分方向 : %s" % os.path.join(out_dir, "by_topic"))
    print("  统计   : %s" % os.path.join(out_dir, "topic_stats.md"))

    if args.pdf_topic:
        download_pdfs(labeled, fetcher, os.path.join(out_dir, "pdfs"),
                      topics=args.pdf_topic, limit=args.pdf_limit)

    return 0


if __name__ == "__main__":
    sys.exit(main())
