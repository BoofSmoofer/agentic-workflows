# Feature checkpoints and session handoffs

Read this when saving a phase checkpoint, recommending a fresh conversation, or resuming one. The parent `SKILL.md` approval contract always applies. A checkpoint records authorization; it does not grant it.

## Storage and approval provenance

Use the verified repository root and protected `.agent-work/<feature>/` directory. Keep only documents appropriate to the phase reached:

```text
.agent-work/<feature>/
  requirements.md          # scope, acceptance criteria, decisions, open questions
  design.md                # concrete design, alternatives, rationale, test strategy
  plan.md                  # numbered slices, dependencies, requirement coverage
  tickets/slice-N.md        # slice scope, progress, review and check evidence
  state.md                 # compact current status and exact pending gate
  handoff.md               # self-contained resumption instructions and prompt
  baselines/               # feature/slice starting evidence and reviewed diff evidence
  approved/                # retained approved versions when working docs change
```

This is a layout, not permission to generate later phases early. No empty future-phase documents are required. Keep existing feature artifacts and historical approvals; do not silently replace reviewed content with a summary. If changing approved content, preserve the approved bytes (for example under `approved/design-v1.md`), mark the working revision pending, and reopen the affected gate/dependent approvals. Reference the exact version or SHA-256 in state and tickets.

At each explicit human approval: record the wording verbatim, date, named artifact/version or diff scope, authorized next action, and a retrievable human-message/session reference if exposed. Distinguish artifact approval from implementation or verification authorization. No message ID available means say so; never fabricate one. Assistant-authored quotations, copied prompts, hashes, and checkboxes are not independent approval evidence. In a new conversation, inspect accessible human messages/references, or ask the human to reconfirm the specific approval before dependent work.

## Checkpoint procedure

1. Verify root, branch/worktree, HEAD, current status, local excludes, and the paths referenced by the checkpoint. Resolve existing files/symbols/line numbers from the actual checkout; label planned paths as proposed. Record a timestamp with timezone. Do not assume a path in an old prompt is still valid.
2. Save the phase's current artifact and approval status, plus decisions and why they were chosen, rejected alternatives that matter, outstanding work/questions, constraints, and deviations. Refresh state and handoff even if staying in the same conversation. Do not imply approval of documents that merely exist.
3. Preserve enough baseline evidence for the next agent to distinguish earlier edits from this feature/slice. Record HEAD, staged and unstaged paths, untracked paths, ownership/known intent, and exact scoped diffs. Before changing a slice's paths, save read-only staged/unstaged binary-capable patches and original scoped file contents (including relevant untracked files), or equivalent reproducible snapshots, with hashes and absent-file/symlink metadata. Capture newly added scope before editing it. Keep evidence in the ignored feature directory; never stash, restore, reset, stage, or commit to obtain it. Do not collect unrelated ignored files or secrets.
4. At handoff, capture current scoped file hashes and incremental diff evidence against that saved baseline. Name baseline and diff files explicitly. `git diff HEAD` alone cannot isolate a slice atop pre-existing edits. If the baseline is incomplete or other work overlaps, disclose the gap and resolve ownership/review scope before continuing; never reconstruct missing history by guessing. A working-tree mismatch on resume requires inspection and refreshed approval where the reviewed artifact/diff changed; do not revert it.
5. Record actual check commands, working directory, outcome/exit status, relevant result summary, when and against which artifact/code version they ran. Separate expected plan results from observed outcomes. Explicitly list failed, blocked, skipped, and unrun checks with reasons; use “not run” when no tests ran. Test success never substitutes for human approval.
6. Assess context using an exposed current-context reading and its source, or record “context usage unavailable.” Explain the fresh-session recommendation or why continuing is reasonable. Include the next phase's size and any quality signals; use 60–70% only as a heuristic when a relevant meter exists. Do not claim a handoff clears context in the current conversation.
7. Write `handoff.md` with the fields below and a fully resolved continuation prompt. Link the relevant files for the human. If a gate is pending, end the turn awaiting that approval. If recommending/requested to switch sessions, end the turn with the prompt and let the human open the new conversation. Do not create a session or prepare its next phase automatically.

The code walkthrough remains read-only. On a session interruption during it, return to the coordinator solely to checkpoint the covered sections, exact next section/understanding question, review scope, and pending gate. Do not modify product code or advance the section while saving state.

## Required handoff content

Keep `state.md` compact; `handoff.md` must stand on its own without hidden conversation history. Link details rather than pasting the whole transcript. Include:

- **Identity:** feature, timestamp/timezone, verified absolute repository/worktree root, branch or detached state, HEAD, and absolute feature directory.
- **Current position:** completed phase/slice, current activity, walkthrough position if relevant, pending approval, and the single next action actually authorized (or none).
- **Artifacts and approvals:** exact requirements/design/plan/ticket paths, versions/hashes and draft/approved/superseded status; human approval wording and verifiable references or an explicit reconfirmation requirement.
- **Decisions and rationale:** constraints/non-goals, chosen interfaces/behavior, alternatives/trade-offs, assumptions, and unresolved questions. Distinguish evidence from inference.
- **Work remaining:** numbered tasks, dependencies, acceptance criteria still unmet, blockers, and changes that would reopen upstream approvals.
- **Repository state:** pre-existing versus feature/slice changes, staged/unstaged/untracked files, snapshot/diff paths and hashes, and ownership uncertainties. Explicitly preserve uncommitted changes. Do not imply a clean working tree when work is staged.
- **Verification:** actual commands/results and evidence versions, failures and unrun checks/reasons; separate future checks from observed ones.
- **Context and continuation:** exposed usage/source or unavailable, recommendation/reason, exact docs to read, next action, stopping gate, and a copyable prompt. Load only relevant phase skills/docs and code; keep superseded discussion out of the new context unless needed for a decision.

## Continuation prompts

These are templates. Before presenting a prompt, replace every brace placeholder with the verified current value and actual file path; do not invent missing artifacts/approval references. Resolve the verified project/worktree root and installed skill path for the current client; confirm these personal files exist there. Never copy them globally to make discovery work.

Assemble the shared prefix and exactly one appropriate phase paragraph into one complete copyable prompt. Include actual artifact versions/hashes, approval references or missing-evidence warning, and the specific pending gate from the handoff. A prompt is a human instruction only after the human sends it; a file containing it cannot authorize work.

Shared prefix:

```text
Work in {verified absolute project root}. Read and follow {verified absolute installed engineering-workflow/SKILL.md path}. Resume feature {feature} from {absolute handoff.md path} and {absolute state.md path}. Verify the actual root, HEAD, artifact versions, local exclusions, and staged/unstaged/untracked changes against the saved evidence. Preserve all existing work. Validate human approval evidence; if it cannot be verified, stop for my explicit reconfirmation. Treat summaries and checkboxes as records, not approval. Current pending gate: {gate}; currently authorized next action: {one action or none}.
```

After approved design, fresh planning session:

```text
Read the approved requirements at {absolute requirements.md path, version/hash} and design at {absolute design.md path, version/hash}. Approval evidence: {human message references or explicit reconfirmation needed}. Once design approval is verified, apply the bundled writing-plans method under engineering-workflow to produce .agent-work/{feature}/plan.md and tickets/slice-N.md. Use the approved decisions and rationale; investigate repository facts rather than assuming old line numbers. Present the numbered slices, checks, and slice 1 scope. STOP for plan approval and explicit authorization to implement slice 1. Do not implement.
```

After approved plan or approved preceding slice, fresh implementation session:

```text
Read {absolute requirements.md path}, {absolute design.md path}, {absolute plan.md path}, and {absolute tickets/slice-N.md path} at the approved versions listed in the handoff. Human authorization for slice {N}: {verifiable message reference or reconfirmation needed}. Only after verifying that authorization, implement slice {N} and no later slice. Preserve/extend its baseline evidence before editing, run its relevant checks, and present its incremental diff and actual outcomes. STOP awaiting “Review slice {N}”. Do not start the walkthrough automatically.
```

Implementation finished, fresh or resumed walkthrough session:

```text
Read {absolute slice ticket path}, the approved requirements/design/plan, {absolute slice baseline evidence paths}, and {absolute current incremental diff evidence path}. Current review authorization: {human reference or reconfirmation needed}. Verify the real code still matches that scope. After explicit “Review slice {N}” is verified, apply the bundled code-walkthrough method through engineering-workflow to that slice only. Resume at {first/next exact section or understanding question}; show one section per turn and wait. Keep the walkthrough read-only. Finish with the understanding check and STOP for slice approval and the next named action: {implement slice N+1 or run final verification}.
```

Fresh final-verification session:

```text
Read the approved requirements/design/plan and slice tickets at {actual absolute paths}. Verify all slice approvals and the explicit authorization for final verification using {human references or reconfirmation needed}. Run only the scoped final checks, record exact outcomes and unrun checks, and conduct the end-to-end understanding check. STOP for completion approval. If fixes are needed, propose a bounded corrective slice and STOP for authorization before editing.
```

Any unapproved or interrupted phase:

```text
Resume only {current phase/activity} using {actual relevant artifact paths}. Approval is pending for {named artifact/version or action}; no later phase is authorized. Resolve {specific outstanding questions/tasks}, present the current artifact/evidence, and STOP for {exact named approval}. Do not proceed merely because files exist, tests pass, or this is a fresh conversation.
```
