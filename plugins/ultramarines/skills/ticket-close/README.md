# Ticket Close

`ticket-close` là skill cuối workflow, dùng để viết nội dung đóng ticket sau khi work đã được approve.

## Dùng khi nào

- Khi cần final Jira comment
- Khi cần QA closure note
- Khi muốn ticket history có closure summary ngắn gọn, dễ scan
- Khi cần giữ lại một security note ngắn gọn trong closure nếu change ảnh hưởng flow nhạy cảm

## Không dùng khi nào

- Khi implementation chưa được approve
- Khi bạn vẫn cần review code hoặc summary kỹ thuật sâu
- Khi mục tiêu là code hoặc commit

## Mục tiêu

- Viết final ticket comment gọn, rõ, professional
- Viết QA handoff note rõ cần verify gì
- Giữ lại security note nếu QA hoặc future readers cần biết
- Ghi lại closure summary cho future readers

## Input thường gặp

- Jira ticket
- Approved change summary
- QA validation notes
- Review outcome

## Output mong đợi

- Final ticket comment
- QA handoff note
- What was fixed
- What QA should verify
- Security note if relevant
- Short closure summary

## Prompt ví dụ

```text
Use ticket-close for ML-39.
Draft the final Jira closure comment, QA handoff note, and short closure summary.
```
