# RESULTS P0d — 2026-09-24（EXPLORATORY；Colab T4 957 s；PREREG_P0d；42 张正向镜像卡 × 4 闸门 × 2 模型）

确认提示与说话人标签在**合法正向请求**上的代价（宽松打分；严格打分括号内）：

| 模型 | 闸门 | CF | WA | OK |
|---|---|---|---|---|
| Qwen2.5-3B-Instruct | none | 0.0 (0.0) | 7.1 (26.2) | 92.9 (69.0) |
| Qwen2.5-3B-Instruct | confirm | 0.0 (0.0) | 7.1 (23.8) | 92.9 (71.4) |
| Qwen2.5-3B-Instruct | confirm_generic | 0.0 (0.0) | 4.8 (21.4) | 95.2 (73.8) |
| Qwen2.5-3B-Instruct | spktag | 0.0 (0.0) | 4.8 (23.8) | 95.2 (71.4) |
| Qwen2.5-7B-Instruct-AWQ | none | 0.0 (0.0) | 0.0 (21.4) | 100.0 (73.8) |
| Qwen2.5-7B-Instruct-AWQ | confirm | 7.1 (7.1) | 0.0 (14.3) | 92.9 (73.8) |
| Qwen2.5-7B-Instruct-AWQ | confirm_generic | 0.0 (0.0) | 0.0 (21.4) | 100.0 (73.8) |
| Qwen2.5-7B-Instruct-AWQ | spktag | 0.0 (0.0) | 2.4 (16.7) | 97.6 (76.2) |

读法：7B 的 confirm 提示在正向卡上确认 7.1%，在 neg_drop 上 9.5%（两组各 42 卡的汇总率，两组文本大多不同；在 7 对逐字相同的输入上原始输出完全一致，这才是 §2 不可能性所要求的）。3B 两种提示在正向卡上都是 0%。
