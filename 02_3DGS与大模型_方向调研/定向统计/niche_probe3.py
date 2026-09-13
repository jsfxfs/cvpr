# -*- coding: utf-8 -*-
"""第三轮定向统计：扫描 3D/大模型两条主线之外的其他方向（CVPR 2025 vs 2026）。

路径说明：语料在 05_CVPR数据与工具/ 下，脚本按自身位置定位，移动目录不需改代码。
"""
import csv, json
from collections import OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent.parent / "05_CVPR数据与工具"   # 语料目录
OUT = HERE / "niche_probe3_results.json"          # 结果输出（脚本同目录）

FILES = {
    2025: str(DATA / "cvpr_papers_2025" / "00_ALL_labeled.csv"),
    2026: str(DATA / "cvpr_papers" / "00_ALL_labeled.csv"),
}

QUERIES = OrderedDict([
    # ---- 扩散/生成 ----
    ("Diffusion_total",   {"any": ["diffusion"]}),
    ("T2I_gen",           {"any": ["text-to-image"]}),
    ("VideoGen",          {"any": ["video generation", "text-to-video", "video diffusion", "image-to-video"]}),
    ("DiffEdit",          {"any": ["diffusion", "generative"], "and": ["image editing", "instruction editing", "instruction-based edit", "image edit"]}),
    ("ConceptErase",      {"any": ["concept erasure", "concept erasing", "erasing concept", "concept removal"]}),
    ("SamplingAccel",     {"any": ["diffusion"], "and": ["distillation", "one-step", "few-step", "accelerat", "efficient sampling", "fast sampling"]}),
    ("Controllable_gen",  {"any": ["controllable generation", "controllable synthesis", "controlnet", "layout control", "spatial control"]}),
    # ---- 视频 ----
    ("Video_total",       {"any": ["video"]}),
    ("LongVideo",         {"any": ["long video", "long-form video", "long-form"]}),
    ("VideoEdit",         {"any": ["video editing", "video edit"]}),
    ("VideoUnderstand",   {"any": ["video understanding", "video captioning", "video question", "videoqa"]}),
    # ---- 可信/安全 ----
    ("Jailbreak",         {"any": ["jailbreak"]}),
    ("Deepfake",          {"any": ["deepfake", "face forgery", "forgery detection", "tampering", "manipulated image"]}),
    ("Watermark_all",     {"any": ["watermark"]}),
    ("Backdoor_all",      {"any": ["backdoor"]}),
    # ---- 效率/压缩 ----
    ("ModelCompress",     {"any": ["quantization", "pruning", "knowledge distillation", "model compression"]}),
    ("EdgeDeploy",        {"any": ["on-device", "edge device", "mobile device", "embedded"]}),
    # ---- 分割 ----
    ("OpenVocabSeg",      {"any": ["open-vocabulary segmentation", "open vocabulary segmentation"]}),
    ("InteractiveSeg",    {"any": ["segment anything", "interactive segmentation"]}),
    # ---- 低层视觉/恢复 ----
    ("Restoration",       {"any": ["image restoration", "super-resolution", "super resolution", "denoising", "deblurring", "low-light", "image enhancement"]}),
    ("Depth_est",         {"any": ["depth estimation", "monocular depth"]}),
    # ---- 检测 ----
    ("Detection_total",   {"any": ["object detection"]}),
    ("OpenVocabDet",      {"any": ["open-vocabulary detection", "open vocabulary detection"]}),
    # ---- 驾驶 ----
    ("Driving_total",     {"any": ["autonomous driving", "self-driving", "autonomous vehicle"]}),
    ("Occupancy",         {"any": ["occupancy"]}),
    ("E2E_driving",       {"any": ["end-to-end driving", "end-to-end autonomous"]}),
    # ---- 人体 ----
    ("HumanPose",         {"any": ["pose estimation"]}),
    ("MotionGen",         {"any": ["motion generation", "human motion", "motion synthesis"]}),
    ("Avatar_all",        {"any": ["avatar"]}),
    ("TalkingHead",       {"any": ["talking head", "talking face", "talking avatar"]}),
    # ---- 医学/遥感 ----
    ("Medical_total",     {"any": ["medical", "clinical", "pathology", "histopathology", "endoscop", "radiology", "ultrasound", " mri"]}),
    ("RemoteSensing",     {"any": ["remote sensing", "satellite", "aerial"]}),
    # ---- 文档/OCR ----
    ("DocAI",             {"any": ["document understanding", "ocr", "scene text", "table recognition", "layout analysis", "document parsing"]}),
    # ---- 其他成熟方向 ----
    ("SSL",               {"any": ["self-supervised"]}),
    ("Face_total",        {"any": ["face recognition", "face generation", "face restoration", "face swapping", "face editing"]}),
    ("AudioVisual",       {"any": ["audio-visual", "audiovisual", "audio visual"]}),
    ("Tracking_total",    {"any": ["object tracking", "visual tracking", "multi-object tracking"]}),
    # ---- 3D 生成（与主线交叉参考）----
    ("PointCloud",        {"any": ["point cloud"]}),
    ("TextTo3D",          {"any": ["text-to-3d", "image-to-3d", "3d generation"]}),
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
            "titles_2026": [row["title"] for row in r[2026]][:25],
        }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nsaved -> %s" % OUT)


if __name__ == "__main__":
    main()
