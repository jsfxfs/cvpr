# -*- coding: utf-8 -*-
"""查看第一轮统计中关键方向的标题样本。"""
import json

from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.load(open(HERE / "niche_probe_results.json", encoding="utf-8"))
for k in ["RAG", "3DGS_security", "3DGS_quality", "3DGS_compress", "Spatial_reason", "Agent", "TestTime", "Token_eff"]:
    print("=" * 20, k, "=" * 20)
    for t in d[k]["titles_2026"][:14]:
        print(" -", t)
