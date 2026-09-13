"""研究方向词表与关键词加权分类器。

背景：CVF openaccess 页面**不提供任何官方的方向/主题/关键词字段**
（详情页只有 title / authors / abstract / bibtex），因此方向必须由我们自己推断。

分类逻辑：
    1. 每个方向配一组 (正则, 权重)，权重 3 = 强特征，2 = 中等，1 = 弱特征。
    2. 打分：标题命中权重 ×3，摘要命中权重 ×1（标题更能代表方向）。
       同一正则最多计 3 次命中，避免长摘要靠词频刷分。
    3. 主方向 = 最高分；多标签 = 分数 ≥ 最高分 ×rel_threshold 且 ≥ min_score。
    4. 置信度 = (最高分 - 次高分) / 最高分，用于挑出需要人工/LLM 复核的样本。

想调整方向划分时，只改本文件的 TOPICS，然后重跑分类阶段即可（无需重新爬取）。
"""

import re
from typing import Dict, List, Optional, Tuple

OTHER = "Other"

# 每个方向: (方向名, [(正则, 权重), ...])
TOPICS: List[Tuple[str, List[Tuple[str, int]]]] = [
    ("3D_Reconstruction", [
        (r"\bpoint\s?cloud", 3), (r"\b3d\s+reconstruction\b", 3), (r"\bmeshes?\b", 2),
        (r"structure[- ]from[- ]motion|\bsfm\b", 3), (r"multi[- ]view stereo|\bmvs\b", 3),
        (r"surface reconstruction", 3), (r"\b3d\s+shape\b|shape (completion|generation)", 2),
        (r"text[- ]to[- ]3d|image[- ]to[- ]3d", 3), (r"\b3d\s+aware\b", 2), (r"\bcad\b", 1),
        (r"scene reconstruction|indoor (scene )?reconstruction", 2), (r"\b3d\s+scene\b", 1),
    ]),
    ("Neural_Rendering_NeRF_3DGS", [
        (r"\bnerf\b|neural radiance field", 3), (r"gaussian splatting|\b3dgs\b", 3),
        (r"radiance field", 3), (r"neural rendering", 3),
        (r"novel view synthesis|view synthesis", 3), (r"volumetric rendering", 2),
        (r"implicit (neural )?(representation|field)", 2), (r"4d (gaussian|reconstruction)", 3),
        (r"dynamic (scene|view) (rendering|synthesis)", 2), (r"relight", 2),
    ]),
    ("Object_Detection", [
        (r"object detection", 3), (r"\bdetectors?\b", 2), (r"\bdetr\b|\byolo\b|r[- ]?cnn", 2),
        (r"bounding box", 2), (r"open[- ]vocabulary (object )?detection", 3),
        (r"anchor[- ]free", 2), (r"3d object detection", 2),
        (r"tiny object|small object", 1), (r"oriented (object|bounding)|rotated (object|bounding)", 3),
        (r"open[- ]world (object|detection)", 3), (r"\bdetection\b", 1),
    ]),
    ("Segmentation", [
        (r"semantic segmentation", 3), (r"instance segmentation", 3), (r"panoptic", 3),
        (r"\bsegmentation\b", 2), (r"segment anything", 2),
        (r"scene parsing", 3), (r"referring (expression )?segmentation", 3),
        (r"image matting|video matting", 3), (r"saliency|salient object", 3),
        (r"open[- ]vocabulary segmentation", 3), (r"video object segmentation", 3),
        (r"part segmentation|co[- ]segmentation", 3),
    ]),
    ("Tracking_MOT", [
        (r"multi[- ]object tracking|\bmot\b", 3), (r"single object tracking|\bsot\b", 3),
        (r"visual object tracking", 3), (r"\btracking\b", 2), (r"\btracker\b", 2),
        (r"re[- ]?identification", 3), (r"data association", 2), (r"multi[- ]target", 2),
    ]),
    ("Human_Pose_Body", [
        (r"(human|body|hand|head|full[- ]body|whole[- ]body)\s+pose", 3),
        (r"pose estimation", 2), (r"human mesh|\bsmpl\b", 3), (r"\bkeypoint", 2),
        (r"skeleton", 2), (r"gait recognition", 3),
        (r"human[- ]object interaction|\bhoi\b", 2), (r"3d human|human body reconstruction", 3),
        (r"crowd (counting|analysis|scene)", 2), (r"pedestrian", 2),
        (r"human (motion|avatar|animation)", 2), (r"clothed human", 3),
    ]),
    ("Face_Biometrics", [
        (r"\bfaces?\b|\bfacial\b", 3), (r"face recognition", 3),
        (r"anti[- ]spoofing|spoof detection|presentation attack", 3),
        (r"face (detection|alignment|parsing|synthesis|generation|swap|editing)", 3),
        (r"biometric", 2), (r"\biris\b|\bfingerprint\b|\bpalmprint\b|\bvein\b", 3),
        (r"gaze estimation|eye tracking|head pose", 2),
        (r"facial (expression|attribute|landmark)", 3),
        (r"3d face|face reconstruction|face model", 3), (r"talking (face|head)", 2),
        (r"micro[- ]expression", 3), (r"face (anti|forgery)", 3),
    ]),
    ("Video_Action_Recognition", [
        (r"action recognition", 3), (r"video (understanding|recognition|classification|representation)", 3),
        (r"temporal action (localization|detection|segmentation)", 3),
        (r"spatio[- ]temporal", 2), (r"egocentric|first[- ]person", 3),
        (r"video (summarization|captioning|retrieval|prediction|generation|editing)", 2),
        (r"long[- ]form video|untrimmed video|long video", 2),
        (r"video segmentation", 2), (r"moment retrieval|video grounding", 3), (r"\bvideo\b", 1),
    ]),
    ("Vision_Language_Multimodal", [
        (r"vision[- ]language", 3), (r"visual[- ]language", 3), (r"\bvlm(s)?\b", 3),
        (r"\bclip\b", 2), (r"multi[- ]?modal", 2), (r"image[- ]text|text[- ]image", 2),
        (r"cross[- ]modal", 2), (r"visual question answering|\bvqa\b", 3),
        (r"image captioning|video captioning|dense caption", 3),
        (r"multimodal (learning|model|understanding|reasoning|alignment)", 3),
        (r"referring expression", 2), (r"visual (instruction|in[- ]context)", 3),
    ]),
    ("LLM_Reasoning_Agent", [
        (r"large (language|vision[- ]language|multimodal) model", 3),
        (r"\bllm(s)?\b|\bmllm(s)?\b", 3), (r"chain[- ]of[- ]thought|\bcot\b", 3),
        (r"instruction (tuning|following)", 3), (r"\bagent(s|ic)?\b", 2),
        (r"in[- ]context learning", 3), (r"\bprompt(s|ing)?\b", 2), (r"\bgpt\b", 2),
        (r"visual reasoning", 2), (r"test[- ]time (scaling|compute)", 2),
        (r"\breasoning\b", 1), (r"hallucinat", 2),
    ]),
    ("Diffusion_Generative", [
        (r"diffusion (model|process|probabilistic|transformer)", 3),
        (r"\bddpm\b|\bddim\b", 3), (r"score[- ]based (generative|model)", 3),
        (r"latent diffusion|stable diffusion", 3), (r"text[- ]to[- ]image|text[- ]to[- ]video", 3),
        (r"image (generation|synthesis)", 2), (r"generative (model|adversarial)", 2),
        (r"\bgan(s)?\b", 2), (r"flow matching|rectified flow|normalizing flow", 2),
        (r"consistency model", 3), (r"controllable (image|generation)|conditional generation", 2),
        (r"image editing|inpainting", 2), (r"personaliz|custom (text|concept|subject)", 2),
        (r"3d generation|3d[- ]aware generation", 2),
    ]),
    ("Restoration_Enhancement", [
        (r"super[- ]resolution", 3), (r"image restoration", 3),
        (r"\bdeblur|\bderain|\bdehaze|\bdenoise|denoising|deblurring|deraining|dehazing", 3),
        (r"low[- ]light|night (image|scene)|dark image", 3), (r"image enhancement", 2),
        (r"inpainting|image completion", 2), (r"underwater image", 3),
        (r"compressed? sensing", 2), (r"motion (deblur|blur)|blur (removal|kernel)", 3),
        (r"shadow removal|rain removal|snow removal|reflection removal", 3),
        (r"face restoration|old photo|photo restoration", 3),
        (r"\bjpeg\b|compression artifact", 2), (r"image (reconstruction|recovery)", 2),
    ]),
    ("Computational_Photography", [
        (r"computational photography", 3), (r"\bhdr\b|high dynamic range", 3),
        (r"white balance|color constancy", 3), (r"demosaick?ing|demosaic", 3),
        (r"\braw (image|sensor|domain)\b", 2), (r"burst (image|processing)", 3),
        (r"reflection separation|flash (image|photography)", 3),
        (r"image signal processing|\bisp\b", 3), (r"bokeh|defocus", 2),
        (r"light field", 3), (r"exposure (correction|bracketing|fusion)", 3),
        (r"color (transfer|enhancement|rendition)", 2), (r"tone mapping", 3),
    ]),
    ("SelfSupervised_Representation", [
        (r"self[- ]supervised", 3), (r"contrastive learning", 3),
        (r"masked (image|autoencoder|modeling)", 3), (r"\bsimclr\b|\bmoco\b|\bbyol\b|\bdino\b", 3),
        (r"representation learning", 2), (r"unsupervised (learning|pretraining|representation)", 2),
        (r"pre[- ]?train(ing)?\b", 2), (r"foundation model", 3), (r"visual (pretraining|pre-training)", 3),
        (r"joint[- ]embedding", 3),
    ]),
    ("Transfer_FewShot_DomainAdaptation", [
        (r"domain adaptation", 3), (r"domain generalization", 3), (r"few[- ]shot", 3),
        (r"zero[- ]shot (learning|recognition|classification)", 3), (r"transfer learning", 2),
        (r"continual learning|incremental learning|lifelong learning", 3),
        (r"long[- ]tailed|long[- ]tail", 2), (r"test[- ]time (adaptation|training)", 3),
        (r"semi[- ]supervised|weakly[- ]supervised", 2), (r"class[- ]incremental", 3),
        (r"anomaly detection", 2), (r"open[- ]set", 2), (r"catastrophic forgetting", 3),
        (r"source[- ]free", 3), (r"novel class|unseen class", 2), (r"out[- ]of[- ]distribution|\bood\b", 2),
    ]),
    ("Autonomous_Driving", [
        (r"autonomous (driving|vehicle)", 3), (r"self[- ]driving", 3),
        (r"\bbev\b|bird'?s[- ]eye[- ]view", 3), (r"lane (detection|segmentation)", 3),
        (r"\blidar\b", 3), (r"hd ?map|high[- ]definition map", 3),
        (r"trajectory prediction|motion forecasting|motion prediction", 3),
        (r"occupancy (network|prediction|grid)", 2), (r"end[- ]to[- ]end (autonomous|driving)", 3),
        (r"\btraffic\b", 2), (r"driving (scene|scenario|video)", 3), (r"\badas\b", 2),
    ]),
    ("Embodied_AI_Robotics", [
        (r"\bembodied\b", 3), (r"\brobot(s|ic|ics)?\b", 3), (r"\bmanipulation\b", 3),
        (r"grasp(ing)?\b", 3), (r"sim[- ]to[- ]real", 3), (r"reinforcement learning", 2),
        (r"vision[- ]language[- ]action|\bvla\b", 3), (r"policy learning|imitation learning", 3),
        (r"visual navigation|vision[- ]and[- ]language navigation|\bvln\b", 3),
        (r"navigation", 2), (r"\bdrone\b|\buav\b", 2), (r"object goal|embodied (ai|agent)", 3),
    ]),
    ("Medical_Bio_RemoteSensing", [
        (r"medical (image|imaging|image analysis|segmentation)", 3),
        (r"\bct\b|\bmri\b|x[- ]ray|ultrasound", 2), (r"patholog|histopatholog", 3),
        (r"clinical", 2), (r"remote sensing", 3), (r"satellite (image|imagery)", 3),
        (r"hyperspectral", 3), (r"\bsar\b|synthetic aperture radar", 3),
        (r"cell (segmentation|detection|tracking)|microscop", 3),
        (r"plant|agricultur|crop|leaf", 2), (r"aerial image", 3),
        (r"brain (image|mri|tumor|decode)", 3), (r"lesion|tumor|organ segmentation", 3),
        (r"change detection", 2), (r"biological imaging|bioimage", 3),
    ]),
    ("Document_OCR_Graphics", [
        (r"\bocr\b", 3), (r"text (detection|recognition|spotting)", 3), (r"scene text", 3),
        (r"document (image|analysis|understanding|layout|parsing)", 3),
        (r"table (detection|recognition|understanding|structure)", 3),
        (r"chart (recognition|understanding|parsing|qa)", 3), (r"handwriting|handwritten", 3),
        (r"math(ematical)? expression|formula recognition", 3), (r"layout analysis", 3),
        (r"\bsvg\b|vector graphics|vectorization", 3), (r"license plate", 2),
        (r"optical character", 3),
    ]),
    ("Efficiency_Compression", [
        (r"quantiz", 3), (r"knowledge distillation", 3), (r"\bpruning\b|\bsparsity\b|sparsif", 2),
        (r"neural architecture search|\bnas\b", 3), (r"model compression|network compression", 3),
        (r"lightweight|light[- ]weight", 2), (r"efficient (inference|model|network|architecture)", 2),
        (r"edge (device|computing|deployment)|mobile device|on[- ]device", 3),
        (r"\blatency\b|\bthroughput\b|\bflops\b|inference speed|speedup", 2),
        (r"token (pruning|merging|reduction|compression)", 3), (r"low[- ]rank|tensor decomposition", 2),
        (r"\bcache\b|caching|early exit", 2), (r"acceleration|accelerate", 1),
    ]),
    ("Trustworthy_Security_Privacy", [
        (r"adversarial (attack|example|robust|defense|training)", 3),
        (r"\brobustness\b", 2), (r"backdoor", 3), (r"watermark", 3),
        (r"deepfake|deep[- ]fake|forgery (detection|localization)|face forgery", 3),
        (r"\bprivacy\b|differential privacy", 3), (r"federated learning", 3),
        (r"fairness|\bbias\b|debiasing", 3), (r"explainab|interpretab|saliency map", 2),
        (r"uncertainty (estimation|quantification)|calibration", 2), (r"\btrustworthy\b", 3),
        (r"jailbreak|\bsafety\b|harmful content", 2), (r"membership inference", 3),
    ]),
    ("LowLevel_Flow_Depth_Matching", [
        (r"optical flow", 3), (r"scene flow", 3), (r"stereo matching|disparity", 3),
        (r"depth estimation|monocular depth|depth completion", 3),
        (r"feature matching|image matching|correspondence", 3),
        (r"homography|camera calibration|pose[- ]free", 3),
        (r"multi[- ]view geometry|epipolar", 3), (r"camera pose|visual localization|visual place", 3),
        (r"structure and motion|\bslam\b|visual odometry", 3), (r"\bnormal (estimation|map)", 2),
    ]),
    ("Audio_Visual", [
        (r"audio[- ]visual|audiovisual", 3), (r"\baudio\b|\bsound\b|\bspeech\b", 2),
        (r"lip[- ]?read|lip sync|talking (face|head) generation", 3),
        (r"sound (source|separation|localization)|audio[- ]visual (segmentation|localization)", 3),
        (r"music|voice|binaural", 2),
    ]),
    ("Recognition_Classification", [
        (r"image classification", 3), (r"fine[- ]grained", 3), (r"object recognition", 3),
        (r"visual recognition|recognition (task|benchmark)", 2), (r"scene (classification|recognition)", 3),
        (r"open[- ]world recognition", 3), (r"long[- ]tailed recognition", 3),
    ]),
]

TOPIC_NAMES = [name for name, _ in TOPICS] + [OTHER]


class TopicClassifier(object):
    """关键词加权分类器。"""

    def __init__(
        self,
        title_weight: float = 3.0,
        abstract_weight: float = 1.0,
        max_hits: int = 3,
        rel_threshold: float = 0.4,
        min_score: float = 6.0,
    ):
        self.title_weight = title_weight
        self.abstract_weight = abstract_weight
        self.max_hits = max_hits
        self.rel_threshold = rel_threshold
        self.min_score = min_score
        self.rules = [
            (name, [(re.compile(pattern, re.I), weight) for pattern, weight in patterns])
            for name, patterns in TOPICS
        ]

    def score(self, title: str, abstract: str) -> Dict[str, float]:
        """返回每个方向的得分（只保留正分）。"""
        scores = {}
        for name, patterns in self.rules:
            total = 0.0
            for regex, weight in patterns:
                hits_title = min(len(regex.findall(title)), self.max_hits)
                hits_abstract = min(len(regex.findall(abstract)), self.max_hits)
                total += weight * (hits_title * self.title_weight + hits_abstract * self.abstract_weight)
            if total > 0:
                scores[name] = total
        return scores

    def classify(self, title: str, abstract: str) -> Tuple[str, List[str], float, float]:
        """返回 (主方向, 多标签列表, 主方向得分, 置信度)。"""
        scores = self.score(title, abstract)
        if not scores:
            return OTHER, [OTHER], 0.0, 0.0

        ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
        primary, top_score = ranked[0]
        second_score = ranked[1][1] if len(ranked) > 1 else 0.0

        labels = [name for name, s in ranked if s >= top_score * self.rel_threshold and s >= self.min_score]
        if primary not in labels:
            labels.insert(0, primary)

        confidence = (top_score - second_score) / top_score if top_score > 0 else 0.0
        return primary, labels, round(top_score, 2), round(confidence, 3)

    def low_confidence(self, confidence: float, threshold: float = 0.2) -> bool:
        """判断是否需要人工或 LLM 复核。"""
        return confidence < threshold


def build_classifier(**kwargs) -> TopicClassifier:
    return TopicClassifier(**kwargs)
