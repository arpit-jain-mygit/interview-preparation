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
- [Domain 2: Tool Design & MCP Integration](#domain-2-tool-design--mcp-integration)
  - [2.1 Designing tool interfaces](#21-designing-tool-interfaces)
  - [2.2 Structured error responses](#22-structured-error-responses)
  - [2.3 Tool distribution and tool_choice](#23-tool-distribution-and-tool_choice)
  - [2.4 MCP server integration](#24-mcp-server-integration)
  - [2.5 Built-in tools (Claude Code)](#25-built-in-tools-claude-code)
  - [Domain 2 exam decision reflexes](#domain-2-exam-decision-reflexes)

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

---

## Domain 2: Tool Design & MCP Integration

### 2.1 Designing tool interfaces

- **Tools are Claude's hands.** A tool is a function Claude can call to do something: look up an order, send an email, query a database.
- **The description is how Claude chooses.** Claude can't see your code, only the tool's name and description. A vague description leads to the wrong tool or no tool at all. Write descriptions for Claude, not for yourself.
- **A strong description covers four things:**
  - what the tool does, in one line
  - when to use it, and when not to (the part people skip, and the one that prevents wrong-tool picks)
  - each parameter, in plain words
  - a short example call
- **Distinct names:** names like `getData` vs. `fetchData` invite confusion. Prefer clear ones like `get_order_by_id` and `search_orders_by_customer`. Overlapping names and descriptions are a top cause of wrong-tool errors.
- **Split vs. consolidate:** size tools around the choices Claude has to make.
  - Split when jobs are distinct, so the choice is clear.
  - Combine steps that always happen together, so there are fewer round-trips.
  - Avoid both extremes: too many tiny tools overwhelm the choice, and one do-everything tool is too vague to describe.
- **Travel booking example:** a single `handle_travel(action, …)` forces Claude to guess the action string. `search_flights`, `book_flight` and `cancel_booking` each do one job and are easy to choose between.
- **Vague interfaces fail quietly.** There's no crash; Claude picks the wrong tool, fills in wrong parameters, or gives up and answers in text. Get the interface right before the logic.

### 2.2 Structured error responses

- **The error message is Claude's only clue.** "Booking failed." gives it nothing to act on. "Payment failed: insufficient balance. Try another method." lets it recover.
- **`isError: true`:** return the failure inside a normal response so Claude sees it and can react. Don't throw a raw exception; it becomes a low-level protocol error that Claude handles poorly.
- **Error categories (tag each error with an `errorCategory`):**
  - `validation`: bad input; fix it and retry.
  - `auth` / `permission`: not allowed; escalate.
  - `not_found`: nothing there to return.
  - `rate_limit` / `transient`: service is busy; wait, then retry.
- **`isRetryable`, the most useful field:**
  - `true` for transient and rate-limit errors.
  - `false` for validation, auth and business-rule errors (for example, a refund over the limit), because retrying always gets the same "no".
  - It stops blind retry loops that waste calls and time.
- **Empty result vs. real failure (the classic Domain 2 trap):**
  - "No orders found" is a success: `isError: false`, `resultCount: 0`.
  - "Couldn't reach the database" is a failure: `isError: true`, retryable.
  - Never retry an empty result as if it were a failure.
- **Write useful errors:** say what was attempted, what failed and what to do next, for example "Couldn't fetch order #4471: DB timed out after 5s. Transient - safe to retry."
- **Sanitize:** never return raw stack traces, which leak your internals. Wrap "no such table: users_v2" as "The requested resource could not be accessed."

### 2.3 Tool distribution and tool_choice

- **Too many tools hurts.** With around 60 tools, selection gets slower and less accurate. A handful of well-chosen tools works better.
- **Scope tools to each role** (the same idea as 1.3). A read-only reporter gets only read tools and a refund agent gets refund tools. A subagent's `allowedTools` lists only what its role needs.
- **Scoping vs. `tool_choice`:** scoping decides which tools exist. `tool_choice` decides whether a tool must be called right now, and which one.
- **The four `tool_choice` modes:**

| Mode | Meaning | Use when |
|---|---|---|
| `auto` (default) | Claude decides | Ordinary chat assistants |
| `any` | Must call some tool; Claude picks which | It must act, but may choose how |
| `tool` | Must call this named tool | A step is non-negotiable or you need guaranteed structured output |
| `none` | No tools this turn | Ask without acting, or a text-only turn |

- `any` and `tool` (forced tool use) **cannot be combined with extended thinking**.
- **Example:** with `auto`, a research agent sometimes replies in text and the findings are lost. `tool_choice: { type: 'tool', name: 'save_report' }` makes it save on every run. Forcing a specific tool is the standard way to guarantee structured output (it comes up again in Domain 4).

### 2.4 MCP server integration

- **MCP (Model Context Protocol)** is one standard way to connect Claude to external systems, like USB-C for AI tools. Instead of a custom connector per tool, you build a server once and any MCP client can plug into it.
- **Tools vs. resources:**
  - Tools are verbs: actions Claude calls, such as `create_issue` and `run_query`.
  - Resources are nouns: read-only data or context, such as a file, a doc or a schema. In Claude Code you pull one in with `@`.
- **Connecting a server:** add one entry under `mcpServers`.
  - `stdio`: a local program Claude launches (`command` + `args`).
  - `http`: a remote server (`url`).
  - The transport is how Claude talks to the server. It's separate from where the config file lives.
- **Keep secrets out of the config:** use `${VAR}` expansion, for example `"env": { "API_TOKEN": "${GITHUB_TOKEN}" }`. `${VAR:-default}` gives a fallback value. Expansion works in `command`, `args`, `env`, `url` and `headers`. A key hard-coded in a shared `.mcp.json` gets committed to git and leaks.
- **The three scopes:**

| Scope | Where it lives | Who it's for |
|---|---|---|
| local (default) | `~/.claude.json` | Only you, this project |
| project | `.mcp.json` (committed) | The whole team |
| user | `~/.claude.json` | You, across all projects |

- Picking the wrong scope is the #1 MCP mistake. A personal token in **project** scope leaks to the whole team.
- **Precedence:** local > project > user. If the same server name exists in two scopes, the higher one wins, so your local override beats the team's. Running from a sub-folder also merges in parent `.mcp.json` files.
- **Multiple servers:** you can run several at once (GitHub, a database, browser automation). Check their status with `/mcp`, and give them clear names such as `github` or `stripe-prod`, not `server1`.

### 2.5 Built-in tools (Claude Code)

- **The six built-in tools:**
  - **Read:** view a file.
  - **Write:** create or overwrite a file.
  - **Edit:** change part of a file.
  - **Bash:** run shell commands.
  - **Grep:** search inside files.
  - **Glob:** find files by name.
- **Grep vs. Glob (the #1 confusion, tested directly):** Grep searches file contents (for example, where `processOrder` is called). Glob matches file names (for example, every `*.test.js`).
- **Edit vs. Write:** use Edit for small changes because it's an exact string replacement with a clean diff. Write rewrites the whole file.
- **Read before Edit:**
  - Edit requires an earlier Read of the file.
  - The target text must match exactly and appear only once.
  - If it isn't unique, include more surrounding text or use `replace_all`.
  - Read + Write is the last-resort fallback, not the default.
- **Prefer built-ins over Bash:** Read instead of `cat`, Grep instead of `grep`, Glob instead of `find`, Edit instead of `sed`. Built-ins give better permission handling, a clearer trail and caching. Keep Bash for actually running things, such as tests or builds.
- **Explore incrementally:** use Grep and Glob to find the few files that matter, then Read only those. Reading everything up front wastes your context budget (covered in Domain 5).

### Domain 2 exam decision reflexes

| Scenario | Answer |
|---|---|
| Claude picks the wrong tool | Improve the description (what/when/params/example) and give tools distinct names |
| One tool with an `action` string | Split it into one tool per distinct action |
| Tool fails | Return `isError: true` with a category and `isRetryable`; don't throw |
| Query returns nothing | Success with `resultCount: 0`, not an error and not retryable |
| Business-rule or validation error | `isRetryable: false` |
| Agent has too many tools | Scope each role to only the tools it needs |
| A step must always happen | `tool_choice: { type: 'tool', name: ... }` |
| Personal API key in MCP config | `${VAR}` expansion, and local or user scope, never project |
| Same MCP server defined twice | local > project > user |
| Search contents vs. find files | Grep for contents, Glob for file names |
