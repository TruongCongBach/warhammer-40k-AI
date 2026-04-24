# SOLID & GRASP — Detailed Reference

Read this when you need to diagnose a design violation or justify a refactoring decision.

## Table of Contents
1. SOLID Principles (with violations and fixes)
2. GRASP Principles
3. Complementary Principles

---

## 1. SOLID Principles

### SRP — Single Responsibility Principle

**Rule**: A class should have only one reason to change.

**Violation**:
```
class User {
  username, password
  saveUser() { /* writes to DB */ }
  authenticateUser() { /* checks credentials */ }
}
```
This class changes when user data changes, when DB schema changes, AND when auth logic changes.

**Fix**: Split into `User` (data), `UserRepository` (persistence), `AuthService` (authentication).

### OCP — Open/Closed Principle

**Rule**: Open for extension, closed for modification.

**Violation**:
```
calculateDiscount(customerType) {
  if (customerType === "Regular") return 0.1
  if (customerType === "Premium") return 0.2
  // Adding VIP requires modifying this function
}
```

**Fix**: Define a `DiscountStrategy` interface. Each customer type implements its own strategy. Adding VIP = adding a new class, not modifying existing code.

### LSP — Liskov Substitution Principle

**Rule**: Subtypes must be substitutable for their base types without breaking correctness.

**Violation**: `Square extends Rectangle` — setting width on a Square also changes height, breaking Rectangle's expected behavior.

**Fix**: Redesign the hierarchy. Use a common `Shape` interface instead of forcing an is-a relationship that doesn't hold.

### ISP — Interface Segregation Principle

**Rule**: Don't force clients to depend on methods they don't use.

**Violation**: `IMachine { print(), scan(), fax() }` — a simple Printer must implement `scan()` and `fax()` even though it can't do them.

**Fix**: Split into `IPrinter`, `IScanner`, `IFax`. A MultiFunctionMachine implements all three; a Printer implements only `IPrinter`.

### DIP — Dependency Inversion Principle

**Rule**: High-level modules depend on abstractions, not on low-level modules.

**Violation**: `PasswordReminder` directly instantiates `MySQLConnection`.

**Fix**: Create `DBConnectionInterface`. `PasswordReminder` depends on the interface. `MySQLConnection` implements it. Swap databases without touching business logic.

---

## 2. GRASP Principles

### Information Expert
Assign responsibility to the class that has the information needed to fulfill it. If `Order` has line items, `Order` should calculate its own total — not an external `OrderCalculator`.

### Creator
Class B should create instances of class A when B contains/aggregates A, B closely uses A, or B has the initialization data for A.

### Controller
Assign system event handling to a dedicated controller class — not to UI elements. The controller coordinates but doesn't contain business logic.

### Low Coupling
Minimize dependencies between classes. When class A changes, class B should not need to change. Achieve through interfaces, dependency injection, and event-driven communication.

### High Cohesion
All methods in a class should be related to a single, focused purpose. If a class has methods that serve different concerns, it has low cohesion — split it.

### Polymorphism
Handle type-based variations through polymorphic interfaces, not conditional logic. Instead of `if (type === "A") doA(); else if (type === "B") doB();`, define an interface and let each type implement its own behavior.

### Pure Fabrication
When assigning responsibility to a domain class would reduce cohesion, create an artificial helper class (e.g., `ConfigurationManager`, `EventDispatcher`) that doesn't exist in the domain model but serves a technical purpose.

### Indirection
Introduce an intermediate object to decouple two classes. Patterns like Adapter, Facade, and Mediator are specializations of this principle.

### Protected Variations
Wrap unstable points behind stable interfaces. When something is likely to change (external APIs, algorithms, data formats), hide it behind an abstraction so changes don't ripple through the system.

---

## 3. Complementary Principles

### DRY — Don't Repeat Yourself
Every piece of logic should have one authoritative location. Duplication means updating the same logic in multiple places — a guaranteed source of bugs.

### YAGNI — You Aren't Gonna Need It
Don't build abstractions, configurations, or features for hypothetical future needs. Build what's needed now, refactor when the real need emerges.

### Law of Demeter (Tell, Don't Ask)
An object should only talk to its immediate collaborators. Avoid: `order.getCustomer().getAddress().getCity()`. Instead: `order.getShippingCity()` — let the object handle its own internals.

### Composition over Inheritance
Prefer composing objects with behaviors over deep inheritance hierarchies. Inheritance creates tight coupling; composition creates flexibility.
