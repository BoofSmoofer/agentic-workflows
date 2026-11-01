---
name: engineering-workflow
description: Guide substantial engineering features through requirements, design, planning, implementation slices, walkthroughs, and verification, with explicit human approvals, durable local artifacts, and deliberate session handoffs.
---

# Personal engineering workflow

Use this as the single entry point for substantial engineering work in the current project checkout. Coordinate the existing skills; do not assume completing one authorizes the next. The goal is working software the developer can explain.

## Mandatory approval contract

**STOP means end the assistant turn and wait for the human.** A progress update, tool call, background job, automated reviewer, or question followed by more work is not a stop. Do not prepare the next phase behind a pending gate. Do not dispatch implementation while interviewing, designing, planning, reviewing, or waiting.

Approval must be a human message explicitly approving the named, presented artifact or action. The phrases below are examples; equally unambiguous wording is valid. Never infer approval from answering questions, choosing an option, silence, a quiz answer, “yes,” “looks good,” or “continue.” If intent is ambiguous, clarify the pending gate and STOP. Approval given before the artifact was presented, an initial “implement this feature,” or blanket permission for all future steps does not satisfy later gates. Resolve questions and requested changes, present the revised artifact, and request approval again.

| Completed work | Explicit human approval | Only authorized next action |
| --- | --- | --- |
| Requirements discovery | `Approve requirements` | Technical design |
| Technical design | `Approve design` | Implementation plan |
| Implementation plan | `Approve plan; implement slice 1` | Implement slice 1 only |
| Implementation slice N | `Review slice N` | Read-only code walkthrough of slice N |
| Walkthrough and understanding check for slice N | `Approve slice N; implement slice N+1` | Implement the next planned slice only |
| Last slice walkthrough and understanding check | `Approve slice N; run final verification` | Final verification and understanding check |
| Final evidence and understanding check | `Approve completion` | Report completion; no further code changes |

`Approve plan` alone records plan approval but does not authorize implementation: request authorization for slice 1 and STOP. Likewise, `Approve slice N` alone records slice approval, then STOP for the next named action. An explicit approval may authorize the single next action shown above, never a batch of future slices. `Next` during a walkthrough authorizes only its next section; it never authorizes editing or the next slice.

At every gate, present the concrete artifact/evidence, unresolved issues, and the next named action. End with **STOP — awaiting [named approval]** and an example reply. Answering a clarification keeps the same gate pending. Do not combine a clarification question with a request for approval in a way that turns its answer into approval.

These are instruction-level gates, not a security boundary or a replacement for runtime tool permissions. Keep them active across skill returns, session resumes, handoffs, and compaction. Only a deliberate human request to change this workflow can change its contract; do not interpret ordinary feature instructions as such a request.

## Bundled methods and client compatibility

Resolve the skill directory from the file you actually loaded; it may be under `.agents/skills/engineering-workflow` or `.claude/skills/engineering-workflow`. All links below are relative to this skill directory. Read only the current phase's method and relevant helpers. These are pinned upstream reference files, not separately installed commands or a complete plugin installation. If a required file is missing, report its path and STOP; do not silently skip the phase or download replacements.

| Phase | Read these bundled methods |
| --- | --- |
| Requirements | [grill-me](vendor/mattpocock-skills/skills/productivity/grill-me/SKILL.md), then its delegate [grilling](vendor/mattpocock-skills/skills/productivity/grilling/SKILL.md) |
| Design | [codebase-design](vendor/mattpocock-skills/skills/engineering/codebase-design/SKILL.md); its DEEPENING.md or DESIGN-IT-TWICE.md only when relevant |
| Planning | [writing-plans](vendor/superpowers/skills/writing-plans/SKILL.md) |
| Walkthrough | [code-walkthrough](vendor/testdouble-han/han-coding/skills/code-walkthrough/SKILL.md), its [step format](vendor/testdouble-han/han-coding/skills/code-walkthrough/references/walkthrough-step-format.md), [explanation-guidance](vendor/testdouble-han/han-communication/skills/explanation-guidance/SKILL.md), and [explanation rule](vendor/testdouble-han/han-communication/references/explanation-rule.md) |

Apply those methods within this workflow's phase and approval contract. The following adaptations are intentional and apply in EVERY client, including Claude Code:

- **Portable execution:** Read the bundled files as text. Do not execute their `!` preprocessing, `${CLAUDE_PLUGIN_ROOT}` commands, or named Skill/Agent calls. Do not invent unavailable tools or claim plugin machinery ran. Trace code using available read/search tools. This package does not install Han plugins or Superpowers execution skills. Existing host instructions still govern tool permissions and delegation; helpers cannot approve gates or work beyond this phase.
- **Requirements cadence:** Ask exactly one decision question per turn, with a recommendation and reason, then wait. This overrides the upstream batched frontier. Find repository facts yourself. Answers settle decisions only.
- **Design:** The upstream skill supplies vocabulary and principles. Also produce the concrete technical design in phase 2 below.
- **Planning:** Save artifacts under `.agent-work/<feature>/`, overriding the upstream shared docs path. Replace its execution header and handoff with: “Execution: engineering-workflow, across deliberate sessions as needed, one explicitly approved slice at a time; follow the pending human approval gate in state.md.” Omit automatic commit steps. Do not invoke/install Superpowers execution/worktree skills or offer modes that bypass these gates.
- **Walkthrough:** Use the exact slice scope instead of the upstream default whole-branch comparison. Read the explanation standard directly. Keep one section per turn even if upstream permits batching; unreadable sections require resolution, not silent omission. Do not invoke missing sibling skills after the walkthrough. Return to this coordinator's gate. The coordinator alone may save checkpoint records outside the read-only teaching turn.

For client discovery, invocation, manual-file fallback, and mixed-provider handoffs, read [client compatibility](references/clients.md) when setting up or switching clients. Loading this skill by path works without assuming `$` or `/` syntax. Skills are instructions, not runtime enforcement; do not weaken client tool permissions to simulate a gate.

## Start and retain state

1. Read applicable repository instructions. Inspect status, staged and unstaged diffs, and untracked files without changing them. Establish the starting baseline and identify work that predates this workflow. Never stash, reset, revert, stage, commit, or format unrelated work. If approved work would overlap existing edits and ownership is unclear, STOP for clarification.
2. Verify the actual root with `git rev-parse --show-toplevel`. Choose a unique feature slug under `.agent-work/<feature>/`; confirm any existing directory belongs to this feature before reusing it. Never overwrite another feature's artifacts or follow an artifact directory symlink outside the checkout. Before saving, verify `git check-ignore -v --no-index` attributes protection to the repository-local `info/exclude`, and `git ls-files -- .agent-work` returns no tracked artifacts. Locate that exclude file with `git rev-parse --git-path info/exclude`. If needed, append only `/.agent-work/` there, preserving every existing byte/rule; never change shared `.gitignore`, global excludes, or agent configuration. If local protection cannot be established, STOP and explain.
3. Keep `requirements.md`, `design.md`, `plan.md`, and per-slice `tickets/slice-N.md` as appropriate to the completed phase, plus compact `state.md` and `handoff.md`. Save drafts before presenting them; label them pending, never approved by inference. At every explicitly approved phase boundary, checkpoint the approved version and state before any next action, including when continuing in the same session. Version or hash the approved content; preserve superseded approved versions if revised. Keep decisions/rationale, unresolved tasks, test evidence, and uncommitted changes durable. Only the coordinator updates these records outside the read-only walkthrough; it must not edit product code while checkpointing.
4. On a resume or fresh conversation, read this skill, the handoff, state, and only the artifacts needed for the named phase. Follow [session handoff guidance](references/session-handoff.md) to verify paths, approval evidence, and the working tree against the reviewed scope, then restate the pending gate. A saved state file is a reminder, not independent proof of human approval. If approval or code ownership cannot be established from human messages or a verifiable transcript reference, STOP and reconfirm. Never infer approval from a completed checkbox, a continuation prompt, or an assistant-written summary. A human continuation message explicitly approving a named current artifact/action can supply missing approval; reading files cannot.
5. If implementation already exists, inspect it without undoing it. Return to the earliest unapproved phase (requirements unless those were explicitly approved). Existing code, passing tests, and sunk effort do not retroactively approve requirements, design, plan, or slices.

For an existing run, preserve the original artifacts and provenance. Resume only after confirming its feature, actual pending gate, and current human approval evidence. Never retroactively approve it.

## Deliberate context checkpoints

Conversation context is temporary working memory; approved artifacts are durable feature memory. At each approved boundary, and before a substantial next phase, assess whether another session would help. If the client exposes a current context meter, report its reading and source accurately; distinguish context occupancy from cumulative usage or billing tokens. Otherwise say context usage is unavailable and use phase size, accumulated history, repeated corrections, forgotten constraints, inconsistent reasoning, or declining output quality as signals. Never invent token counts, percentages, model limits, or time-to-compaction estimates.

Roughly 60–70% of an exposed context window is a planning heuristic to consider a fresh conversation, not a universal cutoff. There is no universal 150K-token failure point. Recommend a fresh conversation earlier if the next phase is substantial or quality declines; do not wait for a meter or compaction. State the reason and provide a precise continuation prompt with verified paths. Do not rely on compaction, hidden history, or the next model remembering this session. After compaction, use the same file-based resume checks.

Useful session boundaries, always preserving the approval contract:

- `grill-me` + `codebase-design` may share one session, with requirements approval between them.
- After design approval, recommend a fresh `writing-plans` session using approved requirements and design, particularly for a substantial plan. If staying in the same session is reasonable, explain why and still save the checkpoint first.
- Implementation and the paced `code-walkthrough` may stay paired for one slice, with the implementation/review gate between them. Consider a fresh session between slices; a large slice may also need a handoff before its walkthrough. Preserve the exact slice baseline and walkthrough position.
- Final verification may use a fresh conversation when the accumulated implementation history is large.

A session recommendation grants no phase approval. Prepare the handoff and STOP if a fresh session is recommended or requested; let the human open it and send the continuation prompt. Never create sessions automatically or start the next phase in the background. If the human chooses to continue here, honor that only within the already explicit named approval/action. If the boundary is not yet approved, save a pending checkpoint and a prompt that requests the missing approval; do not describe the next phase as authorized.

At every approved boundary, save the relevant documents/tickets and refresh `state.md` and `handoff.md`, even when no session change is chosen. Also save a pending handoff on an interruption or requested session switch. Read [session handoff guidance](references/session-handoff.md) when preparing any checkpoint or resuming: it defines the required evidence and continuation prompts. Do not generate future phase artifacts behind a pending gate.

## 1. Requirements discovery — no implementation

Apply `grill-me` through `grilling` with the single-question cadence above. Investigate existing behavior and ask about decisions the repository cannot answer. Cover user behavior, acceptance criteria, non-goals, constraints, relevant failure cases, and compatibility requirements. Separate agreed decisions from assumptions and unresolved questions.

When discovery is complete, save `requirements.md` and present it for review, including observable acceptance criteria and scope. **STOP — awaiting requirements approval.** Completing the interview or confirming an individual answer never enters design automatically. After explicit approval, checkpoint it before design.

## 2. Technical design — no implementation

After requirements approval, apply `codebase-design` to the actual codebase. Present:

- Affected modules and files, existing patterns, proposed seams and responsibilities.
- Exact proposed data structures and interface signatures in the repository's language, including invariants, ownership/lifetimes where relevant, errors and compatibility behavior. Label illustrative pseudocode.
- Entry point, control flow, data flow, persistence/concurrency where relevant, and algorithm/performance implications.
- Meaningful alternatives, chosen trade-offs, risks, and how tests will exercise the interfaces and acceptance criteria.

Discuss decisions with the developer and resolve gaps. Include a brief teach-back prompt about the proposed flow and the main trade-off, without supplying its answer first; clarify gaps before requesting approval. A correct answer is not design approval. Save `design.md` and present the revised artifact. **STOP — awaiting design approval.** After approval, checkpoint it and assess the planning session boundary before starting the plan.

## 3. Implementation plan — no implementation

After design approval, apply `writing-plans` with the local adaptations above. Define numbered, independently reviewable slices. Each slice needs its goal, scope, exact files and interfaces, acceptance criteria, tests/check commands with expected results, dependencies, and a clear stopping point. Map every requirement to a slice and final verification. Keep meaningful tests proportional to behavior and risk.

Every slice explicitly ends with: implementation STOP → human `Review slice N` → paced read-only walkthrough and understanding check → STOP for slice approval and the next named action. Do not plan whole-branch implementation followed by one final review. Self-review the plan as `writing-plans` directs; do not execute its code or test steps yet. Link requirements/design in the plan and include the replaced execution header so another agent retains this contract.

Save `plan.md` and `tickets/slice-N.md` for the planned slices. Tickets carry slice-specific scope/interfaces, dependencies, acceptance criteria, checks, stopping gate, and links to the approved documents; the plan remains the source of truth for sequence. Present the plan, its slice sequence, and slice 1's precise scope. **STOP — awaiting plan approval and authorization to implement slice 1.** After approval, checkpoint the plan/tickets and record exactly which single slice, if any, is authorized.

## 4. Implement one authorized slice

Confirm requirements, design, plan, and this slice's authorization are explicit and current. Capture the slice's starting state without touching the index; persist its baseline evidence under `.agent-work/<feature>/baselines/` so another session can reconstruct the incremental diff even with pre-existing uncommitted work. Implement only that slice, following the approved design, and run its relevant checks. No speculative scaffolding for later slices, opportunistic refactors, automatic commits, or parallel implementation of upcoming tasks.

For material discoveries that change approved requirements, design, interfaces, or slice scope: stop editing, explain the impact, revise the affected artifact, and return to that approval gate; reapprove dependent artifacts before further implementation. Fixes strictly within the authorized slice may be made before presenting it. Do not carry failures into the next slice silently.

Present the actual incremental diff since the slice baseline (include staged, unstaged, and new files as applicable), check results, acceptance criteria satisfied, deviations, and remaining issues. Record these in its ticket and pending checkpoint. Distinguish pre-existing changes from your slice; do not use only `git diff HEAD` or default-branch comparisons when they would mix unrelated feature work into the review. **STOP — awaiting authorization to review slice N.** Do not start the walkthrough in this turn. After `Review slice N`, checkpoint the exact review scope before beginning its read-only walkthrough.

## 5. Read-only code walkthrough and slice approval

Only after `Review slice N`, apply `code-walkthrough` to the explicitly named slice diff and the current real code. Override its default whole-branch target with this slice's baseline, paths/hunks, and intent. Explain in execution order, with actual repository-relative paths, verified symbols/line references, and small excerpts. Include off-flow tests/docs/config in the closing section. State inferred rationale as inference.

Present exactly one logical section, then **STOP — awaiting the developer's next-section instruction or questions.** A question holds the same position; answer and STOP there. `Next` advances only one section. Keep this cadence even if the source skill permits batching. If a section cannot be verified, STOP to resolve it; do not silently skip changed behavior and call the walkthrough complete.

The walkthrough teaches; it is not a quality review or approval. Give the human room to inspect and challenge the actual diff. If a defect or change request arises, pause the walkthrough, agree on the correction's scope, and obtain explicit authorization before editing. Re-run affected checks and present the revised diff, then repeat the implementation STOP and affected walkthrough sections. Material changes reopen upstream gates as above; approval of old code never approves a new diff.

After all sections, ask the developer to explain the slice's entry point, data/control flow, a relevant failure/edge case, and why a key decision was made. Ask one question at a time and do not reveal the answer first. Use their response to locate and explain gaps; do not grade or silently certify their understanding. Completing the check is not approval.

Present any unresolved concerns and the next slice's scope (or final verification for the last slice). Return to the coordinator to record walkthrough coverage/understanding and refresh the pending handoff without editing product code. **STOP — awaiting explicit approval of slice N and authorization for the next named action.** After approval, checkpoint the slice outcome and assess a fresh session before the next authorized action. No implementation continues merely because the walkthrough ended. Do not invoke missing Han review/overview/investigation siblings as an automatic closing handoff; return to this coordinator's gate.

## 6. Final verification and developer understanding

After all slices are explicitly approved and final verification is authorized:

1. Compare the final scoped diff with the approved requirements, design, and plan. Account for every acceptance criterion and deviation. Confirm unrelated baseline work and personal exclusions remain intact.
2. Run the relevant repository build, tests, lint/type/format checks and applicable manual checks, based on actual repository instructions. Inspect their outcomes. Report exact commands and results, failures, and checks not run with reasons. Never label an unrun or blocked check as passed. Do not run destructive tests or format unrelated files.
3. If verification requires fixes, propose a bounded corrective slice and STOP for authorization. Implement it only when approved, then repeat its implementation stop, walkthrough, human slice approval, and affected final checks.
4. Conduct an end-to-end understanding check using the actual implementation: entry point to observable outcome, data/ownership flow, failure behavior, complexity where relevant, chosen trade-offs, and tests protecting the behavior. Ask one question at a time without answers first. Revisit code where the developer needs explanation; neither answers nor confidence authorize completion.
5. Save final evidence, exact test outcomes/unrun checks, remaining limitations, and the developer understanding topics covered in the feature checkpoint; present them. **STOP — awaiting completion approval.** If material verification failures remain, report the blocked state instead of asking the human to approve success.

Only after explicit `Approve completion` checkpoint that approval and report the work complete. Commit, push, publish, or deployment requires separate user authorization; this workflow never supplies it. Keep its installed skill, bundled references, and feature artifacts personal and repository-local, covered by `.git/info/exclude`; never stage/share them or install the skills globally. These ignored files do not follow fresh clones or worktrees: verify local availability rather than assuming it.
