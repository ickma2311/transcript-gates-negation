# PREREG P0c — "可选布尔参数被设为 true 前必须确认"这条规则的收益与代价（Chao 2026-09-24 选定路线 (b)）

## 动机
P0/P0b：提示级确认对通顺语义错误失明；但 7B 在 neg_drop 下的 4 次确认全问在被翻转的可选布尔参数上。
问题：一条不需要检测错误、只看**动作形态**的规则——"要把任何可选布尔参数设为 true 之前先问"——能挡住多少否定丢失，代价是多少？

## 关键设计：正向镜像卡片
现有 42 张卡的 gold 布尔全为 false（否定 → false），规则在它们上面必赢、代价为零，这是构造伪影。
因此新增 **42 张正向镜像卡**（`seed_items.POS_UTTERANCES`，同工具、同参数，用户**确实**要那个 true，gold = 原卡的 flipped 调用）。
规则的代价 = 在正向卡上把合法请求变成确认的比例。

## 两种实现，都报
- **prompted**（`confirm_optbool` 闸门）：系统提示里写明规则，由 LLM 自己执行。
- **wrapper**（`analyze.optbool_wrapper`）：对 none 闸门的输出做确定性后过滤，任一可选布尔为 true → CONFIRM。离线算，不花算力。

## 端点
- blocked(neg_drop) = neg_drop 条件下 CONFIRM 比例（规则挡住了翻转）。
- 代价 = clean（42 否定卡）与 clean_pos（42 正向卡）合并 84 张上的 CONFIRM 比例；分别也报。
- 其余条件（func_drop / content_sub / other_1w / other_1w_mid / other_intent）的 CF 与 WA 一并报。

## 判定（跑前写死）
- **值得做 ≥120 卡确认性实验**：任一模型上 prompted 版 blocked(neg_drop) ≥ 60% **且** 84 张 clean 合并 CF ≤ 30%。
- **关闭 (b) 路线**：两个模型都不满足。wrapper 版只作参考——它对否定丢失的挡住率按构造应接近 100%，代价按构造应接近 50%（正向卡全触发），
  若 prompted 版不能明显低于 wrapper 的代价，说明 LLM 没有利用转写内容来区分，规则等于全体确认。
- 预期声明：我预期 prompted 版会接近 wrapper 版（代价 ≈50%），即**关闭**；跑的意义是把这一点量出来，而不是希望它成立。

## 材料与算力
42 否定卡 × 8 条件 + 42 正向卡 × 1 条件 = 378 trials × 2 闸门（none, confirm_optbool）× 2 模型；一次 Colab T4 会话，$0。标签 EXPLORATORY。

## 冻结哈希
b2b92cb262b56b996c02f730b351be6d74d07c9ec365a45cbce3e2bf32a52a27  seed_items.py
d42c28b9f919bd26ba158f27a6cbc614031e22dfa37e14955f0e1d3dfb1de40d  inject.py
f140a71cd1cb9bc122c2d3ad7b0eb096970b9d461c68ddc75c7e62dc134e111a  run_pilot.py
860942f97cb9e7fc5b7c8e173363d1e25f0b2573cff4a80056048e70662b5a5b  analyze.py
