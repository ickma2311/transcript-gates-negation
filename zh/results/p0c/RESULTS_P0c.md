# RESULTS P0c — 2026-09-24（EXPLORATORY；Colab T4 1005 s；代码 job_bundle_p0c.py；PREREG_P0c sha256 502fdfaf…；第一次运行因客户端无输出超时丢失，第二次改为流式输出后完成，冻结文件哈希未变）

## 判定：两模型均 CLOSE → 按预注册关闭路线 (b)
- prompted（confirm_optbool）：blocked(neg_drop) 3B 0.0% / 7B 2.4%；clean 合并 CF 0% / 0%——规则**没有被执行**：模型照样把可选布尔设为 true 并直接调用（clean_pos 下 OK 95.2% / 100%）。
- wrapper（确定性后过滤）：blocked 97.6% / 97.6%（构造决定），但 clean_pos CF 97.6% / 100%，84 张合并 51.2%——代价 = 合法的"打开某开关"请求中 41/42（3B）与 42/42（7B）都要确认。
- 预注册里的预期（prompted ≈ wrapper，代价≈50%）**错了一半**：prompted 版代价不是 50% 而是 0%，因为它压根不触发；LLM 没有把"参数形态规则"当成要遵守的策略。

## 宽松打分（DEVIATION 同 P0）
```

===== colab_out_p0c_lenient/Qwen2.5-3B-Instruct  (n=1134) =====
condition       gate        n     WA     CF     OK  NOCALL  EXTRA  wer
clean           confirm_optbool  42    4.8    0.0   95.2     0.0    0.0  0.000
clean           none       42    7.1    0.0   92.9     0.0    0.0  0.000
clean           wrapper_optbool  42    2.4    4.8   92.9     0.0    0.0  0.000
clean_pos       confirm_optbool  42    4.8    0.0   95.2     0.0    0.0  0.000
clean_pos       none       42    7.1    0.0   92.9     0.0    0.0  0.000
clean_pos       wrapper_optbool  42    2.4   97.6    0.0     0.0    0.0  0.000
content_sub     confirm_optbool  42   14.3    0.0   85.7     0.0    0.0  0.088
content_sub     none       42   19.0    0.0   81.0     0.0    0.0  0.088
content_sub     wrapper_optbool  42   11.9    7.1   81.0     0.0    0.0  0.088
func_drop       confirm_optbool  42    9.5    0.0   90.5     0.0    0.0  0.088
func_drop       none       42   14.3    0.0   85.7     0.0    0.0  0.088
func_drop       wrapper_optbool  42    2.4   11.9   85.7     0.0    0.0  0.088
neg_drop        confirm_optbool  42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        none       42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        wrapper_optbool  42    0.0   97.6    2.4     0.0    0.0  0.088
other_1w        confirm_optbool  42   16.7    2.4   81.0     0.0    0.0  0.088
other_1w        none       42   21.4    0.0   78.6     0.0    0.0  0.088
other_1w        wrapper_optbool  42    4.8   16.7   78.6     0.0    0.0  0.088
other_1w_mid    confirm_optbool  42   16.7    0.0   83.3     0.0    0.0  0.088
other_1w_mid    none       42   14.3    0.0   85.7     0.0    0.0  0.088
other_1w_mid    wrapper_optbool  42    2.4   11.9   85.7     0.0    0.0  0.088
other_chatter   confirm_optbool  42   11.9    9.5   76.2     2.4    0.0  0.389
other_chatter   none       42   16.7    0.0   81.0     2.4    0.0  0.389
other_chatter   wrapper_optbool  42    7.1    9.5   81.0     2.4    0.0  0.389
other_intent    confirm_optbool  42   21.4   31.0   47.6     0.0    0.0  0.379
other_intent    none       42   28.6    0.0   57.1    14.3    0.0  0.379
other_intent    wrapper_optbool  42   19.0    9.5   57.1    14.3    0.0  0.379
Pre-registered contrasts:
  H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp): +83.3pp  [95% CI +71.4, +92.9]
  clean false-confirm rate @confirm: 0.0%  (must be <= 25%)
  CF on error conditions @confirm: []
P0c (optional-boolean confirmation rule):
  [confirm_optbool] blocked(neg_drop)=0.0%  WA(neg_drop)=97.6%  CF(clean_neg)=0.0%  CF(clean_pos)=0.0%  CF(clean pooled 84)=0.0%  WA(clean_pos)=4.8%
      CF(func_drop)=0.0%  WA=9.5%
      CF(content_sub)=0.0%  WA=14.3%
      CF(other_1w)=2.4%  WA=16.7%
      CF(other_1w_mid)=0.0%  WA=16.7%
      CF(other_intent)=31.0%  WA=21.4%
      => CLOSE (rule: blocked >= 60% and pooled clean CF <= 30%)
  [wrapper_optbool] blocked(neg_drop)=97.6%  WA(neg_drop)=0.0%  CF(clean_neg)=4.8%  CF(clean_pos)=97.6%  CF(clean pooled 84)=51.2%  WA(clean_pos)=2.4%
      CF(func_drop)=11.9%  WA=2.4%
      CF(content_sub)=7.1%  WA=11.9%
      CF(other_1w)=16.7%  WA=4.8%
      CF(other_1w_mid)=11.9%  WA=2.4%
      CF(other_intent)=9.5%  WA=19.0%
      => CLOSE (rule: blocked >= 60% and pooled clean CF <= 30%)

===== colab_out_p0c_lenient/Qwen2.5-7B-Instruct-AWQ  (n=1134) =====
condition       gate        n     WA     CF     OK  NOCALL  EXTRA  wer
clean           confirm_optbool  42    0.0    0.0  100.0     0.0    0.0  0.000
clean           none       42    2.4    0.0   97.6     0.0    0.0  0.000
clean           wrapper_optbool  42    0.0    2.4   97.6     0.0    0.0  0.000
clean_pos       confirm_optbool  42    0.0    0.0  100.0     0.0    0.0  0.000
clean_pos       none       42    0.0    0.0  100.0     0.0    0.0  0.000
clean_pos       wrapper_optbool  42    0.0  100.0    0.0     0.0    0.0  0.000
content_sub     confirm_optbool  42    7.1    0.0   92.9     0.0    0.0  0.088
content_sub     none       42    9.5    0.0   90.5     0.0    0.0  0.088
content_sub     wrapper_optbool  42    7.1    2.4   90.5     0.0    0.0  0.088
func_drop       confirm_optbool  42    0.0    0.0  100.0     0.0    0.0  0.088
func_drop       none       42    4.8    0.0   95.2     0.0    0.0  0.088
func_drop       wrapper_optbool  42    0.0    4.8   95.2     0.0    0.0  0.088
neg_drop        confirm_optbool  42   95.2    2.4    2.4     0.0    0.0  0.088
neg_drop        none       42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        wrapper_optbool  42    0.0   97.6    2.4     0.0    0.0  0.088
other_1w        confirm_optbool  42    4.8    7.1   88.1     0.0    0.0  0.088
other_1w        none       42    9.5    0.0   90.5     0.0    0.0  0.088
other_1w        wrapper_optbool  42    0.0    9.5   90.5     0.0    0.0  0.088
other_1w_mid    confirm_optbool  42    9.5    2.4   88.1     0.0    0.0  0.088
other_1w_mid    none       42   11.9    0.0   88.1     0.0    0.0  0.088
other_1w_mid    wrapper_optbool  42    2.4    9.5   88.1     0.0    0.0  0.088
other_chatter   confirm_optbool  42    4.8    4.8   90.5     0.0    0.0  0.389
other_chatter   none       42    7.1    0.0   92.9     0.0    0.0  0.389
other_chatter   wrapper_optbool  42    0.0    7.1   92.9     0.0    0.0  0.389
other_intent    confirm_optbool  42   11.9    7.1   81.0     0.0    0.0  0.379
other_intent    none       42   21.4    0.0   78.6     0.0    0.0  0.379
other_intent    wrapper_optbool  42   16.7    4.8   78.6     0.0    0.0  0.379
Pre-registered contrasts:
  H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp): +92.9pp  [95% CI +85.7, +100.0]
  clean false-confirm rate @confirm: 0.0%  (must be <= 25%)
  CF on error conditions @confirm: []
P0c (optional-boolean confirmation rule):
  [confirm_optbool] blocked(neg_drop)=2.4%  WA(neg_drop)=95.2%  CF(clean_neg)=0.0%  CF(clean_pos)=0.0%  CF(clean pooled 84)=0.0%  WA(clean_pos)=0.0%
      CF(func_drop)=0.0%  WA=0.0%
      CF(content_sub)=0.0%  WA=7.1%
      CF(other_1w)=7.1%  WA=4.8%
      CF(other_1w_mid)=2.4%  WA=9.5%
      CF(other_intent)=7.1%  WA=11.9%
      => CLOSE (rule: blocked >= 60% and pooled clean CF <= 30%)
  [wrapper_optbool] blocked(neg_drop)=97.6%  WA(neg_drop)=0.0%  CF(clean_neg)=2.4%  CF(clean_pos)=100.0%  CF(clean pooled 84)=51.2%  WA(clean_pos)=0.0%
      CF(func_drop)=4.8%  WA=0.0%
      CF(content_sub)=2.4%  WA=7.1%
      CF(other_1w)=9.5%  WA=0.0%
      CF(other_1w_mid)=9.5%  WA=2.4%
      CF(other_intent)=4.8%  WA=16.7%
      => CLOSE (rule: blocked >= 60% and pooled clean CF <= 30%)
```

## 严格打分
```

===== colab_out_p0c/Qwen2.5-3B-Instruct  (n=1134) =====
condition       gate        n     WA     CF     OK  NOCALL  EXTRA  wer
clean           confirm_optbool  42   23.8    0.0   69.0     0.0    7.1  0.000
clean           none       42   28.6    0.0   64.3     0.0    7.1  0.000
clean           wrapper_optbool  42   23.8    4.8   64.3     0.0    7.1  0.000
clean_pos       confirm_optbool  42   21.4    0.0   73.8     0.0    4.8  0.000
clean_pos       none       42   26.2    0.0   69.0     0.0    4.8  0.000
clean_pos       wrapper_optbool  42    2.4   97.6    0.0     0.0    0.0  0.000
content_sub     confirm_optbool  42   95.2    0.0    2.4     0.0    2.4  0.088
content_sub     none       42   95.2    0.0    2.4     0.0    2.4  0.088
content_sub     wrapper_optbool  42   88.1    7.1    2.4     0.0    2.4  0.088
func_drop       confirm_optbool  42   28.6    0.0   66.7     0.0    4.8  0.088
func_drop       none       42   35.7    0.0   59.5     0.0    4.8  0.088
func_drop       wrapper_optbool  42   23.8   11.9   59.5     0.0    4.8  0.088
neg_drop        confirm_optbool  42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        none       42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        wrapper_optbool  42    0.0   97.6    2.4     0.0    0.0  0.088
other_1w        confirm_optbool  42   31.0    2.4   59.5     0.0    7.1  0.088
other_1w        none       42   35.7    0.0   59.5     0.0    4.8  0.088
other_1w        wrapper_optbool  42   19.0   16.7   59.5     0.0    4.8  0.088
other_1w_mid    confirm_optbool  42   38.1    0.0   54.8     0.0    7.1  0.088
other_1w_mid    none       42   35.7    0.0   57.1     0.0    7.1  0.088
other_1w_mid    wrapper_optbool  42   23.8   11.9   57.1     0.0    7.1  0.088
other_chatter   confirm_optbool  42   31.0    9.5   50.0     2.4    7.1  0.389
other_chatter   none       42   38.1    0.0   52.4     2.4    7.1  0.389
other_chatter   wrapper_optbool  42   28.6    9.5   52.4     2.4    7.1  0.389
other_intent    confirm_optbool  42   33.3   31.0   35.7     0.0    0.0  0.379
other_intent    none       42   42.9    0.0   40.5    14.3    2.4  0.379
other_intent    wrapper_optbool  42   33.3    9.5   40.5    14.3    2.4  0.379
Pre-registered contrasts:
  H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp): +61.9pp  [95% CI +47.6, +76.2]
  clean false-confirm rate @confirm: 0.0%  (must be <= 25%)
  CF on error conditions @confirm: []
P0c (optional-boolean confirmation rule):
  [confirm_optbool] blocked(neg_drop)=0.0%  WA(neg_drop)=97.6%  CF(clean_neg)=0.0%  CF(clean_pos)=0.0%  CF(clean pooled 84)=0.0%  WA(clean_pos)=21.4%
      CF(func_drop)=0.0%  WA=28.6%
      CF(content_sub)=0.0%  WA=95.2%
      CF(other_1w)=2.4%  WA=31.0%
      CF(other_1w_mid)=0.0%  WA=38.1%
      CF(other_intent)=31.0%  WA=33.3%
      => CLOSE (rule: blocked >= 60% and pooled clean CF <= 30%)
  [wrapper_optbool] blocked(neg_drop)=97.6%  WA(neg_drop)=0.0%  CF(clean_neg)=4.8%  CF(clean_pos)=97.6%  CF(clean pooled 84)=51.2%  WA(clean_pos)=2.4%
      CF(func_drop)=11.9%  WA=23.8%
      CF(content_sub)=7.1%  WA=88.1%
      CF(other_1w)=16.7%  WA=19.0%
      CF(other_1w_mid)=11.9%  WA=23.8%
      CF(other_intent)=9.5%  WA=33.3%
      => CLOSE (rule: blocked >= 60% and pooled clean CF <= 30%)

===== colab_out_p0c/Qwen2.5-7B-Instruct-AWQ  (n=1134) =====
condition       gate        n     WA     CF     OK  NOCALL  EXTRA  wer
clean           confirm_optbool  42   21.4    0.0   73.8     0.0    4.8  0.000
clean           none       42   16.7    0.0   78.6     0.0    4.8  0.000
clean           wrapper_optbool  42   14.3    2.4   78.6     0.0    4.8  0.000
clean_pos       confirm_optbool  42   19.0    0.0   73.8     0.0    7.1  0.000
clean_pos       none       42   21.4    0.0   73.8     0.0    4.8  0.000
clean_pos       wrapper_optbool  42    0.0  100.0    0.0     0.0    0.0  0.000
content_sub     confirm_optbool  42   92.9    0.0    4.8     0.0    2.4  0.088
content_sub     none       42   92.9    0.0    4.8     0.0    2.4  0.088
content_sub     wrapper_optbool  42   90.5    2.4    4.8     0.0    2.4  0.088
func_drop       confirm_optbool  42   23.8    0.0   69.0     0.0    7.1  0.088
func_drop       none       42   23.8    0.0   71.4     0.0    4.8  0.088
func_drop       wrapper_optbool  42   19.0    4.8   71.4     0.0    4.8  0.088
neg_drop        confirm_optbool  42   95.2    2.4    2.4     0.0    0.0  0.088
neg_drop        none       42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        wrapper_optbool  42    0.0   97.6    2.4     0.0    0.0  0.088
other_1w        confirm_optbool  42   21.4    7.1   66.7     0.0    4.8  0.088
other_1w        none       42   21.4    0.0   73.8     0.0    4.8  0.088
other_1w        wrapper_optbool  42   11.9    9.5   73.8     0.0    4.8  0.088
other_1w_mid    confirm_optbool  42   28.6    2.4   66.7     0.0    2.4  0.088
other_1w_mid    none       42   31.0    0.0   69.0     0.0    0.0  0.088
other_1w_mid    wrapper_optbool  42   21.4    9.5   69.0     0.0    0.0  0.088
other_chatter   confirm_optbool  42   19.0    4.8   71.4     0.0    4.8  0.389
other_chatter   none       42   19.0    0.0   76.2     0.0    4.8  0.389
other_chatter   wrapper_optbool  42   11.9    7.1   76.2     0.0    4.8  0.389
other_intent    confirm_optbool  42   23.8    7.1   64.3     0.0    4.8  0.379
other_intent    none       42   33.3    0.0   61.9     0.0    4.8  0.379
other_intent    wrapper_optbool  42   28.6    4.8   61.9     0.0    4.8  0.379
Pre-registered contrasts:
  H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp): +73.8pp  [95% CI +59.5, +85.7]
  clean false-confirm rate @confirm: 0.0%  (must be <= 25%)
  CF on error conditions @confirm: []
P0c (optional-boolean confirmation rule):
  [confirm_optbool] blocked(neg_drop)=2.4%  WA(neg_drop)=95.2%  CF(clean_neg)=0.0%  CF(clean_pos)=0.0%  CF(clean pooled 84)=0.0%  WA(clean_pos)=19.0%
      CF(func_drop)=0.0%  WA=23.8%
      CF(content_sub)=0.0%  WA=92.9%
      CF(other_1w)=7.1%  WA=21.4%
      CF(other_1w_mid)=2.4%  WA=28.6%
      CF(other_intent)=7.1%  WA=23.8%
      => CLOSE (rule: blocked >= 60% and pooled clean CF <= 30%)
  [wrapper_optbool] blocked(neg_drop)=97.6%  WA(neg_drop)=0.0%  CF(clean_neg)=2.4%  CF(clean_pos)=100.0%  CF(clean pooled 84)=51.2%  WA(clean_pos)=0.0%
      CF(func_drop)=4.8%  WA=19.0%
      CF(content_sub)=2.4%  WA=90.5%
      CF(other_1w)=9.5%  WA=11.9%
      CF(other_1w_mid)=9.5%  WA=21.4%
      CF(other_intent)=4.8%  WA=28.6%
      => CLOSE (rule: blocked >= 60% and pooled clean CF <= 30%)
```
