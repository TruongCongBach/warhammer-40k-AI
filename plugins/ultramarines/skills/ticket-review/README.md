# Ticket Review

`ticket-review` dùng sau khi code đã được viết xong và cần so lại với ticket.

## Dùng khi nào

- Khi implementation đã có và cần review trước khi approve
- Khi cần so với Jira ticket, acceptance criteria, screenshot/design reference
- Khi cần check UX quality, missing states, test gaps, maintainability
- Khi cần review thêm các rủi ro security ở các flow nhạy cảm

## Không dùng khi nào

- Khi vẫn đang ở bước planning
- Khi chưa có code để review
- Khi mục tiêu là commit hoặc đóng ticket

## Mục tiêu

- Kiểm tra implementation có khớp ticket không
- Chỉ ra phần đúng, phần thiếu, phần mismatch
- Nêu missing states, UX risks, code quality concerns, test gaps
- Nêu security findings nếu auth, permission, token, storage, logging, upload, deep link, WebView, trust boundary bị ảnh hưởng
- Kết luận `ready` hoặc `needs revision`

## Input thường gặp

- Jira ticket
- Changed files / diff
- Screenshot/design image
- Existing analysis/planning context
- Design-context Markdown từ `python3 scripts/extract_design_context.py ...` nếu review phụ thuộc screenshot/design image

## Output mong đợi

- What appears correctly implemented
- What appears incomplete
- Missing states
- UX risks
- Security findings
- Required changes
- Suggested correction order
- Final QA checklist

## Hỗ trợ ảnh design

- Không cần cài thêm skill riêng trên máy khác cho phần này
- Nếu review phụ thuộc ảnh, ưu tiên parse ảnh thành design-context Markdown trước
- Lệnh chuẩn:

```bash
python3 scripts/extract_design_context.py path/to/image.png --include-raw
```

- Primary engine: OmniParser
- Fallback engine: MarkItDown

## Prompt ví dụ

```text
Use ticket-review for ML-39.
Review the implementation against the ticket and tell me what still needs revision before approval.
```
