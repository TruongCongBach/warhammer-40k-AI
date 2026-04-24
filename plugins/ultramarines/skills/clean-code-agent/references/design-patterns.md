# Design Patterns — When to Use Guide

Read this when you're considering applying a design pattern. The goal is to solve a real problem — not to use patterns for their own sake.

## Golden Rule
Apply a pattern when you recognize the problem it solves in your current code. If you can't name the specific problem, you probably don't need the pattern.

---

## Creational Patterns

| Pattern | Use When |
|---------|----------|
| **Factory Method** | You need to create objects without specifying exact classes. The creation logic varies based on context or configuration. |
| **Abstract Factory** | You need to create families of related objects that must be used together (e.g., UI components for different themes). |
| **Builder** | Object construction is complex with many optional parameters. Avoids telescoping constructors. |
| **Prototype** | Creating a new object is expensive; cloning an existing one is cheaper. |
| **Singleton** | Exactly one instance must exist system-wide (use sparingly — often a design smell). |

## Structural Patterns

| Pattern | Use When |
|---------|----------|
| **Adapter** | You need to make an existing class work with an interface it wasn't designed for. Common when integrating external libraries. |
| **Bridge** | You want to separate an abstraction from its implementation so both can evolve independently. |
| **Composite** | You need to treat individual objects and compositions uniformly (e.g., file/folder trees, UI component trees). |
| **Decorator** | You need to add behavior to objects dynamically without modifying their class. |
| **Facade** | You want to provide a simple interface to a complex subsystem. |
| **Proxy** | You need to control access to an object (lazy loading, access control, logging). |

## Behavioral Patterns

| Pattern | Use When |
|---------|----------|
| **Strategy** | You have multiple algorithms/behaviors for the same task and need to swap them at runtime. Replaces if/else chains on type. |
| **Observer** | Objects need to react to changes in another object without tight coupling. Event-driven communication. |
| **Command** | You need to encapsulate a request as an object — for queuing, undo/redo, or logging operations. |
| **State** | An object's behavior changes based on its internal state. Cleaner than state-dependent if/else blocks. |
| **Template Method** | You have an algorithm with fixed steps but some steps need to vary in subclasses. |
| **Chain of Responsibility** | A request should be handled by one of several handlers, but you don't know which one in advance. |
| **Mediator** | Multiple objects interact in complex ways. A central mediator simplifies the communication. |
| **Iterator** | You need to traverse a collection without exposing its internal structure. |
| **Visitor** | You need to add operations to a class hierarchy without modifying the classes. |
| **Memento** | You need to save and restore an object's state (undo functionality). |

---

## Anti-Patterns to Avoid

- **Pattern for the sake of pattern**: If the code is simple and clear without a pattern, leave it alone.
- **Premature abstraction**: Don't create a Factory for one class. Wait until you have 2-3 concrete cases.
- **Singleton abuse**: Global mutable state makes testing and reasoning hard. Prefer dependency injection.
- **Deep inheritance for code reuse**: Use composition instead. Inheritance is for "is-a" relationships, not code sharing.
- **Over-decorated**: Stacking too many decorators makes the code unreadable. Consider if a simpler approach works.
