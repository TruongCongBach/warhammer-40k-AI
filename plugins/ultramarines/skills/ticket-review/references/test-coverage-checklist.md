# Test Coverage Checklist

## Purpose

Use this checklist to assess whether test coverage is sufficient for the implementation.

## Checklist

- Happy path behavior is covered.
- Primary failure path is covered.
- State transitions introduced by the change are covered.
- Validation rules or input handling changes are covered.
- Conditional branches added by the implementation are covered.
- Regression-prone shared components or utilities are covered.
- Tests are aligned with user-visible behavior, not only internal helpers.
- Manual QA is not carrying all risk alone.

## Coverage Guidance

Raise a test coverage gap when:
- the implementation changes user-visible behavior
- the implementation changes branching or state transitions
- the ticket fixes a bug that could regress quietly
- the code introduces complex conditional logic without adequate tests
