# 太乙（wechat-paper-synthesizer）—— 论文多源解读搜索与六维度信息合成系统

[![version](https://img.shields.io/badge/version-1.2.0-blue)]()

> 太乙真人为哪吒重塑肉身，太乙为文献再铸主体。

一个 WorkBuddy Skill，帮助无法获取论文原文的同学，通过检索全网多来源解读文章，**多维度还原论文原文**，同时萃取专家观点，构建个人文献知识库。触发方式：「太乙」或「wechat-paper-synthesizer」均可。

## 核心能力

| 能力            | 说明                                               |
| ------------- | ------------------------------------------------ |
| **多源搜索管道**    | 搜狗微信搜索 → WebSearch 反查 → WebFetch 提取，三级管道获取完整解读正文 |
| **六维度分析框架**   | 文献的（研究目标、研究方法、实验验证、未来方向）+ 解读的（批判分析、实用建议）         |
| **信源画像系统**    | 持续记录信源风格、偏向、盲区，每次使用都在进化                          |
| **交叉验证**      | 多信源交叉验证还原论文原文，数字冲突标注差异                           |
| **OA PDF 下载** | 开放获取论文自动下载 PDF 到本地                               |

## 安装

```bash
# 克隆到 WorkBuddy skills 目录
git clone https://github.com/pygan/wechat-paper-synthesizer.git ~/.workbuddy/skills/wechat-paper-synthesizer

# 在 WorkBuddy 中重新加载 skills
/reload skills
```

## 依赖

本 Skill 需要以下 MCP 服务：

- **weixin-search-mcp**（v0.2.1+）：搜狗微信搜索接口
- **WebSearch**：通用搜索引擎反查真实 URL
- **WebFetch**：提取文章正文

> 确保以上 MCP 服务已在 WorkBuddy 中配置并启用。

## 使用方式

提供论文信息即可触发：

```
分析这篇论文：Ghareeb et al., Nature 2026, "Robin: A multi-agent system for automated scientific discovery"
```

或提供 DOI：

```
分析 https://doi.org/10.1038/s41586-026-10652-y
```

或直接上传论文截图，Skill 会自动识别元数据。

## 文件结构

```
wechat-paper-synthesizer/
├── SKILL.md                     # Skill 主文件（name + description + 完整工作流）
├── README.md                    # 本文件
├── assets/
│   └── report_template.md       # 六维度报告 Markdown 模板
├── references/
│   ├── six_dimensions.md        # 六维度分析框架详细指南
│   ├── search_queries.md        # 搜索关键词构造策略
│   └── source_profiles.md       # 信源画像模板（使用者自行添加画像）
└── scripts/
    └── search_paper.py          # 多源搜索 Python 脚本
```

## 方法论

### 六大维度严格二分

| 类别      | 维度                  | 内容来源              |
| ------- | ------------------- | ----------------- |
| **文献的** | 研究目标、研究方法、实验验证、未来方向 | 论文原文（经由多信源交叉验证还原） |
| **解读的** | 批判分析、实用建议           | 解读文章对论文的点评与建议     |

### 工作流程

```
用户输入 → [Phase 0] 加载信源画像
        → [Phase 1] 多源搜索（全源搜索不设限）
        → [Phase 2] 标题去重筛选
        → [Phase 3] WebSearch 反查 + WebFetch 提取
        → [Phase 4] （可选）下载 OA 论文 PDF
        → [Phase 4.5] 摘要核验
        → [Phase 5] 六维度合成报告（基于信源风格使用，仅提取不生成）
        → [Phase 6] 更新信源画像库（区分至作者/账号层面）
        → 交付报告 + PDF
```

## 信源画像系统

`references/source_profiles.md` 是信源画像模板——包含方法论、四维评价体系（技术深度/批判性/乐观程度/中国视角）、画像条目格式和维护规则。使用者在使用过程中自行添加信源画像条目。

信源画像以**作者/账号**为单位（社区平台如 CSDN 以具体博主为单位），记录每个信源的：

- 风格特征与报道偏好
- 技术深度 / 批判性 / 乐观程度评分
- 已知盲区
- 使用历史与进化记录

**画像仅作用于 Phase 5 合成阶段**（信任权重分配），不限制 Phase 1 搜索范围。每次报告完成后自动更新。

## 局限性

1. 搜索和合成以中文内容为主，英文解读（Medium/Twitter/Substack）暂未覆盖
2. 综述类/热门话题噪音率可达 80%+
3. 科技信源生态存在系统性正面叙事偏向
4. 新领域论文面临画像库冷启动问题（积累 3-5 次后趋于实用）

详见 `SKILL.md` 完整局限性声明。

## 版本

v1.2.0 (2026-05-30) — 四项关键修订：Phase 4.5 摘要核验、仅提取信源观点（不生成）、信源画像至作者/账号层面、系统性偏向透明化（非补偿）。工具名改为「太乙」，信源画像模板化（画像数据由使用者自行积累）。

## 许可

MIT
