# Ticket Commit

`ticket-commit` dùng khi implementation đã ổn và bạn muốn tạo một commit sạch theo đúng scope của Jira issue.

## Dùng khi nào

- Khi nhiều file đang changed nhưng chỉ một phần thuộc current issue
- Khi bạn muốn tránh commit nhầm file không liên quan
- Khi cần generate commit title chuẩn `type: TICKET-ID | summary`

## Không dùng khi nào

- Khi bạn vẫn đang code dở
- Khi implementation chưa được review hoặc chưa đủ tự tin
- Khi bạn muốn commit toàn bộ worktree mà không cần scope control

## Mục tiêu

- Review changed files một cách conservative
- Chia file thành:
  - recommended for commit
  - excluded or needs review
- Stage đúng file liên quan
- Commit bằng message chuẩn

## Input thường gặp

- Jira ticket
- `git status --short`
- Current diff
- Approved implementation/review context

## Output mong đợi

- Changed files detected
- Files recommended for commit
- Files excluded or needing review
- Suggested commit title
- Final recommendation: safe to commit / review needed

## Prompt ví dụ

```text
Use ticket-commit for Jira ticket ML-39.
Inspect the current git changes, recommend only the files that clearly belong to this issue, and prepare a safe commit.
```
