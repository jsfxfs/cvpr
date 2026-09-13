# -*- coding: utf-8 -*-
"""查看第三轮统计中关键方向的标题样本。"""
import json

from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.load(open(HERE / "niche_probe3_results.json", encoding="utf-8"))
for k in ["Watermark_all", "RemoteSensing", "DocAI", "SamplingAccel", "VideoGen", "Jailbreak", "E2E_driving", "ModelCompress"]:
    print("=" * 20, k, "=" * 20)
    for t in d[k]["titles_2026"][:14]:
        print(" -", t)
    print()
