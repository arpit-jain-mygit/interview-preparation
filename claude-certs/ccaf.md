# Claude Certified Architect - Foundations (CCAF)

Study notes from Ankit Mistry's Udemy course slides, one section per exam domain.

## Table of Contents

- [Domain 1: Agentic Architecture & Orchestration](#domain-1-agentic-architecture--orchestration)
  - [1.1 The agentic loop](#11-the-agentic-loop)
  - [1.2 Coordinator-subagent pattern](#12-coordinator-subagent-pattern)
  - [1.3 Spawning subagents and passing context](#13-spawning-subagents-and-passing-context)
  - [1.4 Enforcement and handoffs](#14-enforcement-and-handoffs)
  - [1.5 Agent SDK hooks](#15-agent-sdk-hooks)
  - [1.6 Task decomposition](#16-task-decomposition)
  - [1.7 Session state](#17-session-state)
  - [Domain 1 exam decision reflexes](#domain-1-exam-decision-reflexes)

---

## Domain 1: Agentic Architecture & Orchestration

### 1.1 The agentic loop

- **Chatbot vs. agent:** a chatbot answers once. An agent runs a loop: it calls tools, reads the results and keeps going until the job is done.
- **Four steps, repeated:** Perceive → Reason → Act (call a tool) → Observe (read the result).
- **`stop_reason` drives the loop:**
  - `tool_use` means run the tool, send the result back and loop again.
  - `end_turn` means Claude is done, so stop.
- **Send results back** as a `tool_result` added to the conversation. If you skip this, Claude never sees what the tool found.
- **Worked example (refund for order 9931):** `look_up_order` → no refund on file → `check_refund_policy` → eligible → `end_turn` with an explanation. Claude picks each tool based on the previous result; there is no fixed script.
- **Model-driven beats hardcoded:** for anything non-trivial, the exam prefers letting Claude choose the next tool over writing every if/else branch. Hardcoded logic is brittle.
- **Three anti-patterns (common wrong answers):**
  - ignoring `stop_reason`
  - no end condition, so the loop never stops
  - not sending tool results back

### 1.2 Coordinator-subagent pattern

- **Why:** one agent doing research, analysis and writing gets a cluttered context and loses focus. Splitting the work across specialists keeps each one sharp.
- **Hub-and-spoke:** subagents never talk to each other. Everything goes through the coordinator, which gives one place to see everything and handle errors.
- **Isolated context is the benefit:** each subagent sees only its own task. Use the pattern for tasks with separable parts. Simple single-threaded jobs don't need a coordinator.
- **The coordinator's four jobs:** Route, Manage errors, Select which subagents to run, Synthesize the results. It manages; it doesn't do the work itself.
- **Sequential vs. parallel:** if parts depend on each other, run them in sequence (research → analyze → write). If they're independent, run them in parallel, which is faster.
- **Iterative refinement:** delegate → synthesize → check quality → re-delegate if the result falls short.
- **Narrow-decomposition trap:** the pieces must add up to the whole question. Example: "creative industries" split into only a visual-arts subagent misses music, film and design.

### 1.3 Spawning subagents and passing context

- **Task tool:** the coordinator spawns a subagent with a tool call. The subagent runs its own loop in its own isolated context.
- **An agent definition has four parts:** `description` (tells the coordinator *when* to use it, so write it clearly), `prompt` (how it behaves), `tools` (what it can use) and `model` (optional; a cheaper model works for simple subagents).
- **Scope tools tightly:** give each subagent only the tools its job needs. A research agent gets search, not the refund tool.
- **Parallelism:** several Task calls in one turn run the subagents in parallel.
- **No automatic inheritance (the #1 mistake):** a subagent starts blank. It doesn't see the coordinator's conversation or other subagents' findings.
- **The prompt is the handoff:** put the goal, the relevant facts and the full prior findings into it, in a structured format. A vague one-line summary isn't enough.
- **Give goals, not steps:** state the goal and quality bar ("top 3, with sources") and let the subagent work out how.

### 1.4 Enforcement and handoffs

- **Prompt vs. code:** a prompt gives *probable* compliance. Code gives *guaranteed* (deterministic) compliance.
- **When to enforce in code:** ask what happens if Claude ignores the rule once. If the answer is serious harm, the rule belongs in code. Examples: identity checks before payments, refund limits, safety and compliance gates.
- **Prerequisite gates:** code blocks an action (such as a refund) until a required step (such as identity verification) is done, so Claude cannot skip ahead.
- **Escalation:** hand risky or unclear cases to a human with a structured summary: the customer, the issue, what has been done and a recommended action.

### 1.5 Agent SDK hooks

- A **hook** is code that runs automatically before or after every tool call. It can inspect, change or block what happens.
- **PreToolUse** fires before the tool runs. It can allow the call, change its input or block it. The standard example: block any refund over $500 and route it to a human.
- **PostToolUse** fires after the tool runs, before Claude reads the result. It can transform the result (for example, normalize messy timestamps) and is good for logging.
- In short, PreToolUse guards what goes out and PostToolUse shapes what comes back.
- **Exam reflex:** "this rule must never break" calls for a hook, not a prompt.

### 1.6 Task decomposition

- **Why decompose:** smaller subtasks are more focused, easier to check and more reliable, and independent pieces can run in parallel.
- **Three strategies:**
  - **Sequential:** fixed order where each step feeds the next (extract → validate → format).
  - **Parallel:** independent steps at once (check 5 files simultaneously).
  - **Adaptive (dynamic):** subtasks are discovered as you go (investigate → find leads → spawn follow-ups). Fits research, debugging and exploration.
- **Mapping to patterns:**
  - Fixed, known steps → **prompt chaining** (a pipeline where each output becomes the next input; simple and predictable).
  - Steps discovered along the way → **orchestrator-workers** (a coordinator directing subagents; flexible).
  - The deciding question: can you list the steps upfront?
- **Code review example:** run per-file passes in parallel, then a cross-file pass to catch how the files fit together.
- **Decision path:**
  - Can't list the steps → adaptive + orchestrator.
  - Steps depend on each other → sequential chain.
  - Steps are independent → parallel.

### 1.7 Session state

- **Session:** the saved record of messages, tool calls and results.
- **Resume vs. continue:** `--resume` reopens a specific session and `--continue` picks up the most recent one. Both keep the full prior context.
- **Stale-transcript trap:** a resumed session still holds old tool results. If files or the world have changed, Claude can be confidently wrong.
- **Fork:** `fork_session` branches a copy to experiment on, leaving the original untouched.
- **Branch-and-throw-away:** keep one stable base session, fork it for each investigation, and discard the forks when done.
- **If the session is stale,** don't resume. Start fresh with a short, curated summary of the key facts.

### Domain 1 exam decision reflexes

| Scenario | Answer |
|---|---|
| Rule must never break | Hook (or code gate), not a prompt |
| Fixed, known steps | Prompt chaining |
| Coordinator directing workers | Orchestrator-workers |
| Session is stale | Summarize and start fresh |
| Independent parts | Parallel (several Task calls in one turn) |
| Subagent needs info | Put it explicitly in its prompt (nothing is inherited) |
| Loop control | `tool_use` → continue, `end_turn` → stop |

Domain 1 rests on the agentic loop. Orchestration, spawning, hooks, decomposition and sessions are all things you build around it.
