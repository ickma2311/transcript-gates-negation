# PREREG P0 — 定稿 2026-09-23（查新 PROCEED WITH CAUTION 后按其指出的缺陷修订；sha256 见文末；跑前不再改）

## 问题
在**单编辑、逐条 WER 严格相等**的条件下，四种转写错误（否定词丢失 / 功能词丢失 / 内容词近音替换 / 旁人语音插入）
对 LLM 工具调用的**动作结果**影响是否不同；两种低成本闸门（确认提示、说话人标签）对各类错误的检出率是否不同。

## 材料（已冻结在 `seed_items.py`，42 条 × 6 条件 = 252 trials；`inject.py 0`）
- 42 条口语指令，每条恰有一个否定词，其删除会翻转恰好一个布尔/枚举参数；gold 与 flipped 调用均由构造决定，无需人工标注。
- 条件：clean / neg_drop / func_drop / content_sub / other_1w（**四者每条恰 1 个词级编辑，逐条 WER 严格相同 = 1/L**；content_sub 已改为只用单词替换）/ other_intent / other_chatter（插入 3–6 词旁人片段，WER≈0.38，只作剂量对照）。
- 闸门：none / confirm（系统提示：可能有识别错误则回 `CONFIRM:` 不调用；**同时给出 CONFIRM 与工具调用的回复按调用打分**，因为动作会执行）/ spktag（**所有条件都跑**：`[speaker 1]`/`[speaker 2]` 标签，声明只有 speaker 1 是用户；这是 oracle 标签上限，不是真实说话人验证）。
- 模型：Qwen2.5-3B-Instruct（fp16）、Qwen2.5-7B-Instruct-AWQ；vLLM，temperature 0。

## 主端点（每个模型 × 条件 × 闸门）
- **WA**：错误动作率 = (WRONG_ACTION + FLIPPED + EXTRA_CALL) / n
- **CF**：确认率 = CONFIRM / n（confirm 闸门下）；clean 条件下的 CF 即误报代价
- **主假设 H1（闸门×类型交互，同 WER）**：confirm 闸门在 **other_1w** 上的 CF 比在 neg_drop 上高 ≥ 25pp（"通顺的错误看不出来"）；other_intent 与 neg_drop 的差只作次要报告（剂量不同）。
- **H2（同 WER 不同伤害）**：none 闸门下 neg_drop 的 WA 比 func_drop 高 ≥ 40pp（同为 1 个删除）。
- **H3（来源标签只治插入）**：spktag 使 other_intent 的 WA 相对 none 下降 ≥ 30pp，且 clean 上 WA 不升高 > 5pp；**并报告 spktag 下 neg_drop 的 WA 与 none 的差**（预期 ≈0，是"只治插入"的另一半）。

## 判定规则（写死，跑前不改）
- **GO**：两个模型中 ≥1 个同时满足 H1 与 H2，且该模型 clean 条件下 confirm 闸门 CF ≤ 25%。
- **STOP**：两个模型上 confirm 闸门在所有错误条件的 CF 都 < 10%（提示级闸门完全无效，且无交互可测）**或**
  H2 在两个模型上都不成立（WA 差 < 20pp：否定丢失并不比功能词丢失更伤，构造假设失败）。
- 其余：**INCONCLUSIVE**，写明缺哪条，进入 lite 模式只做最小判别实验。
- 标签纪律：本 pilot 一律 **EXPLORATORY**，只用于分配后续算力。

## 预算
Colab T4 一次会话：vLLM 安装约 5 min + 两个模型各 ~630 prompts（≤ 5 min）→ 总 < 30 min。花费 $0。

## 已知局限（查新评审指出，写在跑前）
- 否定删除按构造必然翻转 gold，H2 只说明幅度，**主结果是 H1 的交互**。
- 说话人标签是 oracle 设定；真实说话人验证是 P1 之后的事。
- 端点是**提议的**工具调用（mock 执行），不是真实执行后果。
- 42 张卡片是手工模板，覆盖窄；GO 之后先扩到 ≥120 张并盲检 gold，再做确认性实验。

## 冻结哈希（2026-09-23，修完查新指出的四处后，GPU 跑前）
09d5fb2a89b8139ba83499fe6c45b5d4e76b09499611f99ef6d6f276de891f03  seed_items.py
5f5bf193bad18fe20f31037cc70bdd4572e070233e76748533f094d89097a563  inject.py
de89bcc35de7c0132d56d9ae583d7c3939c530f5e314f5f2a1fd0ffa3ca5e840  run_pilot.py

## 更正注（2026-09-24，跑后追加；上文冻结文本未改）
材料一行写"6 条件 = 252 trials"，但列出的是七个条件（content_sub 改为单词替换时加入了 other_1w）；冻结的 `inject.py 0` 实际生成 **7 条件 × 42 = 294 trials**，见 `results/p0/*/trials.jsonl`。写作"3–6 词"的旁人片段在保存的 trials 里实为 **2–6 词**。
