# CCAF - Additional Details

Deeper explanations that support the main notes in [ccaf.md](ccaf.md). Each section links back to its topic there.

## Contents

- [1.1 The agentic loop: the four steps in simple words](#11-the-agentic-loop-the-four-steps-in-simple-words)
- [1.1 All stop_reason values](#11-all-stop_reason-values)
- [1.2 The narrow-decomposition trap](#12-the-narrow-decomposition-trap)
- [1.3 Why spawning a subagent is a tool call](#13-why-spawning-a-subagent-is-a-tool-call)

---

## 1.1 The agentic loop: the four steps in simple words

Back to [1.1 The agentic loop](ccaf.md#11-the-agentic-loop).

Think of a support agent at a help desk handling "Where's my refund for order 9931?":

1. **Perceive:** read everything on the desk: the customer's question plus any notes gathered so far.
2. **Reason:** decide what to do next: "I need to look up the order first."
3. **Act:** do one thing: open the order system and search for 9931.
4. **Observe:** read what came back: "No refund on file." This becomes a new note on the desk.

Then go back to step 1 with the new note. The agent repeats this until it has enough to answer, then replies and stops.

**What each step looks like in the Claude API, and where the agent fits:**

The agent is not one of the four steps. It is the whole system that runs all four: **agent = model (Claude) + tools + loop (your code or the Agent SDK)**, guided by the system prompt.

| Step | What happens | Who does it | Agent part used |
|---|---|---|---|
| Perceive | Claude reads the whole `messages` list: the user's request plus every earlier `tool_result` | Claude | Model (the brain) |
| Reason | Claude decides whether it needs a tool, and which one with which inputs | Claude | Model, guided by the system prompt |
| Act | Claude replies with a `tool_use` block and `stop_reason: "tool_use"`; **your code** runs the tool | Claude asks, your code executes | Tools (the hands), run by the loop |
| Observe | Your code appends the output as a `tool_result` and calls the API again | Your code sends it, Claude reads it | Loop (the harness) feeding the model |
| **All four, repeated until `end_turn`** | The cycle continues until Claude has enough to answer | Model + loop together | **The agent** |

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

## 1.1 All stop_reason values

Back to [1.1 The agentic loop](ccaf.md#11-the-agentic-loop).

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

Back to [1.2 Coordinator-subagent pattern](ccaf.md#12-coordinator-subagent-pattern).

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

Back to [1.3 Spawning subagents and passing context](ccaf.md#13-spawning-subagents-and-passing-context).

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
