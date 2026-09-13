# -*- coding: utf-8 -*-
"""查看第二轮补充统计的标题样本。"""
import json

from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.load(open(HERE / "niche_probe2_results.json", encoding="utf-8"))
for k in ["VGGT", "FFGS_finetune", "RAG"]:
    print("=" * 20, k, "=" * 20)
    for t in d[k]["titles_2026"][:18]:
        print(" -", t)
