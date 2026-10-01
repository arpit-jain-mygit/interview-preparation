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
        return symbol.equals(other.symbol);   // BUG: only checks symbol
    }

    @Override
    public int hashCode() {
        return symbol.hashCode();             // BUG: only hashes symbol
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

// Failing test:
// incomingFeed = [ Trade("AAPL","BUY",100,150.0), Trade("AAPL","SELL",50,151.0) ]
// bookedLedger  = [ Trade("AAPL","BUY",100,150.0) ]
// Expected: unbooked contains the AAPL SELL trade (it's genuinely not booked)
// Actual:   unbooked is EMPTY — both trades are "equal" because equals()/hashCode() only look at symbol
```

##### Problem 2
*(→ [Solution](#solution-2-string-to-numeric-parsing-bug))*

```java
class PriceFeed {
    double computeTotal(String[] priceStrings) {
        double total = 0;
        for (String p : priceStrings) {
            total += Float.parseFloat(p);   // BUG: throws on "N/A", "", or null entries
        }
        return total;
    }
}

// Failing test:
// priceStrings = {"150.25", "N/A", "99.50"}
// Expected: total = 249.75 (skip unparseable entries)
// Actual:   throws NumberFormatException on "N/A", test never reaches the assertion
```

##### Problem 3
*(→ [Solution](#solution-3-transactional-ignored-because-built-with-new))*

```java
@Service
class RatingService {
    @Transactional
    void rate(Rating rating) {
        validate(rating);
        RatingHistoryBuilder builder = new RatingHistoryBuilder();  // BUG: plain `new`, not a Spring bean
        builder.record(rating);   // @Transactional(REQUIRES_NEW) on this method is silently ignored
    }
}

class RatingHistoryBuilder {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    void record(Rating rating) {
        if (rating.getScore() < 0) throw new IllegalArgumentException("bad score");
        // ... persist history row ...
    }
}

// Failing test:
// A bad rating.getScore() throws inside record()
// Expected: only the history-record attempt rolls back; the earlier validate()'d rating still commits
// Actual:   the exception rolls back the ENTIRE outer transaction — everything is lost
```

##### Problem 4
*(→ [Solution](#solution-4-reference-equality-instead-of-equals))*

```java
class OrderLookup {
    boolean isDuplicateOrderId(String incomingId, String lastProcessedId) {
        return incomingId == lastProcessedId;   // BUG: reference comparison on Strings
    }
}

// Failing test:
// incomingId = new String("ORD-1001")   // built at runtime, e.g. from a parsed request body
// lastProcessedId = "ORD-1001"          // a literal
// Expected: isDuplicateOrderId returns true (same order ID)
// Actual:   returns false — different String objects, == compares references, not content
```

##### Problem 5
*(→ [Solution](#solution-5-mutable-key-mutated-after-insertion))*

```java
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

class BalanceCache {
    Map<AccountKey, Double> cache = new HashMap<>();

    void test() {
        AccountKey key = new AccountKey("APAC", 42);
        cache.put(key, 1000.0);
        key.region = "EMEA";                 // BUG: mutating the key after it's already in the map
        Double balance = cache.get(new AccountKey("APAC", 42));
        // Expected: 1000.0
        // Actual:   null — the key's hashCode changed, so it now lives in the wrong bucket
    }
}
```

##### Problem 6
*(→ [Solution](#solution-6-wrong-comparator-implementation))*

```java
class TradeByPriceComparator implements Comparator<Trade> {
    @Override
    public int compare(Trade a, Trade b) {
        return (int) (a.price - b.price);   // BUG: truncates/overflows for close or large doubles
    }
}

// Failing test:
// trades with prices 100.3 and 100.7 → (int)(100.3 - 100.7) = (int)(-0.4) = 0 ("equal," wrong)
// Expected: sorted ascending by price, 100.3 before 100.7
// Actual:   sort is unstable/wrong because compare() returns 0 for genuinely different prices
```

##### Problem 7
*(→ [Solution](#solution-7-off-by-one-loop-bound))*

```java
class MovingAverage {
    double average(int[] prices, int windowSize) {
        int sum = 0;
        for (int i = 0; i <= windowSize; i++) {   // BUG: <= instead of <, reads one past the window
            sum += prices[i];
        }
        return (double) sum / windowSize;
    }
}

// Failing test:
// prices = {10, 20, 30, 40}, windowSize = 3
// Expected: average of {10,20,30} = 20.0
// Actual:   either wrong average (includes prices[3]=40) or ArrayIndexOutOfBoundsException if windowSize == prices.length - 1
```

##### Problem 8
*(→ [Solution](#solution-8-missing-null-check))*

```java
class CustomerService {
    String getPreferredRegion(Customer customer) {
        return customer.getProfile().getRegion().toUpperCase();   // BUG: no null checks anywhere in the chain
    }
}

// Failing test:
// customer.getProfile() returns null for a newly-registered customer with no profile yet
// Expected: getPreferredRegion returns a safe default, e.g. "UNKNOWN"
// Actual:   throws NullPointerException — intermittent in production because it only happens for incomplete profiles
```

##### Problem 9
*(→ [Solution](#solution-9-simpledateformat-shared-across-threads))*

```java
class ReportGenerator {
    private static final SimpleDateFormat FORMAT = new SimpleDateFormat("yyyy-MM-dd");  // BUG: shared, not thread-safe

    String formatDate(Date date) {
        return FORMAT.format(date);   // internal Calendar state gets corrupted under concurrent calls
    }
}

// Failing test (run under concurrent load, e.g. 50 threads calling formatDate simultaneously):
// Expected: every call returns a correctly formatted date string
// Actual:   intermittently throws NumberFormatException or returns a garbled/wrong date,
//           because SimpleDateFormat mutates internal Calendar fields and isn't synchronized
```

##### Problem 10
*(→ [Solution](#solution-10-java-streams-misuse))*

```java
class InventoryService {
    void markLowStockItems(List<Item> items) {
        items.stream()
             .filter(i -> i.getQuantity() < 10)
             .peek(i -> i.setLowStock(true));   // BUG: peek() with no terminal operation — stream never runs
    }
}

// Failing test:
// items contain one item with quantity = 5
// Expected: that item's isLowStock() is true after markLowStockItems() runs
// Actual:   isLowStock() is still false — the stream pipeline was never actually executed,
//           because `peek` is an intermediate op and there's no terminal op (forEach/collect/count) to trigger it
```

##### Problem 11
*(→ [Solution](#solution-11-list-passed-by-reference-and-mutated-by-callee))*

```java
class ReportBuilder {
    List<String> buildSummary(List<String> lineItems) {
        Collections.sort(lineItems);     // BUG: sorts the CALLER's list in place, no copy made
        lineItems.removeIf(s -> s.isBlank());
        return lineItems;
    }
}

// Failing test:
// List<String> original = new ArrayList<>(List.of("b", "", "a"));
// List<String> summary = reportBuilder.buildSummary(original);
// Expected: `original` is untouched (still ["b", "", "a"]); `summary` is the cleaned, sorted copy
// Actual:   `original` itself is now sorted and blank-filtered too — the caller's own list was silently mutated
```

---

#### Code Solutions (Segment 2)

##### Solution 1: equals and hashCode Using Only Partial Fields

```java
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
```
**Why it works:** identity now depends on every field that actually distinguishes two trades. The AAPL BUY and AAPL SELL trades no longer collide — `reconcile()` correctly returns the unbooked SELL. Target complexity stays O(n + m) time, O(m) space (unchanged — this is purely a correctness fix, not a performance one).

##### Solution 2: String to Numeric Parsing Bug

```java
double computeTotal(String[] priceStrings) {
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
```
**Why it works:** unparseable or missing entries are explicitly skipped instead of crashing the whole computation — the loop keeps going and the valid entries still sum correctly.

##### Solution 3: Transactional Ignored Because Built with new

See the full walkthrough in [citi.md §23's Rating Microservice scenario](https://github.com/arpit-jain-mygit/interview-preparation/blob/main/curated/citi.md#project-scenario-rating-microservice-transaction-bug).

```java
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
}

@Component   // now a real Spring bean
class RatingHistoryBuilder {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    void record(Rating rating) {
        if (rating.getScore() < 0) throw new IllegalArgumentException("bad score");
    }
}
```
**Why it works:** `RatingHistoryBuilder` is now a container-managed bean, injected via the constructor. Spring wraps it in a real AOP proxy, so `REQUIRES_NEW` actually creates an independent transaction. A failure in `record()` now rolls back only its own transaction — the outer `rate()` transaction (and whatever it already did) is unaffected.

##### Solution 4: Reference Equality Instead of equals

```java
boolean isDuplicateOrderId(String incomingId, String lastProcessedId) {
    return incomingId.equals(lastProcessedId);   // content comparison, not reference
}
```
**Why it works:** `.equals()` compares the actual characters, not whether both variables happen to point at the same pooled/cached object — so it correctly matches `"ORD-1001"` regardless of whether either String came from a literal or was built at runtime.

##### Solution 5: Mutable Key Mutated After Insertion

```java
class AccountKey {
    final String region;          // make fields final
    final int accountNumber;
    AccountKey(String region, int accountNumber) {
        this.region = region;
        this.accountNumber = accountNumber;
    }
    // no setters — equals()/hashCode() unchanged
}
```
**Why it works:** once `region` and `accountNumber` are `final` with no setters, the key is immutable — nobody can change it after it's been inserted, so its `hashCode()` can never drift away from the bucket it was originally placed in. (This is the same idea as [A7 — Why Immutable Objects Are Thread-Safe](#a7-why-immutable-objects-are-thread-safe): removing the possibility of mutation removes the whole class of bug.)

##### Solution 6: Wrong Comparator Implementation

```java
class TradeByPriceComparator implements Comparator<Trade> {
    @Override
    public int compare(Trade a, Trade b) {
        return Double.compare(a.price, b.price);   // correct, no precision loss
    }
}
```
**Why it works:** `Double.compare()` handles the full precision of both values directly instead of subtracting and truncating to `int`, so close values (100.3 vs 100.7) are never incorrectly collapsed to "equal."

##### Solution 7: Off-by-One Loop Bound

```java
double average(int[] prices, int windowSize) {
    int sum = 0;
    for (int i = 0; i < windowSize; i++) {   // strict < , stays inside the window
        sum += prices[i];
    }
    return (double) sum / windowSize;
}
```
**Why it works:** the loop now sums exactly `windowSize` elements (indices `0` to `windowSize - 1`), matching what "a window of size N" actually means, instead of reading one extra element past it.

##### Solution 8: Missing Null Check

```java
String getPreferredRegion(Customer customer) {
    if (customer == null) return "UNKNOWN";
    CustomerProfile profile = customer.getProfile();
    if (profile == null || profile.getRegion() == null) return "UNKNOWN";
    return profile.getRegion().toUpperCase();
}
```
**Why it works:** every link in the chain (`customer` → `profile` → `region`) is checked before being dereferenced, so an incomplete profile returns a safe, well-defined default instead of crashing.

##### Solution 9: SimpleDateFormat Shared Across Threads

```java
class ReportGenerator {
    String formatDate(Date date) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");  // java.time, immutable & thread-safe
        return date.toInstant().atZone(ZoneId.systemDefault()).format(formatter);
    }
}
```
**Why it works:** `java.time.DateTimeFormatter` is immutable and thread-safe by design — unlike `SimpleDateFormat`, it has no internal mutable state to corrupt under concurrent access, so no synchronization is needed at all. (If stuck on an older codebase that must keep `SimpleDateFormat`, the alternative fix is a new instance per call, or a `ThreadLocal<SimpleDateFormat>` — but switching to `java.time` is the modern, preferred fix.)

##### Solution 10: Java Streams Misuse

```java
void markLowStockItems(List<Item> items) {
    items.stream()
         .filter(i -> i.getQuantity() < 10)
         .forEach(i -> i.setLowStock(true));   // forEach is a terminal operation — triggers execution
}
```
**Why it works:** Java streams are lazy — nothing runs until a terminal operation (`forEach`, `collect`, `count`, etc.) is called. `peek()` is only an intermediate operation meant for side-effect debugging *alongside* a terminal op, not a replacement for one. Adding `forEach` (or any terminal op) actually executes the pipeline.

##### Solution 11: List Passed by Reference and Mutated by Callee

```java
List<String> buildSummary(List<String> lineItems) {
    List<String> copy = new ArrayList<>(lineItems);   // defensive copy first
    Collections.sort(copy);
    copy.removeIf(s -> s.isBlank());
    return copy;
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

### Bonus — OOP Design & Code-Review (also confirmed, sometimes substituted in)
- Small OOP design from a one-paragraph spec: design 2–3 classes for something like a parking lot, ATM, rate limiter, or LRU cache — practice stating each class's single responsibility **out loud before coding**
- Code-review drill: take any medium-complexity function, explain what it does, then state 2–3 concrete improvements **without silently rewriting it** — communication is graded here as much as the fix itself
