# Citi Karat Screening Round — Prep

> **Source note:** the format and real-question details below are drawn from a single third-party candidate account (an SEO/blog guide, not an official Citi or Karat document). Treat the exact questions as one data point, not a guarantee — the *format* (Karat-run, 60 min, screen-recorded, rubric-scored) matches how Karat operates across companies generally, so that part is more reliable than the specific questions.

## Table of Contents
1. [Format Overview](#1-format-overview)
2. [The Two Confirmed Real Questions](#2-the-two-confirmed-real-questions)
3. [Scoring & What's Evaluated](#3-scoring--whats-evaluated)
4. [Why Candidates Fail — Hard Rules](#4-why-candidates-fail--hard-rules)
5. [Practice Questions by Segment](#5-practice-questions-by-segment)

---

## 1. Format Overview

- **60 minutes total**, run by a **Karat Interview Engineer** (a Karat employee, not a Citi engineer), on a shared-screen coding platform.
- Breakdown: **~10 min discussion/intro → ~40 min live coding → ~10 min wrap-up/feedback.**
- Session is **fully recorded** (video + code playback) and later reviewed; the recruiter only gets the recording plus the Interview Engineer's written rubric summary — no same-day score.
- Typically **1–2 coding problems**, in this order:
  1. **Bug-fix on a given codebase** (usually a Spring Boot project with a failing unit test) — opens the coding window.
  2. **A smaller counting/array algorithm** — single-pass, O(n)/O(1) pattern.
- Sometimes preceded by **rapid-fire Java/Spring conceptual questions** before the editor even opens.
- Other confirmed-but-less-common substitutions: **code-review style** tasks ("explain this function, then improve it"), small **OOP design** exercises, and **SQL/Python** output-prediction (more common on analytics-adjacent tracks, less likely for a Lead Java Engineer track).

## 2. The Two Confirmed Real Questions

**Q1 — Trade Reconciliation Bug-Fix:**
A Spring Boot project with a failing test in `TradeReconcilerTest`. `TradeReconciler.reconcile()` is supposed to return trades from an incoming feed that aren't yet in the booked ledger, but returns an empty list. Root cause: `Trade.equals()`/`hashCode()` only used the `symbol` field, so two trades with the same symbol but different side/quantity/price collapsed into one entry in a `HashSet`. Fix: both methods must consider all identity fields (symbol, side, quantity, price). Target complexity: O(n + m) time, O(m) space.

**Q2 — Toll-Booth Complete-Journeys Counting:**
Input is a string of events: `E` = a car entered the highway at a booth, `X` = exited. Count complete journeys (matched E→X pairs), ignoring orphan exits (`X` with no prior unmatched `E`) and unfinished entries (`E` with no later `X`). Solution: a running `open` counter (entries not yet closed) and a separate `complete` counter, incremented only when a valid pair closes. Target complexity: O(n) time, O(1) space.

## 3. Scoring & What's Evaluated

- **Rubric-based, not pass/fail.** The Interview Engineer rates competencies — problem-solving, communication, code quality — there's no single number to aim at.
- **Partial credit is real.** A clean, correct, verbally-explained approach counts even if the last edge case isn't finished.
- **Communication is graded alongside code.** Going silent while typing loses points you could have kept by narrating your plan.
- **Deliverable:** the recording + a written competency summary go to the recruiter — no auto-published score.

## 4. Why Candidates Fail — Hard Rules

1. **Any overlay app or helper tool visible on the shared screen → immediate removal.** One candidate was removed on the spot for a desktop overlay during the session.
2. **Tab-switching on a visible monitor triggers an automated "integrity risk" flag** — even without an overlay, switching tabs during coding got flagged and led to removal without explanation.
3. **Running out of time and only explaining (not finishing) the second problem** → rejection, even with articulate reasoning. Prioritize one fully-explained, correct solution over two half-done ones.
4. **Misreading the given codebase** — spending the window in the wrong file because the instructions/codebase weren't read carefully enough up front.
5. **Going silent while coding** — no narration = lost communication-score points, even if the code itself is correct.

**Practical rule:** anything you need for reference must be on a **separate, unshared device** — never alt-tabbed or overlaid on the screen you're sharing.

## 5. Practice Questions by Segment

### Segment 1 — Java/Spring Conceptual Rapid-Fire (~10 min)

Questions below — each links down to its answer; answers are kept separately so the question list itself stays fast to skim.

1. [Checked vs. unchecked exceptions — pros/cons, when to use which](#a1-checked-vs-unchecked-exceptions)
2. [What does "effectively final" mean, and why does it matter for lambdas/anonymous inner classes?](#a2-effectively-final)
3. [How does Spring wire beans?](#a3-how-spring-wires-beans) (`@Component`/`@Service`/`@Repository`, `@Autowired`, constructor vs. field injection, singleton vs. prototype scope)
4. [Why is `@Transactional` silently ignored when called via `new` or self-invocation?](#a4-why-transactional-is-ignored-on-new-or-self-invocation)
5. [The `equals()`/`hashCode()` contract](#a5-the-equals-and-hashcode-contract) — what breaks if you override one but not the other, or omit a field
6. [`HashMap` vs. `HashSet` vs. `TreeMap`](#a6-hashmap-vs-hashset-vs-treemap) — how each relies on `equals()`/`hashCode()`/`compareTo()`
7. [Why immutable objects are inherently thread-safe](#a7-why-immutable-objects-are-thread-safe)
8. [`volatile` vs. `synchronized` vs. `AtomicInteger`](#a8-volatile-vs-synchronized-vs-atomicinteger) — when each is enough
9. [`==` vs. `.equals()` for objects, and the String pool gotcha](#a9-reference-equality-vs-equals-and-the-string-pool)
10. [Interfaces vs. abstract classes](#a10-interfaces-vs-abstract-classes) — when to pick which
11. [`ConcurrentModificationException`](#a11-concurrentmodificationexception) — when it fires, how to avoid it
12. [Checked exception wrapped into a `RuntimeException`](#a12-wrapping-checked-exceptions-in-runtimeexception) — why and when you'd do that

#### Answers

##### A1. Checked vs Unchecked Exceptions

**Checked** (`IOException`, `SQLException`) extend `Exception` and must be declared (`throws`) or caught — the compiler forces you to acknowledge them. **Unchecked** (`RuntimeException` and subclasses — `NullPointerException`, `IllegalArgumentException`) need no declaration.

- **Pros of checked:** forces callers to handle recoverable, expected failures (a file might not exist, a network call might fail) — the API signature documents what can go wrong.
- **Cons of checked:** pollutes method signatures up the whole call stack even when a caller can't do anything about it; famously why many Java devs wrap checked exceptions into unchecked ones at a boundary (see [A12](#a12-wrapping-checked-exceptions-in-runtimeexception)).
- **Rule of thumb:** use checked for conditions a *caller can reasonably recover from* (retry, fallback); use unchecked for programming errors (`null` where a value was required, invalid arguments) that indicate a bug, not a recoverable condition.

##### A2. Effectively Final

A local variable is "effectively final" if it's never reassigned after its first assignment — even though it isn't declared `final` with the keyword. Lambdas and anonymous inner classes can only capture local variables that are effectively final.

**Why it matters:** a lambda/anonymous class may outlive the method it was created in (e.g., it's handed to a thread or stored for later). If it captured a *mutable* local variable, the lambda and the original method could each see a different, inconsistent value, or the variable could change after the lambda captured it, silently corrupting behavior. Requiring effective finality means the lambda always captures one fixed value — no moving target, no race.

```java
int x = 5;
Runnable r = () -> System.out.println(x);  // OK — x never reassigned
x = 10;  // if this line existed, the lambda wouldn't compile
```

##### A3. How Spring Wires Beans

Spring scans your classpath for classes annotated `@Component` (and its specializations `@Service`, `@Repository`, `@Controller` — same mechanism, different semantic labels) and creates one managed instance of each, called a **bean**, stored in the **ApplicationContext** (Spring's IoC container).

- **`@Autowired`** tells Spring to inject one bean into another — by type, then by name if there are multiple candidates of the same type.
- **Constructor injection** (preferred) passes dependencies through the constructor — makes dependencies explicit, required, and immutable (can be `final` fields), and works well with unit testing (no container needed, just call `new` with mocks).
- **Field injection** (`@Autowired` directly on a field) is more concise but hides dependencies, makes a class harder to unit test without reflection tricks, and allows a half-constructed object with null dependencies to exist temporarily.
- **Scope:** `singleton` (default) — exactly one instance per container, shared everywhere. `prototype` — a new instance every time the bean is requested. Singleton is overwhelmingly the default used in practice; prototype is rare (used when a bean genuinely needs fresh, independent state per use).

##### A4. Why Transactional Is Ignored on new or Self-Invocation

`@Transactional` (like `@Async`, `@Cacheable`) is implemented via an **AOP proxy** — Spring wraps the real bean in a proxy object, and the proxy is what actually starts/commits/rolls back the transaction before and after the real method runs.

Two ways this silently breaks:
1. **Object built with `new`** instead of obtained from the Spring container — there's no proxy at all, so the annotation is just inert text with zero effect. (This is exactly the bug in [citi.md §23's Rating Microservice scenario](https://github.com/arpit-jain-mygit/interview-preparation/blob/main/curated/citi.md#project-scenario-rating-microservice-transaction-bug).)
2. **Self-invocation** — calling `this.someTransactionalMethod()` from inside the same class. Even though the object *is* a real Spring bean, that particular call never goes through the external proxy (it's a plain internal Java call on `this`), so the proxy never gets a chance to intercept it.

**Fix for both:** make sure the object is a real Spring-managed bean, and call the `@Transactional` method from a *different* bean (through the proxy), never via `new` or via `this` inside the same class.

##### A5. The equals and hashCode Contract

The contract: **if two objects are `.equals()`, they must have the same `hashCode()`.** (The reverse isn't required — different objects can share a hash code, that's just a "collision," which hash-based collections already handle.)

**What breaks if you violate it:** hash-based collections (`HashSet`, `HashMap`) use `hashCode()` to pick a bucket, then `equals()` to check within that bucket. If two "equal" objects hash differently, they land in different buckets — a `HashSet` can contain two objects that are `.equals()` to each other, and `map.get(key)` can fail to find a value even though an "equal" key was used to insert it.

**The flip side — omitting a field:** if `equals()`/`hashCode()` only check *some* fields (like only `symbol` on a `Trade`, ignoring side/quantity/price — the real Karat bug), objects that are genuinely *different* get treated as equal, and a `HashSet` silently collapses them into one entry. Both directions of this bug are just "the two methods don't agree with each other, or don't reflect true identity."

##### A6. HashMap vs HashSet vs TreeMap

- **`HashMap`/`HashSet`** — backed by a hash table. Uses `hashCode()` to pick a bucket and `equals()` to resolve collisions within it. O(1) average lookup/insert. No ordering guarantee.
- **`TreeMap`/`TreeSet`** — backed by a red-black tree. Uses `compareTo()` (via `Comparable`) or a supplied `Comparator` — **never** `equals()`/`hashCode()` — to decide both ordering *and* uniqueness. Two elements are "the same" if `compareTo()` returns 0, even if `.equals()` would say otherwise — a classic gotcha if your `compareTo()` and `equals()` aren't consistent. O(log n) lookup/insert, but iterates in sorted order.
- **Practical pick:** `HashMap`/`HashSet` by default (fastest); `TreeMap`/`TreeSet` only when you specifically need sorted iteration order or range queries (`firstKey()`, `headMap()`, etc.).

##### A7. Why Immutable Objects Are Thread-Safe

An object is immutable when none of its fields can change after construction (all `final`, no setters, defensive copies of any mutable fields passed in/out). Thread-safety requires protecting against two threads seeing inconsistent state when one mutates while another reads. If nothing can ever be mutated after construction, that failure mode doesn't exist — every thread that sees a reference to the object sees the exact same, permanently-fixed state. No lock is needed to protect something that never changes. (This is the same idea underlying `volatile`'s "single write, safely published once" case — see [A8](#a8-volatile-vs-synchronized-vs-atomicinteger).)

##### A8. volatile vs synchronized vs AtomicInteger

- **`volatile`** — guarantees *visibility* only (a write is immediately visible to other threads' reads), not atomicity. Safe for a single read or single write of a variable (flags); unsafe for read-modify-write (`count++`).
- **`synchronized`** — guarantees both visibility *and* mutual exclusion (only one thread executes the block at a time). Covers any compound operation, at the cost of lock contention and (if used carelessly across multiple locks) deadlock risk.
- **`AtomicInteger`** (and the `Atomic*` family) — lock-free atomicity via CAS (compare-and-swap) at the hardware level. Covers single-variable read-modify-write operations (`incrementAndGet()`) without the overhead of a lock, but doesn't help if you need to atomically update *multiple* variables together — that still needs `synchronized`/a lock.
- **Pick:** `volatile` for flags only; `AtomicInteger` for a single counter/variable under contention; `synchronized` (or a `Lock`) when multiple variables must change together atomically.

##### A9. Reference Equality vs Equals, and the String Pool

**`==`** compares references — are these two variables pointing at the literal same object in memory? **`.equals()`** compares logical/value equality, as defined by the class's own override (defaults to reference equality in `Object` unless overridden, as `String` and the wrapper classes do).

**The String pool gotcha:** Java caches string *literals* in a shared pool for memory efficiency. `String a = "hi"; String b = "hi";` — both `a` and `b` point at the *same* pooled object, so `a == b` happens to be `true`. But `String c = new String("hi");` forces a new object on the heap, outside the pool — `a == c` is `false` even though `a.equals(c)` is `true`. **Rule:** always use `.equals()` for String/object content comparison; never rely on `==` giving the "expected" result just because it happened to work with literals.

##### A10. Interfaces vs Abstract Classes

- **Interface** — a pure contract (what must be done), no state, traditionally no implementation (though `default`/`static` methods now allow some). A class can implement *multiple* interfaces. Use when unrelated classes need to guarantee the same capability (`Comparable`, `Runnable`) without being forced into a shared type hierarchy.
- **Abstract class** — can hold state (fields) and partial implementation, but a class can extend only *one*. Use when there's a genuine "is-a" relationship and real shared code/state to reuse among subclasses, not just a shared method signature.
- **One-line test:** "Do unrelated classes just need to promise the same behavior?" → interface. "Do these classes share actual code and a true type hierarchy?" → abstract class.

##### A11. ConcurrentModificationException

Thrown when a collection is **structurally modified** (add/remove, not just changing an existing element's value) while being iterated with a plain `Iterator`/for-each loop — the iterator detects the collection's internal modification counter changed since it started and fails fast rather than returning undefined/corrupted results.

**Common trigger:**
```java
for (String s : list) {
    if (condition(s)) list.remove(s);  // throws CME
}
```

**Fixes:**
- Use `Iterator.remove()` directly (`it.remove()` inside a `while (it.hasNext())` loop) — this updates the iterator's own state, avoiding the mismatch.
- Use `list.removeIf(condition)` — the cleanest modern fix, handles the iteration/removal safely internally.
- Use a `CopyOnWriteArrayList` (for concurrent/multi-threaded cases) or collect-then-remove (build a separate list of items to remove, then remove them after the loop).

##### A12. Wrapping Checked Exceptions in RuntimeException

Done at a **boundary** where the caller has no meaningful way to recover, and you don't want the checked exception polluting every method signature up the call stack. Example: a repository method internally calls JDBC code that throws `SQLException` (checked); if a typical caller (a service method) can't actually do anything different based on that exception besides log it and fail the request, wrapping it (`throw new RuntimeException("...", e)`, or a custom unchecked exception) keeps the checked exception contained at the layer that understands it, while letting it still propagate (with its original cause preserved via the constructor) to a top-level handler. This is exactly why Spring's own data-access exceptions (`DataAccessException` and subtypes) are all unchecked — Spring deliberately wraps every checked `SQLException` so application code isn't forced to catch it everywhere.

### Segment 2 — Bug-Fix on a Given Codebase (~15–20 min)
Practice spotting and fixing these bug *shapes* fast (confirmed pattern: a failing test, find root cause, fix):
- `equals()`/`hashCode()` using only a partial set of fields → distinct objects collapse in a `HashSet`/`HashMap` (the real Trade reconciliation bug)
- `String` → numeric parsing bug (timestamp as `String` needed as `float`/`double`; `NumberFormatException` handling)
- `@Transactional(REQUIRES_NEW)` silently ignored because the object was built with `new` instead of being a Spring bean (see [citi.md §23 → PROJECT SCENARIO: Rating Microservice Transaction Bug](https://github.com/arpit-jain-mygit/interview-preparation/blob/main/curated/citi.md#project-scenario-rating-microservice-transaction-bug))
- `==` used instead of `.equals()` for `String`/boxed `Integer` comparison
- A mutable object used as a `HashMap` key, then mutated after insertion → lookup silently fails
- Wrong `Comparator`/`Comparable` implementation → incorrect sort order
- Off-by-one loop bound causing wrong aggregation/count
- Missing null check causing an intermittent `NullPointerException`
- `SimpleDateFormat` reused across threads (not thread-safe) causing corrupted date parsing
- Java Streams misuse — forgetting a terminal operation, or wrong `reduce`/`collect` logic
- A list/collection passed by reference and unintentionally mutated by the callee

### Segment 3 — Live Algorithm/Coding Problem (~15–20 min)
Confirmed pattern: single-pass, O(n)/O(1), counter or hashmap-based — not graph/DP-heavy:
- **Toll-booth / complete journeys counting** (E/X event pairs, ignore orphans) — the real confirmed question
- Valid parentheses / balanced brackets
- Maximum nesting depth of brackets
- Two Sum (HashMap pair-sum lookup)
- Group anagrams
- First non-repeating character in a string
- Count pairs with a given sum
- Best single buy/sell for max profit
- Merge overlapping intervals
- Sliding window — max/min sum of subarray of size k
- Find the duplicate / missing number in an array
- Running/prefix sum problems
- String run-length compression
- Check if two strings are anagrams
- Reverse a string / reverse words in place
- Rotate an array by k positions

### Bonus — OOP Design & Code-Review (also confirmed, sometimes substituted in)
- Small OOP design from a one-paragraph spec: design 2–3 classes for something like a parking lot, ATM, rate limiter, or LRU cache — practice stating each class's single responsibility **out loud before coding**
- Code-review drill: take any medium-complexity function, explain what it does, then state 2–3 concrete improvements **without silently rewriting it** — communication is graded here as much as the fix itself
