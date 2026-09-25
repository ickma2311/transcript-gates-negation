# PREREG P0b — 外部评审（gpt-6-sol，session 01a0d14b…）指出的判别性对照，2026-09-23 定稿，P0 出结果前写好

P0（`PREREG_P0.md`，实际运行代码 = `job_bundle_p0_frozen.py` 内嵌版本）不改。P0b 用**同 42 张卡**追加：

- 新条件 **`other_1w_mid`**：同一个旁人单词插到句内子句边界（`but/and/with/without` 之前；没有则句中点），仍恰一个编辑、WER = 1/L。
  目的：排除"句尾悬空词"伪影。
- 新闸门 **`confirm_generic`**：只说"对动作或参数不确定就问"，**不点名任何错误类型**（原 `confirm` 提示点名了缺词/多词/旁人）。
- 主统计量改为**差分之差**（DiD）：[WA(none)−WA(gate)] 在 other_1w(_mid) 上减去在 neg_drop 上，按卡配对 bootstrap 95% CI。
- bootstrap 一律按卡片 ID 配对重采样（`analyze.py`）。
- P1 分类器：插入类只有当插入词恰等于旁人片段、且无其它编辑时才算 `intended`（`acoustic_p1.py`）。

**判定（评审给的，照录）**：`other_1w_mid` 下 confirm 闸门的确认率仍比 neg_drop 高 ≥ 25pp，且 clean 确认 ≤ 25% → H1 成立，继续；
否则原 H1 视为句尾伪影，**方向降级为"闸门对通顺错误无效"的负结果**，只写短报告。
`confirm_generic` 下 DiD 若与 `confirm` 同号且 CI 不含 0 → 交互不是提示措辞的产物。

标签：EXPLORATORY。算力：一次 Colab T4 会话（≤ 30 min，$0）。

## 冻结哈希（P0b 代码）
09d5fb2a89b8139ba83499fe6c45b5d4e76b09499611f99ef6d6f276de891f03  seed_items.py
bf106e55cef8da1be376f021103eeda3dbe591a882568eb7c59c2e43f512afc6  inject.py
f7fa97f41daafe51fdffd1fee3906df106d6004f123551271df4f08ffd38d3fa  run_pilot.py
f64b00f3062a001a479cf9e9332ebca63d7803a84d952b6f57acbc3d37a55b19  analyze.py
8cc8780db0283ee567ee2d7f6d0a849b8f210823702be4cef543da37aee7eb9a  acoustic_p1.py

## 修订注（2026-09-23，方案评审后、P0b 跑前）
继续规则改为**动作级**：DiD = [WA(none)−WA(confirm)] 在 other_1w_mid 上 − 在 neg_drop 上 ≥ 25pp 且配对 CI 不含 0、clean 确认 ≤ 25% → 继续；
确认率之差只作辅助。结果表必须同时列 NO_CALL / PARSE_FAIL / EXTRA_ARG。
