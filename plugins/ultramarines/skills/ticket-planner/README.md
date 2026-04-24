# Ticket Planner

`ticket-planner` dùng sau `ticket-analysis`, trước khi bắt đầu code.

## Dùng khi nào

- Khi ticket đã đủ rõ và bạn cần chọn hướng implement
- Khi cần compare 1-2 hướng fix hoặc feature approach
- Khi cần affected areas, risks, edge cases, test plan trước khi code
- Khi cần chốt security mitigations trước khi implement ở các luồng nhạy cảm

## Không dùng khi nào

- Khi ticket còn mơ hồ, chưa rõ vấn đề
- Khi bạn đã quyết định plan và đang bước vào implement
- Khi bạn chỉ cần review code đã viết

## Mục tiêu

- Chuyển kết quả analysis thành plan thực thi
- Đề xuất approach A/B nếu cần
- Chỉ ra module/file/area có khả năng bị ảnh hưởng
- Nêu risks, tradeoffs, state handling, API dependencies
- Nêu security risks và mitigation nếu ticket đụng auth, permission, token, storage, logging, upload, deep link, WebView

## Input thường gặp

- Output từ `ticket-analysis`
- Jira ticket
- Screenshot/log bổ sung nếu ảnh hưởng tới plan
- Design-context Markdown từ `python3 scripts/extract_design_context.py ...` nếu plan phụ thuộc screenshot/design image

## Output mong đợi

- Proposed approach A
- Proposed approach B nếu relevant
- Recommended approach
- Affected areas
- Risks / tradeoffs
- Security risks / mitigations
- Suggested tests
- Recommendation: proceed / needs clarification first / needs security review

## Hỗ trợ ảnh design

- Không cần cài thêm skill riêng trên máy khác cho phần này
- Nếu hướng implement phụ thuộc ảnh, ưu tiên dùng design-context Markdown đã parse từ ảnh
- Lệnh chuẩn:

```bash
python3 scripts/extract_design_context.py path/to/image.png --include-raw
```

- Primary engine: OmniParser
- Fallback engine: MarkItDown

## Prompt ví dụ

```text
Use ticket-planner for Jira ticket ML-39.
Based on the analysis, propose the implementation approach, affected areas, risks, and suggested tests before coding.
```
