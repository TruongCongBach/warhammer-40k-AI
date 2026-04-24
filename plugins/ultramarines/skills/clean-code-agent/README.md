# Clean Code Agent

`clean-code-agent` là skill dùng trong lúc viết hoặc chỉnh sửa code.

## Dùng khi nào

- Khi bắt đầu implement sau khi đã chốt analysis hoặc plan
- Khi cần giữ scope code gọn, dễ đọc, dễ maintain
- Khi muốn ép agent follow clean code, verification, và test discipline

## Không dùng khi nào

- Khi bạn vẫn đang đọc hiểu ticket
- Khi bạn mới ở bước planning hoặc review
- Khi bạn chỉ cần summary/comment chứ chưa code

## Mục tiêu

- Viết code sạch và đúng scope
- Tôn trọng SOLID, GRASP, DDD, CQS, AVR loop
- Verify lại bằng lint, type-check, test khi phù hợp

## Input thường gặp

- Ticket hoặc plan đã được approve
- File/module cần sửa
- Yêu cầu behavior cụ thể cần implement

## Output mong đợi

- Code change sạch và có structure rõ
- Giải thích kỹ thuật ngắn gọn
- Verification steps đã chạy hoặc lý do chưa chạy được

## Prompt ví dụ

```text
Use clean-code-agent while implementing ML-39.
Keep the change scoped, maintainable, and verified.
```
