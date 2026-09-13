# -*- coding: utf-8 -*-
"""针对候选细分方向的定向统计：CVPR 2025 vs 2026（标题+摘要关键词命中）。

路径说明：语料在 05_CVPR数据与工具/ 下，脚本按自身位置定位，移动目录不需改代码。
"""
import csv, json
from collections import OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent.parent / "05_CVPR数据与工具"   # 语料目录
OUT = HERE / "niche_probe_results.json"           # 结果输出（脚本同目录）

FILES = {
    2025: str(DATA / "cvpr_papers_2025" / "00_ALL_labeled.csv"),
    2026: str(DATA / "cvpr_papers" / "00_ALL_labeled.csv"),
}

GS_ANY = ["gaussian splatting", "3d gaussian", "3dgs"]

QUERIES = OrderedDict([
    # ---- 3DGS 家族 ----
    ("3DGS_total",        {"any": GS_ANY}),
    ("3DGS_feedforward",  {"any": GS_ANY, "and": ["feed-forward", "feedforward", "generalizable", "amortized"]}),
    ("3DGS_semantic",     {"any": GS_ANY, "and": ["semantic", "open-vocabulary", "language", "clip", "text-driven", "referring"]}),
    ("3DGS_vlm",          {"any": GS_ANY, "and": ["vlm", "mllm", "language model", "llm", "gpt"]}),
    ("3DGS_compress",     {"any": GS_ANY, "and": ["compress", "compact", "prun", "quantiz", "codebook", "lightweight"]}),
    ("3DGS_edit",         {"any": GS_ANY, "and": ["edit", "composition", "compositional", "manipulat"]}),
    ("3DGS_security",     {"any": GS_ANY, "and": ["watermark", "backdoor", "adversarial", "copyright", "security"]}),
    ("3DGS_quality",      {"any": GS_ANY, "and": ["quality assessment", "no-reference", "artifact", "failure", "distortion"]}),
    ("3DGS_slam",         {"any": GS_ANY, "and": ["slam", "localization", "relocalization", "camera pose", "pose estimation"]}),
    ("3DGS_sparse",       {"any": GS_ANY, "and": ["sparse view", "sparse-view", "few-shot", "single image", "single-view", "two-view", "few view"]}),
    ("3DGS_dynamic",      {"any": GS_ANY, "and": ["dynamic", "4d", "deform", "temporal"]}),
    ("3DGS_human",        {"any": GS_ANY, "and": ["human", "avatar", "head", "talking", "hand", "body"]}),
    ("3DGS_driving",      {"any": GS_ANY, "and": ["driving", "autonomous", "lidar", "vehicle"]}),
    ("3DGS_relight",      {"any": GS_ANY, "and": ["relighting", "inverse rendering", "material", "intrinsic", "illumination"]}),
    ("3DGS_domain",       {"any": GS_ANY, "and": ["remote sensing", "aerial", "satellite", "uav", "medical", "endoscop", "underwater", "heritage"]}),
    ("3DGS_generative",   {"any": GS_ANY, "and": ["text-to-3d", "generation", "diffusion", "generative"]}),
    ("3DGS_worldmodel",   {"any": GS_ANY, "and": ["world model", "forecast", "predictive"]}),
    # ---- 大模型家族 ----
    ("MLLM_base",         {"any": ["mllm", "multimodal large language", "vision-language model", "large language model", "llm", "vlm"]}),
    ("RAG",               {"any": ["retrieval-augmented", "retrieval augmented"]}),
    ("Agent",             {"any": ["gui agent", "llm agent", "language agent", "multi-agent", "agentic", "tool use", "tool-use"]}),
    ("Token_eff",         {"any": ["token pruning", "token compression", "token merging", "token reduction", "visual token", "kv cache", "token budget"]}),
    ("Hallucination",     {"any": ["hallucination"]}),
    ("TestTime",          {"any": ["test-time", "test time"]}),
    ("PEFT",              {"any": ["lora", "parameter-efficient", "low-rank adaptation"]}),
    ("Spatial_reason",    {"any": ["spatial reasoning", "spatial understanding", "spatial intelligence", "spatial awareness"]}),
    ("RL_post",           {"any": ["grpo", "rlhf", "dpo", "preference optimization", "reward model", "reinforcement fine-tuning"]}),
    ("Benchmark_llm",     {"any": ["benchmark"], "and": ["llm", "vlm", "mllm", "multimodal large", "language model"]}),
    ("Quant_llm",         {"any": ["quantization"], "and": ["llm", "vlm", "language model", "large model", "transformer"]}),
    ("Unlearning",        {"any": ["unlearning"]}),
    ("Knowledge_edit",    {"any": ["knowledge editing", "model editing"]}),
])


def load(path):
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            t = (row.get("title") or "").strip()
            a = (row.get("abstract") or "").strip()
            rows.append({"title": t, "text": (t + " . " + a).lower(), "title_l": t.lower()})
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
    print(f"{'query':<20}{'2025':>6}{'2026':>6}{'growth':>9}{'2026标题命中':>12}")
    for name, spec in QUERIES.items():
        r = {}
        for y in (2025, 2026):
            hits = [row for row in data[y] if match(row, spec)]
            r[y] = hits
        c25, c26 = len(r[2025]), len(r[2026])
        growth = (c26 - c25) / c25 * 100 if c25 else float("inf")
        t26 = sum(1 for row in r[2026] if any(k in row["title_l"] for k in spec["any"]))
        print(f"{name:<20}{c25:>6}{c26:>6}{growth:>8.0f}%{t26:>12}")
        out[name] = {
            "count_2025": c25,
            "count_2026": c26,
            "titles_2026": [row["title"] for row in r[2026]][:40],
            "titles_2025": [row["title"] for row in r[2025]][:20],
        }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nsaved -> %s" % OUT)


if __name__ == "__main__":
    main()
