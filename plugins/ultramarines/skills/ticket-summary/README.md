# Ticket Summary

`ticket-summary` dùng sau khi implementation đã ổn để viết summary kỹ thuật cho QA và future engineers.

## Dùng khi nào

- Khi cần giải thích root cause và fix approach cho người đọc sau
- Khi cần handoff summary cho QA hoặc engineers
- Khi muốn ghi lại change mà không bắt người khác đọc toàn bộ diff
- Khi cần giữ lại security note ngắn gọn cho QA hoặc future engineers nếu change có liên quan

## Không dùng khi nào

- Khi code chưa ổn định
- Khi bạn vẫn cần review implementation
- Khi mục tiêu chính là final Jira closure comment

## Mục tiêu

- Giải thích cause, change, impact
- Tóm tắt what changed và affected areas
- Nêu regression risks và QA focus
- Giữ lại security note nếu nó ảnh hưởng tới verify, rollback, hoặc future debugging
- Tạo short summary cho ticket history và engineering readers

## Input thường gặp

- Jira ticket
- Implementation summary
- Diff summary
- Review findings

## Output mong đợi

- Root cause
- Fix approach
- What changed
- Affected areas
- Regression risks
- Security note if relevant
- QA focus areas
- Short summaries

## Prompt ví dụ

```text
Use ticket-summary for ML-39.
Summarize the root cause, fix approach, affected areas, regression risks, and QA focus for future engineers and QA.
```
