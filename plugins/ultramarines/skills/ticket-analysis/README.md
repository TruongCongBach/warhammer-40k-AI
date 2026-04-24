# Ticket Analysis

`ticket-analysis` là skill đầu tiên nên dùng khi vừa nhận ticket.

## Dùng khi nào

- Khi cần đọc Jira ticket trước khi code
- Khi cần làm rõ expected vs actual behavior
- Khi có screenshot, HAR, Charles, zip log cần triage
- Khi cần quyết định ticket đã đủ rõ để implement chưa
- Khi cần phát hiện sớm security-sensitive impact như auth, permission, token, PII, storage, logging, upload, deep link, WebView

## Không dùng khi nào

- Khi bạn đã hiểu rõ ticket và đang chọn hướng implement
- Khi bạn đã bắt đầu code
- Khi bạn cần review implementation hoặc commit

## Mục tiêu

- Hiểu đúng vấn đề
- Chỉ ra thông tin còn thiếu hoặc ambiguity
- Tóm tắt business impact, expected behavior, actual behavior
- Kết luận `ready to implement` hoặc `not yet ready`
- Gắn cờ `needs security review` nếu có rủi ro bảo mật đáng kể nhưng chưa đủ dữ kiện

## Input thường gặp

- Jira ticket
- Ticket comments
- Screenshot/design image
- HAR, Charles, zip logs
- Design-context Markdown từ `python3 scripts/extract_design_context.py ...` nếu ảnh quan trọng

## Output mong đợi

- Ticket summary
- Problem statement
- Expected vs actual behavior
- Missing information
- Security considerations
- Root-cause hypotheses
- Recommendation: ready / not ready

## Hỗ trợ ảnh design

- Không cần cài thêm skill riêng trên máy khác cho phần này
- Chỉ cần repo skill hiện tại và tool parser tùy chọn
- Ưu tiên parse ảnh bằng `python3 scripts/extract_design_context.py path/to/image.png --include-raw`
- Primary engine: OmniParser nếu máy có `OMNIPARSER_URL` hoặc `OMNIPARSER_CMD`
- Fallback engine: MarkItDown nếu chỉ cần OCR/Markdown
- Output của script là Markdown note để agent đọc tốt hơn, không thay thế design spec thật

## Prompt ví dụ

```text
Use ticket-analysis for Jira ticket ML-39.
Read the ticket first, summarize the issue, identify missing information, and tell me whether this is ready for implementation.
```
