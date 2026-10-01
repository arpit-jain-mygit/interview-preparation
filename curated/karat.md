# Citi Karat Screening Round — Prep

> **Source note:** the format and real-question details below are drawn from a single third-party candidate account (an SEO/blog guide, not an official Citi or Karat document). Treat the exact questions as one data point, not a guarantee — the *format* (Karat-run, 60 min, screen-recorded, rubric-scored) matches how Karat operates across companies generally, so that part is more reliable than the specific questions.

## Table of Contents
1. [Format Overview](#1-format-overview)
2. [The Two Confirmed Real Questions](#2-the-two-confirmed-real-questions)
3. [Scoring & What's Evaluated](#3-scoring--whats-evaluated)
4. [Why Candidates Fail — Hard Rules](#4-why-candidates-fail--hard-rules)
5. [Practice Questions by Segment](#5-practice-questions-by-segment)
   - [Segment 1 — Java/Spring Conceptual Rapid-Fire](#segment-1--javaspring-conceptual-rapid-fire-10-min)
     - [Answers](#answers)
     - [MCQ Practice](#mcq-practice-segment-1--5-questions-per-topic)
     - [MCQ Answer Key](#mcq-answer-key)
   - [Segment 2 — Bug-Fix on a Given Codebase](#segment-2--bug-fix-on-a-given-codebase-1520-min)
     - [Code Practice (Problems)](#code-practice-segment-2--problem--solution-kept-separate)
     - [Code Solutions](#code-solutions-segment-2)
   - [Segment 3 — Live Algorithm/Coding Problem](#segment-3--live-algorithmcoding-problem-1520-min)
     - [Algo Practice (Problems)](#algo-practice-segment-3--problem--solution-kept-separate)
     - [Algo Solutions](#algo-solutions-segment-3)
   - [Bonus — OOP Design & Code-Review](#bonus--oop-design--code-review-also-confirmed-sometimes-substituted-in)

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

#### MCQ Practice (Segment 1) — 5 Questions per Topic

Answers are kept separately in the [MCQ Answer Key](#mcq-answer-key) below — each topic links straight to its own answers.

##### Topic 1: Checked vs Unchecked Exceptions
*(→ [Answers](#answer-key-1-checked-vs-unchecked-exceptions))*

1. Which of the following is **not** required to be declared or caught by the compiler?
   a) `IOException`  b) `SQLException`  c) `NullPointerException`  d) `InterruptedException`
2. What's the main downside of overusing checked exceptions in a public API?
   a) They can't carry a cause  b) They force every method up the call stack to declare or catch them, even when the caller can't recover  c) They can only be thrown, never caught  d) They're slower to construct
3. Which is the best use case for a checked exception?
   a) A programming bug like passing null where a value is required  b) An out-of-bounds array index  c) A recoverable condition, like a file that might not exist, where the caller can retry or fall back  d) Division by zero
4. A method declares `throws Exception`. What's the problem with this?
   a) Nothing, it's correct  b) It's too broad — callers can't distinguish recoverable conditions from bugs and must catch everything indiscriminately  c) `Exception` can't be thrown  d) It blocks `RuntimeException`s
5. Spring's `DataAccessException` hierarchy is deliberately:
   a) Checked, so every DAO caller must handle SQL errors explicitly  b) Unchecked, wrapping the checked `SQLException` so application code isn't forced to catch it everywhere  c) Abstract and cannot be thrown  d) The same class as `SQLException`

##### Topic 2: Effectively Final
*(→ [Answers](#answer-key-2-effectively-final))*

1. A local variable is "effectively final" when:
   a) It's declared with the `final` keyword  b) It's never reassigned after its first assignment, even without `final`  c) It's a primitive type only  d) It's declared inside a lambda
2. Why can't a lambda capture a local variable that gets reassigned later in the enclosing method?
   a) Lambdas can only capture static variables  b) The lambda might run later (e.g. on another thread) and would see an inconsistent value, so Java requires a fixed, stable capture  c) Lambdas can't read local variables at all  d) It's a pure syntax limitation
3. Which snippet fails to compile?
   a) `int x = 5; Runnable r = () -> print(x);`  b) `int x = 5; x = 10; Runnable r = () -> print(x);`  c) `final int x = 5; Runnable r = () -> print(x);`  d) `int x = 5; if (x > 0) {} Runnable r = () -> print(x);`
4. Can a mutable instance field be accessed inside a lambda defined in an instance method?
   a) No, never  b) Yes — effectively-final applies only to local variables/parameters, not instance or static fields  c) Only if the field is `volatile`  d) Only if the field is also `final`
5. What practical risk does the effectively-final rule prevent?
   a) Memory leaks from unused lambdas  b) A race/stale-value bug from a lambda capturing a variable that changes after capture, especially across threads  c) Slower lambda execution  d) Serialization errors

##### Topic 3: How Spring Wires Beans
*(→ [Answers](#answer-key-3-how-spring-wires-beans))*

1. What happens when multiple beans of the same type exist and `@Autowired` has no qualifier?
   a) Picks the first one alphabetically  b) Fails with an ambiguous-dependency error unless disambiguated by name/`@Qualifier`/`@Primary`  c) Creates a new instance  d) Picks one at random
2. Why is constructor injection generally preferred over field injection?
   a) It's faster at runtime  b) It makes dependencies explicit/required, allows `final` fields, and is easier to unit test without a container  c) Field injection no longer works  d) It's required for `@Service` beans
3. What's the default Spring bean scope?
   a) `prototype`  b) `singleton`  c) `request`  d) `session`
4. A `prototype`-scoped bean is injected into a `singleton`-scoped bean via plain `@Autowired`. What happens?
   a) A new prototype instance is created every time the singleton's method runs  b) The singleton captures ONE prototype instance at creation time and reuses that same instance forever  c) Spring throws an exception at startup  d) The prototype becomes a singleton automatically
5. How do `@Component`, `@Service`, `@Repository`, and `@Controller` differ?
   a) Only `@Component` actually registers a bean  b) They're all `@Component` meta-annotations — specialized ones add semantic meaning (and sometimes extra behavior, like exception translation for `@Repository`) but register a bean the same way  c) `@Service` is prototype-scoped by default  d) Only `@Controller` is component-scanned

##### Topic 4: Why Transactional Is Ignored on new or Self-Invocation
*(→ [Answers](#answer-key-4-why-transactional-is-ignored-on-new-or-self-invocation))*

1. `@Transactional` is implemented using:
   a) Compile-time bytecode instrumentation  b) An AOP proxy that wraps the real bean and starts/commits/rolls back around the method call  c) A JVM annotation processor with no proxy  d) Reflection only
2. Why does `@Transactional` have no effect on an object created with `new SomeService()`?
   a) `new` objects are always thread-safe so transactions aren't needed  b) There's no Spring-managed proxy around it, so nothing intercepts the call to start a transaction  c) `new` throws an exception for `@Transactional` classes  d) It requires the class to be `final`
3. A Spring bean `OrderService` calls `this.saveWithAudit()`, another `@Transactional(REQUIRES_NEW)` method in the *same* class. What happens?
   a) A new independent transaction is created as expected  b) The annotation is ignored because the call bypasses the external proxy (self-invocation)  c) Spring throws a runtime exception  d) It behaves identically to calling it from another bean
4. What's the standard fix for the self-invocation problem?
   a) Mark the method `static`  b) Move the `@Transactional` method to a different bean/class and call it from there, through the proxy  c) Add `synchronized`  d) There's no fix
5. Which proxy mechanisms does Spring use for `@Transactional`?
   a) Only CGLIB  b) JDK dynamic proxies (if the bean implements an interface) or CGLIB subclass proxies (otherwise)  c) Only reflection, no proxy  d) A custom Spring-only compiler

##### Topic 5: The equals and hashCode Contract
*(→ [Answers](#answer-key-5-the-equals-and-hashcode-contract))*

1. The contract requires that if `a.equals(b)` is true, then:
   a) `a == b` must also be true  b) `a.hashCode()` must equal `b.hashCode()`  c) `b.equals(a)` can be false  d) `a` and `b` must never be the same class
2. Is the reverse also required — same hash code implies `equals()` must be true?
   a) Yes, always  b) No — equal hash codes can occur between unequal objects ("collision"), which hash-based collections already handle via `equals()` within that bucket  c) Only for Strings  d) Only if `hashCode()` is overridden
3. A class overrides `equals()` to compare only an `id` field but doesn't override `hashCode()` at all. What breaks?
   a) Nothing  b) Two objects that are `.equals()` can land in different `HashMap` buckets, so `map.get()` with an "equal" key can fail to find the value  c) `hashCode()` throws an exception  d) `equals()` stops working entirely
4. In the real Karat bug, `Trade.equals()`/`hashCode()` used only the `symbol` field. The effect in a `HashSet` was:
   a) Trades were sorted by symbol  b) Distinct trades with the same symbol but different side/quantity/price were treated as duplicates and collapsed into one entry  c) A `ConcurrentModificationException`  d) No effect
5. What's the safest way to generate correct `equals()`/`hashCode()`?
   a) Only override `equals()`, never `hashCode()`  b) Use `Objects.equals()`/`Objects.hash()` (or an IDE/Lombok generator) against every field that defines identity  c) Use the default `Object` implementation always  d) Use the memory address directly

##### Topic 6: HashMap vs HashSet vs TreeMap
*(→ [Answers](#answer-key-6-hashmap-vs-hashset-vs-treemap))*

1. `TreeMap` determines "sameness" of keys using:
   a) `hashCode()`/`equals()`  b) `compareTo()` (or a supplied `Comparator`) — returning 0 means "the same key," regardless of `equals()`  c) Reference equality only  d) Insertion order
2. Typical `get()` complexity: `HashMap` vs. `TreeMap`?
   a) O(1) average for `HashMap`, O(log n) for `TreeMap`  b) O(log n) for both  c) O(1) for both  d) O(n) for `HashMap`, O(1) for `TreeMap`
3. If `compareTo()` says two objects are "equal" (returns 0) but `equals()` disagrees, and both are added to a `TreeSet`:
   a) Both are added — `TreeSet` uses `equals()`  b) Only one is kept — `TreeSet`/`TreeMap` treat `compareTo()==0` as duplicate, silently dropping the second  c) An exception is thrown  d) `TreeSet` falls back to `hashCode()`
4. Best choice for "give me all entries between key X and key Y, in order"?
   a) `HashMap`  b) `HashSet`  c) `TreeMap` (via `headMap`/`tailMap`/`subMap`)  d) `LinkedList`
5. Why do `HashMap`/`HashSet` give no ordering guarantee?
   a) They're implemented as linked lists  b) Elements are placed into buckets based on `hashCode()`, which has no relation to natural/insertion order  c) Java forbids ordering in hash structures  d) They iterate in reverse insertion order

##### Topic 7: Why Immutable Objects Are Thread-Safe
*(→ [Answers](#answer-key-7-why-immutable-objects-are-thread-safe))*

1. What makes an object truly immutable?
   a) All fields private  b) All fields `final`, set only in the constructor, no setters, and any mutable fields passed in/out are defensively copied  c) No methods besides getters  d) Marked with an enforced `@Immutable` keyword
2. Why don't immutable objects need synchronization to be shared safely across threads?
   a) The JVM auto-synchronizes them  b) Since no thread can ever change the object's state after construction, no thread can see a stale or half-updated value from another thread's write  c) They're always in CPU cache  d) They aren't actually thread-safe
3. A class has all `final` fields, but one is a mutable `List` passed via the constructor and stored directly (no defensive copy). Is it truly immutable?
   a) Yes, the reference is final  b) No — the caller can still mutate the list's contents after construction, breaking the guarantee  c) Yes, Lists are always immutable  d) Depends only on whether it's sorted
4. Which JDK class is a canonical immutable, thread-safe example?
   a) `StringBuilder`  b) `ArrayList`  c) `String`  d) `HashMap`
5. How does immutability relate to the "D - DESIGN IT OUT" race-condition pattern elsewhere in this prep?
   a) It isn't related  b) Both eliminate races by removing concurrent mutation — one by confining mutation to a single thread, the other by removing mutation entirely  c) Immutability requires a message queue  d) It only works for primitives

##### Topic 8: volatile vs synchronized vs AtomicInteger
*(→ [Answers](#answer-key-8-volatile-vs-synchronized-vs-atomicinteger))*

1. Which of these correctly uses `volatile`?
   a) `volatile int count = 0; count++;`  b) `volatile boolean shutdown = false; ... if (shutdown) {}`  c) `volatile List<String> list; list.add("x");`  d) `volatile int total; total = total + 5;`
2. Why doesn't `volatile` fix a race condition on `count++`?
   a) `volatile` provides no guarantee at all  b) `count++` is really three steps (read, add, write); `volatile` makes each step visible but doesn't stop two threads interleaving between the steps  c) `volatile` only works on booleans  d) `count++` is already atomic
3. `AtomicInteger.incrementAndGet()` is safe under concurrency because:
   a) It uses a lock that blocks all threads system-wide  b) It uses a CAS (compare-and-swap) instruction to atomically update the value, retrying if another thread updated it first  c) It's just a `volatile` field  d) It's `synchronized` on the object's monitor
4. You need to atomically update two related fields (`balance` and `lastUpdated`) together. Best tool?
   a) Two independent `AtomicInteger`/`AtomicLong` fields  b) `volatile` on both  c) `synchronized` (or a `Lock`) around the block updating both — no single `Atomic*` class covers two fields together  d) Not possible safely in Java
5. Main cost of `synchronized` compared to `volatile`/`AtomicInteger`?
   a) Can't be used with primitives  b) Lock contention — threads block and wait, and careless multi-lock use risks deadlock  c) Never guarantees visibility  d) Can't be used inside methods

##### Topic 9: Reference Equality vs Equals, String Pool
*(→ [Answers](#answer-key-9-reference-equality-vs-equals-string-pool))*

1. `String a = "hi"; String b = "hi";` — what does `a == b` evaluate to, and why?
   a) false, strings are never pooled  b) true, both literals resolve to the same object in the String pool  c) true, but only on 32-bit JVMs  d) undefined
2. `String a = "hi"; String c = new String("hi");` — what does `a == c` evaluate to?
   a) true, content is identical  b) false — `new String()` forces a new heap object outside the pool, even though `a.equals(c)` is true  c) compile error  d) true, but `.equals()` is false
3. Why is `==` risky for comparing `Integer` objects instead of `int` primitives?
   a) `Integer` never implements `equals()` correctly  b) Autoboxed Integers are cached only in a small range (default -128 to 127); outside it, equal values can be different objects  c) `==` always throws NPE on `Integer`  d) `Integer`s can't be compared at all
4. What's the single safest rule for comparing object content?
   a) Always use `==` for performance  b) Always use `.equals()` for content comparison; reserve `==` for checking literal reference identity  c) Use `.equals()` only for Strings  d) Use `hashCode()` comparison instead
5. Does the String pool optimization apply to `String s = "h" + someVariable` built at runtime?
   a) Yes, always pooled identically to literals  b) No — runtime-computed strings aren't automatically interned (without calling `.intern()`), so `==` with a literal can unexpectedly be false  c) Only if the variable is `final`  d) Only on old JDKs

##### Topic 10: Interfaces vs Abstract Classes
*(→ [Answers](#answer-key-10-interfaces-vs-abstract-classes))*

1. What's true about multiple inheritance in Java?
   a) A class can extend multiple abstract classes but implement only one interface  b) A class can implement multiple interfaces but extend only one class  c) Neither supports any multiple inheritance  d) Both support unlimited multiple inheritance
2. Since Java 8, interfaces can have:
   a) Only abstract method signatures  b) `default` and `static` methods with actual implementation, in addition to abstract signatures  c) Instance fields with mutable state  d) Constructors
3. When should you pick an abstract class over an interface?
   a) When unrelated classes just need to share a method signature  b) When there's a genuine "is-a" hierarchy and real shared state/implementation to reuse among subclasses  c) When a class must implement multiple unrelated contracts  d) Abstract classes should always be avoided
4. Can an abstract class have a constructor?
   a) No, never  b) Yes — subclasses call it via `super()`, even though the abstract class can't be instantiated directly  c) Only with no abstract methods  d) Only in Java 8+
5. Why are `Comparable` and `Runnable` interfaces, not abstract classes?
   a) Java disallows abstract classes with a single method  b) Many unrelated classes need to promise the same single capability without being forced into one shared class hierarchy  c) Interfaces are faster at runtime  d) It's arbitrary

##### Topic 11: ConcurrentModificationException
*(→ [Answers](#answer-key-11-concurrentmodificationexception))*

1. What triggers CME in a single-threaded for-each loop?
   a) Reading a collection's size  b) Structurally modifying (add/remove) the collection while iterating it with a plain `Iterator`/for-each, detected via a changed modification count  c) Modifying an element's value in place  d) Using `TreeMap` instead of `HashMap`
2. Which of these correctly removes matching elements during iteration without throwing CME?
   a) `for (String s : list) { if (cond(s)) list.remove(s); }`  b) `list.removeIf(cond);`  c) `for (int i=0; i<list.size(); i++) { if (cond(list.get(i))) list.remove(i); }`  d) `list.forEach(s -> { if (cond(s)) list.remove(s); });`
3. Why does `it.remove()` (the `Iterator`'s own method) avoid the exception while `list.remove(s)` inside the loop doesn't?
   a) It doesn't avoid it either  b) `Iterator.remove()` updates the iterator's own tracking of the modification count in sync — `list.remove()` changes the collection without informing the iterator  c) `it.remove()` only works on arrays  d) `list.remove()` is always preferred anyway
4. Is `CopyOnWriteArrayList` reasonable for frequent concurrent reads with rare writes?
   a) No, never safe for iteration  b) Yes — it snapshots the array on each write so iterators never see concurrent modification, at the cost of copying the whole array per write  c) Identical to `ArrayList` with no tradeoffs  d) Only works with primitives
5. Does CME only occur with multiple threads?
   a) Yes, purely multi-threading  b) No — it most commonly happens in single-threaded code, modifying a collection directly while iterating it in the same thread  c) Only with `TreeMap`  d) Never in single-threaded code

##### Topic 12: Wrapping Checked Exceptions in RuntimeException
*(→ [Answers](#answer-key-12-wrapping-checked-exceptions-in-runtimeexception))*

1. What's preserved when you write `throw new RuntimeException("msg", e);`?
   a) Nothing — the original exception and stack trace are lost  b) The original exception is preserved as the "cause," accessible via `getCause()`, including its original stack trace  c) Only the message string  d) The wrapping changes the original exception's type permanently
2. Why would a repository layer wrap a checked `SQLException` into an unchecked exception before it reaches the service layer?
   a) To hide the error from logs entirely  b) So a typical caller, who can't meaningfully recover from a SQL failure anyway, isn't forced to declare/catch it at every layer up the stack  c) `SQLException` can't be caught at all  d) To make it faster to construct
3. Spring's `DataAccessException` hierarchy is an example of:
   a) A checked exception hierarchy requiring explicit handling everywhere  b) Exactly this wrapping pattern — translating various checked, vendor-specific SQL exceptions into a consistent unchecked hierarchy  c) A deprecated pattern no longer used  d) A set of interfaces, not exceptions
4. What's a downside of overusing the wrap-into-`RuntimeException` pattern?
   a) It always loses the original stack trace  b) If overused indiscriminately, it can hide genuinely recoverable conditions a caller could have handled differently, by making everything look unrecoverable  c) It's impossible to log the wrapped exception  d) It prevents the JVM from exiting on uncaught exceptions
5. In `new RuntimeException(message, cause)`, what does `cause` do if the exception is later uncaught?
   a) It's ignored by default exception printing  b) A full stack trace print includes the "Caused by:" chain, showing the original exception too  c) It replaces the message entirely  d) It must be re-thrown separately to be visible

---

#### MCQ Answer Key

##### Answer Key 1: Checked vs Unchecked Exceptions
1. **c** — it's a `RuntimeException` (unchecked); the other three are checked.
2. **b**
3. **c**
4. **b**
5. **b**

##### Answer Key 2: Effectively Final
1. **b**
2. **b**
3. **b**
4. **b**
5. **b**

##### Answer Key 3: How Spring Wires Beans
1. **b**
2. **b**
3. **b**
4. **b**
5. **b**

##### Answer Key 4: Why Transactional Is Ignored on new or Self-Invocation
1. **b**
2. **b**
3. **b**
4. **b**
5. **b**

##### Answer Key 5: The equals and hashCode Contract
1. **b**
2. **b**
3. **b**
4. **b**
5. **b**

##### Answer Key 6: HashMap vs HashSet vs TreeMap
1. **b**
2. **a**
3. **b**
4. **c**
5. **b**

##### Answer Key 7: Why Immutable Objects Are Thread-Safe
1. **b**
2. **b**
3. **b**
4. **c**
5. **b**

##### Answer Key 8: volatile vs synchronized vs AtomicInteger
1. **b**
2. **b**
3. **b**
4. **c**
5. **b**

##### Answer Key 9: Reference Equality vs Equals, String Pool
1. **b**
2. **b**
3. **b**
4. **b**
5. **b**

##### Answer Key 10: Interfaces vs Abstract Classes
1. **b**
2. **b**
3. **b**
4. **b**
5. **b**

##### Answer Key 11: ConcurrentModificationException
1. **b**
2. **b**
3. **b**
4. **b**
5. **b**

##### Answer Key 12: Wrapping Checked Exceptions in RuntimeException
1. **b**
2. **b**
3. **b**
4. **b**
5. **b**

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

#### Code Practice (Segment 2) — Problem & Solution, Kept Separate

Each problem below is buggy code plus a failing test, exactly like the real Karat format. Try to spot and fix it yourself before jumping to the linked solution — all 11 solutions are collected separately in the [Code Solutions](#code-solutions-segment-2) section so you aren't shown the fix while reading the bug.

1. [Problem 1](#problem-1)
2. [Problem 2](#problem-2)
3. [Problem 3](#problem-3)
4. [Problem 4](#problem-4)
5. [Problem 5](#problem-5)
6. [Problem 6](#problem-6)
7. [Problem 7](#problem-7)
8. [Problem 8](#problem-8)
9. [Problem 9](#problem-9)
10. [Problem 10](#problem-10)
11. [Problem 11](#problem-11)

##### Problem 1
*(→ [Solution](#solution-1-equals-and-hashcode-using-only-partial-fields))*

The failing test — `reconcile()` should return trades from the feed that aren't yet booked, but returns an empty list:

```java
import java.util.*;

class Trade {
    String symbol;
    String side;      // BUY or SELL
    int quantity;
    double price;

    Trade(String symbol, String side, int quantity, double price) {
        this.symbol = symbol;
        this.side = side;
        this.quantity = quantity;
        this.price = price;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Trade)) return false;
        Trade other = (Trade) o;
        return symbol.equals(other.symbol);
    }

    @Override
    public int hashCode() {
        return symbol.hashCode();
    }
}

class TradeReconciler {
    List<Trade> reconcile(List<Trade> incomingFeed, List<Trade> bookedLedger) {
        Set<Trade> booked = new HashSet<>(bookedLedger);
        List<Trade> unbooked = new ArrayList<>();
        for (Trade t : incomingFeed) {
            if (!booked.contains(t)) unbooked.add(t);
        }
        return unbooked;
    }
}

public class Solution {
    public static void main(String[] argv) {
        List<Trade> incomingFeed = List.of(
            new Trade("AAPL", "BUY", 100, 150.0),
            new Trade("AAPL", "SELL", 50, 151.0)
        );
        List<Trade> bookedLedger = List.of(
            new Trade("AAPL", "BUY", 100, 150.0)
        );

        List<Trade> unbooked = new TradeReconciler().reconcile(incomingFeed, bookedLedger);
        System.out.println("Unbooked trades: " + unbooked.size());
        // Expected: 1 (the AAPL SELL trade is genuinely not booked)
    }
}
```

##### Problem 2
*(→ [Solution](#solution-2-string-to-numeric-parsing-bug))*

```java
public class Solution {
    static double computeTotal(String[] priceStrings) {
        double total = 0;
        for (String p : priceStrings) {
            total += Float.parseFloat(p);
        }
        return total;
    }

    public static void main(String[] argv) {
        String[] priceStrings = {"150.25", "N/A", "99.50"};
        System.out.println("Total: " + computeTotal(priceStrings));
        // Expected: 249.75 (unparseable entries like "N/A" should be skipped)
    }
}
```

##### Problem 3
*(→ [Solution](#solution-3-transactional-ignored-because-built-with-new))*

```java
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@Service
class RatingService {
    @Transactional
    void rate(Rating rating) {
        validate(rating);
        RatingHistoryBuilder builder = new RatingHistoryBuilder();
        builder.record(rating);
    }
    void validate(Rating rating) { }
}

class RatingHistoryBuilder {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    void record(Rating rating) {
        if (rating.getScore() < 0) throw new IllegalArgumentException("bad score");
        // ... persist history row ...
    }
}

class Rating {
    private final int score;
    Rating(int score) { this.score = score; }
    int getScore() { return score; }
}

public class Solution {
    public static void main(String[] argv) {
        // NOTE: observing the real effect below needs a live Spring ApplicationContext —
        // this main() only shows the call chain that the container would wrap in proxies.
        RatingService service = new RatingService();
        service.rate(new Rating(-5));
        // Expected (inside a real Spring container): only the history-record attempt
        // rolls back; the earlier validate()'d rating still commits.
        // Actual (inside a real Spring container): the exception rolls back the
        // ENTIRE outer transaction — everything is lost.
    }
}
```

##### Problem 4
*(→ [Solution](#solution-4-reference-equality-instead-of-equals))*

```java
public class Solution {
    static boolean isDuplicateOrderId(String incomingId, String lastProcessedId) {
        return incomingId == lastProcessedId;
    }

    public static void main(String[] argv) {
        String incomingId = new String("ORD-1001");   // built at runtime, e.g. from a parsed request body
        String lastProcessedId = "ORD-1001";           // a literal
        System.out.println("Is duplicate: " + isDuplicateOrderId(incomingId, lastProcessedId));
        // Expected: true (same order ID)
    }
}
```

##### Problem 5
*(→ [Solution](#solution-5-mutable-key-mutated-after-insertion))*

```java
import java.util.*;

class AccountKey {
    String region;
    int accountNumber;
    AccountKey(String region, int accountNumber) {
        this.region = region;
        this.accountNumber = accountNumber;
    }
    @Override public boolean equals(Object o) {
        if (!(o instanceof AccountKey)) return false;
        AccountKey k = (AccountKey) o;
        return accountNumber == k.accountNumber && region.equals(k.region);
    }
    @Override public int hashCode() { return Objects.hash(region, accountNumber); }
}

public class Solution {
    public static void main(String[] argv) {
        Map<AccountKey, Double> cache = new HashMap<>();
        AccountKey key = new AccountKey("APAC", 42);
        cache.put(key, 1000.0);
        key.region = "EMEA";
        Double balance = cache.get(new AccountKey("APAC", 42));
        System.out.println("Balance: " + balance);
        // Expected: 1000.0
    }
}
```

##### Problem 6
*(→ [Solution](#solution-6-wrong-comparator-implementation))*

```java
import java.util.*;

class Trade {
    double price;
    Trade(double price) { this.price = price; }
}

class TradeByPriceComparator implements Comparator<Trade> {
    @Override
    public int compare(Trade a, Trade b) {
        return (int) (a.price - b.price);
    }
}

public class Solution {
    public static void main(String[] argv) {
        List<Trade> trades = new ArrayList<>(List.of(new Trade(100.7), new Trade(100.3)));
        trades.sort(new TradeByPriceComparator());
        for (Trade t : trades) System.out.println(t.price);
        // Expected: 100.3 printed before 100.7
    }
}
```

##### Problem 7
*(→ [Solution](#solution-7-off-by-one-loop-bound))*

```java
public class Solution {
    static double average(int[] prices, int windowSize) {
        int sum = 0;
        for (int i = 0; i <= windowSize; i++) {
            sum += prices[i];
        }
        return (double) sum / windowSize;
    }

    public static void main(String[] argv) {
        int[] prices = {10, 20, 30, 40};
        System.out.println("Average: " + average(prices, 3));
        // Expected: 20.0 (average of the first 3 prices: 10, 20, 30)
    }
}
```

##### Problem 8
*(→ [Solution](#solution-8-missing-null-check))*

```java
class CustomerProfile {
    private final String region;
    CustomerProfile(String region) { this.region = region; }
    String getRegion() { return region; }
}

class Customer {
    private final CustomerProfile profile;
    Customer(CustomerProfile profile) { this.profile = profile; }
    CustomerProfile getProfile() { return profile; }
}

public class Solution {
    static String getPreferredRegion(Customer customer) {
        return customer.getProfile().getRegion().toUpperCase();
    }

    public static void main(String[] argv) {
        Customer newCustomer = new Customer(null);   // no profile yet
        System.out.println("Region: " + getPreferredRegion(newCustomer));
        // Expected: "UNKNOWN" (a safe default for an incomplete profile)
    }
}
```

##### Problem 9
*(→ [Solution](#solution-9-simpledateformat-shared-across-threads))*

```java
import java.text.SimpleDateFormat;
import java.util.Date;

class ReportGenerator {
    private static final SimpleDateFormat FORMAT = new SimpleDateFormat("yyyy-MM-dd");

    String formatDate(Date date) {
        return FORMAT.format(date);
    }
}

public class Solution {
    public static void main(String[] argv) throws InterruptedException {
        ReportGenerator generator = new ReportGenerator();
        int threadCount = 50;
        Thread[] threads = new Thread[threadCount];
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> System.out.println(generator.formatDate(new Date())));
            threads[i].start();
        }
        for (Thread t : threads) t.join();
        // Expected: every line prints a correctly formatted date string
        // (run repeatedly under load to observe the intermittent corruption)
    }
}
```

##### Problem 10
*(→ [Solution](#solution-10-java-streams-misuse))*

```java
import java.util.*;

class Item {
    int quantity;
    boolean lowStock;
    Item(int quantity) { this.quantity = quantity; }
    int getQuantity() { return quantity; }
    void setLowStock(boolean v) { this.lowStock = v; }
    boolean isLowStock() { return lowStock; }
}

public class Solution {
    static void markLowStockItems(List<Item> items) {
        items.stream()
             .filter(i -> i.getQuantity() < 10)
             .peek(i -> i.setLowStock(true));
    }

    public static void main(String[] argv) {
        List<Item> items = new ArrayList<>(List.of(new Item(5)));
        markLowStockItems(items);
        System.out.println("Low stock: " + items.get(0).isLowStock());
        // Expected: true
    }
}
```

##### Problem 11
*(→ [Solution](#solution-11-list-passed-by-reference-and-mutated-by-callee))*

```java
import java.util.*;

public class Solution {
    static List<String> buildSummary(List<String> lineItems) {
        Collections.sort(lineItems);
        lineItems.removeIf(s -> s.isBlank());
        return lineItems;
    }

    public static void main(String[] argv) {
        List<String> original = new ArrayList<>(List.of("b", "", "a"));
        List<String> summary = buildSummary(original);
        System.out.println("Original: " + original);
        System.out.println("Summary:  " + summary);
        // Expected: Original stays ["b", "", "a"]; Summary is the cleaned, sorted copy
    }
}
```

---

#### Code Solutions (Segment 2)

##### Solution 1: equals and hashCode Using Only Partial Fields

```java
import java.util.*;

class Trade {
    String symbol;
    String side;
    int quantity;
    double price;

    Trade(String symbol, String side, int quantity, double price) {
        this.symbol = symbol;
        this.side = side;
        this.quantity = quantity;
        this.price = price;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Trade)) return false;
        Trade other = (Trade) o;
        return quantity == other.quantity
            && Double.compare(price, other.price) == 0
            && symbol.equals(other.symbol)
            && side.equals(other.side);
    }

    @Override
    public int hashCode() {
        return Objects.hash(symbol, side, quantity, price);
    }
}

class TradeReconciler {
    List<Trade> reconcile(List<Trade> incomingFeed, List<Trade> bookedLedger) {
        Set<Trade> booked = new HashSet<>(bookedLedger);
        List<Trade> unbooked = new ArrayList<>();
        for (Trade t : incomingFeed) {
            if (!booked.contains(t)) unbooked.add(t);
        }
        return unbooked;
    }
}

public class Solution {
    public static void main(String[] argv) {
        List<Trade> incomingFeed = List.of(
            new Trade("AAPL", "BUY", 100, 150.0),
            new Trade("AAPL", "SELL", 50, 151.0)
        );
        List<Trade> bookedLedger = List.of(
            new Trade("AAPL", "BUY", 100, 150.0)
        );

        List<Trade> unbooked = new TradeReconciler().reconcile(incomingFeed, bookedLedger);
        System.out.println("Unbooked trades: " + unbooked.size());   // prints 1 — correct
    }
}
```
**Why it works:** identity now depends on every field that actually distinguishes two trades. The AAPL BUY and AAPL SELL trades no longer collide — `reconcile()` correctly returns the unbooked SELL. Target complexity stays O(n + m) time, O(m) space (unchanged — this is purely a correctness fix, not a performance one).

##### Solution 2: String to Numeric Parsing Bug

```java
public class Solution {
    static double computeTotal(String[] priceStrings) {
        double total = 0;
        for (String p : priceStrings) {
            if (p == null || p.isBlank()) continue;
            try {
                total += Float.parseFloat(p);
            } catch (NumberFormatException e) {
                // skip unparseable entries like "N/A"
            }
        }
        return total;
    }

    public static void main(String[] argv) {
        String[] priceStrings = {"150.25", "N/A", "99.50"};
        System.out.println("Total: " + computeTotal(priceStrings));   // prints 249.75 — correct
    }
}
```
**Why it works:** unparseable or missing entries are explicitly skipped instead of crashing the whole computation — the loop keeps going and the valid entries still sum correctly.

##### Solution 3: Transactional Ignored Because Built with new

See the full walkthrough in [citi.md §23's Rating Microservice scenario](https://github.com/arpit-jain-mygit/interview-preparation/blob/main/curated/citi.md#project-scenario-rating-microservice-transaction-bug).

```java
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@Service
class RatingService {
    private final RatingHistoryBuilder historyBuilder;

    RatingService(RatingHistoryBuilder historyBuilder) {   // injected, not `new`
        this.historyBuilder = historyBuilder;
    }

    @Transactional
    void rate(Rating rating) {
        validate(rating);
        historyBuilder.record(rating);   // call goes through the real Spring proxy now
    }
    void validate(Rating rating) { }
}

@Component   // now a real Spring bean
class RatingHistoryBuilder {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    void record(Rating rating) {
        if (rating.getScore() < 0) throw new IllegalArgumentException("bad score");
    }
}

class Rating {
    private final int score;
    Rating(int score) { this.score = score; }
    int getScore() { return score; }
}

public class Solution {
    public static void main(String[] argv) {
        // NOTE: this shows the correct WIRING — to actually observe the fixed transactional
        // behavior, both beans need to be resolved from a real Spring ApplicationContext
        // (constructor injection), not constructed with `new`.
        System.out.println("RatingHistoryBuilder is now a real @Component, injected via the constructor.");
    }
}
```
**Why it works:** `RatingHistoryBuilder` is now a container-managed bean, injected via the constructor. Spring wraps it in a real AOP proxy, so `REQUIRES_NEW` actually creates an independent transaction. A failure in `record()` now rolls back only its own transaction — the outer `rate()` transaction (and whatever it already did) is unaffected.

##### Solution 4: Reference Equality Instead of equals

```java
public class Solution {
    static boolean isDuplicateOrderId(String incomingId, String lastProcessedId) {
        return incomingId.equals(lastProcessedId);   // content comparison, not reference
    }

    public static void main(String[] argv) {
        String incomingId = new String("ORD-1001");
        String lastProcessedId = "ORD-1001";
        System.out.println("Is duplicate: " + isDuplicateOrderId(incomingId, lastProcessedId));   // prints true — correct
    }
}
```
**Why it works:** `.equals()` compares the actual characters, not whether both variables happen to point at the same pooled/cached object — so it correctly matches `"ORD-1001"` regardless of whether either String came from a literal or was built at runtime.

##### Solution 5: Mutable Key Mutated After Insertion

```java
import java.util.*;

class AccountKey {
    final String region;          // make fields final
    final int accountNumber;
    AccountKey(String region, int accountNumber) {
        this.region = region;
        this.accountNumber = accountNumber;
    }
    @Override public boolean equals(Object o) {
        if (!(o instanceof AccountKey)) return false;
        AccountKey k = (AccountKey) o;
        return accountNumber == k.accountNumber && region.equals(k.region);
    }
    @Override public int hashCode() { return Objects.hash(region, accountNumber); }
    // no setters
}

public class Solution {
    public static void main(String[] argv) {
        Map<AccountKey, Double> cache = new HashMap<>();
        AccountKey key = new AccountKey("APAC", 42);
        cache.put(key, 1000.0);
        // key.region is final — there's no setter to mutate it after insertion
        Double balance = cache.get(new AccountKey("APAC", 42));
        System.out.println("Balance: " + balance);   // prints 1000.0 — correct
    }
}
```
**Why it works:** once `region` and `accountNumber` are `final` with no setters, the key is immutable — nobody can change it after it's been inserted, so its `hashCode()` can never drift away from the bucket it was originally placed in. (This is the same idea as [A7 — Why Immutable Objects Are Thread-Safe](#a7-why-immutable-objects-are-thread-safe): removing the possibility of mutation removes the whole class of bug.)

##### Solution 6: Wrong Comparator Implementation

```java
import java.util.*;

class Trade {
    double price;
    Trade(double price) { this.price = price; }
}

class TradeByPriceComparator implements Comparator<Trade> {
    @Override
    public int compare(Trade a, Trade b) {
        return Double.compare(a.price, b.price);   // correct, no precision loss
    }
}

public class Solution {
    public static void main(String[] argv) {
        List<Trade> trades = new ArrayList<>(List.of(new Trade(100.7), new Trade(100.3)));
        trades.sort(new TradeByPriceComparator());
        for (Trade t : trades) System.out.println(t.price);   // prints 100.3 then 100.7 — correct
    }
}
```
**Why it works:** `Double.compare()` handles the full precision of both values directly instead of subtracting and truncating to `int`, so close values (100.3 vs 100.7) are never incorrectly collapsed to "equal."

##### Solution 7: Off-by-One Loop Bound

```java
public class Solution {
    static double average(int[] prices, int windowSize) {
        int sum = 0;
        for (int i = 0; i < windowSize; i++) {   // strict < , stays inside the window
            sum += prices[i];
        }
        return (double) sum / windowSize;
    }

    public static void main(String[] argv) {
        int[] prices = {10, 20, 30, 40};
        System.out.println("Average: " + average(prices, 3));   // prints 20.0 — correct
    }
}
```
**Why it works:** the loop now sums exactly `windowSize` elements (indices `0` to `windowSize - 1`), matching what "a window of size N" actually means, instead of reading one extra element past it.

##### Solution 8: Missing Null Check

```java
class CustomerProfile {
    private final String region;
    CustomerProfile(String region) { this.region = region; }
    String getRegion() { return region; }
}

class Customer {
    private final CustomerProfile profile;
    Customer(CustomerProfile profile) { this.profile = profile; }
    CustomerProfile getProfile() { return profile; }
}

public class Solution {
    static String getPreferredRegion(Customer customer) {
        if (customer == null) return "UNKNOWN";
        CustomerProfile profile = customer.getProfile();
        if (profile == null || profile.getRegion() == null) return "UNKNOWN";
        return profile.getRegion().toUpperCase();
    }

    public static void main(String[] argv) {
        Customer newCustomer = new Customer(null);
        System.out.println("Region: " + getPreferredRegion(newCustomer));   // prints UNKNOWN — correct
    }
}
```
**Why it works:** every link in the chain (`customer` → `profile` → `region`) is checked before being dereferenced, so an incomplete profile returns a safe, well-defined default instead of crashing.

##### Solution 9: SimpleDateFormat Shared Across Threads

```java
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Date;

class ReportGenerator {
    String formatDate(Date date) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");  // java.time, immutable & thread-safe
        return date.toInstant().atZone(ZoneId.systemDefault()).format(formatter);
    }
}

public class Solution {
    public static void main(String[] argv) throws InterruptedException {
        ReportGenerator generator = new ReportGenerator();
        int threadCount = 50;
        Thread[] threads = new Thread[threadCount];
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> System.out.println(generator.formatDate(new Date())));
            threads[i].start();
        }
        for (Thread t : threads) t.join();
        // every line prints a correctly formatted date string, every time — no corruption
    }
}
```
**Why it works:** `java.time.DateTimeFormatter` is immutable and thread-safe by design — unlike `SimpleDateFormat`, it has no internal mutable state to corrupt under concurrent access, so no synchronization is needed at all. (If stuck on an older codebase that must keep `SimpleDateFormat`, the alternative fix is a new instance per call, or a `ThreadLocal<SimpleDateFormat>` — but switching to `java.time` is the modern, preferred fix.)

##### Solution 10: Java Streams Misuse

```java
import java.util.*;

class Item {
    int quantity;
    boolean lowStock;
    Item(int quantity) { this.quantity = quantity; }
    int getQuantity() { return quantity; }
    void setLowStock(boolean v) { this.lowStock = v; }
    boolean isLowStock() { return lowStock; }
}

public class Solution {
    static void markLowStockItems(List<Item> items) {
        items.stream()
             .filter(i -> i.getQuantity() < 10)
             .forEach(i -> i.setLowStock(true));   // forEach is a terminal operation — triggers execution
    }

    public static void main(String[] argv) {
        List<Item> items = new ArrayList<>(List.of(new Item(5)));
        markLowStockItems(items);
        System.out.println("Low stock: " + items.get(0).isLowStock());   // prints true — correct
    }
}
```
**Why it works:** Java streams are lazy — nothing runs until a terminal operation (`forEach`, `collect`, `count`, etc.) is called. `peek()` is only an intermediate operation meant for side-effect debugging *alongside* a terminal op, not a replacement for one. Adding `forEach` (or any terminal op) actually executes the pipeline.

##### Solution 11: List Passed by Reference and Mutated by Callee

```java
import java.util.*;

public class Solution {
    static List<String> buildSummary(List<String> lineItems) {
        List<String> copy = new ArrayList<>(lineItems);   // defensive copy first
        Collections.sort(copy);
        copy.removeIf(s -> s.isBlank());
        return copy;
    }

    public static void main(String[] argv) {
        List<String> original = new ArrayList<>(List.of("b", "", "a"));
        List<String> summary = buildSummary(original);
        System.out.println("Original: " + original);   // unchanged: [b, , a]
        System.out.println("Summary:  " + summary);     // cleaned: [a, b]
    }
}
```
**Why it works:** operating on a fresh copy means the caller's original list is never touched — `Collections.sort()` and `removeIf()` only affect the local `copy`, so the method returns a cleaned result without any side effect on data the caller still owns a reference to.

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

#### Algo Practice (Segment 3) — Problem & Solution, Kept Separate

Each problem below is just the problem statement, example input/output, and a method signature — no name, no hint. Try to solve it yourself before jumping to the linked solution — all 16 solutions are collected separately in [Algo Solutions](#algo-solutions-segment-3) below.

1. [Algo Problem 1](#algo-problem-1)
2. [Algo Problem 2](#algo-problem-2)
3. [Algo Problem 3](#algo-problem-3)
4. [Algo Problem 4](#algo-problem-4)
5. [Algo Problem 5](#algo-problem-5)
6. [Algo Problem 6](#algo-problem-6)
7. [Algo Problem 7](#algo-problem-7)
8. [Algo Problem 8](#algo-problem-8)
9. [Algo Problem 9](#algo-problem-9)
10. [Algo Problem 10](#algo-problem-10)
11. [Algo Problem 11](#algo-problem-11)
12. [Algo Problem 12](#algo-problem-12)
13. [Algo Problem 13](#algo-problem-13)
14. [Algo Problem 14](#algo-problem-14)
15. [Algo Problem 15](#algo-problem-15)
16. [Algo Problem 16](#algo-problem-16)

##### Algo Problem 1
*(→ [Solution](#algo-solution-1-toll-booth-complete-journeys-counting))*

Given a string of events where each character is either `E` (a car entered the highway at a booth) or `X` (a car exited), count the number of **complete journeys** — an `E` matched by a later `X` — ignoring any `X` with no prior unmatched `E`, and ignoring any `E` that never gets a later `X`.

```
Example: "EEXXE"
Expected: 2
(two E's open; the two X's each close one of them, completing 2 journeys;
 the trailing E never gets an X, so it doesn't count)
```

```java
public class Solution {
    static int countCompleteJourneys(String events) {
        // TODO
        return 0;
    }

    public static void main(String[] argv) {
        System.out.println(countCompleteJourneys("EEXXE"));
        // Expected: 2
    }
}
```

##### Algo Problem 2
*(→ [Solution](#algo-solution-2-valid-parentheses))*

Given a string containing only the characters `(`, `)`, `{`, `}`, `[`, `]`, determine whether it is valid — every opening character must be closed by the matching type, in the correct order.

```
Example: "{[()]}"  → true
Example: "{[(])}"  → false
```

```java
public class Solution {
    static boolean isValid(String s) {
        // TODO
        return false;
    }

    public static void main(String[] argv) {
        System.out.println(isValid("{[()]}"));   // Expected: true
        System.out.println(isValid("{[(])}"));   // Expected: false
    }
}
```

##### Algo Problem 3
*(→ [Solution](#algo-solution-3-maximum-nesting-depth-of-brackets))*

Given a string containing only `(` and `)`, and guaranteed to be validly balanced, return the maximum depth of nesting.

```
Example: "((()))"  → 3
Example: "()()"    → 1
```

```java
public class Solution {
    static int maxDepth(String s) {
        // TODO
        return 0;
    }

    public static void main(String[] argv) {
        System.out.println(maxDepth("((()))"));   // Expected: 3
        System.out.println(maxDepth("()()"));     // Expected: 1
    }
}
```

##### Algo Problem 4
*(→ [Solution](#algo-solution-4-two-sum))*

Given an array of integers and a target value, return the indices of the two numbers that add up to the target. Exactly one valid pair exists.

```
Example: nums = [2,7,11,15], target = 9  → [0,1]
```

```java
import java.util.*;

public class Solution {
    static int[] twoSum(int[] nums, int target) {
        // TODO
        return new int[0];
    }

    public static void main(String[] argv) {
        System.out.println(Arrays.toString(twoSum(new int[]{2,7,11,15}, 9)));
        // Expected: [0, 1]
    }
}
```

##### Algo Problem 5
*(→ [Solution](#algo-solution-5-group-anagrams))*

Given an array of strings, group the strings that are anagrams of each other.

```
Example: ["eat","tea","tan","ate","nat","bat"]
Expected: [["eat","tea","ate"], ["tan","nat"], ["bat"]]   (order of groups/items doesn't matter)
```

```java
import java.util.*;

public class Solution {
    static List<List<String>> groupAnagrams(String[] strs) {
        // TODO
        return new ArrayList<>();
    }

    public static void main(String[] argv) {
        System.out.println(groupAnagrams(new String[]{"eat","tea","tan","ate","nat","bat"}));
        // Expected: [[eat, tea, ate], [tan, nat], [bat]]  (order may vary)
    }
}
```

##### Algo Problem 6
*(→ [Solution](#algo-solution-6-first-non-repeating-character))*

Given a string, return the first character that does not repeat anywhere else in the string. Return `'\0'` if every character repeats.

```
Example: "swiss"  → 'w'
```

```java
public class Solution {
    static char firstNonRepeating(String s) {
        // TODO
        return '\0';
    }

    public static void main(String[] argv) {
        System.out.println(firstNonRepeating("swiss"));   // Expected: w
    }
}
```

##### Algo Problem 7
*(→ [Solution](#algo-solution-7-count-pairs-with-given-sum))*

Given an array of integers and a target sum, count the number of index pairs `(i, j)` with `i < j` such that `nums[i] + nums[j] == target`.

```
Example: nums = [1,5,7,-1,5], target = 6  → 3
(pairs: (1,5) at indices 0&1, (1,5) at indices 0&4, (7,-1) at indices 2&3)
```

```java
public class Solution {
    static int countPairsWithSum(int[] nums, int target) {
        // TODO
        return 0;
    }

    public static void main(String[] argv) {
        System.out.println(countPairsWithSum(new int[]{1,5,7,-1,5}, 6));   // Expected: 3
    }
}
```

##### Algo Problem 8
*(→ [Solution](#algo-solution-8-best-single-buy-sell-for-max-profit))*

Given an array of daily stock prices, find the maximum profit achievable from buying on one day and selling on a later day (a single transaction only). Return 0 if no profit is possible.

```
Example: prices = [7,1,5,3,6,4]  → 5   (buy at 1, sell at 6)
```

```java
public class Solution {
    static int maxProfit(int[] prices) {
        // TODO
        return 0;
    }

    public static void main(String[] argv) {
        System.out.println(maxProfit(new int[]{7,1,5,3,6,4}));   // Expected: 5
    }
}
```

##### Algo Problem 9
*(→ [Solution](#algo-solution-9-merge-overlapping-intervals))*

Given a list of intervals, merge all overlapping intervals and return the result sorted by start.

```
Example: [[1,3],[2,6],[8,10],[15,18]]
Expected: [[1,6],[8,10],[15,18]]
```

```java
import java.util.*;

public class Solution {
    static List<int[]> mergeIntervals(List<int[]> intervals) {
        // TODO
        return new ArrayList<>();
    }

    public static void main(String[] argv) {
        List<int[]> intervals = new ArrayList<>(List.of(
            new int[]{1,3}, new int[]{2,6}, new int[]{8,10}, new int[]{15,18}
        ));
        for (int[] iv : mergeIntervals(intervals)) System.out.println(Arrays.toString(iv));
        // Expected: [1, 6] / [8, 10] / [15, 18]
    }
}
```

##### Algo Problem 10
*(→ [Solution](#algo-solution-10-sliding-window-max-min-sum-of-subarray-size-k))*

Given an array of integers and an integer `k`, find the maximum sum of any contiguous subarray of size `k`.

```
Example: nums = [2,1,5,1,3,2], k = 3  → 9   (subarray [5,1,3])
```

```java
public class Solution {
    static int maxSubarraySum(int[] nums, int k) {
        // TODO
        return 0;
    }

    public static void main(String[] argv) {
        System.out.println(maxSubarraySum(new int[]{2,1,5,1,3,2}, 3));   // Expected: 9
    }
}
```

##### Algo Problem 11
*(→ [Solution](#algo-solution-11-find-duplicate-or-missing-number-in-array))*

An array of length `n` is supposed to contain every integer from `1` to `n` exactly once, but one number got overwritten by a duplicate of another, so one number is missing and one appears twice. Return `[duplicate, missing]`.

```
Example: nums = [1,2,2,4]  → [2,3]
```

```java
import java.util.*;

public class Solution {
    static int[] findDuplicateAndMissing(int[] nums) {
        // TODO
        return new int[0];
    }

    public static void main(String[] argv) {
        System.out.println(Arrays.toString(findDuplicateAndMissing(new int[]{1,2,2,4})));
        // Expected: [2, 3]
    }
}
```

##### Algo Problem 12
*(→ [Solution](#algo-solution-12-running-prefix-sum))*

Given an array of integers, support repeated range-sum queries `sum(l, r)` (inclusive) as efficiently as possible after a one-time setup cost.

```
Example: nums = [1,2,3,4,5]
sum(1,3) → 2+3+4 = 9
```

```java
class RangeSummer {
    RangeSummer(int[] nums) {
        // TODO
    }
    int sum(int l, int r) {
        // TODO
        return 0;
    }
}

public class Solution {
    public static void main(String[] argv) {
        RangeSummer rs = new RangeSummer(new int[]{1,2,3,4,5});
        System.out.println(rs.sum(1, 3));   // Expected: 9
    }
}
```

##### Algo Problem 13
*(→ [Solution](#algo-solution-13-string-run-length-compression))*

Given a string, compress runs of consecutive repeated characters into `char + count` form (omit the count when it's 1). Return the compressed string only if it's actually shorter than the original; otherwise return the original unchanged.

```
Example: "aabcccccaaa"  → "a2bc5a3"
Example: "abc"          → "abc"   (compressed form "a1b1c1" is longer, so keep original)
```

```java
public class Solution {
    static String compress(String s) {
        // TODO
        return s;
    }

    public static void main(String[] argv) {
        System.out.println(compress("aabcccccaaa"));   // Expected: a2bc5a3
        System.out.println(compress("abc"));            // Expected: abc
    }
}
```

##### Algo Problem 14
*(→ [Solution](#algo-solution-14-check-if-two-strings-are-anagrams))*

Given two strings, determine whether one is a rearrangement of the other's characters (same characters, same frequency, any order).

```
Example: "listen", "silent"  → true
Example: "rat", "car"        → false
```

```java
public class Solution {
    static boolean isAnagram(String a, String b) {
        // TODO
        return false;
    }

    public static void main(String[] argv) {
        System.out.println(isAnagram("listen", "silent"));   // Expected: true
        System.out.println(isAnagram("rat", "car"));          // Expected: false
    }
}
```

##### Algo Problem 15
*(→ [Solution](#algo-solution-15-reverse-words-in-place))*

Given a sentence, return it with the order of its words reversed — the characters within each word stay in their original order.

```
Example: "the sky is blue"  → "blue is sky the"
```

```java
public class Solution {
    static String reverseWords(String s) {
        // TODO
        return s;
    }

    public static void main(String[] argv) {
        System.out.println(reverseWords("the sky is blue"));   // Expected: blue is sky the
    }
}
```

##### Algo Problem 16
*(→ [Solution](#algo-solution-16-rotate-array-by-k-positions))*

Given an array and a non-negative integer `k`, rotate the array to the right by `k` steps, in place.

```
Example: nums = [1,2,3,4,5,6,7], k = 3  → [5,6,7,1,2,3,4]
```

```java
import java.util.*;

public class Solution {
    static void rotate(int[] nums, int k) {
        // TODO
    }

    public static void main(String[] argv) {
        int[] nums = {1,2,3,4,5,6,7};
        rotate(nums, 3);
        System.out.println(Arrays.toString(nums));
        // Expected: [5, 6, 7, 1, 2, 3, 4]
    }
}
```

---

#### Algo Solutions (Segment 3)

##### Algo Solution 1: Toll-Booth Complete Journeys Counting

```java
public class Solution {
    static int countCompleteJourneys(String events) {
        int open = 0, complete = 0;
        for (char c : events.toCharArray()) {
            if (c == 'E') {
                open++;
            } else if (c == 'X' && open > 0) {
                open--;
                complete++;
            }
            // an 'X' with open == 0 is an orphan exit — ignored
        }
        return complete;   // any leftover `open` entries never got a matching X — ignored too
    }

    public static void main(String[] argv) {
        System.out.println(countCompleteJourneys("EEXXE"));   // prints 2 — correct
    }
}
```
**Complexity:** O(n) time, O(1) space. **Why it works:** `open` tracks entries not yet closed; `complete` only increments on an actual matching close, so orphan exits and unfinished entries are naturally excluded without any extra bookkeeping.

##### Algo Solution 2: Valid Parentheses

```java
import java.util.*;

public class Solution {
    static boolean isValid(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        Map<Character, Character> pairs = Map.of(')', '(', ']', '[', '}', '{');
        for (char c : s.toCharArray()) {
            if (pairs.containsValue(c)) {
                stack.push(c);
            } else if (pairs.containsKey(c)) {
                if (stack.isEmpty() || stack.pop() != pairs.get(c)) return false;
            }
        }
        return stack.isEmpty();
    }

    public static void main(String[] argv) {
        System.out.println(isValid("{[()]}"));   // prints true — correct
        System.out.println(isValid("{[(])}"));   // prints false — correct
    }
}
```
**Complexity:** O(n) time, O(n) space. **Why it works:** a stack naturally captures "most recently opened, must be closed first" — pushing on open, popping and checking on close, and requiring an empty stack at the end to reject any unclosed brackets.

##### Algo Solution 3: Maximum Nesting Depth of Brackets

```java
public class Solution {
    static int maxDepth(String s) {
        int depth = 0, max = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') { depth++; max = Math.max(max, depth); }
            else if (c == ')') depth--;
        }
        return max;
    }

    public static void main(String[] argv) {
        System.out.println(maxDepth("((()))"));   // prints 3 — correct
        System.out.println(maxDepth("()()"));     // prints 1 — correct
    }
}
```
**Complexity:** O(n) time, O(1) space. **Why it works:** depth only needs a running counter, not an actual stack — tracking the current open count and recording its peak is enough.

##### Algo Solution 4: Two Sum

```java
import java.util.*;

public class Solution {
    static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();   // value -> index
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (seen.containsKey(complement)) return new int[]{seen.get(complement), i};
            seen.put(nums[i], i);
        }
        throw new IllegalArgumentException("no valid pair");
    }

    public static void main(String[] argv) {
        System.out.println(Arrays.toString(twoSum(new int[]{2,7,11,15}, 9)));   // prints [0, 1] — correct
    }
}
```
**Complexity:** O(n) time, O(n) space. **Why it works:** instead of checking every pair (O(n²)), each number is checked against a running hashmap of everything seen so far — the complement either is or isn't already there, in O(1).

##### Algo Solution 5: Group Anagrams

```java
import java.util.*;

public class Solution {
    static List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> groups = new HashMap<>();
        for (String s : strs) {
            char[] chars = s.toCharArray();
            Arrays.sort(chars);
            String key = new String(chars);          // canonical form, e.g. "eat" -> "aet"
            groups.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(groups.values());
    }

    public static void main(String[] argv) {
        System.out.println(groupAnagrams(new String[]{"eat","tea","tan","ate","nat","bat"}));
        // prints [[eat, tea, ate], [tan, nat], [bat]] (order may vary) — correct
    }
}
```
**Complexity:** O(n · k log k) time (n strings, k = max string length), O(n · k) space. **Why it works:** anagrams share the exact same sorted character sequence, so sorting each string gives a canonical key that groups them automatically via a hashmap.

##### Algo Solution 6: First Non-Repeating Character

```java
public class Solution {
    static char firstNonRepeating(String s) {
        int[] count = new int[256];
        for (char c : s.toCharArray()) count[c]++;
        for (char c : s.toCharArray()) {
            if (count[c] == 1) return c;
        }
        return '\0';
    }

    public static void main(String[] argv) {
        System.out.println(firstNonRepeating("swiss"));   // prints w — correct
    }
}
```
**Complexity:** O(n) time, O(1) space (fixed-size count array). **Why it works:** one pass builds frequency counts, a second pass finds the first character whose count is exactly 1 — two linear passes beat checking every character against the rest of the string (O(n²)).

##### Algo Solution 7: Count Pairs With Given Sum

```java
import java.util.*;

public class Solution {
    static int countPairsWithSum(int[] nums, int target) {
        Map<Integer, Integer> seenCount = new HashMap<>();
        int count = 0;
        for (int n : nums) {
            int complement = target - n;
            count += seenCount.getOrDefault(complement, 0);
            seenCount.merge(n, 1, Integer::sum);
        }
        return count;
    }

    public static void main(String[] argv) {
        System.out.println(countPairsWithSum(new int[]{1,5,7,-1,5}, 6));   // prints 3 — correct
    }
}
```
**Complexity:** O(n) time, O(n) space. **Why it works:** for each number, every earlier occurrence of its complement forms a valid pair with it — a running frequency map lets each element find how many valid partners already came before it, in O(1) per element.

##### Algo Solution 8: Best Single Buy-Sell for Max Profit

```java
public class Solution {
    static int maxProfit(int[] prices) {
        int minSoFar = Integer.MAX_VALUE, maxProfit = 0;
        for (int price : prices) {
            minSoFar = Math.min(minSoFar, price);
            maxProfit = Math.max(maxProfit, price - minSoFar);
        }
        return maxProfit;
    }

    public static void main(String[] argv) {
        System.out.println(maxProfit(new int[]{7,1,5,3,6,4}));   // prints 5 — correct
    }
}
```
**Complexity:** O(n) time, O(1) space. **Why it works:** the best sell price on any given day only needs to know the lowest buy price *seen so far* — tracked as a single running minimum — rather than re-checking every earlier day.

##### Algo Solution 9: Merge Overlapping Intervals

```java
import java.util.*;

public class Solution {
    static List<int[]> mergeIntervals(List<int[]> intervals) {
        intervals.sort((a, b) -> a[0] - b[0]);
        List<int[]> merged = new ArrayList<>();
        for (int[] interval : intervals) {
            if (merged.isEmpty() || merged.get(merged.size() - 1)[1] < interval[0]) {
                merged.add(interval);
            } else {
                merged.get(merged.size() - 1)[1] = Math.max(merged.get(merged.size() - 1)[1], interval[1]);
            }
        }
        return merged;
    }

    public static void main(String[] argv) {
        List<int[]> intervals = new ArrayList<>(List.of(
            new int[]{1,3}, new int[]{2,6}, new int[]{8,10}, new int[]{15,18}
        ));
        for (int[] iv : mergeIntervals(intervals)) System.out.println(Arrays.toString(iv));
        // prints [1, 6] / [8, 10] / [15, 18] — correct
    }
}
```
**Complexity:** O(n log n) time (dominated by the sort), O(n) space. **Why it works:** once sorted by start, two intervals can only ever overlap with their immediate neighbor in the sorted order — so a single pass extending the last merged interval (or starting a new one) is sufficient.

##### Algo Solution 10: Sliding Window Max-Min Sum of Subarray Size K

```java
public class Solution {
    static int maxSubarraySum(int[] nums, int k) {
        int windowSum = 0;
        for (int i = 0; i < k; i++) windowSum += nums[i];
        int maxSum = windowSum;
        for (int i = k; i < nums.length; i++) {
            windowSum += nums[i] - nums[i - k];   // slide: add new element, drop the oldest
            maxSum = Math.max(maxSum, windowSum);
        }
        return maxSum;
    }

    public static void main(String[] argv) {
        System.out.println(maxSubarraySum(new int[]{2,1,5,1,3,2}, 3));   // prints 9 — correct
    }
}
```
**Complexity:** O(n) time, O(1) space. **Why it works:** recomputing the sum of each new window from scratch is O(n·k); instead, sliding the window by adding the new element and subtracting the one that just fell out of range keeps each step O(1).

##### Algo Solution 11: Find Duplicate or Missing Number in Array

```java
import java.util.*;

public class Solution {
    static int[] findDuplicateAndMissing(int[] nums) {
        int n = nums.length;
        int[] count = new int[n + 1];
        for (int x : nums) count[x]++;
        int duplicate = -1, missing = -1;
        for (int i = 1; i <= n; i++) {
            if (count[i] == 2) duplicate = i;
            if (count[i] == 0) missing = i;
        }
        return new int[]{duplicate, missing};
    }

    public static void main(String[] argv) {
        System.out.println(Arrays.toString(findDuplicateAndMissing(new int[]{1,2,2,4})));   // prints [2, 3] — correct
    }
}
```
**Complexity:** O(n) time, O(n) space. **Why it works:** every value from 1 to n should appear exactly once; counting occurrences directly reveals which value appears twice (the duplicate) and which never appears (the missing one).

##### Algo Solution 12: Running Prefix Sum

```java
class RangeSummer {
    private final int[] prefix;

    RangeSummer(int[] nums) {
        prefix = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
    }

    int sum(int l, int r) {
        return prefix[r + 1] - prefix[l];
    }
}

public class Solution {
    public static void main(String[] argv) {
        RangeSummer rs = new RangeSummer(new int[]{1,2,3,4,5});
        System.out.println(rs.sum(1, 3));   // prints 9 — correct
    }
}
```
**Complexity:** O(n) one-time setup, O(1) per query. **Why it works:** `prefix[i]` holds the sum of everything before index `i`; any range sum is just the difference of two prefix values, avoiding re-summing the range on every query.

##### Algo Solution 13: String Run-Length Compression

```java
public class Solution {
    static String compress(String s) {
        StringBuilder sb = new StringBuilder();
        int i = 0;
        while (i < s.length()) {
            char current = s.charAt(i);
            int count = 0;
            while (i < s.length() && s.charAt(i) == current) { count++; i++; }
            sb.append(current);
            if (count > 1) sb.append(count);
        }
        return sb.length() < s.length() ? sb.toString() : s;
    }

    public static void main(String[] argv) {
        System.out.println(compress("aabcccccaaa"));   // prints a2bc5a3 — correct
        System.out.println(compress("abc"));            // prints abc — correct
    }
}
```
**Complexity:** O(n) time, O(n) space. **Why it works:** a single pass counts each run of identical consecutive characters as it goes; the length check at the end enforces the "only if actually shorter" requirement.

##### Algo Solution 14: Check if Two Strings Are Anagrams

```java
public class Solution {
    static boolean isAnagram(String a, String b) {
        if (a.length() != b.length()) return false;
        int[] count = new int[256];
        for (char c : a.toCharArray()) count[c]++;
        for (char c : b.toCharArray()) count[c]--;
        for (int n : count) if (n != 0) return false;
        return true;
    }

    public static void main(String[] argv) {
        System.out.println(isAnagram("listen", "silent"));   // prints true — correct
        System.out.println(isAnagram("rat", "car"));          // prints false — correct
    }
}
```
**Complexity:** O(n) time, O(1) space. **Why it works:** incrementing counts for one string and decrementing for the other means every matching character cancels out to zero — any leftover nonzero count means the character frequencies didn't match.

##### Algo Solution 15: Reverse Words in Place

```java
public class Solution {
    static String reverseWords(String s) {
        String[] words = s.trim().split("\\s+");
        StringBuilder sb = new StringBuilder();
        for (int i = words.length - 1; i >= 0; i--) {
            sb.append(words[i]);
            if (i > 0) sb.append(' ');
        }
        return sb.toString();
    }

    public static void main(String[] argv) {
        System.out.println(reverseWords("the sky is blue"));   // prints "blue is sky the" — correct
    }
}
```
**Complexity:** O(n) time, O(n) space. **Why it works:** splitting on whitespace isolates each word intact, then appending them back in reverse order flips word order without touching the characters inside each word.

##### Algo Solution 16: Rotate Array by K Positions

```java
import java.util.*;

public class Solution {
    static void rotate(int[] nums, int k) {
        int n = nums.length;
        k %= n;
        reverse(nums, 0, n - 1);
        reverse(nums, 0, k - 1);
        reverse(nums, k, n - 1);
    }

    private static void reverse(int[] nums, int lo, int hi) {
        while (lo < hi) {
            int tmp = nums[lo];
            nums[lo] = nums[hi];
            nums[hi] = tmp;
            lo++; hi--;
        }
    }

    public static void main(String[] argv) {
        int[] nums = {1,2,3,4,5,6,7};
        rotate(nums, 3);
        System.out.println(Arrays.toString(nums));   // prints [5, 6, 7, 1, 2, 3, 4] — correct
    }
}
```
**Complexity:** O(n) time, O(1) space. **Why it works:** reversing the whole array, then reversing each of the two resulting segments separately, is a classic trick that produces an in-place rotation — the segments end up in the rotated order without needing a second array. (`k %= n` first handles `k` larger than the array length.)

### Bonus — OOP Design & Code-Review (also confirmed, sometimes substituted in)
- Small OOP design from a one-paragraph spec: design 2–3 classes for something like a parking lot, ATM, rate limiter, or LRU cache — practice stating each class's single responsibility **out loud before coding**
- Code-review drill: take any medium-complexity function, explain what it does, then state 2–3 concrete improvements **without silently rewriting it** — communication is graded here as much as the fix itself
