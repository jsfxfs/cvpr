# 05 · CVPR 数据与工具

CVPR 2025/2026 全量论文语料的爬取、分类与统计工具。`02_3DGS与大模型_方向调研/` 的全部结论都建立在这套数据上。

## 目录结构

```
05_CVPR数据与工具/
├── run_cvpr.py              # 入口：爬取 + 分类 + 导出（三段式流水线）
├── cvpr/                    # 核心模块
│   ├── net.py               # HTTP 层（线程安全 Session、指数退避、礼貌延时）
│   ├── parser.py            # 页面解析（列表页 / 详情页）
│   ├── pipeline.py          # 流水线：元数据 → 摘要（多线程断点续跑）→ 分类导出
│   └── topics.py            # 25 个方向词表与关键词加权分类器
├── cvpr_papers/             # CVPR 2026 语料（4042 篇）
│   ├── 00_ALL_labeled.csv   # 全量表（标题+摘要+方向标签+置信度），约 10 MB
│   ├── by_topic/            # 25 个方向各自 CSV
│   ├── topic_stats.json/md  # 方向分布统计
│   └── raw/                 # 原始元数据 + 摘要缓存（jsonl 可断点续跑）
├── cvpr_papers_2025/        # CVPR 2025 语料（2871 篇，结构同上）
└── crawl.log                # 最近一次全量爬取日志（2026：4042 篇，摘要 0 失败）
```

## 数据口径（引用时必须声明）

- CVF openaccess **不提供官方方向字段**，全部方向由关键词规则分类器（`cvpr/topics.py`）推断：标题命中权重 ×3、摘要 ×1；置信度 = (最高分 − 次高分) / 最高分；
- 约 44% 论文为多标签、约 18% 为低置信度，方向占比应理解为 **±1~2 个百分点**的近似区间；跨方向占比差 <2pp 的视为并列；
- 宽泛方向（LLM/VLM）有高估倾向，专用术语方向有低估倾向；子串匹配有噪音（如 `gui` 会误匹配 guidance），解读时需人工剔除。

## 常用命令（在本目录下执行）

```bash
# 重跑分类（改完词表后，不重新抓取）
conda run -n scrapling python run_cvpr.py --years 2026 --skip-abstracts

# 爬其他年份
conda run -n scrapling python run_cvpr.py --years 2024 --out cvpr_papers_2024

# 小样本试跑 / 只下某方向 PDF（全量 PDF 约 20–60 GB，慎用）
conda run -n scrapling python run_cvpr.py --limit 30
conda run -n scrapling python run_cvpr.py --pdf-topic Diffusion_Generative

# 定向细分统计（脚本在 02_.../定向统计/，自动定位本目录语料）
python ../02_3DGS与大模型_方向调研/定向统计/niche_probe3.py
```

> 环境：conda 环境 `scrapling`（Python 3.10.20 + bs4 4.14.3 + lxml + requests）。
