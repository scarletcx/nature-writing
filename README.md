# nature-writing

> 面向中国 AI / ML 研究者的 Nature 系论文写作 Agent Skill：NMI / NC / NCS / Nature。
> 基于 **44 篇开放获取论文**的逐句抽取，覆盖 abstract、intro、results、methods、discussion 和 figure 全链路。

这是一个 [Agent Skill](https://agentskills.io/specification)，不是论文生成器。它把 Nature 系论文的 craft、taste 和 story-craft 拆成可按任务加载的写作手册；Agent 只在需要时读取相关章节，不会一次把整本手册塞进上下文。

## 它解决什么问题

arXiv 风格通常回答“我们做了什么”。Nature 系审稿人还会问：

- 这篇论文的 story 是什么？antagonist 是谁？
- Fig. 1 是否建立了阅读地图？
- Abstract 的 pivot、KEY-RESULT、outlook 是否与证据强度匹配？
- Results 的顺序是阅读顺序，还是实验时间顺序？
- Limitation 是否具体？Outlook 是否 overclaim？
- 图为什么一眼像 arXiv，而不像 Nature？

这个 skill 把 44 篇 OA 论文里的真实句式、结构、figure caption 和审稿人视角整理成可执行的 checklist、routing table 和 before/after 对照。

## 适合谁

- 主投 **Nature Machine Intelligence** 的 AI / ML 研究者；
- 次投 **Nature Communications**、**Nature Computational Science**；
- 少数冲刺 **Nature** 旗舰的工作；
- 需要把中文研究叙事打磨成 Nature 系英文表达的作者；
- 想系统训练论文 taste，而不只是套模板的人。

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

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/nature-writing" ~/.claude/skills/nature-writing
```

### 项目内安装

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

## 使用

调用技能：

- Command Code、Claude Code、Gemini CLI、Cursor：`/nature-writing`
- Codex：`$nature-writing` 或技能选择器
- GitHub Copilot：选择技能，或直接描述任务

示例：

```text
用 nature-writing 检查这段 abstract 的 pivot、KEY-RESULT 和 outlook 动词。
[paste abstract]
```

```text
按 references/09-reviewer-protocol.md 的 SNEER / NOD / ASK / CUT 协议
审一遍我的 Results，每段给 invisible answer。
```

```text
跑一遍 SKILL.md §2 的提交前 checklist，每条标 ✅ / ⚠️ / ❌，
⚠️ 和 ❌ 给具体修改建议。
```

```text
用 FIGURE-SKILL.md 检查这张 Fig. 1：构图、panel letter、字号、配色和 caption。
```

## 内容结构

```text
nature-writing/
├── README.md
├── LICENSE
├── NOTICE.md
├── skills/nature-writing/
│   ├── SKILL.md                 # 写作瘦索引：骨架、routing、checklist、quick card
│   ├── FIGURE-SKILL.md          # 配图瘦索引
│   ├── _framework.md            # 论文抽取方法论
│   ├── README.md                # 完整使用说明
│   ├── references/              # 15 个写作细节文件
│   ├── figure-references/       # 12 个配图细节文件
│   └── extracts/                # 7 个语料文件 / 44 篇 OA 论文 verbatim
├── scripts/validate_package.py
└── tests/
```

完整目录和每篇论文的语料表见
[`skills/nature-writing/README.md`](skills/nature-writing/README.md)。

### 为什么“瘦索引 + 按需加载”

`SKILL.md` 只保留每次写作都要看的内容：骨架公式、写作顺序、routing table、提交前 checklist、quick card。具体章节拆到 `references/`，比如写 abstract 只读 `references/03-abstract.md`，写 Results 读 `references/05-results.md` + `FIGURE-SKILL.md`。这样既能保留 4000+ 行细节，又不会每轮都占满上下文。

## 语料与版本

- 语料总数：**44 篇 OA 论文**。
- v4 的 36 篇覆盖单细胞、蛋白/结构、物理/气候/材料、药物发现、临床 AI、ML 通用/基础模型。
- v5 新增 8 篇 2024–2026 NMI/NC/Nature 纯 AI 方法论文：DeepSeek-R1、Densing law、AligNet、ADeLe、Webb-MAP、DiscoRL、Farquhar semantic-entropy、Whitelam Simmering。
- 部分早期写作/配图分析仍以 v4 的 36 篇为样本；v5 的新增内容主要集中在 `SKILL.md`、`references/03-abstract.md`、`references/07-discussion.md`、`references/12-subgenres.md` 和 `extracts/07-ai-methods.md`。

## 许可与出处

- **代码 / Markdown 结构 / 抽取框架**：MIT，见 [LICENSE](LICENSE)。
- **verbatim 引文**：原作者保留版权，使用时遵守对应开放获取论文的 license；见 [NOTICE.md](NOTICE.md)。
- **上游项目**：本仓库是对 `SyntaxSmith/nature-writing-skill` 的本地 v5 版本进行跨 agent 打包；写作协议与语料归原项目及论文作者所有。

如果你要商业使用或大量转载 `extracts/` 中的引文，请先逐篇核对原始论文的 OA license。

## 开发与校验

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_package.py
python3 scripts/validate_package.py --json
```

校验器会检查必需文件、frontmatter、v5 标题、44 篇语料索引、无效的旧目录引用和本地 Markdown 链接。

## Credits

- 写作协议与语料：`SyntaxSmith/nature-writing-skill` 及其引用的 44 篇论文作者。
- 跨 agent 打包、安装说明、校验器和仓库结构：本仓库维护者。
