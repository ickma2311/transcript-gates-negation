# PREREG P0d — 确认提示在正向镜像卡上的代价（kill-argument 第一轮 P5 指出的缺口；2026-09-24，跑前写死）

问题：表 2 的"clean 误确认 0%"只在 42 张否定卡上测过；`confirm` / `confirm_generic` / `spktag` 在 42 张**正向**卡（用户确实要那个 true）上的确认率与错误动作率未知。
材料：同一批 `clean_pos` 42 卡（P0c 已冻结）；闸门 none / confirm / confirm_generic / spktag；两模型；一次 Colab T4。
端点：CF(clean_pos) 与 WA(clean_pos) 每闸门；与 P0 的 CF(clean) 并列报告。
判定：无假设检验；这是代价测量。报告规则：表 2 的 clean 代价行必须同时给否定卡与正向卡两个数。
代码不改（run_pilot.py 哈希同 PREREG_P0c）；作业只把 trials 过滤到 clean_pos。
