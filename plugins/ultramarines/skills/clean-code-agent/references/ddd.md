# Domain-Driven Design — Detailed Reference

Read this when you need to apply DDD concepts in depth — designing bounded contexts, modeling aggregates, or structuring a domain layer.

## Table of Contents
1. Strategic Design
2. Tactical Design
3. Pitfalls to Avoid

---

## 1. Strategic Design

### Domain & Subdomains

The entire business is the **Domain** (problem space). It breaks down into:

- **Core Domain**: Where the business creates competitive advantage. Invest the best engineers and most effort here.
- **Supporting Subdomain**: Important but not the differentiator. Custom-built but simpler.
- **Generic Subdomain**: Common functionality (billing, auth, email). Use off-the-shelf solutions when possible.

### Ubiquitous Language

A strict, shared language between developers and domain experts. Every term has one meaning within a Bounded Context. This language must appear directly in code — class names, method names, variable names.

Why it matters: When code uses different words than the business, translation errors accumulate. The code drifts from reality and becomes harder to maintain.

### Bounded Context

A boundary within which a model and its language have a specific, unambiguous meaning. Different contexts can use the same word to mean different things (e.g., "Account" in Banking vs. Marketing).

Key rule: Don't try to build one unified model for the entire business. It doesn't work. Instead, define clear boundaries and translate at the edges.

### Context Map — Integration Patterns

How Bounded Contexts relate to each other:

| Pattern | When to use |
|---------|------------|
| **Partnership** | Two teams share goals and succeed/fail together |
| **Shared Kernel** | Two contexts share a small, co-owned piece of the model |
| **Customer/Supplier** | Downstream team depends on upstream team's output |
| **Conformist** | Downstream team fully adopts upstream's model (simplifies integration) |
| **Anticorruption Layer (ACL)** | Protect your model from external/legacy systems with a translation layer |
| **Open Host Service + Published Language** | Expose your system via standardized services/APIs for multiple consumers |

---

## 2. Tactical Design (Building Blocks)

### Entities
- Defined by **identity**, not attributes
- Identity persists across time and state changes
- Two entities with identical attributes but different IDs are different objects
- State is mutable

### Value Objects
- Defined by **attributes**, not identity
- **Immutable** — when a value changes, create a new object
- Two Value Objects with the same attributes are equal
- Prefer Value Objects over Entities when possible — they reduce complexity

### Aggregates
- A cluster of Entities and Value Objects treated as one unit
- Has exactly one **Aggregate Root** — the single entry point for modifications
- Design rules:
  - Keep Aggregates small
  - Reference other Aggregates by ID, not by direct object reference
  - One transaction = one Aggregate modification
  - Use **Eventual Consistency** for cross-Aggregate changes

### Repositories
- Abstract interface for finding and persisting Aggregate Roots
- Hide database details from the domain layer
- One Repository per Aggregate Root

### Domain Services
- For operations that span multiple objects but don't belong to any single Entity
- Stateless
- Named using Ubiquitous Language

### Domain Events
- Record something important that happened: "OrderPlaced", "PaymentReceived"
- Published for other parts of the system to react to
- Enable loose coupling and eventual consistency between Aggregates/Contexts
- Name in past tense: the event already happened

### Factories
- Encapsulate complex object creation logic
- Keep the client from needing to know internal structure

---

## 3. Pitfalls to Avoid

1. **Over-focusing on technical patterns** before understanding the business domain
2. **Over-engineering** — creating too many layers for simple concepts
3. **Ignoring Ubiquitous Language** — using tech jargon instead of business terms
4. **Misunderstanding Bounded Context** — sharing one Entity (e.g., Customer) across multiple contexts
5. **Neglecting Core Domain** — spending equal effort on Generic Subdomains
6. **Overusing Entities** when Value Objects would be simpler and safer
7. **Breaking Aggregate boundaries** — letting multiple services modify the same object
8. **Overusing Domain Events** — creating noise that degrades performance
9. **Skipping collaboration with domain experts** — code won't reflect real business rules
10. **Treating DDD as a silver bullet** — DDD is expensive; use it for complex Core Domains, not simple CRUD
