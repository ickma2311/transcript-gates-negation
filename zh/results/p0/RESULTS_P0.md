# RESULTS P0 — 2026-09-23（EXPLORATORY；Colab T4；代码 job_bundle_p0_frozen.py；PREREG_P0 sha256 3637272e…）

## 判定：两模型均 NOT GO（H2 成立、H1 与 H3 不成立；确认闸门未"死"，不触发 STOP）→ 按预注册为 INCONCLUSIVE，转 lite 模式

## 严格打分（预注册的打分器；对自由字符串参数过严——见审计）

### Qwen2.5-3B-Instruct
```
model=Qwen/Qwen2.5-3B-Instruct
condition      gate       CORRECT EXTRA_AR  FLIPPED WRONG_AC EXTRA_CA  CONFIRM  NO_CALL PARSE_FA     n
clean          none          64.3      7.1      0.0     28.6      0.0      0.0      0.0      0.0    42
clean          confirm       69.0      7.1      0.0     23.8      0.0      0.0      0.0      0.0    42
clean          spktag        64.3      7.1      0.0     28.6      0.0      0.0      0.0      0.0    42
neg_drop       none           2.4      0.0     69.0     26.2      2.4      0.0      0.0      0.0    42
neg_drop       confirm        2.4      0.0     71.4     23.8      2.4      0.0      0.0      0.0    42
neg_drop       spktag         2.4      0.0     66.7     26.2      4.8      0.0      0.0      0.0    42
func_drop      none          59.5      4.8      0.0     35.7      0.0      0.0      0.0      0.0    42
func_drop      confirm       59.5      4.8      0.0     35.7      0.0      0.0      0.0      0.0    42
func_drop      spktag        61.9      4.8      0.0     33.3      0.0      0.0      0.0      0.0    42
content_sub    none           2.4      2.4      0.0     95.2      0.0      0.0      0.0      0.0    42
content_sub    confirm        2.4      2.4      0.0     95.2      0.0      0.0      0.0      0.0    42
content_sub    spktag         2.4      2.4      0.0     95.2      0.0      0.0      0.0      0.0    42
other_1w       none          59.5      4.8      0.0     28.6      7.1      0.0      0.0      0.0    42
other_1w       confirm       59.5      4.8      0.0     26.2      4.8      4.8      0.0      0.0    42
other_1w       spktag        61.9      4.8      0.0     31.0      2.4      0.0      0.0      0.0    42
other_intent   none          40.5      2.4      0.0     28.6     14.3      0.0     14.3      0.0    42
other_intent   confirm       38.1      0.0      0.0     19.0     11.9     31.0      0.0      0.0    42
other_intent   spktag        47.6      2.4      0.0     23.8     16.7      0.0      9.5      0.0    42
other_chatter  none          52.4      7.1      0.0     31.0      7.1      0.0      2.4      0.0    42
other_chatter  confirm       45.2      7.1      0.0     28.6      2.4     16.7      0.0      0.0    42
other_chatter  spktag        57.1      4.8      0.0     23.8      4.8      0.0      9.5      0.0    42
```

### Qwen2.5-7B-Instruct-AWQ
```
model=Qwen/Qwen2.5-7B-Instruct-AWQ
condition      gate       CORRECT EXTRA_AR  FLIPPED WRONG_AC EXTRA_CA  CONFIRM  NO_CALL PARSE_FA     n
clean          none          78.6      4.8      0.0     16.7      0.0      0.0      0.0      0.0    42
clean          confirm       76.2      4.8      0.0     19.0      0.0      0.0      0.0      0.0    42
clean          spktag        76.2      4.8      0.0     19.0      0.0      0.0      0.0      0.0    42
neg_drop       none           2.4      0.0     78.6     16.7      2.4      0.0      0.0      0.0    42
neg_drop       confirm        2.4      0.0     66.7     19.0      2.4      9.5      0.0      0.0    42
neg_drop       spktag         4.8      0.0     81.0     14.3      0.0      0.0      0.0      0.0    42
func_drop      none          71.4      4.8      0.0     23.8      0.0      0.0      0.0      0.0    42
func_drop      confirm       69.0      7.1      0.0     21.4      0.0      2.4      0.0      0.0    42
func_drop      spktag        73.8      7.1      0.0     19.0      0.0      0.0      0.0      0.0    42
content_sub    none           4.8      2.4      0.0     92.9      0.0      0.0      0.0      0.0    42
content_sub    confirm        4.8      2.4      0.0     92.9      0.0      0.0      0.0      0.0    42
content_sub    spktag         4.8      2.4      0.0     92.9      0.0      0.0      0.0      0.0    42
other_1w       none          73.8      4.8      0.0     21.4      0.0      0.0      0.0      0.0    42
other_1w       confirm       66.7      4.8      0.0     19.0      0.0      9.5      0.0      0.0    42
other_1w       spktag        73.8      4.8      0.0     21.4      0.0      0.0      0.0      0.0    42
other_intent   none          61.9      4.8      0.0     19.0     14.3      0.0      0.0      0.0    42
other_intent   confirm       57.1      0.0      0.0     14.3      7.1     21.4      0.0      0.0    42
other_intent   spktag        73.8      4.8      0.0     21.4      0.0      0.0      0.0      0.0    42
other_chatter  none          76.2      4.8      0.0     19.0      0.0      0.0      0.0      0.0    42
other_chatter  confirm       59.5      2.4      0.0     14.3      0.0     23.8      0.0      0.0    42
other_chatter  spktag        73.8      4.8      0.0     21.4      0.0      0.0      0.0      0.0    42
```

## 宽松重打分（DEVIATION，事后、离线：函数名 + 全部布尔/整数/枚举参数须匹配，自由字符串不计；`rescore.py`）
```

===== colab_out_lenient/Qwen2.5-3B-Instruct  (n=882) =====
condition       gate        n     WA     CF     OK  NOCALL  EXTRA  wer
clean           confirm    42    7.1    0.0   92.9     0.0    0.0  0.000
clean           none       42    7.1    0.0   92.9     0.0    0.0  0.000
clean           spktag     42    7.1    0.0   92.9     0.0    0.0  0.000
content_sub     confirm    42   16.7    0.0   83.3     0.0    0.0  0.088
content_sub     none       42   19.0    0.0   81.0     0.0    0.0  0.088
content_sub     spktag     42   19.0    0.0   81.0     0.0    0.0  0.088
func_drop       confirm    42   14.3    0.0   85.7     0.0    0.0  0.088
func_drop       none       42   14.3    0.0   85.7     0.0    0.0  0.088
func_drop       spktag     42   11.9    0.0   88.1     0.0    0.0  0.088
neg_drop        confirm    42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        none       42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        spktag     42   97.6    0.0    2.4     0.0    0.0  0.088
other_1w        confirm    42   19.0    4.8   76.2     0.0    0.0  0.088
other_1w        none       42   21.4    0.0   78.6     0.0    0.0  0.088
other_1w        spktag     42   14.3    0.0   85.7     0.0    0.0  0.088
other_chatter   confirm    42   11.9   16.7   71.4     0.0    0.0  0.389
other_chatter   none       42   16.7    0.0   81.0     2.4    0.0  0.389
other_chatter   spktag     42   11.9    0.0   78.6     9.5    0.0  0.389
other_intent    confirm    42   19.0   31.0   50.0     0.0    0.0  0.379
other_intent    none       42   28.6    0.0   57.1    14.3    0.0  0.379
other_intent    spktag     42   26.2    0.0   64.3     9.5    0.0  0.379
Pre-registered contrasts:
  H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp): +83.3pp  [95% CI +71.4, +92.9]
  H1  CF(other_1w) - CF(neg_drop) @confirm      (GO needs >= +25pp): +4.8pp  [95% CI +0.0, +11.9]
  H1b CF(other_intent) - CF(neg_drop) @confirm  (secondary): +31.0pp  [95% CI +16.7, +45.2]
  H3  WA(other_intent) none - spktag             (GO needs >= +30pp): +2.4pp  [95% CI -11.9, +16.7]
  H3b WA(clean) spktag - none                    (must be <= +5pp): +0.0pp  [95% CI -7.1, +7.1]
  DiD WA-reduction[other_1w] - WA-reduction[neg_drop] under confirm: +2.4pp [95% CI +0.0, +7.1]
  clean false-confirm rate @confirm: 0.0%  (must be <= 25%)
  CF on error conditions @confirm: [0.0, 0.0, 0.0, 4.8, 31.0, 16.7]
  => NOT GO on this model

===== colab_out_lenient/Qwen2.5-7B-Instruct-AWQ  (n=882) =====
condition       gate        n     WA     CF     OK  NOCALL  EXTRA  wer
clean           confirm    42    0.0    0.0  100.0     0.0    0.0  0.000
clean           none       42    2.4    0.0   97.6     0.0    0.0  0.000
clean           spktag     42    4.8    0.0   95.2     0.0    0.0  0.000
content_sub     confirm    42    9.5    0.0   90.5     0.0    0.0  0.088
content_sub     none       42    9.5    0.0   90.5     0.0    0.0  0.088
content_sub     spktag     42   11.9    0.0   88.1     0.0    0.0  0.088
func_drop       confirm    42    0.0    2.4   97.6     0.0    0.0  0.088
func_drop       none       42    4.8    0.0   95.2     0.0    0.0  0.088
func_drop       spktag     42    2.4    0.0   97.6     0.0    0.0  0.088
neg_drop        confirm    42   88.1    9.5    2.4     0.0    0.0  0.088
neg_drop        none       42   97.6    0.0    2.4     0.0    0.0  0.088
neg_drop        spktag     42   95.2    0.0    4.8     0.0    0.0  0.088
other_1w        confirm    42    7.1    9.5   83.3     0.0    0.0  0.088
other_1w        none       42    9.5    0.0   90.5     0.0    0.0  0.088
other_1w        spktag     42    9.5    0.0   90.5     0.0    0.0  0.088
other_chatter   confirm    42    7.1   23.8   69.0     0.0    0.0  0.389
other_chatter   none       42    7.1    0.0   92.9     0.0    0.0  0.389
other_chatter   spktag     42    9.5    0.0   90.5     0.0    0.0  0.389
other_intent    confirm    42   11.9   21.4   66.7     0.0    0.0  0.379
other_intent    none       42   21.4    0.0   78.6     0.0    0.0  0.379
other_intent    spktag     42    9.5    0.0   90.5     0.0    0.0  0.379
Pre-registered contrasts:
  H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp): +92.9pp  [95% CI +85.7, +100.0]
  H1  CF(other_1w) - CF(neg_drop) @confirm      (GO needs >= +25pp): +0.0pp  [95% CI -11.9, +11.9]
  H1b CF(other_intent) - CF(neg_drop) @confirm  (secondary): +11.9pp  [95% CI +0.0, +23.8]
  H3  WA(other_intent) none - spktag             (GO needs >= +30pp): +11.9pp  [95% CI +0.0, +23.8]
  H3b WA(clean) spktag - none                    (must be <= +5pp): +2.4pp  [95% CI -4.8, +9.5]
  DiD WA-reduction[other_1w] - WA-reduction[neg_drop] under confirm: -7.1pp [95% CI -16.7, +2.4]
  clean false-confirm rate @confirm: 0.0%  (must be <= 25%)
  CF on error conditions @confirm: [9.5, 2.4, 0.0, 9.5, 21.4, 23.8]
  => NOT GO on this model
```

## 严格打分下的预注册对比
```
Pre-registered contrasts:
  H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp): +61.9pp  [95% CI +47.6, +76.2]
  H1  CF(other_1w) - CF(neg_drop) @confirm      (GO needs >= +25pp): +4.8pp  [95% CI +0.0, +11.9]
  H1b CF(other_intent) - CF(neg_drop) @confirm  (secondary): +31.0pp  [95% CI +16.7, +45.2]
  H3  WA(other_intent) none - spktag             (GO needs >= +30pp): +2.4pp  [95% CI -9.5, +14.3]
  H3b WA(clean) spktag - none                    (must be <= +5pp): +0.0pp  [95% CI -7.1, +7.1]
  DiD WA-reduction[other_1w] - WA-reduction[neg_drop] under confirm: +4.8pp [95% CI +0.0, +11.9]
  clean false-confirm rate @confirm: 0.0%  (must be <= 25%)
  CF on error conditions @confirm: [0.0, 0.0, 0.0, 4.8, 31.0, 16.7]
  => NOT GO on this model

===== colab_out/Qwen2.5-7B-Instruct-AWQ  (n=882) =====
--
Pre-registered contrasts:
  H2  WA(neg_drop) - WA(func_drop) @none        (GO needs >= +40pp): +73.8pp  [95% CI +59.5, +85.7]
  H1  CF(other_1w) - CF(neg_drop) @confirm      (GO needs >= +25pp): +0.0pp  [95% CI -11.9, +11.9]
  H1b CF(other_intent) - CF(neg_drop) @confirm  (secondary): +11.9pp  [95% CI +0.0, +23.8]
  H3  WA(other_intent) none - spktag             (GO needs >= +30pp): +11.9pp  [95% CI +0.0, +23.8]
  H3b WA(clean) spktag - none                    (must be <= +5pp): +2.4pp  [95% CI +0.0, +7.1]
  DiD WA-reduction[other_1w] - WA-reduction[neg_drop] under confirm: -7.1pp [95% CI -19.0, +4.8]
  clean false-confirm rate @confirm: 0.0%  (must be <= 25%)
  CF on error conditions @confirm: [9.5, 2.4, 0.0, 9.5, 21.4, 23.8]
  => NOT GO on this model
```

## 打分器审计（clean/none 被判 WRONG 的原始输出）
```
clean/none WRONG_ACTION+EXTRA_ARG: 15
- th1 [EXTRA_ARG] gold={"set_thermostat": {"temperature_f": 72, "eco": false}}
    raw='<tool_call>\n{"name": "set_thermostat", "arguments": {"temperature_f": 72, "mode": "heat", "eco": false}}\n</tool_call>'
- em1 [WRONG_ACTION] gold={"send_email": {"to": "sarah", "subject": "report is ready", "cc_manager": false}}
    raw='<tool_call>\n{"name": "send_email", "arguments": {"to": "sarah", "subject": "Report Ready", "body": "The report you requested is now ready.", "cc_manager": false, "mark_urgent": false}}\n</tool_call>'
- em2 [EXTRA_ARG] gold={"send_email": {"to": "tom", "subject": "meeting moved to friday", "mark_urgent": false}}
    raw='<tool_call>\n{"name": "send_email", "arguments": {"to": "tom", "subject": "Meeting Moved to Friday", "body": "The meeting has been moved to Friday. Please let me know if you have any conflicts.", "mark_urgent": false}}\n</'
- em3 [EXTRA_ARG] gold={"send_email": {"to": "vendor", "subject": "invoice", "cc_manager": false}}
    raw='<tool_call>\n{"name": "send_email", "arguments": {"to": "vendor@example.com", "subject": "Invoice Inquiry", "body": "Dear Vendor, please find attached the invoice for your recent order. We look forward to your prompt paym'
- me2 [WRONG_ACTION] gold={"schedule_meeting": {"title": "design sync", "time": "3", "send_reminder": false}}
    raw='<tool_call>\n{"name": "set_reminder", "arguments": {"text": "Design sync at 3pm", "time": "15:00", "repeat_daily": false}}\n</tool_call>'
- me3 [WRONG_ACTION] gold={"schedule_meeting": {"title": "one on one with priya", "time": "monday at 9", "video_call": false}}
    raw='<tool_call>\n{"name": "schedule_meeting", "arguments": {"title": "One on one with Priya", "time": "Monday at 09:00", "invite_team": false, "send_reminder": false, "video_call": false}}\n</tool_call>'
- ce1 [WRONG_ACTION] gold={"cancel_event": {"event": "4 o'clock standup", "notify_attendees": false}}
    raw='<tool_call>\n{"name": "cancel_event", "arguments": {"event": "four o\'clock standup", "notify_attendees": false}}\n</tool_call>'
- ce2 [WRONG_ACTION] gold={"cancel_event": {"event": "tomorrow's dentist appointment", "notify_attendees": false}}
    raw='<tool_call>\n{"name": "cancel_event", "arguments": {"event": "dentist appointment tomorrow", "notify_attendees": false}}\n</tool_call>'
- co1 [WRONG_ACTION] gold={"cancel_order": {"order_id": "AB123", "refund_to_card": false}}
    raw='<tool_call>\n{"name": "cancel_order", "arguments": {"order_id": "a b one two three", "refund_to_card": false}}\n</tool_call>'
- cp1 [WRONG_ACTION] gold={"close_project": {"project_id": "DA12", "archive": false}}
    raw='<tool_call>\n{"name": "close_project", "arguments": {"project_id": "alpha-project-d-a-twelve", "archive": false, "notify_team": false}}\n</tool_call>'
- df2 [WRONG_ACTION] gold={"delete_files": {"folder": "temp", "keep_backup": false}}
    raw='<tool_call>\n{"name": "delete_files", "arguments": {"folder": "temp", "include_subfolders": true, "keep_backup": false}}\n</tool_call>'
- bf1 [WRONG_ACTION] gold={"book_flight": {"destination": "denver", "date": "the 12th", "refundable": false}}
    raw='<tool_call>\n{"name": "book_flight", "arguments": {"destination": "denver", "date": "twelfth", "refundable": false, "window_seat": false}}\n</tool_call>'
- pm1 [WRONG_ACTION] gold={"play_music": {"query": "taylor swift", "shuffle": false}}
    raw='<tool_call>\n{"name": "play_music", "arguments": {"query": "Taylor Swift", "shuffle": false, "explicit_allowed": true}}\n</tool_call>'
- pm2 [WRONG_ACTION] gold={"play_music": {"query": "workout playlist", "explicit_allowed": false}}
    raw='<tool_call>\n{"name": "play_music", "arguments": {"query": "The Kids Are Alright", "shuffle": false, "explicit_allowed": false}}\n</tool_call>'
- re1 [WRONG_ACTION] gold={"set_reminder": {"text": "call the bank", "time": "2", "repeat_daily": false}}
    raw='<tool_call>\n{"name": "set_reminder", "arguments": {"text": "call the bank", "time": "14:00", "repeat_daily": false}}\n</tool_call>'

Sample CONFIRM replies:
clean/none WRONG_ACTION+EXTRA_ARG: 9
- em1 [EXTRA_ARG] gold={"send_email": {"to": "sarah", "subject": "report is ready", "cc_manager": false}}
    raw='<tool_call>\n{"name": "send_email", "arguments": {"to": "sarah", "subject": "Report is ready", "body": "The report you requested is now available.", "cc_manager": false}}\n</tool_call>'
- em2 [WRONG_ACTION] gold={"send_email": {"to": "tom", "subject": "meeting moved to friday", "mark_urgent": false}}
    raw='<tool_call>\n{"name": "send_email", "arguments": {"to": "tom", "subject": "Meeting rescheduled", "body": "The meeting has been moved to Friday."}}\n</tool_call>'
- em3 [EXTRA_ARG] gold={"send_email": {"to": "vendor", "subject": "invoice", "cc_manager": false}}
    raw='<tool_call>\n{"name": "send_email", "arguments": {"to": "vendor_email@example.com", "subject": "Inquiry about Invoice", "body": "Hello,\\n\\nI hope this message finds you well. I am writing to inquire about the invoice deta'
- me1 [WRONG_ACTION] gold={"schedule_meeting": {"title": "budget review", "time": "tomorrow at 10", "invite_team": false}}
    raw='<tool_call>\n{"name": "schedule_meeting", "arguments": {"title": "Budget Review", "time": "tomorrow at ten", "invite_team": false}}\n</tool_call>'
- me2 [WRONG_ACTION] gold={"schedule_meeting": {"title": "design sync", "time": "3", "send_reminder": false}}
    raw='<tool_call>\n{"name": "schedule_meeting", "arguments": {"title": "Design sync", "time": "three", "invite_team": false, "send_reminder": false, "video_call": false}}\n</tool_call>'
- ce1 [WRONG_ACTION] gold={"cancel_event": {"event": "4 o'clock standup", "notify_attendees": false}}
    raw='<tool_call>\n{"name": "cancel_event", "arguments": {"event": "four o\'clock standup", "notify_attendees": false}}\n</tool_call>'
- ce2 [WRONG_ACTION] gold={"cancel_event": {"event": "tomorrow's dentist appointment", "notify_attendees": false}}
    raw='<tool_call>\n{"name": "cancel_event", "arguments": {"event": "dentist appointment tomorrow", "notify_attendees": false}}\n</tool_call>'
- co1 [WRONG_ACTION] gold={"cancel_order": {"order_id": "AB123", "refund_to_card": false}}
    raw='<tool_call>\n{"name": "cancel_order", "arguments": {"order_id": "a b one two three", "refund_to_card": false}}\n</tool_call>'
- cp1 [WRONG_ACTION] gold={"close_project": {"project_id": "DA12", "archive": false}}
    raw='<tool_call>\n{"name": "close_project", "arguments": {"project_id": "alpha", "archive": false, "notify_team": true}}\n</tool_call>'

Sample CONFIRM replies:
```

## 7B 在 neg_drop 下的 4 次 CONFIRM（问的恰好是被翻转的那个参数）
```
- em3 CONFIRM: Did you mean to send an email to the vendor about the invoice and also carbon copy your manager?
- al2 CONFIRM: Did you say you want sound or vibrate only mode?
- pm2 CONFIRM: Do you want to allow explicit tracks?
- ri2 CONFIRM: Did you say "order a car from home to the station and add a child seat"?
```
