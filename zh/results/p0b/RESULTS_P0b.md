# RESULTS P0b — 2026-09-23（EXPLORATORY；Colab T4 1169 s；代码 job_bundle_p0b.py；PREREG_P0b 含动作级修订注）

## 判定：按 PREREG_P0b，原 H1 **不是句尾伪影，而是不存在** → 方向降级为负结果
- other_1w_mid（句内插入）@confirm 的确认率：3B 0.0%、7B 2.4%（比句尾的 4.8% / 9.5% 还低）
- confirm_generic（不点名错误类型）：neg_drop 0.0 / 2.4%，other_intent 28.6 / 16.7%，clean 0 / 0% —— 与引导性提示同一图案
- 动作级 DiD（confirm 对 other_1w_mid 的 WA 降幅 − 对 neg_drop 的降幅）：3B −4.8 [−11.9, 0.0]；7B −9.5 [−19.0, −2.4]（若有交互，方向与原假设相反：7B 的确认反而略多地救了否定）。注：3B 的 other_1w（句尾）DiD 为 +2.4 [0.0, 7.1]，是唯一为正的一格，仍远低于 25pp。

## 宽松打分（DEVIATION 同 P0）
```

===== colab_out_p0b_lenient/Qwen2.5-3B-Instruct  (n=1344) =====
condition       gate        n     WA     CF     OK  NOCALL  EXTRA  wer
clean           confirm    42    7.1    0.0   92.9     0.0    0.0  0.000
clean           confirm_generic  42    4.8    0.0   95.2     0.0    0.0  0.000
clean           none       42    7.1    0.0   92.9     0.0    0.0  0.000
clean           spktag     42    7.1    0.0   92.9     0.0    0.0  0.000
content_sub     confirm    42   16.7    0.0   83.3     0.0    0.0  0.088
content_sub     confirm_generic  42   14.3    0.0   85.7     0.0    0.0  0.088
content_sub     none       42   19.0    0.0   81.0     0.0    0.0  0.088
content_sub     spktag     42   19.0    0.0   81.0     0.0    0.0  0.088
func_drop       confirm    42   14.3    0.0   85.7     0.0    0.0  0.088
func_drop       confirm_generic  42   14.3    0.0   85.7     0.0    0.0  0.088
func_drop       none       42   14.3    0.0   85.7     0.0    0.0  0.088
func_drop       spktag     42   11.9    0.0   88.1     0.0    0.0  0.088
neg_drop        confirm    42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        confirm_generic  42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        none       42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        spktag     42   97.6    0.0    2.4     0.0    0.0  0.088
other_1w        confirm    42   19.0    4.8   76.2     0.0    0.0  0.088
other_1w        confirm_generic  42   19.0    2.4   78.6     0.0    0.0  0.088
other_1w        none       42   21.4    0.0   78.6     0.0    0.0  0.088
other_1w        spktag     42   14.3    0.0   85.7     0.0    0.0  0.088
other_1w_mid    confirm    42   19.0    0.0   81.0     0.0    0.0  0.088
other_1w_mid    confirm_generic  42   16.7    0.0   83.3     0.0    0.0  0.088
other_1w_mid    none       42   14.3    0.0   85.7     0.0    0.0  0.088
other_1w_mid    spktag     42   19.0    0.0   81.0     0.0    0.0  0.088
other_chatter   confirm    42   11.9   16.7   71.4     0.0    0.0  0.389
other_chatter   confirm_generic  42   11.9   14.3   73.8     0.0    0.0  0.389
other_chatter   none       42   16.7    0.0   81.0     2.4    0.0  0.389
other_chatter   spktag     42   11.9    0.0   78.6     9.5    0.0  0.389
other_intent    confirm    42   19.0   31.0   50.0     0.0    0.0  0.379
other_intent    confirm_generic  42   19.0   28.6   50.0     2.4    0.0  0.379
other_intent    none       42   28.6    0.0   57.1    14.3    0.0  0.379
other_intent    spktag     42   26.2    0.0   64.3     9.5    0.0  0.379
Pre-registered contrasts:
  H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp): +83.3pp  [95% CI +71.4, +92.9]
  H1  CF(other_1w) - CF(neg_drop) @confirm      (GO needs >= +25pp): +4.8pp  [95% CI +0.0, +11.9]
  H1b CF(other_intent) - CF(neg_drop) @confirm  (secondary): +31.0pp  [95% CI +16.7, +45.2]
  H3  WA(other_intent) none - spktag             (GO needs >= +30pp): +2.4pp  [95% CI -11.9, +16.7]
  H3b WA(clean) spktag - none                    (must be <= +5pp): +0.0pp  [95% CI -7.1, +7.1]
  H3c WA(neg_drop) spktag - none                 (expected ~0): +0.0pp  [95% CI +0.0, +0.0]
  P0b CF(other_1w_mid) - CF(neg_drop) @confirm   (continue only if >= +25pp): +0.0pp  [95% CI +0.0, +0.0]
  P0b CF(other_1w) - CF(neg_drop) @confirm_generic (non-leading prompt): +2.4pp  [95% CI +0.0, +7.1]
  DiD WA-reduction[other_1w] - WA-reduction[neg_drop] under confirm: +2.4pp [95% CI +0.0, +7.1]
  DiD WA-reduction[other_1w_mid] - WA-reduction[neg_drop] under confirm: -4.8pp [95% CI -11.9, +0.0]
  DiD WA-reduction[other_1w] - WA-reduction[neg_drop] under confirm_generic: +2.4pp [95% CI +0.0, +7.1]
  DiD WA-reduction[other_1w_mid] - WA-reduction[neg_drop] under confirm_generic: -2.4pp [95% CI -7.1, +0.0]
  clean false-confirm rate @confirm: 0.0%  (must be <= 25%)
  CF on error conditions @confirm: [0.0, 0.0, 0.0, 4.8, 31.0, 16.7]
  => NOT GO on this model

===== colab_out_p0b_lenient/Qwen2.5-7B-Instruct-AWQ  (n=1344) =====
condition       gate        n     WA     CF     OK  NOCALL  EXTRA  wer
clean           confirm    42    0.0    0.0  100.0     0.0    0.0  0.000
clean           confirm_generic  42    0.0    0.0  100.0     0.0    0.0  0.000
clean           none       42    2.4    0.0   97.6     0.0    0.0  0.000
clean           spktag     42    4.8    0.0   95.2     0.0    0.0  0.000
content_sub     confirm    42    9.5    0.0   90.5     0.0    0.0  0.088
content_sub     confirm_generic  42    9.5    0.0   90.5     0.0    0.0  0.088
content_sub     none       42    9.5    0.0   90.5     0.0    0.0  0.088
content_sub     spktag     42   11.9    0.0   88.1     0.0    0.0  0.088
func_drop       confirm    42    0.0    2.4   97.6     0.0    0.0  0.088
func_drop       confirm_generic  42    0.0    2.4   97.6     0.0    0.0  0.088
func_drop       none       42    4.8    0.0   95.2     0.0    0.0  0.088
func_drop       spktag     42    2.4    0.0   97.6     0.0    0.0  0.088
neg_drop        confirm    42   88.1    9.5    2.4     0.0    0.0  0.088
neg_drop        confirm_generic  42   92.9    2.4    4.8     0.0    0.0  0.088
neg_drop        none       42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        spktag     42   95.2    0.0    4.8     0.0    0.0  0.088
other_1w        confirm    42    7.1    9.5   83.3     0.0    0.0  0.088
other_1w        confirm_generic  42    7.1    4.8   88.1     0.0    0.0  0.088
other_1w        none       42    9.5    0.0   90.5     0.0    0.0  0.088
other_1w        spktag     42    9.5    0.0   90.5     0.0    0.0  0.088
other_1w_mid    confirm    42   11.9    2.4   85.7     0.0    0.0  0.088
other_1w_mid    confirm_generic  42   14.3    2.4   83.3     0.0    0.0  0.088
other_1w_mid    none       42   11.9    0.0   88.1     0.0    0.0  0.088
other_1w_mid    spktag     42    7.1    0.0   92.9     0.0    0.0  0.088
other_chatter   confirm    42    7.1   23.8   69.0     0.0    0.0  0.389
other_chatter   confirm_generic  42    7.1   16.7   76.2     0.0    0.0  0.389
other_chatter   none       42    7.1    0.0   92.9     0.0    0.0  0.389
other_chatter   spktag     42    9.5    0.0   90.5     0.0    0.0  0.389
other_intent    confirm    42   11.9   21.4   66.7     0.0    0.0  0.379
other_intent    confirm_generic  42    9.5   16.7   73.8     0.0    0.0  0.379
other_intent    none       42   21.4    0.0   78.6     0.0    0.0  0.379
other_intent    spktag     42    9.5    0.0   90.5     0.0    0.0  0.379
Pre-registered contrasts:
  H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp): +92.9pp  [95% CI +85.7, +100.0]
  H1  CF(other_1w) - CF(neg_drop) @confirm      (GO needs >= +25pp): +0.0pp  [95% CI -11.9, +11.9]
  H1b CF(other_intent) - CF(neg_drop) @confirm  (secondary): +11.9pp  [95% CI +0.0, +23.8]
  H3  WA(other_intent) none - spktag             (GO needs >= +30pp): +11.9pp  [95% CI +0.0, +23.8]
  H3b WA(clean) spktag - none                    (must be <= +5pp): +2.4pp  [95% CI -4.8, +9.5]
  H3c WA(neg_drop) spktag - none                 (expected ~0): -2.4pp  [95% CI -7.1, +0.0]
  P0b CF(other_1w_mid) - CF(neg_drop) @confirm   (continue only if >= +25pp): -7.1pp  [95% CI -16.7, +2.4]
  P0b CF(other_1w) - CF(neg_drop) @confirm_generic (non-leading prompt): +2.4pp  [95% CI -4.8, +11.9]
  DiD WA-reduction[other_1w] - WA-reduction[neg_drop] under confirm: -7.1pp [95% CI -16.7, +2.4]
  DiD WA-reduction[other_1w_mid] - WA-reduction[neg_drop] under confirm: -9.5pp [95% CI -19.0, -2.4]
  DiD WA-reduction[other_1w] - WA-reduction[neg_drop] under confirm_generic: -2.4pp [95% CI -9.5, +4.8]
  DiD WA-reduction[other_1w_mid] - WA-reduction[neg_drop] under confirm_generic: -7.1pp [95% CI -16.7, +0.0]
  clean false-confirm rate @confirm: 0.0%  (must be <= 25%)
  CF on error conditions @confirm: [9.5, 2.4, 0.0, 9.5, 21.4, 23.8]
  => NOT GO on this model
```

## 严格打分对比
```
===== colab_out_p0b/Qwen2.5-3B-Instruct  (n=1344) =====
Pre-registered contrasts:
  H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp): +61.9pp  [95% CI +47.6, +76.2]
  H1  CF(other_1w) - CF(neg_drop) @confirm      (GO needs >= +25pp): +4.8pp  [95% CI +0.0, +11.9]
  H1b CF(other_intent) - CF(neg_drop) @confirm  (secondary): +31.0pp  [95% CI +16.7, +45.2]
  H3  WA(other_intent) none - spktag             (GO needs >= +30pp): +2.4pp  [95% CI -9.5, +14.3]
  H3b WA(clean) spktag - none                    (must be <= +5pp): +0.0pp  [95% CI -7.1, +7.1]
  H3c WA(neg_drop) spktag - none                 (expected ~0): +0.0pp  [95% CI +0.0, +0.0]
  P0b CF(other_1w_mid) - CF(neg_drop) @confirm   (continue only if >= +25pp): +0.0pp  [95% CI +0.0, +0.0]
  P0b CF(other_1w) - CF(neg_drop) @confirm_generic (non-leading prompt): +2.4pp  [95% CI +0.0, +7.1]
  DiD WA-reduction[other_1w] - WA-reduction[neg_drop] under confirm: +4.8pp [95% CI +0.0, +11.9]
  DiD WA-reduction[other_1w_mid] - WA-reduction[neg_drop] under confirm: +0.0pp [95% CI -9.5, +9.5]
  DiD WA-reduction[other_1w] - WA-reduction[neg_drop] under confirm_generic: +0.0pp [95% CI -7.1, +7.1]
  DiD WA-reduction[other_1w_mid] - WA-reduction[neg_drop] under confirm_generic: -2.4pp [95% CI -7.1, +0.0]
  clean false-confirm rate @confirm: 0.0%  (must be <= 25%)
  CF on error conditions @confirm: [0.0, 0.0, 0.0, 4.8, 31.0, 16.7]
  => NOT GO on this model
===== colab_out_p0b/Qwen2.5-7B-Instruct-AWQ  (n=1344) =====
Pre-registered contrasts:
  H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp): +73.8pp  [95% CI +59.5, +85.7]
  H1  CF(other_1w) - CF(neg_drop) @confirm      (GO needs >= +25pp): +0.0pp  [95% CI -11.9, +11.9]
  H1b CF(other_intent) - CF(neg_drop) @confirm  (secondary): +11.9pp  [95% CI +0.0, +23.8]
  H3  WA(other_intent) none - spktag             (GO needs >= +30pp): +11.9pp  [95% CI +0.0, +23.8]
  H3b WA(clean) spktag - none                    (must be <= +5pp): +2.4pp  [95% CI +0.0, +7.1]
  H3c WA(neg_drop) spktag - none                 (expected ~0): -2.4pp  [95% CI -7.1, +0.0]
  P0b CF(other_1w_mid) - CF(neg_drop) @confirm   (continue only if >= +25pp): -7.1pp  [95% CI -16.7, +2.4]
  P0b CF(other_1w) - CF(neg_drop) @confirm_generic (non-leading prompt): +2.4pp  [95% CI -4.8, +11.9]
  DiD WA-reduction[other_1w] - WA-reduction[neg_drop] under confirm: -7.1pp [95% CI -19.0, +4.8]
  DiD WA-reduction[other_1w_mid] - WA-reduction[neg_drop] under confirm: -9.5pp [95% CI -19.0, -2.4]
  DiD WA-reduction[other_1w] - WA-reduction[neg_drop] under confirm_generic: +0.0pp [95% CI -9.5, +9.5]
  DiD WA-reduction[other_1w_mid] - WA-reduction[neg_drop] under confirm_generic: -7.1pp [95% CI -16.7, +0.0]
  clean false-confirm rate @confirm: 0.0%  (must be <= 25%)
  CF on error conditions @confirm: [9.5, 2.4, 0.0, 9.5, 21.4, 23.8]
  => NOT GO on this model
```

## 严格打分完整表
```
model=Qwen/Qwen2.5-3B-Instruct
condition      gate       CORRECT EXTRA_AR  FLIPPED WRONG_AC EXTRA_CA  CONFIRM  NO_CALL PARSE_FA     n
clean          none          64.3      7.1      0.0     28.6      0.0      0.0      0.0      0.0    42
clean          confirm       69.0      7.1      0.0     23.8      0.0      0.0      0.0      0.0    42
clean          confirm_generic     66.7      7.1      0.0     26.2      0.0      0.0      0.0      0.0    42
clean          spktag        64.3      7.1      0.0     28.6      0.0      0.0      0.0      0.0    42
neg_drop       none           2.4      0.0     69.0     26.2      2.4      0.0      0.0      0.0    42
neg_drop       confirm        2.4      0.0     71.4     23.8      2.4      0.0      0.0      0.0    42
neg_drop       confirm_generic      2.4      0.0     73.8     21.4      2.4      0.0      0.0      0.0    42
neg_drop       spktag         2.4      0.0     66.7     26.2      4.8      0.0      0.0      0.0    42
func_drop      none          59.5      4.8      0.0     35.7      0.0      0.0      0.0      0.0    42
func_drop      confirm       59.5      4.8      0.0     35.7      0.0      0.0      0.0      0.0    42
func_drop      confirm_generic     59.5      4.8      0.0     35.7      0.0      0.0      0.0      0.0    42
func_drop      spktag        61.9      4.8      0.0     33.3      0.0      0.0      0.0      0.0    42
content_sub    none           2.4      2.4      0.0     95.2      0.0      0.0      0.0      0.0    42
content_sub    confirm        2.4      2.4      0.0     95.2      0.0      0.0      0.0      0.0    42
content_sub    confirm_generic      2.4      2.4      0.0     95.2      0.0      0.0      0.0      0.0    42
content_sub    spktag         2.4      2.4      0.0     95.2      0.0      0.0      0.0      0.0    42
other_1w       none          59.5      4.8      0.0     28.6      7.1      0.0      0.0      0.0    42
other_1w       confirm       59.5      4.8      0.0     26.2      4.8      4.8      0.0      0.0    42
other_1w       confirm_generic     57.1      4.8      0.0     31.0      4.8      2.4      0.0      0.0    42
other_1w       spktag        61.9      4.8      0.0     31.0      2.4      0.0      0.0      0.0    42
other_1w_mid   none          57.1      7.1      0.0     33.3      2.4      0.0      0.0      0.0    42
other_1w_mid   confirm       57.1      7.1      0.0     33.3      2.4      0.0      0.0      0.0    42
other_1w_mid   confirm_generic     54.8      7.1      0.0     35.7      2.4      0.0      0.0      0.0    42
other_1w_mid   spktag        59.5      4.8      0.0     31.0      4.8      0.0      0.0      0.0    42
other_intent   none          40.5      2.4      0.0     28.6     14.3      0.0     14.3      0.0    42
other_intent   confirm       38.1      0.0      0.0     19.0     11.9     31.0      0.0      0.0    42
other_intent   confirm_generic     38.1      0.0      0.0     21.4      9.5     28.6      2.4      0.0    42
other_intent   spktag        45.2      4.8      0.0     21.4     19.0      0.0      9.5      0.0    42
other_chatter  none          52.4      7.1      0.0     31.0      7.1      0.0      2.4      0.0    42
other_chatter  confirm       45.2      7.1      0.0     28.6      2.4     16.7      0.0      0.0    42
other_chatter  confirm_generic     47.6      7.1      0.0     28.6      2.4     14.3      0.0      0.0    42
other_chatter  spktag        57.1      4.8      0.0     23.8      4.8      0.0      9.5      0.0    42
```
```
model=Qwen/Qwen2.5-7B-Instruct-AWQ
condition      gate       CORRECT EXTRA_AR  FLIPPED WRONG_AC EXTRA_CA  CONFIRM  NO_CALL PARSE_FA     n
clean          none          78.6      4.8      0.0     16.7      0.0      0.0      0.0      0.0    42
clean          confirm       76.2      4.8      0.0     19.0      0.0      0.0      0.0      0.0    42
clean          confirm_generic     78.6      4.8      0.0     16.7      0.0      0.0      0.0      0.0    42
clean          spktag        76.2      4.8      0.0     19.0      0.0      0.0      0.0      0.0    42
neg_drop       none           2.4      0.0     78.6     16.7      2.4      0.0      0.0      0.0    42
neg_drop       confirm        2.4      0.0     66.7     19.0      2.4      9.5      0.0      0.0    42
neg_drop       confirm_generic      4.8      0.0     76.2     16.7      0.0      2.4      0.0      0.0    42
neg_drop       spktag         4.8      0.0     81.0     14.3      0.0      0.0      0.0      0.0    42
func_drop      none          71.4      4.8      0.0     23.8      0.0      0.0      0.0      0.0    42
func_drop      confirm       69.0      7.1      0.0     21.4      0.0      2.4      0.0      0.0    42
func_drop      confirm_generic     71.4      7.1      0.0     19.0      0.0      2.4      0.0      0.0    42
func_drop      spktag        73.8      7.1      0.0     19.0      0.0      0.0      0.0      0.0    42
content_sub    none           4.8      2.4      0.0     92.9      0.0      0.0      0.0      0.0    42
content_sub    confirm        4.8      2.4      0.0     92.9      0.0      0.0      0.0      0.0    42
content_sub    confirm_generic      4.8      2.4      0.0     92.9      0.0      0.0      0.0      0.0    42
content_sub    spktag         4.8      2.4      0.0     92.9      0.0      0.0      0.0      0.0    42
other_1w       none          73.8      4.8      0.0     21.4      0.0      0.0      0.0      0.0    42
other_1w       confirm       66.7      4.8      0.0     19.0      0.0      9.5      0.0      0.0    42
other_1w       confirm_generic     73.8      4.8      0.0     16.7      0.0      4.8      0.0      0.0    42
other_1w       spktag        73.8      4.8      0.0     21.4      0.0      0.0      0.0      0.0    42
other_1w_mid   none          69.0      0.0      0.0     31.0      0.0      0.0      0.0      0.0    42
other_1w_mid   confirm       64.3      2.4      0.0     31.0      0.0      2.4      0.0      0.0    42
other_1w_mid   confirm_generic     64.3      0.0      0.0     33.3      0.0      2.4      0.0      0.0    42
other_1w_mid   spktag        73.8      7.1      0.0     19.0      0.0      0.0      0.0      0.0    42
other_intent   none          61.9      4.8      0.0     19.0     14.3      0.0      0.0      0.0    42
other_intent   confirm       57.1      0.0      0.0     14.3      7.1     21.4      0.0      0.0    42
other_intent   confirm_generic     61.9      2.4      0.0     11.9      7.1     16.7      0.0      0.0    42
other_intent   spktag        73.8      4.8      0.0     21.4      0.0      0.0      0.0      0.0    42
other_chatter  none          76.2      4.8      0.0     19.0      0.0      0.0      0.0      0.0    42
other_chatter  confirm       59.5      2.4      0.0     14.3      0.0     23.8      0.0      0.0    42
other_chatter  confirm_generic     64.3      2.4      0.0     16.7      0.0     16.7      0.0      0.0    42
other_chatter  spktag        73.8      4.8      0.0     21.4      0.0      0.0      0.0      0.0    42
```
