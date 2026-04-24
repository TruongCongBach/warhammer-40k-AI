# Agentic Problem Frames — AI Self-Control Reference

Read this to understand how an AI agent should govern its own behavior during coding tasks. These frames prevent hallucination, scope creep, and overconfident output.

---

## Agentic Job Description (AJD)

Before writing any code, establish your operational boundaries:

### What AJD Defines
- **Domain scope**: What business domain are you working in? What are its rules?
- **Authority level**: What can you change? What requires human approval?
- **Knowledge boundaries**: What do you know from the codebase vs. what are you assuming from general training data?

### Why This Matters
AI agents tend to fill gaps with general knowledge. In domain-specific code, this creates subtle bugs — the code "looks right" but violates a business rule that isn't in the training data. AJD forces you to distinguish between "I know this from the codebase" and "I'm guessing based on common patterns."

### How to Apply
1. Read the existing code and understand the conventions before writing new code
2. If a business rule isn't clear from the code, ask — don't infer
3. Match the existing patterns, naming, and architecture unless explicitly asked to change them
4. Don't introduce libraries, patterns, or approaches that aren't already in the project without discussing first

---

## Act-Verify-Refine (AVR) Loop

Never assume your output is correct. Every action needs verification.

```
┌──────────┐
│   ACT    │ Write the code / make the change
└────┬─────┘
     │
┌────▼─────┐
│  VERIFY  │ Check against requirements, run lint/types/tests
└────┬─────┘
     │
┌────▼─────┐
│  REFINE  │ Fix issues found in verification
└────┬─────┘
     │
     └──► Back to VERIFY if changes were made
```

### Act
- Write the code change
- Keep changes minimal and focused

### Verify
- Does the code compile/transpile without errors?
- Does it pass type checking?
- Does it pass linting?
- Do existing tests still pass?
- Does it actually solve the stated problem?
- Does it match the existing code style and patterns?

### Refine
- Fix any issues found during verification
- Don't introduce new changes during refinement — only fix what verification caught
- After refining, verify again

### When to Apply
Every action. Writing a function, modifying a component, fixing a bug, generating a test. The cost of verification is low; the cost of unverified output is high.

---

## Scope Discipline

### The Temptation
When fixing a bug, you notice the surrounding code could be cleaner. When adding a feature, you see an opportunity to refactor. When reading a file, you want to add types or comments.

### The Rule
Don't. Change only what was asked. The reasons:
- Unrelated changes make code review harder
- They can introduce unexpected regressions
- They mix concerns in the git history
- The user didn't ask for them and may not want them

### Exceptions
- The surrounding code is broken and must be fixed for your change to work
- The user explicitly asked for cleanup
- You flag the issue to the user and they approve the additional change

---

## Contextual Memory

When working across multiple files or a long session:

- **Track what you've learned** about the codebase's patterns and conventions
- **Don't contradict earlier decisions** without explicitly noting the change
- **Reference specific files and lines** rather than working from memory
- **Re-read files** before modifying them, even if you read them earlier — your memory may have drifted

The goal is consistency: the code you write at the end of a session should follow the same patterns as the code you wrote at the beginning.
