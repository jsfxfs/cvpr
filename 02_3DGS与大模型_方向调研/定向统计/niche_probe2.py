# -*- coding: utf-8 -*-
"""补充统计：长上下文 vs RAG、通用前馈模型提及量、前馈模型的微调/适配热度。

路径说明：语料在 05_CVPR数据与工具/ 下，脚本按自身位置定位，移动目录不需改代码。
"""
import csv, json
from collections import OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent.parent / "05_CVPR数据与工具"   # 语料目录
OUT = HERE / "niche_probe2_results.json"          # 结果输出（脚本同目录）

FILES = {
    2025: str(DATA / "cvpr_papers_2025" / "00_ALL_labeled.csv"),
    2026: str(DATA / "cvpr_papers" / "00_ALL_labeled.csv"),
}

GS_ANY = ["gaussian splatting", "3d gaussian", "3dgs"]

QUERIES = OrderedDict([
    ("LongContext",      {"any": ["long context", "long-context", "context window", "context length", "long sequence"]}),
    ("Retrieval_all",    {"any": ["retrieval"]}),
    ("RAG",              {"any": ["retrieval-augmented", "retrieval augmented"]}),
    ("VGGT",             {"any": ["vggt"]}),
    ("DUSt3R_family",    {"any": ["dust3r", "mast3r", "cut3r", "fast3r", "monst3r"]}),
    ("MVSplat_family",   {"any": ["mvsplat", "splatt3r", "latent splatting"]}),
    ("Uni3R_family",     {"any": ["uni3r", "splatpose"]}),
    ("FFGS_finetune",    {"any": ["fine-tun", "finetun", "adaptation", "adaptive", "test-time"],
                          "and": GS_ANY + ["feed-forward", "feedforward", "dust3r", "vggt", "generalizable reconstruction"]}),
    ("FFGS_uncertainty", {"any": ["uncertain"], "and": GS_ANY + ["feed-forward", "dust3r", "vggt"]}),
])


def load(path):
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            t = (row.get("title") or "").strip()
            a = (row.get("abstract") or "").strip()
            rows.append({"title": t, "text": (t + " . " + a).lower()})
    return rows


def match(row, spec):
    if not any(k in row["text"] for k in spec["any"]):
        return False
    if "and" in spec and not any(k in row["text"] for k in spec["and"]):
        return False
    return True


def main():
    data = {y: load(p) for y, p in FILES.items()}
    out = {}
    print(f"{'query':<20}{'2025':>6}{'2026':>6}{'growth':>9}")
    for name, spec in QUERIES.items():
        hits = {y: [r for r in data[y] if match(r, spec)] for y in (2025, 2026)}
        c25, c26 = len(hits[2025]), len(hits[2026])
        growth = (c26 - c25) / c25 * 100 if c25 else float("inf")
        print(f"{name:<20}{c25:>6}{c26:>6}{growth:>8.0f}%")
        out[name] = {
            "count_2025": c25,
            "count_2026": c26,
            "titles_2026": [r["title"] for r in hits[2026]][:25],
        }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nsaved -> %s" % OUT)


if __name__ == "__main__":
    main()
