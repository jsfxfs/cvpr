# 实例：NGC2 的"数据层"——"数据为中心"做成了一套能跑的系统

> 用途：给 `modaf-study/` 两篇材料配的真实实例。只讲它怎么工作、怎么构成，不铺时间线。
> 定位说明（2026-09-21）：本实例偏"数据层 / 数据传输与互操作"视角，**已降为备选**；现主实例为同目录 `实例_Hadean_Palantir_AI兵棋与评估.md`（评估/推演类，与课题组"体系效能评估"方向更贴）。需讲美军/DoDAF 语境或"数据层怎么落地"时仍用本文。
> 事实截至 2026-09，来源见文末；正式引用前建议复核原文链接。

## 一句话

美国陆军把原来 17 个各自立项、互不通气的指挥系统（火力一套、后勤一套、防空一套……）换成一套四层结构，叫 **NGC2**。2026 年 6 月，其中的**数据层**定型，就三样东西：

- **Anduril 的 Lattice**：管战术边缘（离战场最近的那一端）；
- **Palantir 的 Foundry**：管云端；
- **Raft 的数据平台**：管中间——数据注册、格式转换、联邦。

定完之后，所有应用——厂商写的、士兵自己写的——都只接这一个数据层，不再各自去接传感器。这就是"数据为中心"落地后的实际形态。

官方术语对照：这套东西叫 common data baseline（通用数据基线）；Foundry = cloud data layer（云数据层），Lattice = tactical data layer（战术数据层），两者合起来叫 edge-to-cloud data mesh（边缘到云数据网格）。

## 骨架：四层各干什么

| 层 | 干什么 | 靠什么 |
| --- | --- | --- |
| 传输层 | 在"拒止、降级、时断时续、低带宽"（DDIL）环境下把数据传出去 | LEO 卫星、5G 专网、新旧电台 |
| 计算层 | 跑 AI/ML，把海量数据分类、整理、排序 | 边缘：加固计算盒（TEC，战术边缘计算机，装在车/指挥所/无人机上）；云：数据中心 |
| 数据层 | 把传感器、平台、指挥数据变成一套"共同语言"，谁都能读能写 | Lattice + Foundry + Raft（下面三节） |
| 应用层 | 人实际操作的界面 | 态势图、火力、后勤、空域管理……厂商应用 + 士兵自建应用 |

层与层之间走政府掌握的开放 API，每层可以单独换供应商——这是"不搞烟囱"在工程上的具体做法。

## 数据层（一）边缘：Lattice 把杂乱的传感器合成一份"目标清单"

- **跑在哪**：TEC。演习里从 65 台扩到 130 台。
- **收什么**：雷达回波、红外图像、射频信号、无人机画面——各家厂商、各种格式。
- **做什么**：在本地（不是传回后方）融合成统一的目标航迹；只传结构化的小数据——位置、速度、类型，不传原始视频。
- **为什么这么设计**：
  1. 带宽小也能用：被电子战压制时，传视频的系统瘫痪，"目标数据"还能走；
  2. 链路自愈：一路被干扰，数据自动从别的节点绕过去；
  3. 断链不死：跟云端断开时，边缘自己就是一个完整系统，照常作战。
- 第三方传感器/武器靠 SDK 接入，厂商自己写接口就能入网。

## 数据层（二）云端：Foundry 让所有系统对"同一个东西"有同一个说法

核心概念叫 **Ontology（本体）**，说人话就四件事：

- 定义**对象**：一个目标、一批弹药、一辆车、一名士兵；
- 定义对象之间的**关系**：这批弹药属于哪个单位、这个目标谁在跟踪；
- 定义能做的**动作**：下补给单、分配火力任务；
- 定义**函数**：算，比如按当前消耗速度预测弹药还能打几天。

为什么这一步是关键：以前情报的"目标"、火力的"目标"、后勤的"消耗"是三套数据结构，接不起来。都放进同一个本体之后，陆军给出的典型推演是：

情报系统在地图上标一个红 X → 火力系统的地图上自动出现同一个红 X（不用重新标定）→ 后勤能看到打这个目标消耗了多少弹药 → 自动生成预测性补给建议。

这就是"先统一定义数据、再谈应用"的字面含义。对照材料：Foundry 的本体 ≈ MODAF 的 M3/MODEM 那一层（数据字典），都是定义"有哪些实体、怎么关联"；区别是 M3 供人画视图、出文档，Ontology 是运行中的数据结构，应用直接读写它。

## 数据层（三）接缝：Raft 管注册、转换、联邦

- **注册表**：谁生产什么数据、谁消费什么数据，登记在册；
- **转换**：把各家格式在下发前归一化成通用格式；
- **联邦**：决定哪些数据可以被发现、连接、路由。

关键设计：新传感器、新应用只要注册接入，不用改 Lattice 和 Foundry 的核心代码。动机就一个——防止数据层变成新的供应商锁定：地基不动，上面随便换。

## 一条数据实际怎么走

演习里真跑过的场景（Ivy Sting 4）：

1. 模拟干扰机切断卫星链路，部队与"师级云"失联；
2. 中队的雷达/红外在 TEC 上融合出航迹，Lattice 在本地分发，中队层级照常作战；
3. 干扰源被定位、用迫击炮打掉；
4. 链路恢复，边缘数据自动回灌到师、师级数据自动下推回中队，态势图无缝拼回一块。

链路正常时，这就是官方说的 edge-to-cloud data mesh：Lattice 管边缘那半张网，Foundry 管云上那半张网，数据两个方向都流。断的时候两边各自活，恢复后自动对齐——这是整套东西最像"架构"的地方。

## 它怎么被造出来：两个团队、两个师、同一道题

不是"立项—招标—造十年—交付"，而是两家团队各配一个师、做同一件事，靠演习加码来比：

- Anduril + Palantir → 第 4 步兵师（Ivy Sting 系列，科罗拉多）；
- Lockheed 团队 → 第 25 步兵师（Lightning Surge 系列）。

比的刻度就是规模：到 Ivy Mass 演习时——TEC 65→130 台、士兵接入设备 10→2500+ 台、应用 40 个、数据流 36 路、传感器与效应器 37 个、9 种硬件形态，再叠加网络/电子战攻击。

结果：2026 年 6 月陆军选 Anduril 牵头数据层（Palantir、Raft 参与）；Lockheed 没出局，继续管第 25 师的全栈实施，并把方案并到同一个数据底座上——数据层只有一份，上层应用各家自己做。这个安排本身就是"数据为中心"：锁在下面，开放在上面。

## 能随手举的 5 个例子（都在演习里跑过）

1. **同一张图**：后勤、火力、情报参谋在同一界面看同一份数据，省掉"为对齐情况开一小时参谋会"。
2. **油弹自动上报**：一辆坦克、一辆布拉德利、几辆斯崔克装了油料/弹药传感器，余量实时进系统，指挥官据此直接下补给单；下一步推到营级。
3. **士兵体征**：随身体感器上报生命体征和伤亡状态；军医在现场记录处置措施、直送后方野战医院接诊医生；指挥官随时知道还剩多少人在战斗，而不是靠估。
4. **抗干扰**：上面"一条数据怎么走"那个场景。
5. **空域管理**：无人机太多，"给火力打击放行空域"变得极复杂——四家厂商在 Ivy Sting 里做一个统一界面（统一跟踪无人机和飞机），替代几套各管一段的旧系统。

## 如果被追问"这跟 MODAF / DoDAF 什么关系"

只讲对得上的，不硬扯：

1. **"数据为中心"**：MODAF 里它是原则——图是数据的投影，先有数据后有图，但数据服务于"把体系描述清楚"；NGC2 里它是运行机制——传感器和应用直接读写同一个数据层，接口是工程强制的。同一个想法，一个落在文档上，一个落在系统里。
2. **元模型 vs 本体**：M3/MODEM 和 Foundry Ontology 干的是同一件事——定义"有哪些实体、怎么关联"。M3 是描述体系用的数据字典（产出：视图/文档），Ontology 是作战系统用的数据字典（产出：决策/指令）。
3. **框架 vs 平台**：MODAF 回答"怎么把体系描述清楚"；NGC2 回答"怎么让数据在体系里流动"。MODAF 2021 年退役（由 NAF v4 取代），但它要解决的问题——互操作、反烟囱——没消失；美军现在的答案不是新框架，而是直接建数据底座。

## 备选实例（要换例子时用）

| 实例 | 一句机制 | 适合讲什么 |
| --- | --- | --- |
| 北约 MSS NATO（2025） | Palantir 平台用于情报融合、目标锁定、态势感知；6 个月从需求走到合同 | 平台级 AI 进入联盟作战体系 |
| TITAN（2026-09 批产） | Palantir 主承包的陆军地面情报站，批产 8 套（与 Anduril 合作） | 从原型到量产、进编制 |

## 来源

- 陆军公告（2026-06-22）：<https://www.army.mil/article/293409/army_and_industry_align_on_common_data_baseline_as_next_generation_command_and_control_moves_from_prototyping_to_delivery>
- DefenseScoop 解读（含数据层构成、Welch/Kramer 引语）：<https://defensescoop.com/2026/06/22/army-taps-anduril-lead-ngc2-common-data-layer-baseline/>
- Palantir 新闻稿（Foundry=云数据层、Lattice=战术数据层）：<https://www.businesswire.com/news/home/20260622171213/en/Palantir-Secures-Foundational-Role-in-NGC2-Data-Layer>（镜像：<https://www.stocktitan.net/news/PLTR/palantir-secures-foundational-role-in-ngc2-data-oyuib538gyv0.html>）
- Tectonic Defense（Ivy Mass 规模数字、Raft 分工）：<https://www.tectonicdefense.com/anduril-tapped-to-lead-ngc2-common-data-baseline/>
- Defense One（Ivy Sting 4 现场细节：后勤/体征/抗干扰）：<https://www.defenseone.com/defense-systems/2026/02/army-moves-link-full-division-its-next-gen-c2-prototype/411259/>
- Inside Defense（NGC2 空域管理工具）：<https://insidedefense.com/daily-news/really-complicated-problem-army-developing-ngc2-airspace-management-tool-through-ivy>
- Palantir 官方文档（Ontology 四要素）：<https://www.palantir.com/docs/foundry/ontology/overview>
- 渊亭防务（中文四层堆栈梳理、红 X 推演）：<https://news.qq.com/rain/a/20251010A04POA00>
- 陆军演习报道：Ivy Sting 4（<https://www.army.mil/article/290401/4th_infantry_division_showcases_ivy_sting_4_a_leap_forward_in_command_and_control>）、Ivy Mass（<https://www.army.mil/article/292999/ivy_mass_exercises_ngc2_at_division_scale>）

> 注：以上均为公开新闻稿/官方页面信息，整理于 2026-09；部分数字（TEC 台数、应用数等）来自厂商与防务媒体报道，未经陆军逐条确认。
