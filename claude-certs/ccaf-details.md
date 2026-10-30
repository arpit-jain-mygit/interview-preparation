# CCAF - Additional Details

Deeper explanations that support the main notes in [ccaf.md](ccaf.md). Each section links back to its topic there.

## Contents

- [1.1 The agentic loop: the four steps in simple words](#11-the-agentic-loop-the-four-steps-in-simple-words)
- [1.1 What is a turn in the loop?](#11-what-is-a-turn-in-the-loop)
- [1.1 Which PRAO steps repeat, and where: two loops](#11-which-prao-steps-repeat-and-where-two-loops)
- [1.1 All stop_reason values](#11-all-stop_reason-values)
- [1.1 Tool vs. agent](#11-tool-vs-agent)
- [1.2 The narrow-decomposition trap](#12-the-narrow-decomposition-trap)
- [1.2 The coordinator picks subagents at runtime](#12-the-coordinator-picks-subagents-at-runtime)
- [1.2 Synthesize: combining subagent answers](#12-synthesize-combining-subagent-answers)
- [1.2 Manage errors when a subagent fails](#12-manage-errors-when-a-subagent-fails)
- [1.2 Iterative refinement: check, then re-delegate](#12-iterative-refinement-check-then-re-delegate)
- [1.3 Why spawning a subagent is a tool call](#13-why-spawning-a-subagent-is-a-tool-call)
- [1.3 How a subagent knows which tools it has](#13-how-a-subagent-knows-which-tools-it-has)
- [1.3 Passing context to a subagent](#13-passing-context-to-a-subagent)
- [1.3 Model per subagent (practice extra)](#13-model-per-subagent-practice-extra)
- [1.4 Gate a refund behind the policy check](#14-gate-a-refund-behind-the-policy-check)
- [1.4 Handoff summary for a human agent](#14-handoff-summary-for-a-human-agent)
- [1.5 Pre-execution hook: block and redirect](#15-pre-execution-hook-block-and-redirect)
- [1.5 PostToolUse hook: normalize results](#15-posttooluse-hook-normalize-results)

---

## 1.1 The agentic loop: the four steps in simple words

Back to [1.1 Design and implement agentic loops](ccaf.md#11-design-and-implement-agentic-loops-for-autonomous-task-execution).

Think of a support agent at a help desk handling "Where's my refund for order 9931?":

1. **Perceive:** read everything on the desk: the customer's question plus any notes gathered so far.
2. **Reason:** decide what to do next: "I need to look up the order first."
3. **Act:** do one thing: open the order system and search for 9931.
4. **Observe:** read what came back: "No refund on file." This becomes a new note on the desk.

Then go back to step 1 with the new note. The agent repeats this until it has enough to answer, then replies and stops.

**What each step looks like in the Claude API, and where the agent fits:**

The agent is not one of the four steps. It is the whole system that runs all four: **agent = model (Claude) + tools + loop (your code or the Agent SDK)**, guided by the system prompt.

| Step | What happens | Who does it (in our practice app) |
|---|---|---|
| **Perceive** | Claude reads the whole `messages` list, the system prompt and the tool list | **Claude** reads. **`run_agent()`** in `agents/agent_loop.py` sends it with `client.messages.create(...)`. |
| **Reason** | Claude decides: answer now, or request one or more tools with their inputs. It sets `stop_reason` to say which. | **Claude**, guided by the system prompt (the coordinator's prompt in `agents/orchestrator.py`, or a worker's `prompt` in `agents/worker_agents.json`) and the tool descriptions. |
| **Act** | The loop reads each `tool_use` block and calls the function in `tools[block.name]` | **`run_agent()`** runs it. For a plain tool, the function is in `tools/functions.py`, for example `look_up_order`. For a delegation tool (`ask_order_agent`, `ask_refund_agent`), the function is in `agents/orchestrator.py` and starts a whole worker agent by calling `run_agent()` again. |
| **Observe** | The result is wrapped as a `tool_result` and appended to `messages` | **`run_agent()`** records it. Claude sees it on the next Perceive. For a delegation tool, the worker's final answer is the result. |
| **Stop check** | Whether to run Act at all | **Claude** sets `stop_reason`, and **`run_agent()`** reads it. `end_turn` ends the loop. |

So Claude decides and reads, our code sends, runs and records. The **agent** is the whole arrangement: Claude + its tools + `run_agent()` (+ the coordinator, when there is one).


- **Claude alone** is just a model: one request in, one reply out.
- **Claude + tools + loop** is an agent: it keeps acting until the job is done.
- **Agent SDK:** runs the loop and the tools for you; you supply instructions and tools.
- **Claude Code:** a ready-made agent built the same way (Claude + Read/Edit/Bash/... + the loop).

**Where `stop_reason` fits:**

`stop_reason` is not a step of its own. It is the **handoff signal between Reason and Act**: Claude sets it at the end of Reason, and your loop reads it to decide whether Act happens at all.

```
Perceive → Reason ──[stop_reason]──→ Act → Observe → (back to Perceive)
                         │
                         └── end_turn → stop, give the answer
```

| Step | What happens to `stop_reason` |
|---|---|
| **Reason** (Claude) | Claude finishes thinking and **sets** `stop_reason` in its response: `tool_use` if it wants a tool, `end_turn` if it's ready to answer |
| **Between Reason and Act** (your loop) | Your code **reads** `stop_reason` and branches on it |
| **Act** (your code) | Happens **only if** `stop_reason` was `tool_use`. Your code runs the tool. |

- `stop_reason` is **produced by** Reason. It records Claude's decision.
- It **decides whether** Act happens, but it isn't part of running the tool.
- It's the **exit check** for the whole loop: `end_turn` skips Act and Observe, and the agent stops.
- **For the exam:** Claude decides and your code obeys. `stop_reason` is how Claude's decision reaches your loop.
- **Other values (from the Claude docs, not the course slides):**
  - `max_tokens`: the reply hit the token limit and was cut off. It's not a finished answer, so handle it rather than treating it as done.
  - `pause_turn`: a long-running server-side tool paused. Send the response back to let it continue.

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

---

## 1.1 What is a turn in the loop?

Back to [1.1 Design and implement agentic loops](ccaf.md#11-design-and-implement-agentic-loops-for-autonomous-task-execution).

A **turn** is one round trip to Claude:

1. The loop sends the whole conversation so far, plus the tool list, to Claude.
2. Claude replies, and the reply is one of two things:
   - **Tool requests** (`stop_reason` = `tool_use`): our code runs the tools and adds the results to the conversation. That starts the next turn.
   - **A final answer** (`stop_reason` = `end_turn`): the loop stops.

One turn is one reply from Claude. It is not one tool call. Claude can ask for several tools in one reply, and they all run in that turn.

**Example from the practice app.** The order agent was asked where order 9931 is:

- **Turn 1:** Claude asked for `look_up_order` and `track_shipment` in one reply. Our code ran both, one after the other, and added both results to the conversation.
- **Turn 2:** Claude read both results and wrote the answer. `stop_reason` was `end_turn`, so the loop stopped.

**Why it took two turns, not one.** It's tempting to think Claude could request both tools and then answer in the same reply. It can't. Claude has to see the tool results before it can write an answer that depends on them, and it only sees them in the next request. So every reply that asks for tools is followed by another turn, and the answer always comes in a turn of its own.

If a tool depended on another tool's result (for example, you need the order's price before you can check a refund), Claude would need a new turn after each step.

**Why `MAX_TURNS` exists.** It caps the number of round trips one agent can take. A normal agent finishes in a few turns. The cap stops a confused agent that keeps asking for tools and never answers. Hitting the cap is a failure to report, not a normal finish.

**Reference:** [How the agent loop works - Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/agent-loop) and [How tool use works - Claude docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview): the loop sends each request with the full message history, and a tool result goes back to Claude in the next request.

---

## 1.1 Which PRAO steps repeat, and where: two loops

Back to [1.1 Design and implement agentic loops](ccaf.md#11-design-and-implement-agentic-loops-for-autonomous-task-execution).

The loop has two levels, one inside the other:

- **Outer loop (once per turn):** Perceive, then Reason. Every turn runs both.
- **Inner loop (once per tool request):** Act, then Observe. It runs once for each `tool_use` block in Claude's reply.

| Step | Loop | How many times |
|---|---|---|
| Perceive | outer | once per turn |
| Reason | outer | once per turn |
| Act | inner | once per tool request |
| Observe | inner | once per tool request |

After the inner loop, all the tool results go back to Claude as one message. That message is part of the same turn.

**Example from the order agent.** In turn 1, Claude asked for two tools. The inner loop ran twice, so Act and Observe each ran twice. In turn 2, Claude gave a final answer with no tool request, so the inner loop ran zero times.

**Why it's split this way.** Reason decides whether there is anything to act on. If Claude asks for no tools, there is nothing for the inner loop to do, so the outer loop ends.

**In the code:** [agents/agent_loop.py](https://github.com/arpit-jain-mygit/agentic-ai-hello-world/blob/main/agents/agent_loop.py) has the outer `for turn in range(...)` loop and the inner `for block in response.content` loop.

**Reference:** [How the agent loop works - Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/agent-loop), which describes the same cycle of model call, tool execution and result return.

---

## 1.1 All stop_reason values

Back to [1.1 Design and implement agentic loops](ccaf.md#11-design-and-implement-agentic-loops-for-autonomous-task-execution).

Every Messages API response carries a `stop_reason` that says why Claude stopped. The course only covers the first two; the rest come from the Claude docs.

| Value | What it means | What your loop should do |
|---|---|---|
| `end_turn` | Claude finished its answer naturally. The most common value. | Stop the loop and use the answer. |
| `tool_use` | Claude wants to call one or more tools. | Run the tools, send back the `tool_result`s, and call the API again. |
| `max_tokens` | The reply hit the `max_tokens` limit you set and was cut off. | Don't treat it as finished. Continue, or retry with a higher limit (always retry if the last block is a half-written `tool_use`). |
| `stop_sequence` | Claude produced one of your custom `stop_sequences`. | Treat it as a deliberate stop at your marker and process the output. |
| `pause_turn` | A server-side tool loop (such as web search) hit its iteration limit, 10 per request by default, before Claude finished. | Send the response back as-is so Claude can continue. |
| `refusal` | Claude declined to respond for safety reasons. It arrives as a normal HTTP 200, not an error. | Don't retry blindly. Handle it as a refusal (rephrase, or tell the user). |
| `model_context_window_exceeded` | Claude stopped because the conversation reached the model's context window limit. | Trim or compact the context (see Domain 5), then continue. |

**For the exam:** the agentic loop only needs `tool_use` (keep going) and `end_turn` (stop). A robust loop should also handle `max_tokens` and `pause_turn` instead of treating them as "done".

**Common pitfalls (from the docs):**

- **Empty `end_turn` responses.** If you add a text block right after a `tool_result` in the same user message, Claude may learn the pattern "user always speaks after a tool" and end its turn with an empty reply. Send `tool_result`s on their own.
- **Retrying an empty response unchanged doesn't work.** Claude has already decided it's done. Add a new user message such as "Please continue" instead.

**Reference:** [Handling stop reasons - Claude docs](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)

---

## 1.2 The narrow-decomposition trap

Back to [1.2 Orchestrate multi-agent systems](ccaf.md#12-orchestrate-multi-agent-systems-with-coordinator-subagent-patterns).

**In one line:** when the coordinator splits a big question into subtasks, the subtasks together must cover the *whole* question. If they cover only part of it, the final answer quietly answers a smaller question.

**Simple analogy:** you ask a friend to "plan our family holiday". They book flights and nothing else. Every flight detail is perfect, but there's no hotel, no food plan and no activities. Nothing failed; the job was just cut too small at the start.

**The course example, step by step:**

1. User asks: "Research the impact of AI on the **creative industries**."
2. The coordinator decomposes it into a single subagent: "Research AI in **visual arts**."
3. That subagent does excellent work on visual arts.
4. The coordinator synthesizes and returns a polished report.
5. The report says nothing about music, film, writing, design or gaming, so most of the question was never answered.

```
Asked:      creative industries = visual arts + music + film + writing + design + gaming
Delegated:                        visual arts
Missing:                                        music + film + writing + design + gaming
```

**Why it's a trap:**

- **It fails silently.** Every subagent succeeds, there are no errors, and the report looks confident and complete.
- **The fault is in the coordinator, not the subagents.** Each subagent did exactly what it was asked. The gap was created at the decomposition step, before any work started. (Exam questions often offer "improve the subagents' prompts" or "add more tools" as wrong answers; the right fix is in how the coordinator splits the task.)

**How to avoid it:**

| Fix | What it means |
|---|---|
| List the full scope first | Before delegating, have the coordinator list every part the question covers (all the creative industries), then assign subtasks from that list. |
| Coverage check | Ask "do these subtasks add up to the original question?" before spawning subagents. |
| Clear boundaries per subagent | Give each subagent an objective, output format and explicit scope, so there are no gaps and no overlaps. |
| Check after synthesis | In the refinement step, compare the combined result against the original question and re-delegate anything missing. |

**The opposite mistake:** vague, overlapping subtasks, where several subagents research the same thing and waste effort. Good decomposition avoids both **gaps** (too narrow) and **duplicates** (unclear boundaries).

**For the exam:** if the final report is good but incomplete and every subagent succeeded, the root cause is the coordinator's decomposition being too narrow.

**Reference:** [How we built our multi-agent research system - Anthropic](https://www.anthropic.com/research/multi-agent-research-system), section "Teach the orchestrator how to delegate": each subagent needs an objective, output format, tool guidance and clear task boundaries, or agents "duplicate work, leave gaps, or fail to find necessary information."

---

## 1.3 Why spawning a subagent is a tool call

Back to [1.3 Configure subagent invocation](ccaf.md#13-configure-subagent-invocation-context-passing-and-spawning).

**The doubt:** "Tools are called by an agent when needed, and the orchestrator shares the tool descriptions with the agent. So why does the coordinator spawn a subagent *with a tool call*? Shouldn't it just share all the tool info with the agent?"

**The short answer:** your first assumption is right. Tools are called by an agent when it needs them. The key is that **the coordinator is itself an agent**, and "spawn a subagent" is just **one of its tools**. There are two separate levels:

| Level | Who | Its tools | What its tool calls do |
|---|---|---|---|
| Coordinator | An agent running its own loop | Usually few: mainly the **Task tool** (spawn a subagent), maybe a few others | Calling Task starts a whole new agent |
| Subagent | Another agent, with its own loop and context | Its own working tools: search, read, refund lookup, ... | Calling them does the actual work |

**Simple analogy:** a manager (coordinator) and team members (subagents).

- The manager's "tool" for getting work done is **assigning a task** to someone: "Riya, research music industry trends and send me the top 3 findings."
- Riya has her own tools (search engine, reports, spreadsheets) and decides for herself how to use them.
- The manager doesn't hand Riya a list of every tool in the company each time. Riya's job role already defines which tools she has.

**How spawning works in the loop:**

1. Coordinator runs its loop and reasons: "I need music research done."
2. It replies with `tool_use` for the **Task** tool, with input like `{ subagent_type: "researcher", prompt: "Research AI in the music industry. Return the top 3 findings with sources." }`.
3. The harness (Agent SDK / Claude Code) executes that tool call by **starting a new agent**: fresh, isolated context, the subagent's own system prompt and tools.
4. The subagent runs its own Perceive → Reason → Act → Observe loop, calling *its* tools as needed.
5. When it finishes, its final answer comes back to the coordinator as the **`tool_result`** of the Task call.
6. The coordinator observes that result and continues its own loop.

So from the coordinator's point of view, a whole subagent run looks exactly like one tool call and one tool result.

**Why not just "share all the tools" with the subagent?**

- **The orchestrator doesn't pass tools at runtime.** A subagent's tools are fixed in its **definition** (the `tools` field), written by you, the developer. At spawn time the coordinator passes only the **task** (the prompt). Everything else the subagent needs must be in that prompt, because it inherits no conversation history (see 1.3).
- **You *can* give it everything.** If you leave out the `tools` field, the subagent inherits every tool available to subagents. It's allowed; it's just usually not the best design.
- **Fewer tools = better choices.** A subagent with 5 relevant tools picks the right one more reliably than one with 60 (see 2.3).
- **Safety (least privilege).** A research subagent shouldn't be able to issue refunds or delete files. Giving it only search tools makes that impossible, not just unlikely.
- **Focus.** The whole point of a subagent is a small, clean context for one job. Loading it with unrelated tool descriptions works against that.

**Name note:** the course calls it the **Task tool**. The current Claude Code and Agent SDK docs call the same thing the **Agent tool**. Same idea: a tool whose job is to start a subagent.

**For the exam:**

- Spawning a subagent = the coordinator calls the Task tool; the subagent's final answer comes back as the tool result.
- Several Task calls in one turn = subagents run in parallel.
- A subagent's tools come from its definition, scoped to its role; context comes only from the prompt passed at spawn time.

**References:**

- [Subagents in the SDK - Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/subagents): "Claude invokes subagents through the Agent tool"; the `tools` field, "If omitted, inherits every tool available to subagents"
- [Create custom subagents - Claude Code docs](https://code.claude.com/docs/en/sub-agents): each subagent runs in its own context window with a custom system prompt, specific tool access and independent permissions

---

## 1.3 How a subagent knows which tools it has

Back to [1.3 Configure subagent invocation](ccaf.md#13-configure-subagent-invocation-context-passing-and-spawning).

**The doubt:** "If the orchestrator doesn't share the tool list, how does the subagent (Riya) know which tools she can use?"

**The short answer:** the **harness** (your code, the Agent SDK or Claude Code) tells her, not the orchestrator. Every time Riya's loop calls the Claude API, the harness includes her tool list in the request's `tools` parameter, built from **her definition**, which **you, the developer**, wrote in advance.

**Analogy:** when Riya joins the company, **IT sets up her laptop** based on her job role: search portal, reports app, spreadsheet. Her manager never lists the apps. When she gets a task, she just opens the laptop and sees what's installed.

| Office | Agent system |
|---|---|
| HR writes the job role | **You (developer)** write the subagent definition: `description`, `prompt`, `tools`, `model` |
| IT installs the apps on her laptop | **The harness** sends her tool schemas (name, description, input format) with every API call she makes |
| Manager gives her a task | **The coordinator** calls the Task tool with only `subagent_type` and the task `prompt` |
| Riya uses the apps she sees | **The subagent** (Claude) reads the tool descriptions in its request and picks what it needs |

**Who shares what:**

| Who | Shares | With whom |
|---|---|---|
| Developer | The subagent definitions (written once, in code or `.claude/agents/` files) | The harness |
| Harness | The Task tool, whose description lists the available subagent types and their `description`s | The coordinator |
| Coordinator (Claude) | The chosen `subagent_type` + a task `prompt` (goal, facts, prior findings) | The subagent |
| Harness | That subagent's own tool schemas, on every API call in its loop | The subagent |

**So the orchestrator never handles tools for the subagent.** It only decides *which* subagent to start and *what* to tell it. That's also why the subagent's `description` matters so much: it is the only thing the coordinator sees when deciding which subagent to use (1.3).

**Remember from 1.1:** Claude has no memory between API calls. "Knowing its tools" just means the tool schemas are included in each request the harness sends. This is the same mechanism as for any single agent; a subagent is no different.

**For the exam:**

- A subagent's tools are fixed in its definition and delivered by the harness, not passed by the coordinator.
- The coordinator passes only the task prompt, so all context the subagent needs must be written into that prompt.
- The coordinator chooses subagents by reading their `description`s.

**References:**

- [Subagents in the SDK - Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/subagents): the `AgentDefinition` fields (`description`, `prompt`, `tools`, `model`)
- [How tool use works - Claude docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview): tools are sent in the `tools` parameter of each API request

---

## 1.2 The coordinator picks subagents at runtime

Back to [1.2 Orchestrate multi-agent systems](ccaf.md#12-orchestrate-multi-agent-systems-with-coordinator-subagent-patterns).

**The doubt:** "Does the orchestrator also decide at runtime which agent to call?"

**Yes.** The coordinator is an agent, so it runs the same loop as any agent (1.1). Its "tools" are the spawn tools, one per subagent, and its model reads their **descriptions** and decides, for each request:

- **which** subagents to call (one, several or none),
- in **what order**,
- **how many times** (it can call one again if the answer falls short, which is iterative refinement),
- and **what task text** to give each one.

Your code never says "call the order agent first". This is the coordinator's **Select** and **Route** jobs, done by the model, not by if/else code (model-driven vs. hardcoded, 1.1).

**What is fixed vs. decided at runtime:**

| Fixed in advance (by you, the developer) | Decided at runtime (by the coordinator's model) |
|---|---|
| Which subagents exist | Which of them to call for this request |
| Each subagent's `description`, prompt and tools | The order of the calls |
| The coordinator's system prompt | How many times to call each one |
| | The task text passed to each subagent |
| | When to stop and give the final answer |

**Example with an orchestrator, an order agent and a refund agent** (from the [agentic-ai-hello-world](https://github.com/arpit-jain-mygit/agentic-ai-hello-world) practice app):

| User asks | The coordinator will likely call |
|---|---|
| "Where is my order 9931?" | order agent only |
| "Can I get a refund for 9931?" | refund agent (maybe the order agent first, to get the price) |
| "9931 arrived broken. Where is it and can I get a refund?" | both |
| "Hi, what are your opening hours?" | neither; it answers directly |

Because it's a model decision, the same question can sometimes take a different path on a different run.

**Why the `description` matters:** it is the only thing the coordinator sees about each subagent when choosing. A vague or overlapping description leads to the wrong subagent or no subagent, just like the wrong-tool problem in 2.1.

**When you *don't* want the model to choose:** if the steps are fixed and known in advance, use a simple pipeline (prompt chaining) instead of an orchestrator (1.6). If one step must always happen, force it with a hook or `tool_choice` rather than hoping the coordinator picks it (1.5, 2.3).

**For the exam:** the coordinator dynamically selects subagents based on the request. It is not a fixed routing script.

**Reference:** [Building effective agents - Anthropic](https://www.anthropic.com/research/building-effective-agents), "orchestrator-workers" workflow: subtasks aren't pre-defined but determined by the orchestrator based on the specific input.

---

## 1.1 Tool vs. agent

Back to [1.1 Design and implement agentic loops](ccaf.md#11-design-and-implement-agentic-loops-for-autonomous-task-execution).

**In one line:** a **tool** does one fixed job when asked. An **agent** decides what to do, uses tools to do it, and keeps going until the job is done.

**Analogy:** a calculator is a tool: press the same buttons, get the same answer, every time. An accountant is an agent: they decide which calculations to run, look at the results, and decide what to do next. The accountant *uses* the calculator.

| | Tool | Agent |
|---|---|---|
| What it is | A function: code with inputs and an output (an API call, a database query, a file read) | A model + system prompt + its own tools, running the agentic loop |
| Thinks? | No. Same input gives the same output | Yes. It decides what to do next based on what it has seen |
| Steps | One call, one result | Many turns, until it decides it's done (`end_turn`) |
| Who runs it | Your code (the harness), when the model asks | The harness runs its loop; the model drives it |
| Has tools? | No | Yes, a scoped set |
| Has context? | No memory, no conversation | Its own conversation (context window) |
| Example | `look_up_order(order_id)`, `issue_refund(...)` | an order agent, a refund agent, Claude Code itself |

**Where they meet: a subagent looks like a tool from outside.** This is the usual source of confusion.

**How an agent can be started "by a tool call"**, step by step:

1. **A model can't run anything.** All it can do is write text. To get something done, it writes a tool request, such as "call `look_up_order` with `order_id=9931`". Our code reads that request and runs the matching Python function.
2. **So the model can't start another agent by itself either.** It has no "start agent" ability. It can only ask for a tool by name.
3. **So we give it a tool whose Python function starts an agent.** When the orchestrator's model asks for `ask_refund_agent`, our code runs that function, and the function's body calls `run_agent(...)` for the refund agent.
4. **The model can't tell the difference.** For both kinds of tool it sends a name and inputs, and gets one result back. What ran in between is hidden from it.

The only difference is what the Python function does when it runs:

```python
def look_up_order(order_id):          # plain tool: fixed code, returns at once
    return ORDERS[order_id]

def ask_refund_agent(task):           # delegation tool: its body starts a whole agent
    answer = run_agent("refund_agent", REFUND_PROMPT, REFUND_TOOLS, task)
    return {"answer": answer}
```

**Analogy:** the manager sits in a closed room and can only pass notes through a slot. A note might say "look up order 9931", and the assistant outside checks the system and passes the answer back. Or it might say "ask Riya about a refund", and the assistant takes it to Riya, who works on it for a while using her own tools and then writes a reply that comes back through the slot. From inside the room both look the same: a note out, a reply in. Behind the slot, one was a quick lookup and the other was a person doing real work.

Claude's Task / Agent tool works the same way: the model asks for the Task tool, and the Agent SDK's code behind it starts a subagent.

**A simple test:** does it make decisions? If it always does the same thing for the same input, it's a tool. If a model chooses its next step, it's an agent.

**Good code structure:** keep plain tools and agent definitions in separate places (for example `tools.py` vs. `subagents.py` / `orchestrator.py`), with the "start a subagent" wrapper living next to the agent that uses it. The practice app [agentic-ai-hello-world](https://github.com/arpit-jain-mygit/agentic-ai-hello-world) is laid out this way.

**For the exam:**

- Tools are how an agent *acts*; the loop is what makes it an *agent* (agent = model + tools + loop).
- Spawning a subagent is a tool call (Task tool); the subagent itself is an agent with isolated context and scoped tools.

**References:**

- [Building effective agents - Anthropic](https://www.anthropic.com/research/building-effective-agents): agents as LLMs using tools based on environmental feedback in a loop
- [How tool use works - Claude docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview): what a tool is and how Claude calls it

---

## 1.2 Synthesize: combining subagent answers

Back to [1.2 Orchestrate multi-agent systems](ccaf.md#12-orchestrate-multi-agent-systems-with-coordinator-subagent-patterns).

**In one line:** no single subagent knows the whole answer. The coordinator takes their separate answers and **combines them into one reply**. "Synthesize" just means *combine into one*.

**Example** (customer: "Order 9931 arrived broken. Where is it and can I get a refund?"):

```
Order agent   knows:  "delivered, $120"     (nothing about refunds)
Refund agent  knows:  "refunded $120"       (nothing about delivery)
                          │                       │
                          └──── Coordinator ──────┘
                                     │
                    combines both into ONE reply
                                     ↓
"Your order 9931 was delivered. Since it arrived broken, I've refunded $120."
```

**Analogy:** a manager gets two status updates from the team ("parcel delivered", "refund done") and writes **one** clear email to the customer, instead of forwarding two separate messages.

**Where it happens:** in the coordinator's last turn. Its LLM sees the whole conversation, including every subagent answer (each returned as a tool result), and replies with `end_turn` and the combined answer.

**The coordinator's four jobs, simply:**

| Job | Simple meaning | In the example |
|---|---|---|
| Select | Decide *which* helpers are needed | order agent + refund agent |
| Route | Send each one its task | "Find status...", "Refund 9931, $120..." |
| Manage errors | Handle it if a helper fails | (nothing failed) |
| Synthesize | Combine their answers into one | the final reply |

**Good synthesis:** it covers every part of the original question (see [the narrow-decomposition trap](#12-the-narrow-decomposition-trap)), keeps each fact as the subagent reported it, and says honestly if a part is missing (for example "refund status unavailable") instead of hiding the gap.

**For the exam:** the coordinator *assembles* the final answer from subagent results; it doesn't do the subagents' work itself. If the coordinator finds the combined result falls short, it can send work back for another pass (iterative refinement).

**Reference:** [How we built our multi-agent research system - Anthropic](https://www.anthropic.com/research/multi-agent-research-system): the lead agent synthesizes subagents' results and decides whether more research is needed.

## 1.2 Manage errors when a subagent fails

Back to [1.2 Orchestrate multi-agent systems](ccaf.md#12-orchestrate-multi-agent-systems-with-coordinator-subagent-patterns).

**In one line:** the coordinator is the only place that sees every subagent, so it is also the only place that can decide what to do when one fails.

**Why it matters:** if a subagent fails and the coordinator never hears about it, the customer gets a confident answer built on nothing. In hub-and-spoke, every failure must come back to the hub as a message, not as an exception that stops the whole run.

**What the practice code does** ([agents/orchestrator.py](https://github.com/arpit-jain-mygit/agentic-ai-hello-world/blob/main/agents/orchestrator.py)):

1. A tool that fails returns `{"error": ...}` with `is_error: true` on its tool result, so Claude knows the call failed and can try another way.
2. A subagent that fails returns `{"error": "refund_agent failed: ..."}` to the coordinator instead of crashing it.
3. The coordinator's prompt says what to do with that: retry once with a clearer task, or tell the customer which part could not be checked.

**Example:**

```
Refund agent  -> error: "refund_agent failed: overloaded"
Coordinator   -> retries once with a clearer task
              -> still fails: tells the customer "I could not check the refund, please try again"
```

**Reference:** [Handle tool calls - Claude API docs](https://docs.claude.com/en/docs/agents-and-tools/tool-use/implement-tool-use): a tool result can be marked as an error with `is_error`.

---

## 1.2 Iterative refinement: check, then re-delegate

Back to [1.2 Orchestrate multi-agent systems](ccaf.md#12-orchestrate-multi-agent-systems-with-coordinator-subagent-patterns).

**In one line:** after the coordinator writes its answer, a second check looks for gaps. If it finds one, the coordinator delegates again instead of stopping.

**The loop:** delegate, then synthesize, then check, then re-delegate if the answer falls short. Repeat until the check passes.

**What the practice code does** ([agents/orchestrator.py](https://github.com/arpit-jain-mygit/agentic-ai-hello-world/blob/main/agents/orchestrator.py)): `run_orchestrator` calls a reviewer agent that has no tools. The reviewer replies `PASS` or `FAIL: <gap>`. On `FAIL`, the coordinator runs again with its previous answer and the gap, and it delegates again. `MAX_REFINEMENTS = 2` is a safety limit, so a bad answer cannot loop forever.

**Why a cap:** the exam text says to repeat "until coverage is sufficient". A real system still needs a stop, or cost and waiting time grow without limit. Two rounds is a choice for this app, not a rule from the exam.

**Example:**

```
Round 0: coordinator answers "delivered, $120"               reviewer: FAIL: no refund decision
Round 1: coordinator delegates to the refund agent, answers  reviewer: PASS
```

**Reference:** [Building effective agents - Anthropic](https://www.anthropic.com/engineering/building-effective-agents): the evaluator-optimizer workflow, where one model checks another's output and feeds back what to fix.

---

## 1.3 Passing context to a subagent

Back to [1.3 Configure subagent invocation, context passing, and spawning](ccaf.md#13-configure-subagent-invocation-context-passing-and-spawning).

**In one line:** the prompt is the only handoff. A subagent starts with nothing, so every fact it needs must be in the task text.

**What the practice code does** ([agents/orchestrator.py](https://github.com/arpit-jain-mygit/agentic-ai-hello-world/blob/main/agents/orchestrator.py)):

- `start_subagent` sends the subagent only the `task` string. It never sends the coordinator's messages.
- `HANDOFF_HINT` is added to each delegation tool's description: "Pass a complete task: the subagent knows nothing else." This tells the coordinator to write a full task.

**What is still weak:** nothing checks the task. A short task such as "check the refund" still goes through. The exam text asks for complete prior findings in a structured format, and the code does not enforce that yet.

**Example:**

```
Vague:    "check the refund"
Complete: "Order 9931, Headphones, $120, delivered 3 days ago. The customer says it arrived broken.
           Check the refund policy and say eligible yes or no, with the rule used."
```

**Reference:** [Subagents in the SDK - Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/subagents): each subagent runs in its own context window, and the parent passes it the task in the prompt.

---

## 1.3 Model per subagent (practice extra)

Back to [1.3 Configure subagent invocation, context passing, and spawning](ccaf.md#13-configure-subagent-invocation-context-passing-and-spawning).

**Not in the 1.3 text:** the current exam text lists the description, system prompt and tools for an agent definition. The practice app also gives each agent an optional `model`. That is a cost choice, not an exam requirement.

**In one line:** a simple subagent can name a cheaper model, while the coordinator and the reviewer keep the default.

**What the practice code does:** `worker_agents.json` names `claude-haiku-5-5` for the order agent and `claude-opus-5-5` for the refund agent. The coordinator and the reviewer use the default model. `run_agent` takes a `model` argument, and `start_subagent` passes each agent's model through.

---

## 1.4 Gate a refund behind the policy check

Back to [1.4 Implement multi-step workflows](ccaf.md#14-implement-multi-step-workflows-with-enforcement-and-handoff-patterns).

**In one line:** a prompt that says "check the policy first" can be skipped. A gate in code cannot.

**Why code, not a prompt:** the exam text says prompts alone have a non-zero failure rate. When a rule must hold every time, such as "no refund before the policy check", put it in code.

**What the practice code does** ([tools/functions.py](https://github.com/arpit-jain-mygit/agentic-ai-hello-world/blob/main/tools/functions.py)):

1. `check_refund_policy` adds the order to `ELIGIBLE_ORDERS` when the order is within the 30-day rule.
2. `issue_refund` returns an error unless the order is in `ELIGIBLE_ORDERS`.

So the refund agent can still call the tools in any order. The wrong order fails, and the error comes back to Claude as `is_error`.

**Example:**

```
issue_refund(9931)                 -> blocked: check_refund_policy must say eligible first
check_refund_policy(9931)          -> eligible: true
issue_refund(9931)                 -> refunded
```

**Caveat:** `ELIGIBLE_ORDERS` lives in the running process. A real system would store it somewhere durable, such as a database, so a restart does not forget the check.

**Reference:** [Intercept and control agent behavior with hooks - Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/hooks): hooks run in code before a tool call, so a rule holds whatever the model says.

---

## 1.4 Handoff summary for a human agent

Back to [1.4 Implement multi-step workflows](ccaf.md#14-implement-multi-step-workflows-with-enforcement-and-handoff-patterns).

**In one line:** when a case goes to a human, the human should not have to read the whole chat to act.

**What the summary holds:** the order ID, the customer's email, the item and price, the root cause, and the recommended action. The exam text lists customer ID, root cause, refund amount and recommended action. The practice app uses the customer email because that is the only customer ID in its data.

**What the practice code does:** the `prepare_handoff` tool in [tools/functions.py](https://github.com/arpit-jain-mygit/agentic-ai-hello-world/blob/main/tools/functions.py) builds that summary from the order record. The refund agent calls it when the policy says no.

**Example:**

```
Order 4471, Laptop stand, $40, sam@example.com
Root cause:          not delivered yet
Recommended action:  wait for delivery, then re-check the policy
```

---

## 1.5 Pre-execution hook: block and redirect

Back to [1.5 Apply Agent SDK hooks](ccaf.md#15-apply-agent-sdk-hooks-for-tool-call-interception-and-data-normalization).

**In one line:** a pre-execution hook looks at a tool call before it runs. If the call breaks a rule, the hook stops it and sends the case somewhere else.

**The rule in the practice app:** refunds above $100 are not allowed. The cap is low on purpose: the demo prices are $40 and $120, so a $500 cap would never trigger.

**What the practice code does** ([tools/hooks.py](https://github.com/arpit-jain-mygit/agentic-ai-hello-world/blob/main/tools/hooks.py)): `pre_tool_hook` runs before each tool call. For `issue_refund` above the cap, it does not run the refund. It calls `prepare_handoff` and returns an error with the handoff summary. The loop in [agents/agent_loop.py](https://github.com/arpit-jain-mygit/agentic-ai-hello-world/blob/main/agents/agent_loop.py) checks the hook result before it runs the tool.

**Example:**

```
issue_refund(9931, 120)   -> blocked: refund above $100 is not allowed; sent to a human agent
issue_refund(9931, 50)    -> refunded
```

**Reference:** [Intercept and control agent behavior with hooks - Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/hooks): a PreToolUse hook can block a tool call before it runs.

---

## 1.5 PostToolUse hook: normalize results

Back to [1.5 Apply Agent SDK hooks](ccaf.md#15-apply-agent-sdk-hooks-for-tool-call-interception-and-data-normalization).

**In one line:** a PostToolUse hook cleans up a tool's result before Claude reads it, so Claude sees one consistent format.

**Why it matters:** tools from different systems often return dates, money and status codes in different shapes. If Claude has to make sense of each shape, its answers get less reliable. Fixing the shape in code means Claude always sees the same thing.

**What the practice code does** ([tools/hooks.py](https://github.com/arpit-jain-mygit/agentic-ai-hello-world/blob/main/tools/hooks.py)): `post_tool_hook` changes the price from a number to text with a currency, so `120` becomes `"120.00 USD"`. The loop runs the hook after the tool and before the result goes back to Claude.

**Example:**

```
Tool returns:   {"price": 120}
Claude reads:   {"price": "120.00 USD"}
```

Real MCP tools would need more than this: Unix timestamps turned into ISO 8601 dates, and numeric status codes turned into words. The practice app has only the price rule, because its data is already consistent.

**Reference:** [Intercept and control agent behavior with hooks - Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/hooks): a PostToolUse hook runs after a tool call and can change its result.
