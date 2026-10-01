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
- Checked vs. unchecked exceptions — pros/cons, when to use which
- What does "effectively final" mean, and why does it matter for lambdas/anonymous inner classes?
- How does Spring wire beans? (`@Component`/`@Service`/`@Repository`, `@Autowired`, constructor vs. field injection, singleton vs. prototype scope)
- Why is `@Transactional` silently ignored when called via `new` or self-invocation (`this.method()`)? — proxy-based AOP gotcha
- The `equals()`/`hashCode()` contract — what breaks if you override one but not the other, or omit a field
- `HashMap` vs. `HashSet` vs. `TreeMap` — how each relies on `equals()`/`hashCode()`/`compareTo()`
- Why immutable objects are inherently thread-safe
- `volatile` vs. `synchronized` vs. `AtomicInteger` — when each is enough
- `==` vs. `.equals()` for objects, and the String pool gotcha
- Interfaces vs. abstract classes — when to pick which
- `ConcurrentModificationException` — when it fires, how to avoid it (iterator vs. `removeIf`)
- Checked exception wrapped into a `RuntimeException` — why and when you'd do that

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
