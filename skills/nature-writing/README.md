# nature-writing

> 面向中国 AI / ML 研究者的 Nature 系论文写作 Agent Skill：主投 **Nature Machine Intelligence**，次投 **Nature Communications / Nature Computational Science**，必要时冲刺 **Nature**。

把“能过审的 arXiv 风格”打磨成“Nature 系审稿人读完会说 *well-written, clearly motivated, compelling, careful, and hard to put down* 的论文”。本 skill 是从 **44 篇开放获取论文**逐句抽取出来的 craft + taste + story-craft 手册，覆盖 abstract / intro / results / methods / discussion / figure 全链路。

## 是什么

| 部分 | 文件 | 内容 |
|---|---|---|
| 写作 skill | `SKILL.md` | 骨架公式、写作顺序、按任务加载的 routing table、提交前 checklist、屏幕边 quick card、44 篇语料附录 |
| 写作细节 | `references/01-story.md` … `15-taste-development.md` | 15 个主题文件，按需 Read |
| 配图 skill | `FIGURE-SKILL.md` | Fig. 1 schematic 构图、Wong/Okabe-Ito 8 色、字体字号、matplotlib/ggplot 模板、Illustrator 拼版流程 |
| 配图细节 | `figure-references/01..12-*.md` | 12 个主题文件，按需 Read |
| 语料 | `extracts/01-singlecell.md` … `07-ai-methods.md` | 7 类领域 / 44 篇 OA 论文的 verbatim 抽取，所有引文可 grep 回原文 |
| 抽取方法 | `_framework.md` | 重建 / 扩充时参考 |

### 为什么“瘦索引 + 按需加载”

写作不是线性的。`SKILL.md` 只保留全局看得见的部分（骨架、顺序、checklist、quick card），其余数千行细节拆到 `references/`，按 routing 表只 Read 1–2 个文件，避免把整本手册塞进 context window。

| 你正在做什么 | Read |
|---|---|
| 写 abstract | `references/03-abstract.md` |
| 写 Results 子节 | `references/05-results.md` + `FIGURE-SKILL.md` |
| 自审稿 | `references/09-reviewer-protocol.md` + `references/13-antipatterns.md` |
| 选投哪个刊 | `references/14-journals.md` |
| 卡在一句话上 | `references/08-sentence-taste.md` |
| 长期 taste 培养 | `references/15-taste-development.md` |

完整 routing 表见 [`SKILL.md`](./SKILL.md) §1。

## 安装

仓库根目录包含 `skills/nature-writing/`，安装的是这个子目录。下面的命令使用 `scarletcx` 账号；如果你 fork 了项目，请替换成自己的账号。

### 大多数 agent 共用一处

```bash
git clone https://github.com/scarletcx/nature-writing.git
cd nature-writing
mkdir -p ~/.agents/skills
ln -s "$(pwd)/skills/nature-writing" ~/.agents/skills/nature-writing
```

`~/.agents/skills/` 会被 Command Code、Codex、Gemini CLI、Cursor、GitHub Copilot 读取。

### Claude Code

Claude Code 不读 `~/.agents/skills/`，需要再链接一次：

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/nature-writing" ~/.claude/skills/nature-writing
```

### Codex

Codex 支持从 `~/.agents/skills/` 发现 Agent Skills，上面的通用安装已经覆盖它。若使用较旧版本或只想在单个项目中启用，可以在项目的 `AGENTS.md` 里加指针：

```markdown
## Nature-family writing

When drafting or revising papers for NMI / NC / NCS / Nature, first read
`~/.agents/skills/nature-writing/SKILL.md`, then load only the relevant
`references/*.md` per the routing table in §1.1.
```

### 项目内安装

希望团队共享时，把技能目录提交到仓库：

```bash
mkdir -p .agents/skills
cp -R /path/to/nature-writing/skills/nature-writing .agents/skills/nature-writing
```

Claude Code 项目内安装：

```bash
mkdir -p .claude/skills
cp -R /path/to/nature-writing/skills/nature-writing .claude/skills/nature-writing
```

### GitHub Copilot CLI

```bash
gh skill install scarletcx/nature-writing nature-writing
gh skill preview scarletcx/nature-writing nature-writing
```

### 其他 agent / chatbot

`SKILL.md` 和所有 references 都是纯 Markdown，没有专属语法。任何能读文件的 LLM 工具都可以把它们作为 system prompt 或附件使用；只需按 routing 表加载相关文件，不要一次性塞入全部语料。

## 用法示例

**写 abstract**

```text
我有一段 ML 方法论文的 abstract，请用 nature-writing skill 检查 pivot、
KEY-RESULT 是否有 named baseline、outlook 动词是否与证据强度匹配。

[paste abstract]
```

**自审稿（5-pass harsh referee）**

```text
用 references/09-reviewer-protocol.md 的 SNEER / NOD / ASK / CUT 协议
审一遍我的 Results 章节，每段给 invisible answer。
```

**提交前总扫**

```text
跑一遍 SKILL.md §2 的 checklist，每条标 ✅ / ⚠️ / ❌，
⚠️ 和 ❌ 给具体修改建议。
```

**子门类剧本**

```text
这是一篇 LLM-agent 论文，按 references/12-subgenres.md 的剧本检查：
prompt 报告完整性、tool schema 在不在 SI、外部 API 版本和 date 有没有写。
```

**配图**

```text
用 FIGURE-SKILL.md 和 figure-references/ 检查这张 Fig. 1：
构图是否服务主 story、panel letter 和字号是否合规、配色是否过饱和。
```

## 目录结构

仓库根目录：

```text
nature-writing/
├── README.md                 # 仓库入口与安装说明
├── LICENSE                   # MIT（代码 / Markdown 结构 / 抽取框架）
├── NOTICE.md                 # verbatim 引文的版权与 OA license 说明
├── skills/nature-writing/    # 安装这个目录
│   ├── SKILL.md              # 写作 skill 瘦索引（必读）
│   ├── FIGURE-SKILL.md       # 配图 skill 瘦索引
│   ├── _framework.md         # 抽取方法论
│   ├── README.md             # 本文件
│   ├── references/           # 15 个写作细节文件
│   ├── figure-references/    # 12 个配图细节文件
│   └── extracts/             # 7 个语料文件 / 44 篇 OA 论文 verbatim
├── scripts/validate_package.py
└── tests/
```

`references/` 的 15 个文件：

```text
01-story.md              7 种 canonical story shapes、Fig. 1 四种功能
02-title.md              Title 6 种定式
03-abstract.md           5–8 句句式图、Two-gap、carve-out
04-intro.md              漏斗 4–6 段、6 种 hook、GAP 词库
05-results.md            标题三风格、figure call-out、统计写法、ablation
06-methods.md            复现性三处呼应、LLM-agent 专用清单
07-discussion.md         Outlook 动词等级、Limitation as boundary
08-sentence-taste.md     rhythm、经济、restraint、negative space
09-reviewer-protocol.md  5-pass harsh referee protocol
10-voice.md              DeepMind / NMI / NC / NCS / 临床 5 种 voice
11-language-bank.md      强动词 / hedge / 段间连接
12-subgenres.md          7 个子门类剧本
13-antipatterns.md       craft + AI-specific + taste 反模式
14-journals.md           各刊 voice 与策略
15-taste-development.md  读法 / 临摹 / taste notebook
```

## 语料来源（44 篇 OA 论文）

| # | 领域 | 论文 | 刊物 |
|---|---|---|---|
| 1–6 | 单细胞基因组 | Geneformer · SCimilarity · Tangram · scIB · CellOracle · CellFM | Nature × 3 / Nat Methods × 2 / NC |
| 7–12 | 蛋白 / 结构 AI | AlphaFold2 · ESM-2 · ProteinMPNN · RFdiffusion · AlphaMissense · Foldseek | Nature × 2 / Science × 3 / Nat Biotechnol |
| 13–18 | 物理 / 气候 / 材料 | GraphCast · GenCast · DIMON · M3GNet · HINTS · GNoME | Science / Nature × 2 / NCS × 2 / NMI |
| 19–24 | 药物发现 | DynamicBind · Wong-MRSA · Halicin · SyntheMol · RetroExplainer · DRAGONFLY | NC × 4 / Nature / Cell |
| 25–30 | 临床 AI | MedSAM · UNI · CONCH · Virchow · MedPerf · Ferber-GPT4V | Nat Med × 3 / NC × 2 / NMI |
| 31–36 | ML 通用 / 基础模型 | ChemCrow · AlphaGeometry · MolE · SemanticLens · Cancer-Imaging-FM · FunSearch | NMI × 4 / Nature × 2 / NC |
| 37–44 | 纯 AI 方法（v5 新增） | DeepSeek-R1 · Densing-law · AligNet · ADeLe · Webb-MAP · DiscoRL · Farquhar-semantic-entropy · Whitelam-Simmering | Nature × 5 / NMI / NC × 2 |

所有引文均来自开放获取论文（CC-BY 等 license），用于学术评论 / 写作教学。原作者保留版权；转载或商业使用前请核对每篇论文的具体 OA license，详见 [`NOTICE.md`](./NOTICE.md)。

## 如何扩展

新增第 8 类领域 / 第 45 篇论文：

1. 用 [`_framework.md`](./_framework.md) 的抽取格式，在 `extracts/` 下加新文件。
2. 把新句式 / 新模板回灌到对应 `references/*.md`（不是 `SKILL.md`，后者保持瘦索引）。
3. 更新 `SKILL.md` 附录 A 的 corpus 表、`references/README.md` 的目录和本 README 的统计。

## 许可与出处

- **代码 / Markdown 结构 / 抽取框架**：MIT，见 [`LICENSE`](./LICENSE)。
- **verbatim 引文**：原作者保留版权，使用时遵守对应 OA license；见 [`NOTICE.md`](./NOTICE.md)。
- **上游项目**：本仓库是对 `SyntaxSmith/nature-writing-skill` 的本地 v5 版本进行跨 agent 打包；写作协议与语料归原项目及论文作者所有。

## Patron sentence

> "Many problems in mathematical sciences are *easy to evaluate*, despite being typically *hard to solve*."  
> — FunSearch (Romera-Paredes et al., *Nature* 2024)

写论文这件事正相反：易写难精。这个 skill 的目标，是让写得“对”和写得“好”之间的 gap 缩短一些。
