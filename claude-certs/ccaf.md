# Claude Certified Architect - Foundations (CCAF)

Study notes built on the official **Claude Certified Architect - Foundations Exam Guide** (exam code CCAR-F, version 1.0, effective July 2026). Every domain and task statement below follows the guide. Deeper explanations of individual topics live in [Additional Details](ccaf-details.md).

## Table of Contents

- [Exam at a Glance](#exam-at-a-glance)
- [Exam Scenarios](#exam-scenarios)
- [Domain 1: Agentic Architecture & Orchestration (27%)](#domain-1-agentic-architecture--orchestration-27)
  - [1.1 Design and implement agentic loops for autonomous task execution](#11-design-and-implement-agentic-loops-for-autonomous-task-execution)
  - [1.2 Orchestrate multi-agent systems with coordinator-subagent patterns](#12-orchestrate-multi-agent-systems-with-coordinator-subagent-patterns)
  - [1.3 Configure subagent invocation, context passing, and spawning](#13-configure-subagent-invocation-context-passing-and-spawning)
  - [1.4 Implement multi-step workflows with enforcement and handoff patterns](#14-implement-multi-step-workflows-with-enforcement-and-handoff-patterns)
  - [1.5 Apply Agent SDK hooks for tool call interception and data normalization](#15-apply-agent-sdk-hooks-for-tool-call-interception-and-data-normalization)
  - [1.6 Design task decomposition strategies for complex workflows](#16-design-task-decomposition-strategies-for-complex-workflows)
  - [1.7 Manage session state, resumption, and forking](#17-manage-session-state-resumption-and-forking)
  - [Domain 1 exam decision reflexes](#domain-1-exam-decision-reflexes)
- [Domain 2: Tool Design & MCP Integration (18%)](#domain-2-tool-design--mcp-integration-18)
  - [2.1 Design effective tool interfaces with clear descriptions and boundaries](#21-design-effective-tool-interfaces-with-clear-descriptions-and-boundaries)
  - [2.2 Implement structured error responses for MCP tools](#22-implement-structured-error-responses-for-mcp-tools)
  - [2.3 Distribute tools appropriately across agents and configure tool choice](#23-distribute-tools-appropriately-across-agents-and-configure-tool-choice)
  - [2.4 Integrate MCP servers into Claude Code and agent workflows](#24-integrate-mcp-servers-into-claude-code-and-agent-workflows)
  - [2.5 Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively](#25-select-and-apply-built-in-tools-read-write-edit-bash-grep-glob-effectively)
  - [Domain 2 exam decision reflexes](#domain-2-exam-decision-reflexes)
- [Domain 3: Claude Code Configuration & Workflows (20%)](#domain-3-claude-code-configuration--workflows-20)
  - [3.1 Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization](#31-configure-claudemd-files-with-appropriate-hierarchy-scoping-and-modular-organization)
  - [3.2 Create and configure custom slash commands and skills](#32-create-and-configure-custom-slash-commands-and-skills)
  - [3.3 Apply path-specific rules for conditional convention loading](#33-apply-path-specific-rules-for-conditional-convention-loading)
  - [3.4 Determine when to use plan mode vs direct execution](#34-determine-when-to-use-plan-mode-vs-direct-execution)
  - [3.5 Apply iterative refinement techniques for progressive improvement](#35-apply-iterative-refinement-techniques-for-progressive-improvement)
  - [3.6 Integrate Claude Code into CI/CD pipelines](#36-integrate-claude-code-into-cicd-pipelines)
  - [Domain 3 exam decision reflexes](#domain-3-exam-decision-reflexes)
- [Domain 4: Prompt Engineering & Structured Output (20%)](#domain-4-prompt-engineering--structured-output-20)
  - [4.1 Design prompts with explicit criteria to improve precision and reduce false positives](#41-design-prompts-with-explicit-criteria-to-improve-precision-and-reduce-false-positives)
  - [4.2 Apply few-shot prompting to improve output consistency and quality](#42-apply-few-shot-prompting-to-improve-output-consistency-and-quality)
  - [4.3 Enforce structured output using tool use and JSON schemas](#43-enforce-structured-output-using-tool-use-and-json-schemas)
  - [4.4 Implement validation, retry, and feedback loops for extraction quality](#44-implement-validation-retry-and-feedback-loops-for-extraction-quality)
  - [4.5 Design efficient batch processing strategies](#45-design-efficient-batch-processing-strategies)
  - [4.6 Design multi-instance and multi-pass review architectures](#46-design-multi-instance-and-multi-pass-review-architectures)
  - [Domain 4 exam decision reflexes](#domain-4-exam-decision-reflexes)
- [Domain 5: Context Management & Reliability (15%)](#domain-5-context-management--reliability-15)
  - [5.1 Manage conversation context to preserve critical information across long interactions](#51-manage-conversation-context-to-preserve-critical-information-across-long-interactions)
  - [5.2 Design effective escalation and ambiguity resolution patterns](#52-design-effective-escalation-and-ambiguity-resolution-patterns)
  - [5.3 Implement error propagation strategies across multi-agent systems](#53-implement-error-propagation-strategies-across-multi-agent-systems)
  - [5.4 Manage context effectively in large codebase exploration](#54-manage-context-effectively-in-large-codebase-exploration)
  - [5.5 Design human review workflows and confidence calibration](#55-design-human-review-workflows-and-confidence-calibration)
  - [5.6 Preserve information provenance and handle uncertainty in multi-source synthesis](#56-preserve-information-provenance-and-handle-uncertainty-in-multi-source-synthesis)
  - [Domain 5 exam decision reflexes](#domain-5-exam-decision-reflexes)
- [How to Prepare](#how-to-prepare)
- [Exam Policies](#exam-policies)
- [Scope: In and Out](#scope-in-and-out)

---

## Exam at a Glance

| Item | Detail |
|---|---|
| Credential | Claude Certified Architect - Foundations |
| Exam code | CCAR-F |
| Number of items | 60 |
| Item format | Multiple-choice and multiple-response; each item states how many responses to select |
| Scenario structure | 4 scenarios drawn at random from a bank of 6 |
| Time limit | 120 minutes |
| Delivery | Proctored: online proctored or test center, per program policy |
| Passing score | Scaled score of 720 on a 100-1,000 scale |
| Exam fee | $125 USD |
| Validity | 12 months from the date the credential is awarded |
| Result reporting | Pass/fail with scaled score, plus percent-correct by domain on the score report |

**Blueprint (domain weights):**

| Domain | Content domain | Weight |
|---|---|---|
| 1 | Agentic Architecture & Orchestration | 27% |
| 2 | Tool Design & MCP Integration | 18% |
| 3 | Claude Code Configuration & Workflows | 20% |
| 4 | Prompt Engineering & Structured Output | 20% |
| 5 | Context Management & Reliability | 15% |

Domain 1 carries the most weight, so it is the place to start.

---

## Exam Scenarios

The exam is built on six scenarios. Four are picked at random for each candidate.

1. **Customer Support Resolution Agent** (Agent SDK + custom MCP tools `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`; target 80%+ first-contact resolution). Primary domains: 1, 2, 5.
2. **Code Generation with Claude Code** (custom slash commands, CLAUDE.md, plan mode vs direct execution). Primary domains: 3, 5.
3. **Multi-Agent Research System** (coordinator with web search, document analysis, synthesis and report subagents). Primary domains: 1, 2, 5.
4. **Developer Productivity with Claude** (Agent SDK tools that explore codebases, generate boilerplate and automate tasks using built-in tools and MCP servers). Primary domains: 2, 3, 1.
5. **Claude Code for Continuous Integration** (automated code review and test generation in a CI/CD pipeline; actionable feedback with few false positives). Primary domains: 3, 4.
6. **Structured Data Extraction** (extraction from unstructured documents validated against JSON schemas, with edge cases handled gracefully). Primary domains: 4, 5.

---

## Domain 1: Agentic Architecture & Orchestration (27%)

### 1.1 Design and implement agentic loops for autonomous task execution

**Knowledge**
- The loop: send a request to Claude, check `stop_reason` (`tool_use` vs `end_turn`), run the requested tools, return the results for the next iteration. ([the four steps, simply](ccaf-details.md#11-the-agentic-loop-the-four-steps-in-simple-words))
- Tool results are appended to the conversation history so Claude can reason about the next action. ([all `stop_reason` values](ccaf-details.md#11-all-stop_reason-values))
- Model-driven decisions (Claude picks the next tool from context) vs pre-configured decision trees or fixed tool sequences. ([tool vs. agent](ccaf-details.md#11-tool-vs-agent))

**Skills**
- Control flow: continue on `tool_use`, stop on `end_turn`.
- Add tool results to the context between iterations so Claude can use the new information.
- Avoid the anti-patterns: parsing natural language to decide when to stop, using an arbitrary iteration cap as the main stop condition, or treating assistant text as a completion signal.

### 1.2 Orchestrate multi-agent systems with coordinator-subagent patterns

**Knowledge**
- Hub-and-spoke: the coordinator manages all communication between subagents, error handling and routing.
- Subagents run in isolated context and do not inherit the coordinator's history.
- The coordinator decomposes the task, delegates, aggregates results and decides which subagents to call based on query complexity.
- Risk: overly narrow decomposition leaves broad topics incompletely covered. ([narrow-decomposition trap](ccaf-details.md#12-the-narrow-decomposition-trap))

**Skills**
- Design a coordinator that analyzes the query and selects subagents, instead of always running the full pipeline. ([the coordinator picks subagents at runtime](ccaf-details.md#12-the-coordinator-picks-subagents-at-runtime))
- Partition research scope so subagents do not duplicate work (distinct subtopics or source types).
- Run iterative refinement: the coordinator evaluates synthesis output for gaps, re-delegates with targeted queries, and repeats until coverage is sufficient. ([synthesize](ccaf-details.md#12-synthesize-combining-subagent-answers))
- Route all subagent communication through the coordinator for observability and consistent error handling.

### 1.3 Configure subagent invocation, context passing, and spawning

**Knowledge**
- The `Task` tool spawns subagents. A coordinator's `allowedTools` must include `"Task"` to spawn them. ([spawning is a tool call](ccaf-details.md#13-why-spawning-a-subagent-is-a-tool-call))
- Subagent context must be passed explicitly in its prompt. Nothing is inherited or shared automatically. ([how a subagent knows its tools](ccaf-details.md#13-how-a-subagent-knows-which-tools-it-has))
- An `AgentDefinition` holds the description, system prompt and tool restrictions for each subagent type.
- Fork-based session management explores divergent approaches from a shared baseline.

**Skills**
- Put complete prior findings (for example, search results) directly into the next subagent's prompt.
- Use structured formats that separate content from metadata (source URLs, document names, page numbers) so attribution survives.
- Spawn parallel subagents by emitting several `Task` calls in one coordinator response.
- Write coordinator prompts that state goals and quality criteria, not step-by-step procedures.

### 1.4 Implement multi-step workflows with enforcement and handoff patterns

**Knowledge**
- Programmatic enforcement (hooks, prerequisite gates) vs prompt-based guidance. Prompts alone have a non-zero failure rate.
- Use code when deterministic compliance is required, such as identity verification before a financial operation.
- Structured handoff protocols for mid-process escalation: customer details, root-cause analysis and recommended actions.

**Skills**
- Block downstream tool calls until prerequisites are done. Example: block `process_refund` until `get_customer` returns a verified customer ID.
- Split multi-concern requests into distinct items, investigate each (in parallel where possible), then synthesize one resolution.
- Compile a structured handoff summary (customer ID, root cause, refund amount, recommended action) for a human agent who cannot see the transcript.

### 1.5 Apply Agent SDK hooks for tool call interception and data normalization

**Knowledge**
- PostToolUse hooks transform tool results before the model reads them.
- Pre-execution hooks intercept outgoing tool calls to enforce rules, such as blocking refunds above a threshold.
- Hooks give deterministic guarantees. Prompt instructions give probabilistic compliance.

**Skills**
- Normalize heterogeneous data from MCP tools (Unix timestamps, ISO 8601, numeric status codes) in PostToolUse before the agent sees it.
- Block policy-violating calls (for example, refunds above $500) and redirect them to another workflow such as human escalation.
- Choose hooks over prompts whenever a business rule must hold every time.

### 1.6 Design task decomposition strategies for complex workflows

**Knowledge**
- Fixed sequential pipelines (prompt chaining) vs dynamic adaptive decomposition driven by what each step finds.
- Prompt chaining can split a review into per-file passes followed by a cross-file integration pass.
- Adaptive plans generate subtasks as discoveries are made.

**Skills**
- Pick the pattern that fits: prompt chaining for predictable multi-aspect reviews, dynamic decomposition for open-ended investigation.
- Split large code reviews into per-file local passes plus a cross-file integration pass, to avoid attention dilution.
- For open-ended work (such as "add comprehensive tests to a legacy codebase"), map the structure first, identify high-impact areas, then build a prioritized plan that adapts as dependencies appear.

### 1.7 Manage session state, resumption, and forking

**Knowledge**
- Named resumption with `--resume <session-name>` continues a specific prior conversation.
- `fork_session` creates independent branches from a shared analysis baseline.
- Tell the agent about file changes made since a session was analyzed.
- A new session with a structured summary is more reliable than resuming when tool results have gone stale.

**Skills**
- Use `--resume` with session names to continue named investigations across work sessions.
- Use `fork_session` to compare parallel approaches (two test strategies, two refactors) from one shared analysis.
- Choose between resuming (prior context mostly still valid) and starting fresh with an injected summary (prior tool results are stale).
- After a resume, inform the session about specific file changes so it re-analyzes only what changed.

### Domain 1 exam decision reflexes

| Scenario | Answer |
|---|---|
| Rule must never break | Hook or code gate, not a prompt |
| Fixed, known steps | Prompt chaining |
| Steps discovered along the way | Adaptive decomposition with a coordinator |
| Subagent needs information | Put it explicitly in its prompt (nothing is inherited) |
| Independent subagents | Several `Task` calls in one coordinator response |
| Session is stale | Summarize and start fresh |

---

## Domain 2: Tool Design & MCP Integration (18%)

### 2.1 Design effective tool interfaces with clear descriptions and boundaries

**Knowledge**
- Tool descriptions are how Claude selects tools. Minimal descriptions cause unreliable selection among similar tools.
- A good description includes input formats, example queries, edge cases and boundaries (when to use it and when not to).
- Overlapping names or descriptions cause misrouting, for example `analyze_content` vs `analyze_document`.
- System prompt wording can create unintended tool associations, for example keyword-sensitive instructions.

**Skills**
- Write descriptions that separate each tool's purpose, inputs, outputs and when to use it versus similar tools.
- Rename tools to remove overlap (for example, `analyze_content` becomes `extract_web_results` with a web-specific description).
- Split generic tools into purpose-specific ones with clear input/output contracts (`extract_data_points`, `summarize_content`, `verify_claim_against_source`).
- Review system prompts for keyword-sensitive instructions that override good tool descriptions.

### 2.2 Implement structured error responses for MCP tools

**Knowledge**
- The MCP `isError` flag reports tool failures back to the agent.
- Three kinds of failure: transient (timeouts, service unavailable), validation (invalid input), and business or permission errors (policy violations, not allowed).
- Uniform errors such as "Operation failed" stop the agent from choosing a sensible recovery.
- Retryable and non-retryable errors must be distinguishable, so the agent does not waste retries.

**Skills**
- Return structured error metadata: `errorCategory` (transient / validation / permission), `isRetryable` (boolean) and a human-readable message.
- For business-rule violations, return `isRetryable: false` with an explanation the customer can understand.
- Handle transient failures locally inside a subagent. Propagate only what it cannot resolve, along with partial results and what was attempted.
- Tell an access failure (needs a retry decision) apart from a valid empty result (a successful query with no matches).

### 2.3 Distribute tools appropriately across agents and configure tool choice

**Knowledge**
- Too many tools (18 instead of 4-5) degrades selection reliability.
- Agents given tools outside their specialization misuse them, for example a synthesis agent attempting web searches.
- Scoped tool access: each agent gets the tools its role needs. Limited cross-role tools are allowed for high-frequency needs.
- `tool_choice` options: `"auto"`, `"any"`, and forced selection with `{"type": "tool", "name": "..."}`.

**Skills**
- Restrict each subagent's tool set to its role.
- Replace generic tools with constrained ones (for example, replace `fetch_url` with `load_document`, which validates document URLs).
- Give a synthesis agent a scoped `verify_fact` tool for high-frequency checks, and route complex cases through the coordinator.
- Use forced tool selection to guarantee a specific tool runs first, and `"any"` to guarantee a tool call rather than a text reply.

### 2.4 Integrate MCP servers into Claude Code and agent workflows

**Knowledge**
- Server scoping: project `.mcp.json` for shared team tooling, user `~/.claude.json` for personal or experimental servers.
- `${VAR}` expansion in `.mcp.json` keeps credentials out of committed files.
- Tools from all configured servers are discovered at connection time and available together.
- MCP resources expose content catalogs (issue summaries, documentation hierarchies, database schemas), which cut down on exploratory tool calls.

**Skills**
- Configure shared servers in project `.mcp.json` with `${VAR}` expansion for tokens.
- Configure personal or experimental servers in user-scoped `~/.claude.json`.
- Write MCP tool descriptions in enough detail that the agent prefers the capable MCP tool over a built-in one (such as Grep).
- Use an existing community MCP server for standard integrations (for example Jira) and build custom servers only for team-specific workflows.
- Expose content catalogs as MCP resources so the agent can see what data is available.

### 2.5 Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively

**Knowledge**
- Grep searches file contents (function names, error messages, import statements).
- Glob matches file paths by name or extension.
- Read and Write handle full-file operations. Edit makes targeted changes that need a unique text match.
- When Edit fails on a non-unique match, Read + Write is the fallback.

**Skills**
- Use Grep to find code, and Glob for naming patterns such as `**/*.test.tsx`.
- Build understanding step by step: Grep for entry points, then Read to follow imports and trace the flow. Do not read everything up front.
- To trace a function across wrapper modules, list the exported names first, then Grep for each one.

### Domain 2 exam decision reflexes

| Scenario | Answer |
|---|---|
| Claude picks the wrong tool | Improve descriptions (purpose, when to use, parameters, examples) and make names distinct |
| One tool with an `action` string | Split into one tool per action |
| Tool fails | Return `isError` with `errorCategory` and `isRetryable`; don't throw |
| Query returns nothing | Success with zero results, not an error and not retryable |
| Business-rule or validation error | `isRetryable: false` |
| Agent has too many tools | Scope each role to the tools it needs |
| A step must always happen | Forced `tool_choice` naming that tool |
| Personal API key in MCP config | `${VAR}` expansion, and local or user scope, never project |
| Search contents vs. find files | Grep for contents, Glob for file names |

---

## Domain 3: Claude Code Configuration & Workflows (20%)

### 3.1 Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization

**Knowledge**
- The hierarchy: user `~/.claude/CLAUDE.md`, project `.claude/CLAUDE.md` or root `CLAUDE.md`, and directory-level subfolder `CLAUDE.md` files.
- User-level instructions are personal. They are not shared with teammates through version control.
- `@import` keeps CLAUDE.md modular by referencing standards files.
- `.claude/rules/` holds topic-specific rule files as an alternative to one large CLAUDE.md.

**Skills**
- Diagnose hierarchy problems, such as a new team member missing instructions because they live in user-level config instead of project config.
- Use `@import` to pull in only the standards each package needs.
- Split a large CLAUDE.md into focused files in `.claude/rules/` (for example `testing.md`, `api-conventions.md`, `deployment.md`).
- Use `/memory` to check which memory files are loaded when behavior differs between sessions.

### 3.2 Create and configure custom slash commands and skills

**Knowledge**
- Project commands in `.claude/commands/` are shared through version control. Personal commands in `~/.claude/commands/` are not.
- Skills in `.claude/skills/<name>/SKILL.md` support frontmatter: `context`, `allowed-tools`, `argument-hint`.
- `context: fork` runs a skill in an isolated sub-agent context so its verbose output does not pollute the main conversation.
- Personal skill variants go in `~/.claude/skills/` under different names, so they do not affect teammates.

**Skills**
- Create team-wide commands in `.claude/commands/`.
- Use `context: fork` for skills that produce verbose output (codebase analysis) or explore alternatives.
- Use `allowed-tools` to restrict tools during a skill's run (for example, no file writes in a review skill).
- Use `argument-hint` to prompt for required parameters when a skill is invoked without them.
- Choose between a skill (on-demand, task-specific) and CLAUDE.md (always loaded, universal standards).

### 3.3 Apply path-specific rules for conditional convention loading

**Knowledge**
- `.claude/rules/` files with YAML frontmatter `paths:` glob patterns activate only for matching files.
- Path-scoped rules load only when matching files are edited, which saves context and tokens.
- Glob rules beat directory-level CLAUDE.md files for conventions that span directories, such as test files spread across a codebase.

**Skills**
- Write rule files with `paths:` scoping, for example `paths: ["terraform/**/*"]`.
- Use glob patterns such as `**/*.test.tsx` to apply conventions by file type, wherever the file lives.
- Pick path-specific rules over subdirectory CLAUDE.md files when a convention applies across the codebase.

### 3.4 Determine when to use plan mode vs direct execution

**Knowledge**
- Plan mode suits complex work: large-scale changes, several valid approaches, architectural decisions and multi-file edits.
- Direct execution suits simple, well-scoped changes, such as adding one validation check to one function.
- Plan mode allows safe exploration and design before changes are made, so costly rework is avoided.
- The Explore subagent isolates verbose discovery output and returns summaries to the main context.

**Skills**
- Use plan mode for architectural work (microservice restructuring) and for migrations that touch many files (for example, 45+ files).
- Use direct execution for a single-file bug fix with a clear stack trace, or a small conditional added to a date check.
- Use the Explore subagent for verbose discovery phases, so the main context does not run out.
- Combine them: plan the migration first, then execute the approved plan directly.

### 3.5 Apply iterative refinement techniques for progressive improvement

**Knowledge**
- Concrete input/output examples communicate expected transformations best when prose descriptions are read inconsistently.
- Test-driven iteration: write tests first, then share failures to guide each pass.
- The interview pattern: Claude asks questions that surface design considerations before it implements.
- Use a single detailed message for interacting problems. Fix independent problems one at a time.

**Skills**
- Give 2-3 concrete input/output examples to pin down transformation rules, especially for edge cases such as null values in migration scripts.
- Write tests covering expected behavior, edge cases and performance before implementation, then iterate on the failures.
- Use the interview pattern to surface design choices (cache invalidation strategy, failure modes) in unfamiliar domains.
- Batch interacting issues into one message. Fix independent issues in sequence.

### 3.6 Integrate Claude Code into CI/CD pipelines

**Knowledge**
- The `-p` (`--print`) flag runs Claude Code non-interactively in pipelines.
- `--output-format json` and `--json-schema` enforce machine-parseable output in CI.
- CLAUDE.md gives CI runs the project context: testing standards, fixture conventions, review criteria.
- Session context isolation: the session that wrote code reviews it less effectively than an independent instance.

**Skills**
- Run Claude Code with `-p` so a pipeline never hangs waiting for input.
- Use `--output-format json` with `--json-schema` to get structured findings that can be posted as inline PR comments.
- When re-running a review after new commits, pass prior findings and ask for new or still-unaddressed issues only, to avoid duplicate comments.
- Pass existing test files into context so generated tests do not repeat scenarios already covered.

### Domain 3 exam decision reflexes

| Scenario | Answer |
|---|---|
| Team-wide conventions | Project CLAUDE.md, committed |
| Personal preference across projects | `~/.claude/CLAUDE.md` |
| Rules for a pattern across the repo (`*.test.tsx`) | `.claude/rules/*.md` with `paths:` |
| Repeatable task the team shares | `.claude/commands/` or `.claude/skills/` |
| Skill output is verbose | `context: fork` |
| "`allowed-tools` restricts tools" | False; it only pre-approves |
| Big, risky or multi-file change | Plan mode |
| Run in CI | `claude -p` with `--output-format json` and `--json-schema` |
| Unbiased code review | A separate Claude instance |

---

## Domain 4: Prompt Engineering & Structured Output (20%)

### 4.1 Design prompts with explicit criteria to improve precision and reduce false positives

**Knowledge**
- Explicit criteria beat vague instructions. "Flag comments only when the claimed behavior contradicts the code" works where "be conservative" does not.
- General instructions such as "only report high-confidence findings" do not improve precision as much as specific categorical criteria.
- High false-positive rates erode developer trust, and that spills over onto the accurate categories.

**Skills**
- Write review criteria that name which issues to report (bugs, security) and which to skip (minor style, local patterns).
- Temporarily disable a high-false-positive category to restore trust while the prompt for that category is improved.
- Define severity levels with concrete code examples, so classification is consistent.

### 4.2 Apply few-shot prompting to improve output consistency and quality

**Knowledge**
- Few-shot examples are the most effective way to get consistently formatted, actionable output when detailed instructions alone are not enough.
- Examples show how to handle ambiguous cases (why one action was picked over plausible alternatives).
- Examples let Claude generalize judgment to new patterns, not only the cases shown.
- Examples reduce hallucination in extraction, for example by showing how to handle informal measurements and varied document structures.

**Skills**
- Write 2-4 targeted examples for ambiguous scenarios, each with the reasoning behind the choice.
- Show the exact output format in the examples (location, issue, severity, suggested fix).
- Include examples that separate acceptable code patterns from real issues, to cut false positives.
- Include examples of varied document structures (inline citations vs bibliographies) and of correct null handling for missing required fields.

### 4.3 Enforce structured output using tool use and JSON schemas

**Knowledge**
- Tool use with JSON schemas is the most reliable way to get schema-compliant output. It removes JSON syntax errors.
- `tool_choice`: `"auto"` may return text instead of calling a tool, `"any"` forces a tool call but lets Claude pick which, and a forced named tool must be called.
- Strict schemas remove syntax errors but not semantic ones (line items that do not sum to the total, values in the wrong field).
- Schema design: required vs optional fields, enums with `"other"` plus a detail string, and `"unclear"` for ambiguous cases.

**Skills**
- Define extraction tools with JSON schemas as input parameters, then read structured data from the `tool_use` block.
- Use `tool_choice: "any"` when several extraction schemas exist and the document type is unknown.
- Force a specific tool (for example `extract_metadata`) so it always runs before enrichment.
- Make fields optional or nullable when the source may not contain them, so the model returns `null` instead of inventing a value.
- Add `"unclear"` and `"other"` plus a detail field for extensible categories.
- Put format normalization rules in the prompt alongside the strict schema, to handle inconsistent source formatting.

### 4.4 Implement validation, retry, and feedback loops for extraction quality

**Knowledge**
- Retry with error feedback: append the specific validation error to the prompt on retry.
- Retries do not help when the information is absent from the source. They do help for format and structural errors.
- Feedback loop design: record which constructs trigger findings (a `detected_pattern` field) to spot patterns in dismissals.
- Semantic errors (values that don't sum, wrong field placement) are different from schema syntax errors, which tool use already eliminates.

**Skills**
- Send follow-up requests that include the original document, the failed extraction and the specific validation error.
- Recognize when a retry will fail: the information exists only in a document that was not provided.
- Add a `detected_pattern` field to findings, so false-positive patterns can be analyzed.
- Build self-correction flows: extract `calculated_total` and `stated_total`, flag mismatches with `conflict_detected`.

### 4.5 Design efficient batch processing strategies

**Knowledge**
- The Message Batches API: 50% cost savings, up to a 24-hour processing window, no guaranteed latency SLA.
- Batch suits latency-tolerant work (overnight reports, weekly audits, nightly test generation). It does not suit blocking workflows such as pre-merge checks.
- The batch API cannot run multi-turn tool calls within one request.
- `custom_id` matches each batch result to its request.

**Skills**
- Use the synchronous API for blocking pre-merge checks, and batch for overnight or weekly analysis.
- Work out submission frequency from the SLA (for example, 4-hour windows to meet a 30-hour SLA with 24-hour processing).
- On batch failures, resubmit only the failed documents (found by `custom_id`), with changes such as chunking oversized documents.
- Refine the prompt on a sample set before batch-processing a large volume, to raise first-pass success.

### 4.6 Design multi-instance and multi-pass review architectures

**Knowledge**
- Self-review is limited: a model keeps its reasoning from generation, so it is less likely to question its own decisions in the same session.
- Independent review instances, without the prior reasoning, catch subtle issues better than self-review instructions or extended thinking.
- Multi-pass review: per-file local passes plus cross-file integration passes, to avoid attention dilution and contradictory findings.

**Skills**
- Use a second, independent Claude instance to review generated code without the generator's reasoning.
- Split large multi-file reviews into per-file passes for local issues, plus a separate integration pass for cross-file data flow.
- Run verification passes where the model self-reports confidence on each finding, to route reviews by calibrated confidence.

### Domain 4 exam decision reflexes

| Scenario | Answer |
|---|---|
| Inconsistent review results | Explicit, testable criteria plus severity levels |
| Too many false positives | Tighten or disable the noisy category, not "be careful" |
| Inconsistent labels or format | Few-shot examples (varied, edge cases, uniform, before the input) |
| Claude makes up missing data | Optional or nullable field, plus a missing-data example |
| Need guaranteed JSON | Tool use with an `input_schema`, plus `tool_choice` set to `any` or a named tool |
| Odd inputs forced into the wrong enum value | `"other"` plus a detail field |
| Valid JSON but wrong values | Validate in code, retry with specific feedback (2-3 max), then escalate |
| Large non-urgent job | Message Batches API with `custom_id` |
| A user is waiting | Synchronous API, never batch |
| Unbiased, thorough review | Separate instance, per-file plus cross-file passes, confidence routing |

---

## Domain 5: Context Management & Reliability (15%)

### 5.1 Manage conversation context to preserve critical information across long interactions

**Knowledge**
- Progressive summarization can turn exact numbers, dates and customer-stated expectations into vague summaries. Keep those facts exact.
- The "lost in the middle" effect: models reliably use the start and end of long inputs, and may miss findings in the middle.
- Tool results pile up and cost far more tokens than their relevance warrants (40+ fields per order lookup when 5 matter).
- Complete conversation history must be passed in later requests to keep the conversation coherent.

**Skills**
- Extract transactional facts (amounts, dates, order numbers, statuses) into a persistent case-facts block, kept outside the summarized history.
- Keep issue data (IDs, amounts, statuses) for multi-issue sessions in a separate context layer.
- Trim tool output to the relevant fields before it accumulates (for example, only the return-relevant fields from an order lookup).
- Put key findings at the top of aggregated inputs and label detailed results with section headers.
- Require subagents to include metadata (dates, source locations, methodology) in structured outputs.
- When downstream agents have tight context budgets, have upstream agents return structured data (key facts, citations, relevance scores) instead of verbose prose.

### 5.2 Design effective escalation and ambiguity resolution patterns

**Knowledge**
- Escalation triggers: a customer asks for a human, a policy gap or exception, or no meaningful progress is possible.
- Escalate immediately when the customer explicitly asks for a human. Offer a resolution first only when the issue is straightforward.
- Sentiment and self-reported confidence are unreliable proxies for case complexity.
- Multiple customer matches call for a clarifying question (ask for another identifier), not a heuristic pick.

**Skills**
- Add explicit escalation criteria with few-shot examples to the system prompt, showing when to escalate and when to resolve on its own.
- Acknowledge frustration and offer a resolution when the issue is within the agent's capability. Escalate only if the customer repeats the request.
- Escalate when policy is silent on the request (for example, competitor price matching when the policy covers only own-site adjustments).
- When a tool returns several matches, ask the customer for additional identifiers rather than choosing.

### 5.3 Implement error propagation strategies across multi-agent systems

**Knowledge**
- Structured error context (failure type, attempted query, partial results, alternatives) lets the coordinator recover intelligently.
- An access failure (timeout, needs retry) is different from a valid empty result (a successful query with no matches).
- Generic statuses such as "search unavailable" hide context the coordinator needs.
- Anti-patterns: silently suppressing errors (returning empty results as success) and killing the whole workflow on one failure.

**Skills**
- Return structured error context: failure type, what was attempted, partial results, potential alternatives.
- Tell access failures apart from valid empty results, so the coordinator decides correctly.
- Have subagents recover from transient failures locally. Propagate only the errors they cannot resolve, with what was attempted and the partial results.
- Structure the synthesis output with coverage annotations: which findings are well supported and which topic areas have gaps because sources were unavailable.

### 5.4 Manage context effectively in large codebase exploration

**Knowledge**
- Context degradation in long sessions: answers become inconsistent and fall back to "typical patterns" instead of the specific classes found earlier.
- Scratchpad files hold key findings across context boundaries.
- Subagent delegation isolates verbose exploration output, so the main agent keeps the high-level picture.
- Structured state persistence: each agent exports its state to a known location, and the coordinator loads a manifest on resume.

**Skills**
- Spawn subagents to answer specific questions ("find all test files", "trace the refund flow dependencies") while the main agent keeps the overall picture.
- Keep a scratchpad file of key findings and refer back to it in later questions.
- Summarize one exploration phase before spawning subagents for the next phase, and inject that summary into their starting context.
- Design crash recovery around manifests that the coordinator loads on resume and injects into agent prompts.
- Use `/compact` to shrink context during long exploration sessions when verbose discovery output fills it.

### 5.5 Design human review workflows and confidence calibration

**Knowledge**
- Aggregate accuracy can hide poor performance on specific document types or fields (97% overall may conceal a weak field).
- Stratified random sampling measures error rates in high-confidence extractions and surfaces new error patterns.
- Field-level confidence scores, calibrated against labeled validation sets, decide where review attention goes.
- Validate accuracy by document type and field before automating high-confidence extractions.

**Skills**
- Sample high-confidence extractions in strata, to keep measuring error rates and spotting new patterns.
- Check accuracy by document type and field to confirm consistency across all segments before reducing human review.
- Have the model output field-level confidence scores, then calibrate review thresholds on labeled validation sets.
- Route low-confidence or contradictory extractions to human review, prioritizing limited reviewer capacity.

### 5.6 Preserve information provenance and handle uncertainty in multi-source synthesis

**Knowledge**
- Source attribution is lost when findings are summarized without keeping claim-source mappings.
- Structured claim-source mappings must survive synthesis and merging.
- Conflicting statistics from credible sources are annotated with attribution, not silently resolved by picking one.
- Temporal data: publication and collection dates must be in structured outputs, so differences over time are not read as contradictions.

**Skills**
- Have subagents output structured claim-source mappings (source URL, document name, relevant excerpt).
- Structure reports into sections: well-established findings vs contested ones, keeping each source's characterization and methodology.
- Show conflicting values with explicit annotations, letting the coordinator reconcile them before synthesis.
- Have subagents include publication or collection dates in their outputs.
- Render content by type: financial data as tables, news as prose, technical findings as structured lists.

### Domain 5 exam decision reflexes

| Scenario | Answer |
|---|---|
| Key fact missed in a long chat | Case-facts block, kept outside summarized history |
| Context filling with old tool dumps | Trim tool output, keep conclusions |
| No rule covers the case | Escalate; never invent a policy |
| User asks for a human | Escalate immediately |
| Request matches two records | Ask the user for another identifier |
| Subagent fails | Structured error passed up with type and partial results; never fail silently |
| Source reachable but empty | A valid answer; don't retry |
| Long refactor might crash | Manifest plus scratchpad files |
| Which outputs to review | Field-level confidence routing plus stratified sampling across all bands |
| Sources disagree | Show both with their sources and flag uncertainty |

---

## How to Prepare

The guide suggests these hands-on activities:

- Build an agent with the Claude Agent SDK: an agentic loop with tool calling, error handling and session management. Practice spawning subagents and passing context between them.
- Configure Claude Code for a real project: CLAUDE.md with a configuration hierarchy, path-specific rules in `.claude/rules/`, custom skills with frontmatter (`context: fork`, `allowed-tools`), and at least one MCP server.
- Design and test MCP tools: tool descriptions that separate similar tools, structured errors with categories and retryable flags.
- Build a structured extraction pipeline: `tool_use` with JSON schemas, validation-retry loops, optional and nullable fields, and batch processing with the Message Batches API.
- Practice prompt engineering: few-shot examples for ambiguous cases, explicit review criteria, multi-pass review.
- Study context management: extracting facts from verbose tool output, scratchpad files for long sessions, subagent delegation.
- Review escalation and human-in-the-loop patterns, and confidence-based routing.

The guide's **preparation exercises** (multi-tool agent with escalation, Claude Code team setup, extraction pipeline, multi-agent research pipeline) map onto these activities.

---

## Exam Policies

- **Identification:** a valid, unexpired, government-issued photo ID whose name matches the registration exactly.
- **Accommodations:** request through Pearson VUE and get approval before scheduling.
- **Retakes:** after a required waiting period that grows with each failed attempt: 14 days after the first, 30 days after the second, 90 days after the third. At most four attempts in a rolling twelve-month period.
- **No-show or late arrival:** the exam fee is forfeited and the candidate must register again.
- **Renewal:** renew within the 12-month validity with a free, non-proctored assessment on the Anthropic Partner Academy. If the credential lapses, retake the full exam at the full fee.
- **Conduct:** no notes, phones, watches, headphones or other materials. Do not capture or share exam content. Breaking the rules can invalidate the result and bar future exams.
- **Confidentiality:** you must accept a non-disclosure agreement before the exam starts.

---

## Scope: In and Out

**In scope:** agentic loops and orchestration; subagent context and error propagation; hooks; tool interface design and `tool_choice`; MCP server configuration; Claude Code CLAUDE.md, commands, skills, rules, plan mode and CI use; few-shot prompting, JSON-schema tool use, validation loops and batch processing; context management, escalation, human review and provenance.

**Out of scope:** fine-tuning or training Claude; Claude API authentication, billing and account management; detailed implementation in specific languages or frameworks; hosting or deploying MCP servers; Claude's internal architecture; Constitutional AI or RLHF; embeddings and vector database internals; computer use; vision; streaming internals; rate limits and pricing calculations; performance benchmarking or model comparison metrics; prompt caching internals; token counting details; OAuth and key rotation; cloud provider configuration.
