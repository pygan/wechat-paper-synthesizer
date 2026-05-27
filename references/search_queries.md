# 论文解读搜索关键词构造指南

> **版本**: v1.1  
> **用途**: 为分层搜索架构（Layer 1 + Layer 2）构造最优关键词组合。支持中英混合、通道差异化、模块化策略扩展。

---

## 设计原则

1. **中英混合优先**：中文科技写作者常用中英混杂（"DNA binder" 而非 "DNA结合蛋白"），关键词必须覆盖两种风格
2. **分层递进**：Layer 1 快速覆盖 → 不足时 Layer 2 深度补漏
3. **模块化扩展**：Layer 2 策略以独立模块定义，新增策略不改搜索框架
4. **通道差异**：微信公众号标题依赖人物IP和成果数字，WebSearch 对概念泛化更友好

---

## Layer 1: 标准搜索策略

四策略 + 中英混合增强。每组策略生成「中英混合版」和「纯中文版」两组独立搜索词。

### 策略一：原文信息驱动（必选，2-3组）

包含论文精确信息，用于找到直接解读文章。

**中英混合版模板**：
```
"{期刊英文}" "{标题关键词1} {标题关键词2}" {年份} {中文领域} 解读
```

**纯中文版模板**：
```
{期刊中文译名} {标题词中文翻译} {年份} {中文领域} 解读 综述
```

**示例**：
| 中英混合版 | 纯中文版 |
|-----------|---------|
| `"Nature" "DNA binder" 2026 蛋白设计 解读` | `《自然》 DNA结合蛋白 从头设计 2026 解读` |
| `"Nature Medicine" "Rentosertib" 2025 IPF 临床` | `《自然医学》 Rentosertib 特发性肺纤维化 临床2期` |

### 策略二：作者/团队驱动（必选，1-2组）

用作者名 + 关键词定位关注该领域的公众号。

**中英混合版模板**：
```
"{通讯作者}" "{标题英文关键词}" "{期刊英文}" {中文领域}
```

**纯中文版模板**：
```
{通讯作者名} {中文核心概念} {中文期刊译名} {领域}
```

**示例**：
| 中英混合版 | 纯中文版 |
|-----------|---------|
| `"David Baker" "DNA binder" "de novo" 蛋白质设计` | `David Baker DNA结合 从头设计 蛋白质 生物` |
| `"任峰" "Rentosertib" TNIK IPF 临床` | `任峰 英矽智能 Rentosertib 特发性肺纤维化` |

### 策略三：中文概念泛化（必选，1组）

纯中文同义表达，覆盖没有引用英文标题的解读文章。

**中英混合版模板**：
```
{核心概念英文保留} {中文关键词} {领域词}
```

**纯中文版模板**：
```
{中文核心概念全称} {中文关键词} {领域词} {作者姓氏}
```

**示例**：
| 中英混合版 | 纯中文版 |
|-----------|---------|
| `DNA binder 从头设计 蛋白质 人工智能 特异性` | `DNA结合蛋白 从头设计 人工智能 特异性识别 Baker` |
| `AI drug discovery IPF 靶点发现 临床验证` | `AI药物研发 特发性肺纤维化 靶点发现 临床2期` |

### 策略四：长尾试探（可选，0-1组）

针对特定角度的深度搜索。

**中英混合版模板**：
```
{特定角度词} {英文核心词}
```

**纯中文版模板**：
```
{特定角度中文词} {核心关键词} {方法/工具名}
```

**示例**：
| 中英混合版 | 纯中文版 |
|-----------|---------|
| `"可编程基因调控" "de novo" protein binder` | `可编程基因调控 蛋白设计 基因编辑 RFdiffusion` |
| `"AI制药 里程碑" 靶点发现 临床验证` | `AI制药 里程碑 靶点发现 临床验证 英矽智能` |

---

## 中英混合关键词生成规则

### 保留英文的术语类型

以下类型在「中英混合版」中**保留英文原词**：

| 类型 | 保留英文 | 不翻译为 |
|------|---------|---------|
| 专业方法名 | binder, diffusion, screening, design | 结合剂, 扩散, 筛选, 设计 |
| 工具/模型名 | RFdiffusion, AlphaFold, LigandMPNN | — |
| 期刊名（优先） | "Nature", "Science", "Cell" | 《自然》《科学》《细胞》 |
| 生物学术语 | DNA, RNA, siRNA, in vivo, in silico | — |
| 成果描述词 | first-in-class, de novo, proof-of-concept | 首创, 从头, 概念验证 |

### 翻译为中文的术语类型

以下类型在「纯中文版」中**翻译为中文**：

| 类型 | 英文 | 中文 |
|------|------|------|
| 通用概念 | protein design, gene regulation | 蛋白质设计, 基因调控 |
| 疾病名 | idiopathic pulmonary fibrosis | 特发性肺纤维化 |
| 技术方向 | deep learning, generative AI | 深度学习, 生成式AI |

### 双版本生成规则

- 每个策略**必须同时生成**中英混合版和纯中文版
- 两组版本在搜索时作为**两个独立查询**发出，不合并为一个
- 如果某个策略的英文词本身就是中文通用的（如 "AI"），可不区分版本

---

## Layer 2: 模块化升级策略

仅当 Layer 1 未达阈值（< 3 篇不同信源可提取完整正文）时激活。

### 模块设计规范

每个 Layer 2 策略模块包含以下字段：

```yaml
module_id: "L2_XXX"           # 唯一标识
name: "策略中文名"              # 人类可读名称
trigger:                       # 触发条件
  condition: "描述"
  required_fields: ["字段1"]   # 需要从论文元数据中提取的字段
channel_preference: "A" | "B" | "A=B"  # 通道偏好
query_templates:               # 关键词模板
  channel_A: ["模板1", "模板2"]
  channel_B: ["模板1", "模板2"]
notes: "补充说明"
```

新增策略只需在下方「策略模块清单」中添加一个条目，**无需修改 SKILL.md 或其他文件**。

---

### 策略模块清单

#### L2_BIG_NAME: 大牛锚点

```yaml
module_id: "L2_BIG_NAME"
name: "大牛锚点"
trigger:
  condition: "通讯作者为领域知名人物（Nature/Science/Cell 常客、H-index > 50、获重大奖项）"
  required_fields: ["通讯作者", "中文领域词", "英文领域词"]
channel_preference: "B"  # 公众号标题天然倾向人物IP
query_templates:
  channel_A:
    - '"{大牛名}" {中文领域词} 最新 论文'
    - '"{大牛名}" {英文领域词} 2026'
  channel_B:
    - '"{大牛名}" {英文领域词}'                # 最简洁锚点
    - '"{大牛名}" {英文核心方法名} {英文领域词}'  # 人物+工具组合
    - '"{大牛名}实验室" {中文领域词} 突破'
notes: |
  核心思路：公众号解读文章几乎必然在标题中挂靠大牛名字（如"David Baker｜..."）。
  不绑定期刊/年份，扩大覆盖面——同一大牛的最新工作可能被同一篇解读连带提及。
  大牛判定参考：近5年在CNS发表 ≥3 篇通讯作者论文，或获诺奖/拉斯克/科学突破奖。
```

**示例**：
| 通道 | 搜索词 |
|------|--------|
| A | `"David Baker" 蛋白质设计 最新 论文` |
| A | `"David Baker" "de novo protein design" 2026` |
| B | `"David Baker" "DNA binder"` |
| B | `"David Baker" RFdiffusion3 "DNA binder"` |

#### L2_HIGHLIGHT: 亮点猜测

```yaml
module_id: "L2_HIGHLIGHT"
name: "亮点猜测"
trigger:
  condition: "论文摘要含显著数字声明（n-fold/X倍、first/largest/record-breaking）或突破性声明（'first demonstration'、'unprecedented'）"
  required_fields: ["关键数字/声明", "中文核心概念", "英文核心概念"]
channel_preference: "A"  # 泛化搜索，WebSearch 覆盖面更广
query_templates:
  channel_A:
    - '{中文核心概念} {数字声明} {领域词} {年份}'        # 如"蛋白质设计 100倍 特异性 2026"
    - '{中文核心概念} "{突破声明}" {领域词}'              # 如"蛋白质设计 首次实现 从头设计"
    - '{数字声明}倍 {英文核心概念} 突破 解读'             # 如"100倍 protein design 突破 解读"
  channel_B:
    - '{数字声明}倍 {英文核心概念}'                       # 如"100倍 DNA binder"
    - '"{突破声明中文}" {英文核心概念}'                   # 如"首次实现 de novo protein design"
notes: |
  核心思路：解读文章标题常包装成果亮点（如"实现100倍跃迁"），而非照搬论文标题。
  从论文摘要中提取的数字和声明，反向猜测中文解读文章会用的"包装语"。
  数字声明提取示例：100-fold → "100倍"；first demonstration → "首次实现"；record-breaking → "破纪录"。
```

**示例**：
| 通道 | 搜索词 |
|------|--------|
| A | `蛋白质从头设计 100倍 特异性 DNA 2026` |
| A | `蛋白质设计 "首次实现" DNA binder 从头设计` |
| B | `100倍 DNA binder 特异性` |
| B | `"首次实现" de novo DNA binder` |

#### L2_TOOL_CHAIN: 工具方法链

```yaml
module_id: "L2_TOOL_CHAIN"
name: "工具方法链"
trigger:
  condition: "论文涉及 ≥2 个知名计算工具/方法（如 RFdiffusion、AlphaFold、Rosetta、LigandMPNN 等）"
  required_fields: ["工具名列表", "应用领域"]
channel_preference: "B"  # 公众号深度解读常以工具/方法名为卖点
query_templates:
  channel_A:
    - '{工具1} {工具2} {中文领域}'                       # 如"RFdiffusion AlphaFold 蛋白质设计"
    - '"{工具1}" {应用领域} 论文 解读'                    # 如"RFdiffusion3 DNA 论文 解读"
  channel_B:
    - '"{工具1}" "{工具2}" {英文领域词}'                  # 如"RFdiffusion3" "AlphaFold3" DNA
    - '{工具1} {应用领域} 设计'                           # 如"RFdiffusion DNA binder 设计"
notes: |
  核心思路：公众号深度技术解读常用工具/方法链作为卖点（如蓝极BlueArctic文章标题中的RFdiffusion3+AlphaFold3）。
  工具知名度判定：GitHub stars > 1000 或 CNS 正刊中引用 ≥5 次的工具。
```

**示例**：
| 通道 | 搜索词 |
|------|--------|
| A | `RFdiffusion AlphaFold 蛋白质设计 2026` |
| A | `"RFdiffusion3" DNA 结合 论文 解读` |
| B | `"RFdiffusion3" "AlphaFold3" DNA binder` |
| B | `RFdiffusion DNA binder 从头设计` |

---

### 如何新增策略模块

1. 在「策略模块清单」中添加新条目，按 `module_id` 字母序排列
2. 填写完整的模块定义（触发条件、通道偏好、关键词模板）
3. 在 SKILL.md 的 §1.3.2 策略模块一览表中添加对应行
4. **不需要修改** Phase 1 搜索框架逻辑

新增模块必须满足：
- `module_id` 格式为 `L2_{大写蛇形命名}`
- `query_templates` 中 channel_A 和 channel_B 各至少提供 1 个模板
- `trigger.condition` 描述清晰、可自动判定（不依赖人工判断）

---

## 通道差异化策略

### 关键词风格对比

| 维度 | 通道 A: WebSearch | 通道 B: 微信搜索 |
|------|-----------------|-----------------|
| **Layer 1 侧重** | 均衡（所有策略全发） | 优先策略一二（作者驱动 + 原文精确匹配） |
| **Layer 2 侧重** | L2_HIGHLIGHT（概念泛化 + 成果包装） | L2_BIG_NAME + L2_TOOL_CHAIN（人物/工具锚） |
| **关键词特征** | 偏中文长尾 + 概念泛化 | 人物IP锚 + 英文工具名 + 成果数字 |
| **搜索词风格** | `蛋白质从头设计 100倍 特异性 DNA 2026` | `"David Baker" RFdiffusion3 DNA binder 100倍` |

### 差异化原因

微信公众号标题格式天然倾向 **「人物 IP | 工具/方法 | 成果亮点」** 三段式：
- 蓝极BlueArctic: `David Baker｜DNA binder 设计实现 100 倍跃迁，关键不是"结合"而是"区分"`
- 生物世界: `Nature | David Baker团队用AI设计全新DNA结合蛋白`
- DrugAI: `RFdiffusion3 + AlphaFold3 | 从头设计DNA结合蛋白`

而 WebSearch 覆盖的泛科技媒体（搜狐、腾讯云、CSDN）标题更多样，对中文概念泛化和长尾词更友好。

---

## 噪音控制

### 热门词噪音率预估

| 论文特征 | 噪音率 | Layer 策略 |
|----------|--------|-----------|
| 冷门药靶点/小众方向 | 低（<30%） | Layer 1 基础策略即可 |
| 知名科学家人名 | 中（30-60%） | L1 加期刊+年份过滤 |
| "AI"+"蛋白质/药物"等热门交叉词 | 高（60-85%） | L1 必须用精确英文标题过滤；L2 用工具链降噪 |
| 顶刊综述（Nature/Science/Cell Review） | 极高（>80%） | L1 标题必须精确；L2 慎用亮点猜测（泛化噪音大） |

### 噪音过滤链路

1. 多源搜索（双通道 + Layer 1/2）→ 获取标题列表
2. 标题正则过滤：必须同时包含论文核心要素（作者名 OR 英文关键词 OR 工具名）
3. 跨通道去重
4. 如果噪音率 > 70%，在报告中标注并建议用户手动确认候选文章

---

## 关键词模板速查

```python
# Layer 1 搜索词生成（伪代码）
L1_QUERIES = {
    "s1_exact": {
        "mixed": '"{journal_en}" "{title_kw1} {title_kw2}" {year} {field_cn} 解读',
        "cn":     '{journal_cn} {title_kw_cn} {year} {field_cn} 解读 综述',
    },
    "s2_author": {
        "mixed": '"{author}" "{title_kw_en}" "{journal_en}" {field_cn}',
        "cn":     '{author} {concept_cn} {journal_cn} {field_cn}',
    },
    "s3_concept": {
        "mixed": '{concept_en} {keywords_cn} {field_cn}',
        "cn":     '{concept_cn_full} {keywords_cn} {field_cn} {author_surname}',
    },
    "s4_longtail": {
        "mixed": '{angle_en_cn} {core_kw_en}',
        "cn":     '{angle_cn} {core_kw_cn} {tool_name}',
    },
}

# Layer 2 搜索词生成（伪代码，按模块激活）
L2_MODULES = {
    "L2_BIG_NAME": {
        "prefer": "B",
        "A": ['"{big_name}" {field_cn} 最新 论文',
              '"{big_name}" {field_en} {year}'],
        "B": ['"{big_name}" {field_en}',
              '"{big_name}" {tool_en} {field_en}',
              '"{big_name}实验室" {field_cn} 突破'],
    },
    "L2_HIGHLIGHT": {
        "prefer": "A",
        "A": ['{concept_cn} {number_cn} {field_cn} {year}',
              '{concept_cn} "{claim_cn}" {field_cn}',
              '{number_cn}倍 {concept_en} 突破 解读'],
        "B": ['{number_cn}倍 {concept_en}',
              '"{claim_cn}" {concept_en}'],
    },
    "L2_TOOL_CHAIN": {
        "prefer": "B",
        "A": ['{tool1} {tool2} {field_cn}',
              '"{tool1}" {application_cn} 论文 解读'],
        "B": ['"{tool1}" "{tool2}" {field_en}',
              '{tool1} {application_en} 设计'],
    },
}
```
