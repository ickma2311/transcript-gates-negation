verdict: partial
reviewer: gpt-6-sol (reasoning effort high, 常规档) · codex session 01a0d470-560c-7310-b263-495d37b01c56 · 2026-09-24
integrity_status: unavailable（未跑 /experiment-audit）→ 本判定标为 provisional
evidence pre-check: 24/24 cited values verified（存在性；`.aris/evidence_precheck.json`）
reviewer re-ran analyze.py and both scorers on all 5,964 saved outputs: every stored label matched; per-card WER equal across one-word conditions on all 42 cards.

# 各主张的判定与采用的措辞

| # | 原主张 | 判定 | 采用的措辞（照抄评审） | 置信度 |
|---|---|---|---|---|
| K1 | 同 WER 不同伤害 | **yes**（限本卡片） | 在 42 条构造指令上、逐条 WER 相同时，删除否定词在两个 Qwen 模型上产生的错误提议调用远多于删除功能词 | high |
| K2 | 确认闸门对通顺单词错误失明 | partial | 在这两个 Qwen 模型上，所测的确认提示对构造的单词错误（含否定删除）很少请求澄清；预注册的旁人-否定确认率差不存在 | 量 high / 释 medium |
| K3 | 闸门只对多词不连贯反应 | partial | 所测确认提示在较长旁人片段上更常发问；这些片段的 WER 也高得多（长度、WER、位置、内容一起变，不能归因于"不连贯"） | 量 high / 释 medium |
| K4 | oracle 说话人标签 | partial | oracle 说话人标签未达到预注册的 30pp 错误动作降幅：3B 2.4pp、7B 11.9pp（**不能说 3B "忽略"标签**：其输出有变化，NO_CALL 6/42→4/42） | high |
| K5 | 动作形态规则分不开"真要"与"否定丢失" | partial | 在这些成对卡片上，提示版可选布尔规则几乎从不挡住否定删除；确定性版挡住 97.6% 但把 97.6–100% 的合法正向请求也变成确认；否定删除卡上忠于转写的调用与其正向镜像卡的 gold 调用完全相同，所以只看调用的规则分不开二者【2026-09-24 更正：评审原话写的是"成对的 gold 调用完全相同"，实际上这一对的 gold 相反，相同的是提议的调用】。**51.2% 是人为 1:1 配比下的数字，不是部署代价** | high |
| K6 | 打分器 | partial | 报告预注册的严格打分与事后宽松打分：严格版因自由文本表示把许多 clean 调用判错，宽松版无法可靠测量实体替换的伤害 | high |
| 总 | "同 WER、闸门失明、否定无指纹" | **partial** | 在一个用 42 条构造指令和两个 Qwen 模型的探索性文本注入 pilot 里，同 WER 的否定删除比功能词删除造成多得多的错误提议调用；两种确认提示很少澄清单词错误；一个可选布尔调用过滤器以近乎全体确认合法正向请求为代价换来高否定拦截 | medium |

# 数据不支持、报告里不写的
- 任何关于"通顺语义错误（含实体）"的一般性结论——实体替换的伤害在两种打分器之间未解决（严格 93–95%，宽松 9.5–19%）。
- "便宜闸门都失明"的一般性结论；"3B 忽略标签"；"51.2% 是代价"；真实 ASR / 真实执行后果。

# 评审重算发现的一处错误（已改）
IDEA_REPORT / RESULTS_P0b 里"动作级 DiD 全部 ≤0"不对：3B other_1w 在 confirm 与 confirm_generic 下均为 +2.4pp [0.0, 7.1]。不影响预注册结论（远低于 25pp）。

# 路由
partial → 主张按上表收窄；补充实验：仅当报告提及实体伤害时才需要盲判 content_sub（选择不提）；负结果短报告不需要新实验。
