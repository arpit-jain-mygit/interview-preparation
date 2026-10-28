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
- [Domain 3: Claude Code Configuration & Workflows](#domain-3-claude-code-configuration--workflows)
  - [3.1 CLAUDE.md hierarchy](#31-claudemd-hierarchy)
  - [3.2 Slash commands and skills](#32-slash-commands-and-skills)
  - [3.3 Path-specific rules](#33-path-specific-rules)
  - [3.4 Plan mode vs. direct execution](#34-plan-mode-vs-direct-execution)
  - [3.5 Iterative refinement](#35-iterative-refinement)
  - [3.6 Claude Code in CI/CD](#36-claude-code-in-cicd)
  - [Domain 3 exam decision reflexes](#domain-3-exam-decision-reflexes)
- [Domain 4: Prompt Engineering & Structured Output](#domain-4-prompt-engineering--structured-output)
  - [4.1 Explicit criteria and false positives](#41-explicit-criteria-and-false-positives)
  - [4.2 Few-shot prompting](#42-few-shot-prompting)
  - [4.3 Structured output with tool use](#43-structured-output-with-tool-use)
  - [4.4 Validation and retry loops](#44-validation-and-retry-loops)
  - [4.5 Batch processing](#45-batch-processing)
  - [4.6 Multi-instance and multi-pass review](#46-multi-instance-and-multi-pass-review)
  - [Domain 4 exam decision reflexes](#domain-4-exam-decision-reflexes)
- [Domain 5: Context Management & Reliability](#domain-5-context-management--reliability)
  - [5.1 Conversation context in long sessions](#51-conversation-context-in-long-sessions)
  - [5.2 Escalation and ambiguity resolution](#52-escalation-and-ambiguity-resolution)
  - [5.3 Error propagation in multi-agent systems](#53-error-propagation-in-multi-agent-systems)
  - [5.4 Context in large-codebase exploration](#54-context-in-large-codebase-exploration)
  - [5.5 Human review and confidence calibration](#55-human-review-and-confidence-calibration)
  - [5.6 Provenance and multi-source synthesis](#56-provenance-and-multi-source-synthesis)
  - [Domain 5 exam decision reflexes](#domain-5-exam-decision-reflexes)

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

#### The four steps, in simple words

Think of a support agent at a help desk handling "Where's my refund for order 9931?":

1. **Perceive:** read everything on the desk: the customer's question plus any notes gathered so far.
2. **Reason:** decide what to do next: "I need to look up the order first."
3. **Act:** do one thing: open the order system and search for 9931.
4. **Observe:** read what came back: "No refund on file." This becomes a new note on the desk.

Then go back to step 1 with the new note. The agent repeats this until it has enough to answer, then replies and stops.

**What each step looks like in the Claude API:**

| Step | What happens | Who does it |
|---|---|---|
| Perceive | Claude reads the whole `messages` list: the user's request plus every earlier `tool_result` | Claude |
| Reason | Claude decides whether it needs a tool, and which one with which inputs | Claude |
| Act | Claude replies with a `tool_use` block and `stop_reason: "tool_use"`; **your code** runs the tool | Claude asks, your code executes |
| Observe | Your code appends the output as a `tool_result` and calls the API again | Your code sends it, Claude reads it |

**Key details:**

- **Claude never runs the tool itself.** It only asks for it. Your application (or the Agent SDK, which runs this loop for you) executes the tool and sends the result back.
- **Claude has no memory between calls.** Each API call re-sends the full conversation, so Observe only works if you append the `tool_result` before calling again. This is why "not sending results back" breaks the loop.
- **Each pass gives Claude new facts.** Its next decision is based on real tool output rather than a guess, which is why it can pick a different tool depending on what it just learned.
- **The loop ends on `end_turn`.** That's when Claude has enough to answer. Add a safety cap (a maximum number of turns) so a confused agent can't loop forever.

**The whole loop in pseudocode:**

```python
messages = [user_request]
while True:
    response = claude.messages.create(messages=messages, tools=tools)   # Perceive + Reason
    messages.append(response)
    if response.stop_reason == "end_turn":                              # done
        break
    results = [run_tool(block) for block in response.content
               if block.type == "tool_use"]                              # Act
    messages.append({"role": "user", "content": results})               # Observe (tool_result)
```

**References:**

- [How tool use works - Claude docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview): the `tool_use` → `tool_result` round trip and `stop_reason`
- [How the agent loop works - Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/agent-loop): the same loop, run for you by the SDK
- [Building effective agents - Anthropic](https://www.anthropic.com/research/building-effective-agents): agents as an LLM using tools in a loop, based on feedback from its environment

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

---

## Domain 3: Claude Code Configuration & Workflows

### 3.1 CLAUDE.md hierarchy

- **CLAUDE.md** is project memory that Claude Code reads automatically at the start of every session. Write build commands, conventions and gotchas once instead of re-explaining them each time.
- **The three levels (enterprise policy sits above them all):**

| Level | Location | Purpose |
|---|---|---|
| user | `~/.claude/CLAUDE.md` | Your preferences, across all projects |
| project | `./CLAUDE.md` (committed) | Shared with the team |
| directory | nested `CLAUDE.md` in a folder | Rules for that folder only |

- **How the levels combine:** they merge into one context rather than replacing each other. When rules conflict, the more specific one wins. For example, if your personal file says 2-space indent and the project says 4-space, the project rule wins.
- **Nested files load on demand.** `frontend/CLAUDE.md` loads only when Claude works on frontend files, which suits large monorepos.
- **Tools for managing it:**
  - `@import` (for example `@docs/style.md`) keeps the file modular. Everything is still loaded at launch, so it doesn't save context.
  - `/memory` opens the memory files for editing.
  - Typing `#` at the start of a message quick-adds a rule; Claude asks which file to save it in.
- **What belongs in it:** pitfalls, conventions that differ from the defaults, and the reasons behind rules. Leave out what Claude can work out itself, such as folder layout or dependency lists.
- Keep it **under about 200 lines**. A bloated CLAUDE.md actually reduces how well Claude follows it.

### 3.2 Slash commands and skills

- **Custom commands:** a Markdown file in `.claude/commands/` (project, shared with the team) or `~/.claude/commands/` (personal) becomes a slash command.
  - The filename is the command name and the body is the prompt.
  - `$ARGUMENTS` inserts what you type after the command. For example, `fix-issue.md` makes `/fix-issue 123`, where `$ARGUMENTS` is `123`.
- **Command frontmatter:**
  - `description`: shown in `/help`, and lets Claude suggest the command when a request matches.
  - `argument-hint`: autocomplete hint for the input.
  - `allowed-tools`: tools the command may use without asking.
  - `model`: pin a cheaper or faster model.
- **Skills are the richer form.** Commands have been merged into skills.
  - `.claude/skills/<name>/SKILL.md` also creates `/name`.
  - A skill has a folder for supporting files.
  - Claude can discover and invoke a skill on its own when it's relevant.
  - If a skill and a command share a name, the skill wins.
- **Skill frontmatter the exam cares about:**
  - `context: fork`: run the skill in an isolated context.
  - `allowed-tools`: **pre-approves** the listed tools. It does **not** restrict anything; every other tool stays available.
  - `disable-model-invocation: true`: only you can trigger it. Use this for commands with side effects, such as `/commit` or `/deploy`.
- **CLAUDE.md vs. command/skill:** CLAUDE.md holds standing conventions Claude always reads. A command or skill is a repeatable task you (or Claude) run on demand.

### 3.3 Path-specific rules

- One CLAUDE.md applies everywhere, so in a big repo most of it is irrelevant to any one task. API-security rules don't help when you're editing CSS.
- **`.claude/rules/*.md`:** split rules into focused files such as `api.md`, `tests.md` and `style.md`. Each one loads as project memory, at the same priority as `.claude/CLAUDE.md`.
- **Scoping with `paths:`:** add a list of globs to a rule file's frontmatter, for example `paths: ['src/api/**']`. The rule then loads only when Claude touches a matching file.
  - With `paths:`, the rule loads conditionally, only in its area.
  - Without `paths:`, it loads in every session.
- **Glob rule vs. subdirectory CLAUDE.md:**
  - A pattern spread across the repo (for example every `*.test.js`) calls for a glob rule.
  - Everything under one folder calls for a CLAUDE.md in that folder.
- **Precedence:** user → project → path-specific. Path rules are added last when you touch matching files, so the most specific rule wins.

### 3.4 Plan mode vs. direct execution

- **Direct execution** suits small, obvious changes. **Plan mode** suits big or risky ones ("measure twice, cut once").
- **Plan mode is read-only.** Claude reads, searches and drafts a numbered plan. Write and Edit are **blocked at the tool level** until you approve, so this is enforced, not just requested.
- **Three ways to turn it on:**
  - `Shift+Tab` twice (it cycles Default → Auto-Accept → Plan).
  - `/plan`.
  - `--permission-mode plan`, which also works with headless `-p`.
- **When to use it:** multi-file changes, refactors, migrations, auth, payment or production code, unfamiliar repos and ambiguous tasks. Skip it for single-file tweaks.
- **Why it pays off:** 20 unguided choices that are each 80% likely to be right have only about a 1% chance of all being right.
- **Explore subagent:** a read-only scout (Read, Grep and Glob only) that works in its own context window and returns just its findings, keeping your main context clean.
- **The plan loop:** Explore → Plan → Approve (or edit the plan first) → Execute → Verify with tests or a build.

### 3.5 Iterative refinement

- Treat the first output as a draft and refine it in passes instead of aiming for a perfect one-shot.
- **Input/output examples:** showing a sample input and the exact output you want pins down format and detail better than more description. (Few-shot prompting is covered fully in 4.2.)
- **Interview pattern:** ask Claude to interview you first. Its questions surface decisions you hadn't made yet (framework, error handling, edge cases), turning a vague request into a precise spec.
- **Test-driven iteration:** write the test first and let Claude iterate until it passes. A passing test is an objective target.
- **Ordering fixes:** batch independent fixes together to save round-trips. Do dependent fixes in sequence to avoid rework.

### 3.6 Claude Code in CI/CD

- **Headless mode:** Claude Code runs unattended in a pipeline, on pull requests, on a schedule or from a script.
- **`claude -p "prompt"`** (print mode) is the headless switch. It runs to completion, prints the result, exits with a status code the pipeline can branch on, and never opens an interactive session.
- **Structured output:**
  - `--output-format json` returns the result plus metadata such as cost and `session_id`; parse it with `jq`.
  - `--json-schema` forces an exact shape into `structured_output`.
  - The formats are `text` (default), `json` and `stream-json` (real-time).
- **Safety guards for unattended runs:**
  - `--max-turns` caps how much work it does.
  - `--allowedTools` narrows permissions.
  - `--max-budget-usd` caps cost.
  - Check the output content, not just the exit code.
- **CLAUDE.md as CI context:** the same CLAUDE.md loads in CI, so your conventions become the pipeline's context automatically.
- **Self-review isolation:** run the reviewer as a separate instance. It didn't write the code, so it isn't biased toward defending its own choices.

### Domain 3 exam decision reflexes

| Scenario | Answer |
|---|---|
| Team-wide conventions | Project `./CLAUDE.md`, committed |
| Personal preference across projects | `~/.claude/CLAUDE.md` |
| User and project rules conflict | The more specific (project) rule wins |
| Rules for one folder | A CLAUDE.md in that directory |
| Rules for a pattern across the repo (`*.test.js`) | `.claude/rules/*.md` with `paths:` |
| Repeatable task the team shares | `.claude/commands/` or `.claude/skills/` |
| Claude must never auto-run `/deploy` | `disable-model-invocation: true` |
| "`allowed-tools` restricts tools" | False; it only pre-approves |
| Big, risky or multi-file change | Plan mode |
| Run in CI | `claude -p` with `--output-format json` / `--json-schema`, plus turn, tool and budget caps |
| Unbiased code review | A separate Claude instance |

---

## Domain 4: Prompt Engineering & Structured Output

### 4.1 Explicit criteria and false positives

- **Claude judges against the standard you give it.** Ask "Is this code good?" and Claude invents a standard that drifts from run to run. Explicit criteria give the same standard every time.
- **Make criteria specific and testable.** "Check for security problems" is a wish. "Flag any SQL query built with string concatenation" is a rule you could check by hand.
- **Severity levels** keep important issues from being buried:
  - **Critical:** blocks the release (for example a hard-coded password).
  - **Major:** fix soon (for example missing error handling).
  - **Minor:** nice to fix (for example an inconsistent name).
- **False positives** are flags on things that are actually fine. They come from over-broad criteria. (A false negative is a missed real issue.)
- **Noise destroys trust.** When 18 nonsense flags bury 2 real ones, people stop reading and dismiss everything, including the real critical issue. A noisy reviewer is worse than none.
- **The fix:** tighten the rule for a noisy category or disable it. Adding "be more careful" to the prompt doesn't work. Fewer, precise flags beat many noisy ones.
- **Example:** "Review this code" produced 15 flags, mostly style noise, and the team ignored them. Criteria plus severity plus tuning produced 3 flags (1 critical, 2 major), all real, and the team acted on them.

### 4.2 Few-shot prompting

- **Zero-shot** means no examples, **one-shot** means one, and **few-shot** means several. "Shot" just means example.
- **Examples beat description.** One good example shows tone, format and edge-case handling at once, which is hard to express as rules.
- **Examples remove ambiguity and fix the format.** They show what a fuzzy label like "urgent" actually means, and Claude copies the exact output shape. An inconsistent classifier is usually fixed by adding examples.
- **Generalization:** Claude learns the pattern, not the literal cases. Show 3 messy addresses and their clean versions, and it can clean a 4th it hasn't seen.
- **Reduce hallucination:** include an example where the data is missing and the right answer is `null` or "not found". If every example is complete, Claude assumes it must always produce a value and makes one up.
- **Choosing examples:** they must be correct, varied and include edge cases (ambiguous input, a missing field, an odd format). Three near-identical easy examples teach almost nothing.
- **How many and where:** usually 2 to 5; stop when accuracy stops improving. Keep every example in the same format, and put them **before** the real input.

### 4.3 Structured output with tool use

- **Free text is unreliable for automation.** Claude may add "Here's the data:", wrap it in markdown fences or rename a field, and the parser breaks.
- **Use forced tool use for structured output.** Claude has no separate JSON mode. You define a tool whose `input_schema` describes your fields, Claude "calls" it, and you get a clean `tool_use` block.
- **The JSON Schema** names every field, its type and which ones are required. A malformed schema is rejected up front with a 400 error before Claude runs.
- **Required vs. nullable (the root-cause fix for made-up values):**
  - If a field the document might not have is marked required, Claude invents a value for it.
  - Make such fields optional or nullable, for example `"type": ["string", "null"]`, so they come back as `null`.
  - Mark only always-present fields as required. Saying "don't guess" in the prompt is not the fix.
- **Enums with an "other" option:** an enum keeps values consistent. Without an escape hatch, Claude forces odd inputs into the closest wrong option, so add `"other"` plus a `detail` field.
- **`tool_choice`:** with `auto`, Claude may skip the tool and reply in prose. Use `any` or a specific named `tool` to guarantee the call.
- **What it does not fix:** structured output guarantees the **shape**, never the **truth**. Syntax errors go away; wrong sums, wrong fields and made-up values don't.

### 4.4 Validation and retry loops

- **Syntax vs. semantic errors:**
  - A syntax error is malformed JSON. Tool use already prevents it.
  - A semantic error is a valid shape with wrong content: bad sums, the wrong field or a made-up value. Only your own validation catches it.
- **The validation step** checks the content in code: Do the line items add up to the total? Are dates real and in range? Does every value actually appear in the source document?
- **Retry with feedback:** send back the document, the bad extraction and the **specific** error. "Line items sum to ₹4,800 but total says ₹5,000 - please fix" gets fixed fast; "it's wrong" doesn't.
- **Retry limits:** cap retries (usually 2 or 3), then flag the item for a human or mark it low-confidence. Without a cap you get an infinite loop that wastes time and money.
- **The self-correction loop:** Extract (tool use) → Validate → Feedback → Re-validate → Escalate when the cap is reached.
- **Example:** the first attempt returned items [2000, 2800] with total 5000 and failed validation. After feedback the total became 4800 and passed. The JSON was valid both times; only validation caught the wrong number.

### 4.5 Batch processing

- The **Message Batches API** takes many requests in one submission and processes them asynchronously, with the same model and quality.
- **The trade-off:**
  - **50% off** both input and output tokens, plus a separate rate-limit pool.
  - Results arrive within **24 hours** (often minutes to hours).
  - No streaming and no real-time use.
- **Decision rule:** is it OK for the result to arrive within 24 hours? If yes, use batch (bulk extraction, evals, moderation). If no, use the normal synchronous API (chat, live UI).
- **`custom_id`:** results come back out of order. Tag each request with a meaningful ID, such as the claim number, so you can match each result to its input.
- **Workflow:** Submit (up to 100k requests or 256 MB per batch) → Poll for status (or use a webhook) → Retrieve the JSONL results by `custom_id` → Save. Results are kept only about **29 days**, so save them right away. Split very large jobs into several batches.
- **Example:** 10,000 claims run as one nightly batch with `custom_id` set to the claim number, using the same schema (4.3), and each result still goes through validation (4.4).

### 4.6 Multi-instance and multi-pass review

- **One pass isn't enough** for two reasons: attention spreads thin across many files, and an author reviewing its own work is biased toward approving it.
- **Independent reviewer:** a separate Claude instance with its own context. It never saw the author's reasoning, so it judges the work on its merits.
- **Per-file and cross-file passes:**
  - A per-file pass reviews each file in depth and catches local bugs.
  - A cross-file pass checks how files fit together and catches integration bugs and mismatched interfaces.
  - You need both.
- **Confidence on each finding:** tag every finding high, medium or low. Act on high-confidence findings automatically and send low-confidence ones to a human.
- **Aggregate, don't just concatenate:** remove duplicates, keep the highest severity where findings overlap, and group by confidence for routing.
- **Full architecture:** independent reviewer → per-file pass → cross-file pass → confidence on each finding → aggregate and route.

### Domain 4 exam decision reflexes

| Scenario | Answer |
|---|---|
| Inconsistent review results | Explicit, testable criteria plus severity levels |
| Too many false positives | Tighten or disable the noisy category, not "be careful" |
| Inconsistent labels or format | Add few-shot examples (varied, edge cases, uniform, before the input) |
| Claude makes up missing data | Make the field optional or nullable, and add a missing-data example |
| Need guaranteed JSON | Tool use with an `input_schema`, plus `tool_choice` set to `any` or a named tool |
| Odd inputs forced into the wrong enum value | Add an `"other"` value plus a `detail` field |
| Valid JSON but wrong values | Validate in code, then retry with specific feedback (2 or 3 max), then escalate |
| Large non-urgent job | Message Batches API (50% off, within 24h, `custom_id`) |
| A user is waiting | Synchronous API, never batch |
| Unbiased, thorough review | A separate instance, per-file plus cross-file passes, confidence routing |

---

## Domain 5: Context Management & Reliability

### 5.1 Conversation context in long sessions

- **Long chats get worse, not just longer.** As the context window fills, accuracy drops ("context rot"). Claude pays most attention to the **start and end**, so a key fact buried in the **middle** can be missed ("lost in the middle").
- **Trim bulky tool output.** Old tool results are the biggest space-waster. Once you've used a 2,000-line file read or API dump, clear it and keep only the conclusion.
- **Progressive summarization:** condense older turns and swap the summary in, which is what `/compact` does. The risk is that a careless summary silently drops a detail you still need, so tell Claude what must be kept.
- **Case-facts block:** a short block with the essentials (customer ID, the issue, decisions made), **re-inserted near the end** of the prompt every turn, where Claude's attention is highest. This directly counters lost-in-the-middle.
- **Core principle, extract and persist:** pull out the key facts, keep them, and trim everything else. This idea runs through the whole domain.

### 5.2 Escalation and ambiguity resolution

- **A confidently wrong action is worse than asking.** Escalating is correct behavior, not a failure.
- **Escalation triggers:**
  - **Low confidence:** Claude isn't sure enough to act.
  - **High stakes:** money, safety or anything legal.
  - **Policy gap:** no rule covers the case. Claude must escalate rather than invent a policy. This one is tested on the exam.
- **Honor an explicit request for a human.** "I want to speak to a person" means escalate immediately. Don't try to resolve it first or talk them out of it.
- **Multiple matches → ask a clarifying question.** If there are two customers named "Sharma" or two orders that fit, ask "Did you mean order #A or #B?" instead of picking one. This is a question to the user, not a handoff to a human.

### 5.3 Error propagation in multi-agent systems

- **The danger is silence, not the failure.** If a subagent returns nothing, the coordinator may build a confident but incomplete answer.
- **Structured error hand-back:** the subagent reports what failed, why, and what it did get, passing it **up** to the coordinator. It reuses the 2.2 format (`isError`, category).
- **Include the failure type and any partial results** (for example "got 2 of 5 sources").
- **Access failure vs. empty result:** "couldn't reach the source" is a real, retryable failure. "Reached it, found 0 results" is a valid answer; don't retry it. This is the same trap as 2.2.
- **Recovery strategies for the coordinator:**
  - **Retry** if the error was transient, such as a timeout.
  - **Skip and note the gap** if the missing part is non-critical.
  - **Escalate** to a human if it's critical.
- **Report honestly:** "Findings complete except news sources, which were unavailable" is better than a report that's silently incomplete.

### 5.4 Context in large-codebase exploration

- **Exploring code fills the window fast.** Each file read dumps its contents into context, and within a few dozen files the window is full and quality drops.
- **Scratchpad files:** write key findings to disk ("auth lives in auth/, the bug is in login()"). Disk is unlimited; context isn't. Re-read only the note you need.
- **`/compact`:** summarizes the conversation and replaces the history so a long task can continue. Run it **proactively at about 70-75% full**, at a natural break, so you control what it keeps.
- **Crash-recovery manifest:** a file recording the task, what's done and what's next. If the session dies, a new one reads it and picks up where it left off; a refactor that crashes at file 40 doesn't restart at file 1.
- **Explore subagent (from 3.4):** heavy reading happens in its own context and only the conclusions come back.
- **Four tools together:** the Explore subagent (read elsewhere), scratchpad files (save findings), `/compact` (shrink the history) and a manifest (survive a crash).

### 5.5 Human review and confidence calibration

- **Review the right outputs, not all and not none.** Reviewing everything at scale is impossible and reviewing nothing is risky, so target the outputs most likely to be wrong.
- **Field-level confidence:** score each field, not the whole document. A typed policy number may be certain while a handwritten total isn't, so only the shaky field gets reviewed.
- **Route by confidence:** high confidence is accepted automatically and low confidence goes to a human, so people spend time only on uncertain cases.
- **Stratified sampling:** spot-check **every** confidence band (high, medium and low). Reviewing only low-confidence items misses cases where Claude was confidently wrong.
- **Track accuracy by document type and by field.** If handwritten forms or the "total" field are error-prone, review them more heavily, and relax on fields that are consistently correct.

### 5.6 Provenance and multi-source synthesis

- **Facts lose their sources.** When ten sources are blended into smooth prose, you can't tell a real finding from a made-up one, and an unsourced claim can't be checked.
- **Claim-to-source mapping:** keep each claim linked to the source it came from, like a citation, so the final answer can be audited.
- **Surface conflicts.** When sources disagree, show both views with their sources. Don't silently pick one or average them, and flag low-certainty claims instead of stating them flatly.
- **Temporal framing:** label when each fact is from. A 2019 figure and a 2026 figure aren't equally current, and an old fact presented as current is quietly wrong.

### Domain 5 exam decision reflexes

| Scenario | Answer |
|---|---|
| Key fact missed in a long chat | Case-facts block re-inserted at the end of the prompt |
| Context filling with old tool dumps | Trim or clear old tool output and keep the conclusions |
| Need to summarize | `/compact` proactively at about 70-75% full, protecting what must be kept |
| No rule covers the case | Escalate; never invent a policy |
| User asks for a human | Escalate immediately |
| Request matches two records | Ask the user a clarifying question |
| Subagent fails | Structured error passed up with type and partial results; never fail silently |
| Source reachable but empty | A valid answer; don't retry |
| Long refactor might crash | Crash-recovery manifest plus scratchpad files |
| Which outputs to review | Field-level confidence routing plus stratified sampling across all bands |
| Sources disagree | Show both with their sources and flag uncertainty |
| Old vs. new facts | Label each with its date |
