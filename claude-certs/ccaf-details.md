# CCAF - Additional Details

Deeper explanations that support the main notes in [ccaf.md](ccaf.md). Each section links back to its topic there.

## Contents

- [1.1 The agentic loop: the four steps in simple words](#11-the-agentic-loop-the-four-steps-in-simple-words)
- [1.1 All stop_reason values](#11-all-stop_reason-values)

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
