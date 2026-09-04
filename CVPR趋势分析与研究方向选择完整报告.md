# CVPR 2025/2026 趋势分析与研究方向选择完整报告

> 整理时间：2026-09-03
> 数据来源：本地爬取的 CVPR openaccess 论文数据（含标题+摘要+方向标签）
> 约束条件：算力 3×3090(24G) + 4×4080(16G) + 8×2080(11G)（分三台服务器）；时间 < 1 年；组背景为三维重建；个人有深度学习/LoRA微调/RAG 基础

---

# 目录

1. 数据集概览
2. CVPR 2026 详细趋势总结
3. CVPR 2025 详细趋势总结
4. 2025 → 2026 跨年趋势对比
5. 修正清单（重要：以修正后版本为准）
6. 专题一：前馈式 3DGS（Feed-Forward 3DGS）客观分析
7. 专题二：测试时方法科普（TTA / Test-time Scaling / 与微调的区别）
8. 方向选择系列建议
9. 个人约束条件汇总
10. 最终决策矩阵与建议
11. 附录：数据文件位置与复现方法

---

# 1. 数据集概览

| 数据集 | 论文数 | 摘要 | 多标签论文 | 低置信度论文 | 存放位置 |
| --- | ---: | --- | ---: | ---: | --- |
| CVPR 2026 | 4042 | 4042 / 缺 0 | 1803（44.6%） | 744（18.4%） | `cvpr_papers/` |
| CVPR 2025 | 2871 | 2871 / 缺 0 | 1245（43.4%） | 518（18.0%） | `cvpr_papers_2025/` |

- 爬取工具：`run_cvpr.py`（三段式流水线：元数据 → 摘要 → 分类导出），运行环境为 conda 环境 `scrapling`（Python 3.10.20 + bs4 4.14.3 + lxml + requests）。
- CVPR 2025 爬取命令：`conda run -n scrapling python run_cvpr.py --years 2025 --out cvpr_papers_2025`，2871 篇摘要 0 失败。
- **方向分类方法说明**：CVF openaccess 不提供官方方向字段，所有方向由关键词规则分类器（`cvpr/topics.py`）推断：标题命中权重×3、摘要命中权重×1，主方向=最高分，多标签=分数≥最高分×40% 且≥6 分，置信度=(最高分-次高分)/最高分。
- **方法学局限**：约 44% 论文为多标签、约 18% 为低置信度，方向边界模糊；LLM/VLM 等关键词宽泛方向存在高估倾向，专用术语方向存在低估倾向。所有方向占比应理解为 ±1~2 个百分点的近似区间。

---

# 2. CVPR 2026 详细趋势总结

## 2.1 总体格局

2026 年 CVPR 共 **4042 篇**论文，其中 1803 篇（约 45%）被打多方向标签，交叉研究已成常态。全量摘要高频词暴露三个压倒性事实：

- **生成式是绝对主流**：`generation`（2109次）、`generative`（1534次）、`diffusion`（1303次）稳居全局词汇前三；
- **大模型彻底接管视觉**：`reasoning`（1798次）、`multimodal`（1170次）、`language`（892次）表明 LLM/VLM 已成为几乎所有方向的"基础设施"；
- **效率与可靠性是共同焦虑**：`efficient`（1275次命中）、`consistency`（925次）、`alignment`（1076次）随处可见。

**主方向数量排序**：Diffusion(463) ≈ LLM/智能体(455) ≈ 多模态(434) 三强领跑，之后是视频(262)、具身智能(232)、神经渲染(190)、可信AI(178)、效率压缩(157)、迁移学习(156)、3D重建(153)。

### 2026 主方向分布（每篇只计一次）

| 方向 | 论文数 | 占比 |
| --- | ---: | ---: |
| Diffusion_Generative | 463 | 11.5% |
| LLM_Reasoning_Agent | 455 | 11.3% |
| Vision_Language_Multimodal | 434 | 10.7% |
| Video_Action_Recognition | 262 | 6.5% |
| Embodied_AI_Robotics | 232 | 5.7% |
| Neural_Rendering_NeRF_3DGS | 190 | 4.7% |
| Trustworthy_Security_Privacy | 178 | 4.4% |
| Efficiency_Compression | 157 | 3.9% |
| Transfer_FewShot_DomainAdaptation | 156 | 3.9% |
| 3D_Reconstruction | 153 | 3.8% |
| Segmentation | 141 | 3.5% |
| Medical_Bio_RemoteSensing | 134 | 3.3% |
| SelfSupervised_Representation | 132 | 3.3% |
| LowLevel_Flow_Depth_Matching | 126 | 3.1% |
| Object_Detection | 113 | 2.8% |
| Restoration_Enhancement | 112 | 2.8% |
| Autonomous_Driving | 106 | 2.6% |
| Human_Pose_Body | 106 | 2.6% |
| Face_Biometrics | 80 | 2.0% |
| Recognition_Classification | 73 | 1.8% |
| Other | 69 | 1.7% |
| Tracking_MOT | 64 | 1.6% |
| Audio_Visual | 49 | 1.2% |
| Document_OCR_Graphics | 35 | 0.9% |
| Computational_Photography | 22 | 0.5% |

## 2.2 三大领跑方向详解

### 2.2.1 扩散生成（Diffusion_Generative，463篇，11.5%）

- **标题 Bigram 画像**：`text-to-image generation`(24)、`diffusion transformers`(23)、`flow matching`(18)、`diffusion transformer`(12)、`text-to-image diffusion`(9)、`latent diffusion`(9)、`concept erasure`(7)、`preference optimization`(7)、`rectified flow`(7)、`autoregressive diffusion`(5)。
- **核心趋势**：
  1. **Flow Matching 大规模接棒 DDPM**，扩散 Transformer（DiT）架构成为主力，多篇研究 self-evaluation/guidance 提升采样质量；
  2. **图像编辑**走向"细粒度指令+多属性解耦"（如 `CompBench` 复杂指令编辑基准、`FlowDC` 流式解耦编辑）；
  3. **概念擦除/安全**成为成熟子方向（`Erasing Thousands of Concepts` 一次擦除数千概念）；
  4. **自回归扩散**（autoregressive diffusion/generation）与视觉自回归（VAR）正在融合；
  5. 大量工作关注**采样效率**（低分辨率预览、一步生成、token 压缩）。
- 代表论文：Functional Mean Flow in Hilbert Space；FlowDC；What Is It Like to Be a Noise?；Toward Diffusible High-Dimensional Latent Spaces；Anatomica；Self-Evaluation Unlocks Any-Step Text-to-Image Generation。

### 2.2.2 大模型推理与智能体（LLM_Reasoning_Agent，455篇，11.3%）

- **画像**：`multimodal language`(34)、`multimodal llms`(11)、`spatial reasoning`(8)、`GUI agents`(6)、`test-time scaling`(5)、`mitigating hallucinations`(5)、`instruction tuning`(4)。
- **核心趋势**：
  1. **视觉推理（visual reasoning）**取代"识别"成为核心命题；
  2. **Agent 化**——`GardenDesigner`（链式 agent）、`RAAS`（用 GRPO 做 agent 系统架构搜索）、`OS-Oracle`（跨平台 GUI 评审模型）等，GUI 自动化、工具调用、多智能体协作成为新热点（GUI agent 全库 18 篇）；
  3. **推理时扩展（test-time scaling）**与**奖励模型/GRPO/RL**（92篇命中 RL 相关）全面渗透；
  4. **幻觉治理**是该方向最集中的可靠性议题（54篇），如 `Reallocating Attention Across Layers` 用免训练插件重分配层间注意力降低幻觉。
- 代表论文：Unlocking Token Rewards via Training-Free Reward Attribution；Human-like Abstract Visual Reasoning；RAAS；OS-Oracle。

### 2.2.3 视觉-语言多模态（Vision_Language_Multimodal，434篇，10.7%）

- **画像**：`multimodal reasoning`(14)、`unified multimodal`(11)、`vision-language alignment`(6)、`spatial reasoning`(6)、`anomaly detection`(6)、`autonomous driving`(5)。
- **核心趋势**：
  1. **从"对齐"走向"推理"**——空间推理、图问答（`DynamicGTR`）、相册级理解（`Album-Level VQA`）、全景 3D 空间智能（`PanoEnv`，用 RL+几何奖励训练 VLM 做 360° 空间推理）都是新增长点；
  2. **检索与融合智能化**——组合检索、红外-可见光融合、水印感知检索；
  3. **评测基准爆发**——benchmark(242)、dataset(187) 显示新任务配新基准已成标配；
  4. 该方向是**幻觉治理**与 anomaly detection 的第二大战场。
- 代表论文：Multi-Modal Image Fusion via Intervention-Stable Feature Learning；CLAY；Camouflage-aware Image-Text Retrieval；Beyond Graph Model。

## 2.3 第二梯队方向

### 视频与动作识别（262篇，6.5%）

- **画像**：`long understanding`(11)、`action recognition`(8)、`temporal grounding`(5)、`long-video understanding`(4)、`multi-shot generation`(4)、`image-to-video generation`(4)。
- **核心趋势**：**长视频**是最大关键词（45篇），既有长视频理解也有长视频生成；**视频生成**（108篇命中）全面爆发，含图像到视频、多镜头生成、定制化生成、透明视频（RGB-A）；**运动控制/迁移**（`FlowMotion` 免训练运动迁移）成为新操控入口；视频压缩（`UniComp`）与视频编辑（19篇）也占一席。
- 代表：FlowMotion；First Frame Is the Place to Go for Video Content Customization；AE2VID；Real-Time Neural Video Compression。

### 具身智能与机器人（232篇，5.7%）

- **画像**：`robotic manipulation`(17)、`vision-and-language navigation`(7)、`embodied agents`(5)、`latent action`(3)。
- **核心趋势**：
  1. **VLA（视觉-语言-动作）模型**集中爆发（全库 79 篇，本方向 62 篇），如 `HybridDriveVLA`（CoT+ToT 评估）；
  2. **世界模型**成为具身大脑（本方向16篇，全库58篇），`Planning in 8 Tokens`、`GRWM`（潜空间几何对世界模型保真的关键作用）；
  3. **人形机器人**崛起（15篇），大量 sim2real 工作（`VIRAL` 大规模人形视觉 sim2real）；
  4. 双臂协调、全身移动操作、接触感知动力学、触觉（Haptic Neural Fields）等物理交互主题密集；
  5. **物理先验**（52篇）是具身方向最鲜明的方法论特征。
- 代表：CUBic；Planning in 8 Tokens；Contact-Aware Neural Dynamics；VIRAL。

### 神经渲染 NeRF/3DGS（190篇，4.7%）

- **画像**：`gaussian splatting`(91)、`view synthesis`(20)、`feed-forward gaussian`(7)、`dynamic scenes`(7)。
- **核心趋势**：
  1. **3DGS 完胜 NeRF**——全库 3DGS 命中 205 次 vs NeRF 仅 42 次，NeRF 已基本退居"局部优化对象"；
  2. **前馈（feed-forward）重建**与**稀疏视角**是攻坚点（`FlashVGGT`、`EcoSplat`、`RT-Splatting`）；
  3. **动态 4D 场景**成为主战场（本方向47篇 4D/dynamic），`Catalyst4D` 做 3D→4D 编辑、ChronoGS 多周期场景分解；
  4. 鱼眼/全景输入、触觉场、逆渲染（物理光照 `IR-HGP`）等传感器与物理扩展方向活跃。
- 代表：RT-Splatting；Intrinsic Geometry-Appearance Consistency；Faster-GS；Scaling View Synthesis Transformers。

### 可信、安全与隐私（178篇，4.4%）

- **画像**：`deepfake detection`(9)、`personalized federated`(6)、`adversarial robustness`(5)、`spiking neural`(3)。
- **核心趋势**：
  1. **深度伪造/合成内容检测**成为最大单一热点（17篇+跨方向64篇），AI 内容治理已从论文题变成安全刚需；
  2. **联邦学习**（29篇）聚焦个性化、去学习（unlearning）、对抗鲁棒；
  3. 对抗鲁棒性转向**真实防御**；
  4. 脉冲神经网络（SNN）鲁棒性研究异军突起；
  5. 内容水印、越狱防护、提示注入防御等 LLM 安全议题进入视觉会议。
- 代表：Towards Robust Vision Transformers；Computation and Communication Efficient Federated Unlearning。

## 2.4 基础设施类与其他方向

### 效率与压缩（157篇，3.9%）
- **画像**：`token pruning`(11)、`token compression`(9)、`token merging`(6)、`post-training quantization`(3)、`diffusion acceleration`(3)、`speculative decoding`(3)。
- **核心趋势**：**Token 级稀疏化**（剪枝/合并/压缩）是第一主题；量化转向**大 VLM 的 PTQ**（`Quant Experts` 用 MoE 做 token 感知量化误差重建）；同时是扩散加速和自回归加速的汇聚点。

### 迁移/小样本/域适应（156篇，3.9%）
- **画像**：`anomaly detection`(24)、`test-time adaptation`(16)、`domain adaptation`(7)、`out-of-distribution detection`(6)。
- **核心趋势**：① **异常检测意外成为第一大子主题**（24篇+全库46篇）；② **测试时适应（TTA）** 大放异彩（16篇），与持续学习结合成"终身在线适应"范式；③ **持续/增量学习**密集；④ 模型遗忘/去学习（unlearning 本方向35篇）是新热点。

### 3D 重建（153篇，3.8%）
- **画像**：`point cloud`(17+6)、`scene reconstruction`(10)、`cloud registration`(4)。
- **核心趋势**：点云处理仍是基本盘，**前馈重建**与 feed-forward 3DGS 强势渗透；**CAD 代码生成**（`CME-CAD` 多专家强化学习生成 CADQuery 代码）把重建推向"可编辑工业资产"；旋转不变分析、形状匹配谱方法、关节物体重建持续演进。

### 底层视觉：光流/深度/匹配（126篇，3.1%）
- **画像**：`depth estimation`(18)、`metric depth`(7)、`gaussian splatting`(6)、`optical flow`(6)、`stereo matching`(5)。
- **核心趋势**：**单目度量深度**是最大热点；**零样本/合成训练数据**成为新方法论；3DGS 与 SLAM/定位深度结合；基础矩阵估计等经典几何问题被重新数学化打磨。

### 分割（141篇，3.5%）
- **画像**：`semantic segmentation`(34)、`open-vocabulary semantic`(6)、`training-free open-vocabulary`(4)。
- **核心趋势**：**开放词汇分割**（18次）已从新事物变成标配，且流行**免训练**路线；可交互 amodal 分割、3D 实例分割、提示/点击交互分割是主要工程创新；Mamba 注意力的效率型分割体现新架构渗透。

### 目标检测（113篇，2.8%）
- **画像**：`object detection`(65)、`monocular object`(5)、`open-vocabulary object`(4)、`small object`(4)。
- **核心趋势**：热点在**单目 3D 检测**（标注稀疏化）、**开放词汇检测**、**遥感/无人机小目标**，以及**AI 生成内容检测**。

### 图像恢复与增强（112篇，2.8%）
- **画像**：`low-light enhancement`(5)、`real-world super-resolution`(5)、`all-in-one restoration`(3)、`one-step diffusion`(3)。
- **核心趋势**：**扩散先验一统恢复**（49篇），多篇做 all-in-one 通用恢复器（`UniLDiff`）；**单步/时间感知扩散**解决实时性；真实世界退化建模走向工程化；自回归模型首次进入超分（`DVAR`）。

### 自动驾驶（106篇，2.6%）
- **画像**：`autonomous driving`(28)、`trajectory prediction`(6)、`occupancy prediction`(5)。
- **核心趋势**：① **端到端范式**全面固化；② **占用预测**成为感知主赛道（`Dr.Occ`、`ShelfOcc`）；③ **LiDAR 世界模型**（`GEM`）与驾驶场景生成将生成式引入驾驶；④ 长时程轨迹预测、稀疏协同感知（`Long-SCOPE`）、离线矢量化地图持续演进。

### 人体姿态与形体（106篇，2.6%）
- **画像**：`pose estimation`(24)、`human motion`(17)、`human-object interaction`(9)、`gait recognition`(6)。
- **核心趋势**：**物理感知**成为方法论中心（25篇）——`InterPhys` 动态场景物理感知运动合成、基于地面反作用力的惯性捕捉；**运动生成**与**运动分解重组**加速；交互（HOI）、步态识别、残缺肢体重建并存。

### 人脸与生物特征（80篇，2.0%）
- **画像**：`gaze estimation`(5)、`face generation`(4)、`face swapping`(3)、`talking face`(3)、`face forgery`(3)。
- **核心趋势**：**3D 头面部 avatar 重建**（`FHAvatar`、`ProgressiveAvatars`）与生成/交换并重；**伪造检测**与生成攻防形成闭环；虹膜、注视估计等细节方向仍在推进。

### 医疗/生物/遥感（134篇，3.3%）
- **画像**：`medical segmentation`(17)、`remote sensing`(15)、`report generation`(4)、`whole slide`(3)。
- **核心趋势**：医疗侧分割仍是基本盘（48篇），但**报告生成**、**全切片预后**、多中心基准（`LUMINA`）、图像配准等转向"大模型+临床流程"；遥感侧变化检测、泛锐化、**天气预测**（`STCast`）延伸出"地球观测基础模型"；脑机接口（EEG 融合 `BrainSSD`）也进入 CVPR。

### 跟踪 MOT（64篇，1.6%）
- **画像**：`person re-identification`(7)、`multi-object tracking`(7)、`point tracking`(5)。
- **核心趋势**：**生成式跟踪**（`TGTrack`）、**脉冲/事件驱动跟踪**（`SpikeTrack`）、多相机多目标（`GMT`）；红外-可见光跨模态 ReID、无人机跟踪、遮挡感知（`Occlusion-Aware SORT`）。

### 音视频（49篇，1.2%）
- **画像**：`video-to-audio generation`(4)、`audio generation`(3)、`co-speech gesture`(2)、`talking avatars`(2)。
- **核心趋势**：**视频到音频生成**、**说话 avatar**（`ActAvatar`、`UniLS`）、**音频-视觉分割**、**3D 音视频场景**（`SonoWorld`）是最亮新方向；三模态检索（文本+视觉+音频，`OmniRet`）出现。

### 文档/OCR/图形（35篇，0.9%）
- **画像**：`scene text`(4)、`document parsing`(2)、`mathematical expression recognition`(2)。
- **核心趋势**：数学/手写公式识别（`UniMERNet`）与**场景文字渲染/编辑**为主；可微渲染（位图/笔画原语）、图像矢量化（`Clair Obscur`）、表格识别是图形侧亮点。

### 计算摄影（22篇，0.5%）
- **画像**：`hdr reconstruction`(3)、`color grading`(2)。
- **核心趋势**：编码孔径/编码曝光成像、RAW 重建与多域 RAW 翻译、事件光场、多曝光融合基准、微分对焦深度（`SpiderCam`）。**事件相机/脉冲相机**（全库 57 篇）成为传感器层面新兴主力。

## 2.5 十大跨方向主题（结构性变化）

1. **世界模型（World Model）**：58 篇，集中在具身(16)、视频(10)、驾驶(7)——"生成未来"取代"识别过去"。
2. **3DGS 技术普惠**：205 篇，从渲染反向渗透到 3D重建(15)、底层视觉(9)、具身(7)、人脸、驾驶。
3. **强化学习+奖励对齐**：336 篇，GRPO/RLHF/DPO 从 LLM 扩散到 VLM 推理、扩散偏好优化、驾驶轨迹、天气预测。
4. **物理感知（Physics）**：348 篇，具身、人体、渲染、恢复、驾驶都在引入物理约束。
5. **测试时适应与终身学习**：TTA(48篇)+持续/增量+unlearning(109篇)。
6. **幻觉治理**：100 篇直接命中+483 篇可靠性相关，方法走向免训练（推理时干预）。
7. **Token 经济与效率**：efficiency 类 1275 篇命中，token 剪枝/量化/MoE/蒸馏。
8. **合成数据**：121 篇，从训练到评测全面"以假乱真"。
9. **长视频/长时程**：78 篇，理解与生成的尺度竞赛从秒级走向分钟级。
10. **安全与内容治理闭环**：deepfake 检测、概念擦除、水印、越狱防护（135篇安全对齐）。

## 2.6 一句话总结（2026）

CVPR 2026 已彻底进入 **"生成 × 大模型 × 物理"** 三引擎时代：扩散/自回归+Flow Matching 重构视觉任务为生成任务，MLLM/智能体把"识别"升级为"推理"，3DGS 与具身智能把研究推向 4D 物理世界；与此同时，效率（token 经济）、可靠性（幻觉/安全/遗忘）、测试时自适应成为全体方向共用的"底座问题"。

---

# 3. CVPR 2025 详细趋势总结

**基本盘**：2871 篇。格局是 **"扩散单极 + 大模型萌芽 + 3DGS 换血"**。

## 3.1 主方向分布

| 方向 | 论文数 | 占比 |
| --- | ---: | ---: |
| Diffusion_Generative | 426 | 14.8% |
| Vision_Language_Multimodal | 239 | 8.3% |
| LLM_Reasoning_Agent | 212 | 7.4% |
| Video_Action_Recognition | 175 | 6.1% |
| Neural_Rendering_NeRF_3DGS | 168 | 5.9% |
| 3D_Reconstruction | 139 | 4.8% |
| Transfer_FewShot_DomainAdaptation | 136 | 4.7% |
| Trustworthy_Security_Privacy | 132 | 4.6% |
| Human_Pose_Body | 117 | 4.1% |
| Segmentation | 116 | 4.0% |
| LowLevel_Flow_Depth_Matching | 108 | 3.8% |
| Restoration_Enhancement | 102 | 3.6% |
| Embodied_AI_Robotics | 98 | 3.4% |
| Efficiency_Compression | 97 | 3.4% |
| Face_Biometrics | 85 | 3.0% |
| SelfSupervised_Representation | 84 | 2.9% |
| Object_Detection | 81 | 2.8% |
| Autonomous_Driving | 76 | 2.6% |
| Medical_Bio_RemoteSensing | 69 | 2.4% |
| Other | 51 | 1.8% |
| Audio_Visual | 43 | 1.5% |
| Tracking_MOT | 40 | 1.4% |
| Recognition_Classification | 38 | 1.3% |
| Document_OCR_Graphics | 23 | 0.8% |
| Computational_Photography | 16 | 0.6% |

## 3.2 各方向详解

**1. 扩散生成（426篇，14.8%，第一）**
- 核心词：`text-to-image generation`(17)、`latent diffusion`(15)、`diffusion transformers`(9)。
- 技术画像：以 **Latent Diffusion / DDPM 为主**，Flow Matching 尚在萌芽；DiT 刚起步。
- 代表：Nested Diffusion Models Using Hierarchical Latent Priors；Latent Space Imaging；Stretching Each Dollar（微预算从零训练扩散）；h-Edit（基于 Doob's h-Transform 编辑）。
- 与 2026 相比：编辑、擦除、偏好优化（DPO/RL）等"扩散后处理"主题明显少。

**2. 视觉-语言多模态（239篇，8.3%，第二）**
- 核心词：`vlms`、`question answering`(7)、`unified multimodal`(5)、`cross-modal alignment`(5)。
- 代表：**Janus**（解耦视觉编码的统一多模态模型）、One Model for ALL、Continual SFT Matches Multimodal RLHF。
- 特征：集中在**"统一架构 + 对齐"**，空间推理/智能体还很少。

**3. 大模型推理与智能体（212篇，7.4%，第三）**
- 核心词：`mllms`、`instruction tuning`(4)、`multimodal language`(28)。
- 代表：**ComfyBench**（LLM 智能体在 ComfyUI 中自主搭图，GUI 智能体雏形）、**RLAIF-V**（AI 反馈对齐）、Associative Transformer。
- 特征：幻觉治理、指令跟随为主，**推理时扩展完全缺席**（0篇）。

**4. 视频与动作（175篇，6.1%）**
- 核心词：`long generation`(6)、`text-to-video generation`(4)、`image-to-video generation`(4)。
- 代表：MANTA（**Diffusion Mamba** 长时程视频预测）、AnimateAnything、Learning Physics From Video。
- 特征：长时程预测 + 运动可控 + 物理参数估计。

**5. 神经渲染 NeRF/3DGS（168篇，5.9%）**
- 核心词：`gaussian splatting`(74 bigram)、`view synthesis`(14)、`inverse rendering`(6)。
- **2025 是 3DGS 全面换血 NeRF 的年份**：3DGS 命中 116 次 vs NeRF 仅 44 次。
- 代表：Gaussian Splashing、Splatter-360、RNG（可重光照）、IRGS、3DGUT（失真相机+次级光线）。

**6. 3D 重建（139篇，4.8%）**
- 核心词：`point cloud`(32 bigram)、`surface reconstruction`(7)、`cloud completion`(5)。
- 代表：UniK3D（通用单目 3D 估计）、CMMLoc（文本到点云定位）、ArcPro、生成式扩散重建。
- 特征：经典点云任务占主体，生成式重建开始渗透。

**7. 迁移/小样本/域适应（136篇，4.7%）**
- 核心词：`anomaly detection`(16)、`domain generalization`(11)、`test-time adaptation`(8)。
- 特征：异常检测已冒头，测试时适应（TTA）形成独立流派。

**8. 可信安全（132篇，4.6%）**
- 核心词：`adversarial`(38)、`federated`(21)、`deepfake detection`(5)、`backdoor`。
- 代表：无数据通用对抗扰动、联邦后门攻击、FedAWA。
- 特征：以对抗攻击/联邦学习为主；deepfake 检测刚起步。

**9. 人体姿态（117篇，4.1%）** — `motion`(47)、`hand`(30)、`diffusion`(24)；代表 Any6D、ChainHOI、WildAvatar。特征：扩散进入人体运动生成 + HOI 交互建模。

**10. 分割（116篇，4.0%）** — `open-vocabulary`(21)、`weakly supervised`(7)；代表 Scene-Centric Unsupervised Panoptic、Camouflage Anything。特征：开放词汇已普及，弱监督/无监督是主战场。

**11. 底层视觉（108篇，3.8%）** — `depth estimation`(30)、`zero-shot`(18)、`monocular depth`(7)；代表 HyperPose、Scene-agnostic Pose Regression。特征：零样本泛化成为深度估计新基准。

**12. 恢复增强（102篇，3.6%）** — `diffusion`(35)、`super-resolution`(34)、`all-in-one restoration`(3)；代表 UniRestore、URWKV。特征：扩散先验进入恢复、统一恢复器雏形已现。

**13. 具身智能（98篇，3.4%）** — `robot`(59)、`manipulation`(44)、`navigation`(34)、`diffusion policy`(2)；代表 Neural Motion Simulator（世界模型推 RL 上限）、ManipTrans、UniGraspTransformer。特征：体量尚小，但"世界模型 + 扩散策略"两大伏笔已埋下。

**14. 效率压缩（97篇，3.4%）** — `quantization`(21)、`token`(20)、`post-training quantization`(5)、`token pruning`(3)。特征：PTQ 主导，token 稀疏化刚萌芽。

**15. 人脸（85篇，3.0%）** — `face recognition`(6)、`gaze estimation`(5)、`face forgery`(4)；代表 GazeGene（大规模合成注视）、SapiensID、GIF（生成式人脸识别数据合成）。特征：合成数据训练人脸识别是亮点。

**16. 自监督（84篇，2.9%）** — `foundation model`(29)、`contrastive`(24)、`masked`(14)；代表 Hyperbolic Category Discovery、Transformers without Normalization。特征：基础模型预训练 + 几何方法。

**17. 目标检测（81篇，2.8%）** — `object detection`(45)、`oriented object`(3)。特征：传统检测明显收缩，DETR 体系为主。

**18. 自动驾驶（76篇，2.6%）** — `trajectory prediction`(7)、`occupancy prediction`(6)；代表 **GaussianWorld**（高斯世界模型做流式占用预测）、OccMamba、SOAP。特征：占用预测新范式 + 世界模型入场，是 2025 驾驶方向标志性信号。

**19. 医疗遥感（69篇，2.4%）** — `medical segmentation`(10)、`tumor segmentation`(7)、`semi-supervised medical`(5)。特征：半监督 + 全切片 + 高光谱。

**20-25. 小方向**：音视频（43，视听分割/配音，代表 Crab 统一视听理解）；跟踪（40，ReID + 点跟踪）；识别分类（38，细粒度 + 多视图聚类）；文档OCR（23，SVG 生成/矢量化如 StarVector、场景文字合成 DreamText）；计算摄影（16，Integral FFT Color Constancy、UltraFusion、Event Fields 事件光场）。

## 3.3 2025 年五个"时代特征"

1. **3DGS 元年**：全面替代 NeRF，但"前馈重建/动态场景"还没有像 2026 那样成熟。
2. **扩散独大**：占比 14.8% 遥遥领先，Flow Matching 尚未普及。
3. **大模型处于"对齐期"**：做统一架构、对齐、指令跟随；没有 test-time scaling，GUI 智能体仅 2 篇，VLA 仅 7 篇，world model 仅 19 次命中。
4. **Mamba 的高光时刻**：state space / Mamba 全库 80 次命中（2026 跌到 45）。
5. **异常检测与测试时适应崛起**：成为迁移学习内部两大主赛道。

---

# 4. 2025 → 2026 跨年趋势对比

## 4.1 大盘

论文总数 **2871 → 4042（+40.8%）**。判断"真热点"的基准线是 **+40.8%**：增速高于此才算实质性扩张，低于此就是相对退潮。

## 4.2 主方向占比迁移

| 方向 | 2025 | 2026 | 变化(pp) | 判定 |
| --- | ---: | ---: | ---: | --- |
| 扩散生成 | 14.8% | 11.5% | ▼3.3 | 份额被稀释（绝对数 426→463 仍增） |
| **大模型推理/智能体** | 7.4% | **11.3%** | ▲3.9 | 最大增量 |
| **视觉-语言多模态** | 8.3% | **10.7%** | ▲2.4 | 最大增量 |
| **具身智能** | 3.4% | **5.7%** | ▲2.3 | 翻倍爆发 |
| 视频与动作 | 6.1% | 6.5% | ▲0.4 | 稳定 |
| 神经渲染 3DGS | 5.9% | 4.7% | ▼1.2 | 相对收缩 |
| 3D 重建 | 4.8% | 3.8% | ▼1.0 | 相对收缩 |
| 人体姿态 | 4.1% | 2.6% | ▼1.5 | 收缩最明显 |
| 可信安全 | 4.6% | 4.4% | ~0 | 持平 |
| 医疗/遥感 | 2.4% | 3.3% | ▲0.9 | 上升 |
| 效率压缩 | 3.4% | 3.9% | ▲0.5 | 上升 |

**结论**：`LLM + VLM + 具身` 三者合计从 **19.1% → 27.7%**，直接"虹吸"了扩散与全部传统视觉任务的相对份额。单极（扩散）格局正式变为 **"生成 × 大模型 × 具身"三极**。

## 4.3 绝对数变化（修正后的准确判断）

**绝对数高增长（真热点，增速远超基准）**：
- 具身智能 98→232（+137%）
- 大模型推理 212→455（+115%）
- 医疗/遥感 69→134（+94%）
- 识别分类 38→73（+92%）
- 视觉-语言多模态 239→434（+82%）
- 效率压缩 97→157（+62%）
- 跟踪 40→64（+60%）
- 自监督 84→132（+57%）

**绝对数增长但低于基准（相对占比稀释，非收缩）**：扩散 +9%、神经渲染 +13%、3D重建 +10%、恢复 +10%、迁移 +15%、底层视觉 +17%、分割 +22%、可信 +35%、检测 +40%、驾驶 +39%、视频 +50%。

**绝对数真正下降（真收缩）**：人体姿态 117→106（-9%）、人脸 85→80（-6%）——仅有这两个方向在绝对规模上也缩小了。

## 4.4 热点主题增速排行（方向性判断）

**爆发级（增速远超 +40.8% 基准）**：

| 主题 | 2025→2026 | 备注 |
| --- | ---: | --- |
| VLA（视觉-语言-动作） | 7 → 79 | 低基数，方向性判断"从无到有" |
| RL/GRPO/奖励模型 | 61 → 336 | ×5.5 |
| Test-time scaling | 0 → 17 | 从零出现 |
| GUI 智能体 | 2 → 18 | 低基数 |
| 空间推理/3D 空间智能 | 28 → 102 | ×3.6 |
| 人形机器人 | 7 → 25 | 低基数 |
| token 剪枝/压缩 | 18 → 62 | ×3.4 |
| 世界模型 | 19 → 58 | ×3 |
| 自回归生成（VAR） | 53 → 147 | ×2.8 |
| MoE | 27 → 74 | ×2.7 |
| 测试时适应（TTA） | 18 → 48 | ×2.7 |
| 遥感/地球观测 | 49 → 116 | ×2.4 |
| 多智能体 | 20 → 45 | ×2.3 |
| VLM/MLLM 全局渗透 | 400 → 890 | ×2.2 |
| 物理感知 | 157 → 348 | ×2.2 |
| 幻觉治理 | 48 → 100 | ×2.1 |
| 天气预测 | 19 → 44 | ×2.3 |
| 4D/动态场景 | 101 → 203 | ×2 |
| 持续/增量学习 | 77 → 137 | ×1.8 |

**退潮级（低于基准或负增长）**：
- **Mamba/状态空间 80 → 45（▼44%）**——作为独立新架构卖点明显降温，但"线性注意力/高效序列建模"需求未消失，只是换了叙事。
- **NeRF 60 → 42（▼30%）**——被 3DGS 系统性替代。
- 轨迹预测 23 → 18（▼22%）；数字人/头像 56 → 51（▼9%）；视频压缩 11 → 9。
- **合成数据 98 → 121（+23%，低于基准）**、**3DGS 180 → 205（+14%，低于基准）**：两项"2025 明星"进入**平台期**——从独立卖点沉淀为其他方向的默认组件（渗透>爆发）。

## 4.5 五条结构性结论

1. **对齐方式换了引擎**：2025 用 SFT/指令微调对齐 VLM，2026 全面转向 **GRPO/RLHF/奖励模型**（61→336），"用 RL 打分数"从 LLM 扩散到扩散模型偏好、驾驶轨迹、天气预测等所有任务。
2. **从"看世界"到"建世界"**：世界模型（19→58）、VLA、具身（98→232）、物理感知（157→348）同频爆发；空间推理（28→102）证明 3D 空间智能被列为大模型必修课。
3. **推理时开销成为新战场**：test-time scaling 从 0 到 17、token 剪枝/压缩 ×3.4、MoE ×2.7 并行爆发——效率问题从部署环节上升到算法环节。
4. **安全治理随生成力同频放大**：deepfake 检测（38→64）、幻觉治理（48→100）、安全/越狱/水印（57→135）全部翻倍。
5. **技术代际更替规律清晰**：Mamba 和 NeRF 是"上一代明星"；3DGS 和扩散则从"独立主题"升格为"所有方向默认组件"。CVPR 的方向洗牌速度以年为单位。

---

# 5. 修正清单（重要：以修正后版本为准）

在回顾此前总结时，发现 5 处需要修正的问题。**数字本身来自脚本生成的 `topic_stats.json`，是可靠的；修正集中在"解读"层面。**

**修正 1：「传统视觉任务普遍收缩」——表述失真，应改为「相对占比稀释，绝对规模绝大多数仍在增长」**
- **理由**：原表述只强调占比下降，误导为"收缩"。实际核对两年主方向绝对数，真正下降的只有 2 个：人体姿态 117→106、人脸 85→80。其余传统方向全部增长（分割 +22%、底层视觉 +17%、检测 +40% 等），只是增速低于总量增速（+40.8%）导致占比被稀释。
- **修正后**：不是"传统方向在消亡"，而是"被大模型/生成式的新增论文稀释了相对份额，但其自身也在以 10~40% 的速度增长"。

**修正 2：「VLA 7→79（×11）」「Test-time scaling 0→17」「GUI agent 2→18」等低基数增速——需标注不可靠**
- **理由**：这些是基于子串词典的命中统计，2025 年基数极低（个位数），且概念词典存在系统性偏差（VLA、test-time scaling 这类新术语 2025 年论文可能用了别的表述，没被词典捕捉）。×11 这种倍数在低基数下会严重放大。
- **修正后**：只表述"VLA、推理时扩展、GUI 智能体这三个主题在 2025 年几乎没有出现、2026 年开始成批出现（数十篇）"，不给精确倍数。

**修正 3：缺少分类方法的局限性声明——方向占比是推断值，不是官方标签**
- **理由**：CVF openaccess 不提供官方方向字段，所有方向由关键词规则分类器推断。多标签约 44%、低置信度约 18%，LLM/VLM 等宽泛方向存在高估倾向，专用术语方向存在低估倾向。
- **修正后**：所有方向占比应理解为 ±1~2 个百分点的近似区间，跨方向占比差 <2pp 的（如 Diffusion 11.5% vs LLM 11.3% vs VLM 10.7%）应视为**并列第一梯队**，而非有先后。

**修正 4：「Mamba 退潮 80→45（▼44%）」——方向正确但需谨慎归因**
- **理由**：命中数下降受多标签词典影响，"退潮"结论应限定为"作为独立卖点退潮"，实际被吸收的场合可能以"efficient/linear attention"等词替代而未被词典捕获。
- **修正后**：Mamba/状态空间作为**独立新架构卖点**在 2026 明显降温，但"线性注意力/高效序列建模"的需求本身并未消失。

**修正 5：代表作抽样的代表性问题**
- **理由**：之前列的"代表论文"是按分类器置信度排序抽样的，偏向"关键词匹配最典型"的论文，不一定是该方向影响力最大的工作（经典/高被引往往措辞中庸、置信度不高）。
- **修正后**：代表作仅用于"示意该方向的典型工作形态"，不构成"该方向最重要论文"的排序。

---

# 6. 专题一：前馈式 3DGS（Feed-Forward 3DGS）客观分析

## 6.1 结论

- **学术上：强烈推荐做。** 前馈式 3DGS 是 CVPR 2026 最确定的爆发点之一，赛道仍在快速扩张。
- **工业上：正在被真实使用，但"纯前馈直接出成品"的成熟产品还不多**；行业主流是"前馈做秒级粗稿 → 优化式精修"的混合路线。
- **3090：完全够用。** 前馈式推理很轻，复现/微调主流 baseline 可行；只有"从零预训练 VGGT 级别大模型"才需要多卡集群。

## 6.2 学术热度（数据）

| 指标 | CVPR 2025 | CVPR 2026 | 变化 |
| --- | ---: | ---: | ---: |
| 标题含 "feed-forward" 的论文 | 6 | 35 | +483% |
| NeRF/3DGS 主方向中提及 feed-forward | 8 | 30 | ~×4 |
| 论文总数 | 2871 | 4042 | +40.8% |

前馈式论文增速（近 6 倍）远超整体收录量增速（1.4 倍），是**结构性热点**。2026 年它已从"稀疏视角新视角合成"单点扩张到：

- **4D/动态**：Any4D、MoRe、DGGT（驾驶）、PhysGM（物理大模型 4D 合成，北理工+理想汽车）
- **场景重建**：SparseSplat、AnchorSplat、Z-Order Transformer、PanoVGGT、VGG-T³、AMB3R、Gen3R
- **人体/数字人**：ForeHOI、UniSH、Feed-forward Gaussian Registration for Head Avatar
- **效率/部署**：EcoSplat（可控制高斯数量）、Off The Grid（原语检测，非网格对齐）
- **语义/智能体**：EmbodiedSplat（开放词汇语义 3DGS）、AREA3D（主动重建智能体）、Uni3R
- **逆渲染/SLAM**：MVInverse、FUSER、Global SfM meets Feedforward

2025 年的 6 篇：PanSplat、FLARE、OmniSplat、FRESA、Light3R-SfM、Prometheus。

## 6.3 前馈式 vs 优化式（经典 3DGS）本质对比

| 维度 | 优化式（per-scene） | 前馈式（feed-forward） |
| --- | --- | --- |
| 原理 | 对每个场景迭代优化高斯参数（几分钟~几十分钟） | 一个神经网络前向传播，从图像直接回归高斯参数（秒级） |
| 速度 | 慢，逐场景 | **快，秒级，可批处理** |
| 泛化 | 无（每场景从头学） | **有**（训练分布内的场景零样本重建） |
| 质量上限 | **高**（逐场景拟合，细节/锐度好） | 中（分布内好；分布外、极端视角、反射/无纹理区明显退化） |
| 数据需求 | 一个场景 20~100 张图即可 | 训练需要大规模多视角数据集（成千上万场景），通常依赖 COLMAP 标注 |
| 推理硬件 | 单卡即可，3090 绰绰有余 | 推理更轻；训练重 |
| 多视角扩展 | 天然支持任意多视角 | 输入视角越多，显存/复杂度增长快 |
| 可编辑/动画 | 成熟（绑定、动画、光照） | 新兴，正在补 |
| 稳定性 | 每场景可调、结果确定 | 无训练分布外保证，偶发几何伪影 |

**核心权衡一句话**：前馈式用"质量上限"换"速度+泛化"。它不适合当"扫描仪"做单场景最高保真重建，但适合任何"不可能慢下来"的场景。

## 6.4 市场/工业应用现状

**已经在上量产的领域（前馈是唯一解）**：
- **移动端/端侧**：华为开发者论坛已有 3DGS 端侧重建能力开放；ECCV 2026 的 Flux-GS 把 3D 重建跑到手机上。
- **数字人/头像**：FRESA（2025，少图前馈重建可动头像）、GBC-Splat 等已在虚拟主播/数字人公司落地。
- **SLAM/实时感知**：LingBot-Map（单目前馈 3D 重建 SLAM）、EmbodiedSplat。
- **自动驾驶**：理想汽车等车企参与前馈 4D 合成（PhysGM）。

**仍以优化式为主、前馈为辅的领域**：
- 主流 3D 扫描 App（Luma / Polycam / KIRI / Scaniverse 类）核心仍是云端优化式 + 几十分钟出图；前馈被用来做预览、粗重建初始化或 COLMAP 替代。

**行业共识——混合路线**：
- 2026 年多篇顶会做"前馈+精修"统一：UFO（前馈与优化统一）、GIFSplat（生成先验+迭代前馈）、ZipMap（线性时间 test-time training）——**"前馈出粗稿、优化式打磨"几乎是工业界标准答案**。

## 6.5 必须知道的缺点/风险

1. **质量上限硬伤**：精细几何、遮挡、镜面反射、无纹理大平面，前馈式目前仍打不过逐场景优化；这是原理性差距。
2. **训练数据是命门**：高质量多视角训练集难获取，多靠 COLMAP 标注（有误差），Reliev3R 这类"去标注"工作说明学界都在被它卡。
3. **多视角越多越脆**：视角增多时显存和一致性负担快速上升，"多视角缩放/一致性"是公开难题。
4. **评估基准未统一**："泛化性"与"质量"两难，横向对比要小心。
5. **工业成熟度参差**：开源生态（DUSt3R、VGGT、SplatPose 系）比商业工具快，落地通常要自己改。

## 6.6 一句话总结（前馈式 3DGS）

前馈式 3DGS 不是"替代品"而是"提速器+泛化器"：它在秒级、可泛化、可部署的场景里是真刚需（手机、数字人、SLAM、自动驾驶已经在用），但在"单场景最高保真"上仍是优化式的天下。3090 做前馈式研究或"前馈+优化"混合产品完全可行——**推荐入，但别把它当优化式的上位替代，而是当它的另一半**。

---

# 7. 专题二：测试时方法科普

## 7.1 什么是"测试时方法"（Test-time Methods）

机器学习分两个阶段：**训练（training）** 和 **测试/推理（inference/test time）**。传统范式：训练时学好 → 部署后权重冻结 → 直接用。

**"测试时方法"指：模型已部署、正在做推理的那一刻，额外做计算或调整来提升效果，而不是依赖"训练时就把一切学好"。** 它把"下功夫"的时机从训练时挪到推理时。两大类：

### 测试时适应（Test-Time Adaptation, TTA）
- **问题**：模型训练用"训练分布"数据（晴天），部署后遇到"新分布"（雨雪/夜间/不同设备），性能掉。
- **做法**：模型在测试时，用当前遇到的**未标注数据自我微调**——更新 BatchNorm 统计量、熵最小化、自训练，"现场适应"新环境。
- **例子**：自动驾驶模型白天训练的，晚上部署时边跑边适应夜间画面，不用重新收集数据重训。
- **代表**：TENT、EATA；CVPR 2026 有 48 篇。

### 测试时扩展 / 测试时计算（Test-Time Scaling / Compute）
- **问题**：模型一次推理给不出好答案，怎么办？
- **做法**：**推理时多花算力换更准的结果**——让模型"思考更久"（更长思维链）、采样多个答案再投票（best-of-N）、搜索（树搜索/MCTS）、用验证器挑最优解。
- **为什么爆火**：OpenAI o1 / DeepSeek-R1 证明"推理时多算"能大幅提升推理能力，形成与"训练时堆算力"并列的第二增长曲线。
- **数据**：2025 年 CVPR 0 篇，2026 年 17 篇——**全新赛道**。

**为什么这类方法算力友好**：核心是"不重训大模型"，只在推理端做文章，所以算力门槛低、任何组都能做。

## 7.2 "免训练"的准确含义

> **"免训练（training-free）"≠"不要算力"，它的意思是"不更新模型权重"**——没有反向传播、没有梯度下降，只做前向推理 + 分析/干预。

以 `Reallocating Attention Across Layers` 为例：它在 VLM **推理时**，分析每一层的注意力头，识别哪些是"感知头"哪些是"推理头"，重新分配贡献比例来减少幻觉。整个过程**模型权重一个字节都没改**，但需要反复跑模型推理、读取注意力权重、做统计。

所以算力需求 = **推理的成本**，不是训练的成本。

## 7.3 3090（24GB）实际能跑什么模型

| 模型规模 | 精度 | 显存占用 | 3090 能跑吗 |
| --- | --- | --- | --- |
| 7B | FP16 | ~14-16GB | ✅ 轻松 |
| 7B | INT4 量化 | ~4GB | ✅ 极轻松 |
| 13B | FP16 | ~26GB | ❌ 超了 |
| 13B | INT8/INT4 量化 | ~13GB / ~7GB | ✅ 可以 |
| 30B+ | INT4 量化 | ~18-20GB | ✅ 勉强可以 |

（视觉部分 ViT 会再多占 1~2GB。）

**做研究两种形态**：
1. **需要读模型内部信息**（注意力、隐藏层、logits）→ 必须用**开源模型本地跑**（LLaVA、Qwen-VL、InternVL 等 7B/13B），因为 API 拿不到模型内部。3090 跑 7B 全精度、13B 量化完全够。
2. **只看输入输出**（黑盒方法，如多采样投票、思维链扩展）→ 可以本地跑开源模型，也可以直接**调 API**（GPT-4V、Gemini），连本地模型都不用。

**所以"测试时方法只能跑本地小模型"是误解**：要读内部就用本地开源模型（3090 能到 13B，多卡 70B 量化），黑盒方法直接调 API 也行。

## 7.4 微调 vs TTA vs Test-time Scaling（三者区别）

| 维度 | 大模型微调（Fine-tuning） | 测试时适应（TTA） | 测试时扩展（Test-time Scaling） |
| --- | --- | --- | --- |
| **改权重？** | ✅ 大范围改 | ✅ 小范围改（BN/LN 统计量、小 adapter） | ❌ **完全不改** |
| **发生阶段** | 部署**前**（离线） | 部署**后**（在线） | 部署**后** |
| **用什么数据** | 有标注训练集 | 测试时遇到的**未标注**数据 | 不需要数据 |
| **目的** | 让模型**学会**一个任务/领域 | 让模型**适应**当前这个具体环境 | 多花推理算力换更准 |
| **是否永久** | 永久改变模型 | 通常临时（换环境再适应） | 不改模型 |
| **算力** | 高（要训练） | 低（轻量更新或仅前向） | 低（仅推理） |
| **严格"免训练"？** | 否 | 否（有轻量训练） | **是** |

**通俗类比**：
- **微调** = 上岗前的**培训**——用医学影像把 VLM 训练成"懂医学"，训完定型。
- **TTA** = 上岗后的**入乡随俗**——模型部署到新医院，边收新数据边自我微调，适应这台设备。
- **Test-time Scaling** = 做题时**多打草稿/多检查几遍**——模型本身没变，就是推理时多费点脑子。

---

# 8. 方向选择系列建议

## 8.1 若做 3DGS 方向：为什么前馈式不是最优 + 更好的选择

**为什么前馈式不是这组算力下的最优选**：
- **赛道过挤**：2026 标题含 feed-forward 已 35 篇，对手是 Google DeepMind（VGGT）、Meta、国内大厂——拼通用前馈基础模型没有数据和算力优势。
- **训练成本高**：要 SOTA 需大规模多视角训练数据 + 多卡预训练，做到 SOTA 难，论文容易变成"又一篇 MVSplat 变体"。
- **差异化空间小**：35 篇意味着大量"前馈+X"已被占坑。

**3DGS 方向内推荐（按性价比排序）**：

| 方向 | 学术热度 | 竞争拥挤度 | 算力适配 | 一年可控性 | 综合 |
| --- | --- | --- | --- | --- | --- |
| 通用前馈式重建 | 极高 | 极高 | 中（拼不过大厂） | 中 | ★★ |
| **3DGS×生成融合** | 高 | 中高 | **好（复用开源权重）** | **好** | ★★★★★ |
| **4D 动态 3DGS** | 高 | 中 | 好（单场景级） | 中 | ★★★★ |
| 3DGS×语义/具身 | 中高 | 中 | 好 | 中（需数据/环境） | ★★★☆ |
| 特殊模态 3DGS | 中 | **低** | **最好** | **最好** | ★★★★（取决于数据） |

- **首选：3DGS × 生成式融合（稀疏视角补全/生成先验引导）**——站在 2026 第一主流（生成式，generative 命中 1534）与 3DGS 的交叉，用开源生成权重就能起步，差异化空间大（补全/编辑/4D 补全）。参考 Gen3R、GIFSplat、Pano3DComposer。
- **次选：4D 动态 3DGS**——4D/dynamic 2026 命中 47 篇且扩张中（2025 仅 25 篇），故事是"从静态世界到动态世界"。参考 Catalyst4D、PhysGM、ProgressiveAvatars。
- **第三：3DGS × 语义/具身底座**——开放词汇语义 3DGS（EmbodiedSplat、Uni3R），前提是组里有机器人/具身资源。
- **稳妥保底：特殊模态 3DGS（全景/红外/事件/鱼眼）**——竞争最少、差异化最强（DirectFisheye-GS、PhysIR-Splat、PanSplat），前提是有特殊传感器数据。

## 8.2 若跳出 3DGS：更广泛的推荐

**第一梯队（强烈推荐）**：
1. **测试时方法（TTA / test-time scaling / 推理时计算）**
   - 数据：TTA 18→48（+167%）；test-time scaling 0→17（全新）。
   - 算力最优：核心是"用预训练模型 + 推理时自适应/校准"，不重训大模型，单张 3090 可跑。
   - 时间完全可控，竞争新兴未被大厂垄断。
2. **大模型可靠性 / 幻觉治理 / 推理时干预**
   - 数据：幻觉 48→100（+108%）；可靠性相关 483 篇。
   - 算力最优：大量工作免训练，只需推理+分析。
   - 故事：大模型落地第一质量瓶颈。

**第二梯队（推荐）**：
3. **视觉推理 / 空间推理（VLM 推理）**——spatial reasoning 28→102（+264%），算力★★★★。
4. **智能体（GUI Agent / 多智能体）**——GUI agent 2→18、multi-agent 20→45，算力★★★☆（需环境）。
5. **效率压缩（量化/token稀疏/MoE）**——97→157（+62%），算力★★★★，但偏工程。

**第三梯队（有条件再做）**：
6. 具身智能/世界模型（需仿真/机器人资源）；7. 医疗 AI（需医疗数据合作）；8. 扩散生成/编辑（最拥挤）。

**两者可合并**：做"**推理时增强大模型可靠性/推理能力**"（推理时视觉 grounding 校准、测试时幻觉抑制），站在两个热点交叉上。

**一句话**：这套算力和时间，**不要去卷"更大的模型/更通用的重建"（拼资源拼不过），要去做"让现有大模型在部署端更聪明/更可靠"的推理时方法**——这是数据里增速最猛、算力要求最低、竞争最不拥挤的交叉地带。

## 8.3 留守 3DGS vs 换方向：决策建议

**结论：换，但不是逃离三维重建，而是带着三维重建的家底"升维"——从"为了重建而重建"转向"为空间智能/世界模型/3D生成服务的 3D 表征"。**

**为什么不建议留守传统 3DGS**：
- 3DGS 主方向绝对数 168→190（+13%），低于总量增速（+40.8%），纯"渲染/重建质量内卷"已被稀释；通用前馈式一年冒出 35 篇，极度拥挤。

**为什么不建议完全跳到纯大模型/NLP**：
- 组积累清零，与本来做 NLP/大模型的组竞争没优势；纯大模型方向算力不够拼；纯 NLP 不在 CVPR 数据范围内，无法基于数据判断。

**为什么"带着 3D 家底换赛道"最优**：
- 2026 年增长最猛的三个引擎，底座全都是 3D：具身智能（+137%）、世界模型（×3）、空间推理（×3.6）、4D（×2）。
- 这些方向拼的不是"谁重建得更准"，而是"谁能让 AI 理解、预测、生成 3D 物理世界"——三维重建背景的人是最对口的接盘者。

**推荐大方向（按优先级）**：
1. **空间智能 / 3D 世界模型**——三维重建背景最对口的下一站。
2. **3D 生成（3D AIGC）**——text/image-to-3D、3D 资产生成与编辑，懂几何的人做 3D 生成有优势。
3. **具身智能的 3D 感知底座**——前提是组里能搭上机器人/仿真资源。

## 8.4 空间智能 / 3D 世界模型详解

### 这个方向是什么（三条线）

CVPR 2026 标题含 world model 的论文 2025 年 12 篇 → 2026 年 **34 篇**，实际分三条线：

**A 线：3D/几何世界模型（最对口）**
用显式 3D 表征（3DGS、点云、占用网格）作为世界模型的"状态"，预测世界随时间/动作演化。2026 代表：
- GaussianDWM（3D 高斯驾驶世界模型）
- GeoWorld（几何世界模型）
- PointWorld（点云世界模型用于机器人操作）
- TraceGen（3D 轨迹空间世界建模）
- GenieDrive（4D 占用引导的物理感知驾驶世界模型）
- SparseWorld-TC（轨迹条件稀疏占用世界模型）
- 前身是 2025 的 GaussianWorld

**B 线：视频世界模型的 3D 化**
给视频生成模型装上"3D 的骨架"——相机控制、3D/4D 几何一致性。代表：VerseCrafter（4D 几何控制）、Stereo World Model（相机引导）、GEN3C（3D 一致性视频生成）、AC3D、BulletTime。2025 这类 14 篇、2026 又 10 篇。

**C 线：空间智能（VLM 的 3D 空间推理）**
让大模型理解 3D 空间关系（方位、距离、遮挡、视角变换）。2025 标题仅 2 篇 → 2026 **28 篇**（×14 倍）：SpatialStack、Think with 3D、SpaceMind、PanoEnv。

### 与三维重建的关联 & 3DGS 知识复用度

| 线 | 具体内容 | 3DGS/重建知识复用 |
| --- | --- | --- |
| A 线 3D 世界模型 | 3DGS/点云/占用当世界模型状态表征 | **80~100%**：高斯参数化、相机模型、多视角几何、占用/深度直接用 |
| B 线 视频 3D 化 | 相机轨迹/深度/视角一致性作为视频模型控制条件 | **60~80%**：极线几何、投影、视角合成是核心 |
| C 线 空间智能 | 把 3D 几何知识"喂"给 VLM | **40~60%**：3D 几何是内核，模型主体换成 VLM |

### "世界模型吃算力"的澄清

| 层次 | 算力需求 | 能否做 |
| --- | --- | --- |
| 从零预训练视频世界模型 | 数百张 H100 | ❌ |
| 全参微调 14B 视频模型 | 8~32 张 A100 | ❌ |
| LoRA/adapter 微调 2B~5B 视频模型 | 单卡 24G | ✅ 3090 机器 |
| 开源视频模型上加 3D 控制模块（B线） | 1~4 卡 | ✅ |
| **3D/高斯世界模型（A线）** | 1~4 卡 | ✅ **最匹配** |
| 组件研究（tokenizer/潜空间/评测） | 1~4 卡 | ✅ |

**关键洞察**：A 线恰恰绕开算力壁垒——状态用显式 3D，不依赖海量视频预训练，在公开数据集上训中等模型即可。2026 年 GaussianDWM/PointWorld/GeoWorld/TraceGen 密集出现说明：**学术界自己发现了"3D 表征是世界模型的算力捷径"**。

### 具体细分领域推荐（按性价比排序）

1. **3D/高斯世界模型（A线）——首选**：2025 仅 GaussianWorld 一两篇 → 2026 一批，正在爆发且未饱和。可切入：驾驶/室内场景高斯世界模型（时序预测+新视角渲染闭环）、带不确定性的 4D 世界模型、动作条件 3D 世界模型。
2. **视频生成模型的 3D/相机控制（B线）**：两年合计 24 篇且持续。可切入：相机轨迹精确控制的视频生成、视角/几何一致性损失、3D 先验约束视频扩散。有开源视频权重可搭（CogVideoX、Wan2.1）。
3. **空间智能 / VLM 3D 空间推理（C线）**：2025→2026 标题数 ×14（2→28），全库增长最陡细分之一。可切入：3D 表征注入 VLM、几何想象 3D 推理、3D 空间推理 benchmark。很多工作免训练或轻量微调，算力最省。
4. **（穿插备选）世界模型组件与评测**：tokenizer（Planning in 8 Tokens）、潜空间几何（Cloning Deterministic Worlds）、世界模型评测（WorldLens）。算力最友好。

## 8.5 大模型方向（微调/推理优化/token压缩）详解

### 数据热度

| 细分 | 2025→2026 | 增速 |
| --- | ---: | --- |
| 效率压缩大方向 | 97 → 157 篇 | +62% |
| token 剪枝/合并/压缩 | 18 → 62 | ×3.4 |
| MoE | 27 → 74 | ×2.7 |
| 量化 | 54 → 70 | +30% |
| RL/GRPO/奖励模型 | 61 → 336 | ×5.5 |
| test-time scaling | 0 → 17 | 全新 |
| 幻觉治理 | 48 → 100 | ×2.1 |
| VLM/MLLM 渗透 | 400 → 890 | +122% |

### 三维评估（时间/算力/方向）

- **时间**：✅ 最友好。有 LoRA/RAG 基础，微调类实验周期短（单卡几小时到几天一轮），一年能跑 2~3 轮完整迭代。
- **算力**：✅ 匹配度极高。7B 模型 LoRA/QLoRA 单卡 3090 就够；token 压缩/推理优化研究通常在中小模型上验证。比空间智能算力门槛更低。RL 后训练（GRPO）稍吃算力，3×3090 做 7B 级是下限可行。
- **方向**：⚠️ 有隐忧——① 拥挤且对手强（大厂工程团队顺手就做，纯"方法微改进"易被淹没）；② 脱离组积累（3D 组转纯大模型后组内资源用不上）。

### 细分方向推荐（按"学术空间×就业价值×算力匹配"排序）

1. **多模态大模型（VLM）的推理优化与 token 压缩 —— 首选**
   - 数据：`pruning vision-language` 已成 2026 标题 bigram；Quant Experts（VLM 量化 MoE）等密集出现。
   - 为什么好：VLM 视觉 token 动辄几百上千个，冗余严重，压缩空间比纯文本大得多，研究不饱和；是大模型方向里唯一能沾视觉背景边的细分。
   - 就业：VLM 部署优化是大厂和自动驾驶/机器人公司刚需岗位。
2. **推理时方法（test-time scaling / 推理时干预）—— 学术最新**
   - 0→17 全新赛道，幻觉治理 ×2.1。算力要求最低，偏研究向。
3. **PEFT/微调方法学（LoRA 变体、MoE 微调、持续微调）—— 舒适区延伸**
   - 有基础切入快，但较挤，需找独特场景（多模态微调、增量微调、微调稳定性）。
4. **RL 后训练（GRPO/RLHF）—— 就业单价最高**
   - 61→336（×5.5）。7B 级 GRPO 在 3×3090 上下限可行；就业市场"会做 RL 后训练"溢价最高。
   - 风险：偏工程，发论文需找方法创新点。
5. **幻觉治理/可靠性 —— 学术价值高、就业一般**
   - 免训练方法多、算力友好、CVPR 痛点明确（483 篇），但工业界对口岗位相对少。

---

# 9. 个人约束条件汇总

| 项目 | 详情 |
| --- | --- |
| **算力** | 服务器1：3×3090（24G）= 72G；服务器2：4×4080（16G）= 64G；服务器3：8×2080（11G，Turing 架构）= 88G |
| **算力使用建议** | 3090 机器：主力训练（3DGS/高斯世界模型、2B~5B 视频模型 LoRA、7B VLM 微调）；4080 机器：第二训练机（4DGS、中型模型微调）；2080 机器：推理/评测/小模型/数据并行（注意 Turing 架构不支持 bf16/FlashAttention-2，跑新型视频扩散模型有兼容性问题）；不建议跨机分布式训大模型（网络带宽瓶颈），按"机器=实验单元"任务级并行 |
| **时间** | 不到一年（~10-12 个月），需选"现成 baseline + 细分新颖点"的赛道 |
| **组背景** | 全组做三维重建，三维重建领域知识积累深厚（但用户感觉"卷到头"） |
| **个人基础** | 深度学习基础、LoRA 微调、RAG 经验 |
| **导师态度** | 允许发散，方向不限（CV、大模型均可） |

---

# 10. 最终决策矩阵与建议

## 10.1 各候选方向综合对比

| 方向 | 学术热度 | 增长斜率 | 组积累复用 | 算力适配 | 一年可控 | 竞争密度 | 就业面 | 就业单价 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 通用前馈式 3DGS | 极高 | 高 | 高 | 中（拼不过大厂） | 中 | 极高 | 窄 | 高 |
| 3DGS×生成融合 | 高 | 高 | 高 | **好** | **好** | 中高 | 窄 | 高 |
| 4D 动态 3DGS | 高 | 高 | 高 | 好 | 中 | 中 | 窄 | 高 |
| **空间智能/3D世界模型** | 高 | **最陡（×3~14）** | **80~100%** | 好（3D表征路线） | 中 | 中 | 窄 | 高 |
| 测试时方法（TTA/TT-scaling） | 新且快增 | 陡（0→17） | 低 | **最好** | **最好** | 低 | 中 | 中 |
| 大模型可靠性/幻觉治理 | 高（+108%） | 陡 | 低 | 最好 | 好 | 中 | 中 | 中 |
| **大模型微调/推理优化/token压缩** | 高 | 陡（×3.4） | 接近 0 | **最好** | **最好** | 高 | **宽** | 中高 |
| VLM 推理优化/token压缩 | 高 | 陡 | 部分（视觉边） | 最好 | 最好 | 中 | 宽 | 高 |

## 10.2 分情境结论

**情境 A：纯发论文（一年内学术产出最大化）**
→ **推荐空间智能/3D世界模型优先**。理由：增长斜率最陡、竞争最稀疏、组积累直接复用、差异化强。大模型微调/推理优化赛道人太多，一年内做出"非变体式"贡献更难。
→ 此情境下大模型方向只推荐：**多模态大模型的 token 压缩/推理优化**（沾视觉边，且是效率赛道里相对不挤的）。

**情境 B：结合就业**
→ **天平反转，推荐大模型方向**。理由：
1. 就业面差距是数量级的——"大模型微调/推理优化/RAG/后训练"对应 LLM 算法、AI Infra、推理引擎、应用开发等几乎所有 AI 公司的岗位；空间智能对口岗位集中在少数自动驾驶/机器人/AR 公司。
2. LoRA/RAG 基础 + 一年深耕"微调+推理优化"，简历技能直接对口，投入产出比最高。
3. 推理优化/token 压缩这类"让模型跑得快"的技能是长期刚需，职业生命周期长。
→ 此情境下细分排序：**VLM 推理优化/token压缩 > RL 后训练（若算力扛得住）> PEFT 微调方法 > test-time scaling**。

## 10.3 综合最优解

**最优解是交叉：「多模态大模型（VLM）的推理优化 / token 压缩」**。理由：
- **论文端**：站在效率（+62%）× VLM（+122%）× token 压缩（×3.4）三个增长曲线的交点，且有视觉 token 这个差异化抓手，不是纯变体；
- **就业端**：VLM 部署优化是 2026 年大厂、自动驾驶、机器人公司都在抢人的岗位；
- **背景端**：3D 视觉组出身，懂视觉特征/token 的几何含义，比纯 NLP 背景的人做"视觉 token 压缩"更有直觉；
- **算力端**：7B 级 VLM 微调+推理优化，3090 单卡起步，三台机器完全够。

**备选路线（学术优先）：空间智能/3D世界模型的 A 线（3D/高斯世界模型）**——3DGS 知识复用度最高（80~100%）、算力门槛最低（1~4 卡）、2026 正在爆发且未饱和。

**一句话总决策**：
> 纯冲学术选空间智能/3D世界模型；考虑就业选大模型——而如果两头都想占，就做**"多模态大模型的推理优化/token 压缩"**，它是视觉背景、大模型就业红利、和有限算力三方约束下的最大公约数。无论选哪条，都**不要去卷"更大的模型/更通用的重建"（拼资源拼不过），要去做"让现有模型在部署端更聪明/更快/更可靠"的方向**。

---

# 11. 附录：数据文件位置与复现方法

## 11.1 数据文件

```
e:\Work\yan1\early_explore\paper\
├── run_cvpr.py                  # 爬取+分类入口脚本
├── cvpr/                        # 核心模块
│   ├── net.py                   # HTTP 层（线程安全 Session、指数退避、礼貌延时）
│   ├── parser.py                # 页面解析（列表页/详情页）
│   ├── pipeline.py              # 三段式流水线（元数据→摘要→分类导出）
│   └── topics.py                # 方向词表与关键词加权分类器
├── cvpr_papers/                 # CVPR 2026 数据（4042 篇）
│   ├── 00_ALL_labeled.csv       # 全量表（含方向标签+摘要）
│   ├── by_topic/                # 25 个方向各自 CSV
│   ├── topic_stats.json/md      # 统计
│   └── raw/                     # 原始元数据+摘要缓存
└── cvpr_papers_2025/            # CVPR 2025 数据（2871 篇，结构同上）
```

## 11.2 复现/扩展方法

- **重新分类**（改词表后）：`conda run -n scrapling python run_cvpr.py --years 2026 --skip-abstracts`
- **爬其他年份**：`conda run -n scrapling python run_cvpr.py --years 2024 --out cvpr_papers_2024`
- **只下某方向 PDF**：`conda run -n scrapling python run_cvpr.py --pdf-topic Diffusion_Generative`
- **试跑**：`conda run -n scrapling python run_cvpr.py --limit 30`

## 11.3 分析方法说明

本报告所有统计基于对 `00_ALL_labeled.csv` 的关键词频次分析，包括：
- 各方向摘要高频词、技术术语命中数（基于技术术语词典子串匹配）
- 标题 Bigram 频次
- 跨方向热点主题命中数（基于查询词典，一篇可命中多个主题）

**注意**：术语命中存在子串误匹配噪音（如 `gui` 会误匹配 "guidance"、`var` 会误匹配 "various"），解读时已剔除明显噪音项。所有"增长倍数"在 2025 年基数极低（个位数）时仅供参考方向性，不作为精确扩张度量。

---

*报告完*
