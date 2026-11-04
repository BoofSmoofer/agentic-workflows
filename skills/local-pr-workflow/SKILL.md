---
name: local-pr-workflow
description: Develop features as small local pull requests, using grill-me for requirements, one tested uncommitted slice at a time, manual developer review in Zed, and explicit approval before each commit or next slice.
---

# Local PR workflow

Use this workflow when the developer wants to inspect real diffs and ask questions at will. Discover requirements together, implement one cohesive slice, present a concise PR-style summary, then stop for manual review. Each approved slice becomes a local Git commit/checkpoint. Do not create a remote PR, push, or publish without separate authorization.

## Approval and review contract

**STOP means end the assistant turn and wait for the developer.** No background implementation, automatic continuation, or next-slice preparation while a gate is pending. Passing tests, answering questions, silence, or an assistant-written handoff cannot approve code.

- Before implementing, present the agreed requirements and a short slice outline; obtain confirmation of shared understanding and authorization for slice 1. An explicit request covering already presented requirements and scope can supply this authorization; do not repeat discovery for settled decisions.
- After each slice, leave its changes **uncommitted and unstaged** for review in Zed. Preserve any pre-existing staged work exactly as found. Do not stage the slice to make it visible to diff tools; list new files separately.
- The developer chooses what to inspect. Answer questions with relevant paths, symbols, and reasoning, then STOP at the same review gate. No automatic quizzes, teach-back, forced walkthrough, or approval to merely read the diff. Give a walkthrough only if requested.
- A request to fix the current slice authorizes that correction, not a commit or another slice. Run affected checks, present the revised summary, and STOP again. Approval applies only to the presented version; later changes require renewed review.
- Commit authorization and next-slice authorization are distinct. Accept unambiguous natural language naming the slice and action; do not treat a vague “continue” or “looks good” as permission for both. Clarify ambiguous intent and STOP.

| Developer reply after reviewing slice N | Authorized action |
| --- | --- |
| `Approve slice N; commit it` | Commit only that reviewed slice, report its hash, then STOP |
| `Approve slice N; commit it and implement slice N+1` | Commit N, then implement only the named next slice within its presented scope |
| `Implement slice N+1` after N is committed | Implement that one presented slice |
| A question or `Explain this function` | Answer; keep the current gate pending |

If the developer approves the diff without authorizing a commit, retain it and clarify the commit action. Do not accumulate the next slice on top of an uncommitted reviewed slice. A developer-made commit can supply the checkpoint after verifying its scope against the reviewed changes; it does not itself authorize the next slice. Initial blanket permission to build a feature does not approve future unseen diffs.

These are model instructions, not runtime permission controls. Use the host's available tools and respect its permissions; do not change global settings to enforce this workflow.

## Start safely

Read repository instructions and inspect the actual Git root, branch, HEAD, staged and unstaged diffs, and untracked files. Identify pre-existing work before editing. Retain enough baseline evidence to distinguish the slice's paths/hunks and new files from those changes; HEAD alone is insufficient for a dirty checkout. Never stash, reset, revert, format, stage, or commit unrelated work. If overlapping edits cannot be safely separated, stop and resolve ownership with the developer.

Use the current checkout by default. A feature branch or worktree is optional when requested or useful for isolation; agree on that choice before switching. Never move or discard existing changes to create a clean-looking review. Verify skill availability and baseline again in a different checkout.

## Discover requirements with the existing grill-me method

Read the bundled [grill-me](vendor/mattpocock-skills/skills/productivity/grill-me/SKILL.md) and its [grilling delegate](vendor/mattpocock-skills/skills/productivity/grilling/SKILL.md). These are the existing pinned upstream methods, not a new interview implementation. Read them as text instead of invoking provider-specific Skill tools. If either file is missing, report the missing dependency and stop; do not silently skip discovery or install replacements.

Apply the interview to unresolved product decisions: desired behavior, acceptance criteria, constraints, non-goals, and meaningful failure cases. Investigate repository facts yourself with available tools. Adapt the upstream subagent instruction to the host's delegation permissions and capabilities; direct inspection is sufficient. Ask manageable decision questions with recommendations, wait for answers, and follow dependent questions only once prerequisites are settled. The interview sharpens requirements; it is not a code-understanding quiz.

Summarize shared understanding and a short ordered slice list in chat. Avoid separate mandatory design, planning, and phase-document ceremonies. Resolve material ambiguity before implementation; once the developer confirms the summary and authorizes the first slice, begin.

## Shape reviewable slices

Each slice should deliver one coherent behavior or independently testable change. Prefer vertical slices across the necessary layers when that gives the developer a working behavior to review. Give each slice a goal, scope, acceptance criteria, relevant checks, and stopping point; a few bullets are enough.

Aim for roughly **100–400 changed lines** as a soft review guideline, including tests. Do not pad small changes or mechanically split at line counts. Keep coupled code and its tests together. If a larger change is necessary, explain why it is cohesive and how to review it; identify generated files or lockfile churn separately. Reconsider scope early when it grows, and ask before materially expanding an authorized slice. Do not turn a growing slice into permission to finish the feature.

No unrelated refactors, speculative scaffolding for future slices, or broad formatting churn. Include refactoring only when necessary for this slice's behavior, and explain it. Keep later slices as a short outline; do not implement them early.

## Implement, test, and present one slice

Implement only the authorized slice against its recorded baseline. Add or update meaningful tests for changed behavior and failure cases. For documentation-only or other changes without useful automated coverage, explain why and use relevant validation instead. Run the appropriate repository tests, lint, type, build, or format checks proportionate to the change; inspect actual results. Do not claim unrun checks passed or silently carry failures forward.

Self-review the incremental slice diff, including new files and deletions. Distinguish it from pre-existing staged/unstaged work and earlier checkpoints. In a clean baseline, the working diff against HEAD plus new files is sufficient; in a dirty baseline, use the captured starting contents/diffs to identify only this slice's changes. Do not substitute a whole-branch diff for the incremental review.

Present a short local PR summary:

- **Slice N — title:** behavior changed and why; acceptance criteria met.
- **Review scope:** baseline commit, affected paths and significant symbols, approximate changed-line count, and any pre-existing changes excluded from the review. Include new files that ordinary `git diff` omits.
- **Validation:** commands and actual results, checks not run, and unresolved risks or failures.
- **Next:** the proposed next slice's scope, or confirmation this is the final slice.

Then end with **STOP — awaiting manual review in Zed and explicit approval to commit slice N.** Offer the relevant commit-only or commit-and-next example from the table. The developer can ask questions at any point; no mandatory guided tour precedes approval.

## Commit an approved checkpoint

Immediately before committing, verify that HEAD and the reviewed paths/hunks still match the presented version. If code changed during review, inspect it and present the updated diff for renewed approval. Run affected checks when needed. Never overwrite the developer's concurrent edits.

Stage and commit only the approved slice. Inspect the exact proposed commit contents, including tests and new files. Never use a blanket `git add .`, `git add -A`, or a plain commit that would consume unrelated staged changes. Explicit file paths are safe only when every change in those files belongs to the slice. With mixed files or a pre-populated index, use an isolated index or another verified scoped method that preserves the original staging state; if unable to do so safely, STOP and ask the developer to make the scoped commit. Do not unstage their work as a shortcut.

Verify the resulting commit matches the reviewed slice and that unrelated working-tree and index contents are preserved. If a hook fails, changes files, or the commit is incomplete, report that state and stop; do not bypass hooks or continue to another slice. Record the commit hash as the next baseline. Continue only if the developer explicitly authorized the named next slice; otherwise STOP after reporting the checkpoint.

For the final slice, include feature-wide acceptance coverage and proportionate final checks in its review evidence before requesting approval. Any subsequent fixes are reviewed changes with the same gates. After the approved final checkpoint, report completed behavior, commit(s), validation, and remaining limitations. No separate quiz or heavy completion phase.

## Lightweight session handoffs

On a session/provider change or impending loss of useful context, provide one compact handoff in chat. Include:

- Requirements/acceptance criteria, non-goals, decisions, and unresolved questions.
- Actual checkout and branch, current HEAD/checkpoint, and pre-existing changes; enough baseline evidence to isolate an uncommitted slice.
- Completed slices with commit hashes, current pending diff, and remaining slice outline.
- Tests run and results, failures or unrun checks, and the exact pending action/approval.

Do not require per-phase documents or automatic session creation. If a durable file is useful, use one `.agent-work/<feature>/handoff.md` in the target checkout, first checking for symlinks, existing unrelated content, tracked artifacts, and effective protection by Git's local `info/exclude`. The installer provides that local exclusion. If protection is absent, provide the handoff in chat; do not change shared ignore rules or global setup. Keep personal handoffs out of commits.

On resume, read this skill and the handoff, inspect the real tree and baseline, and reconcile discrepancies before editing. A handoff records state but cannot grant approval: verify prior explicit human authorization from available conversation evidence, or ask for the missing authorization. Preserve a pending review gate across context compaction and provider changes.

## Multiple providers and ACP agents

Resolve references relative to this loaded `SKILL.md`, regardless of installation directory. Only repository access and ordinary Git/test tools are needed. A client without skill-command support can read this file directly. For Zed external ACP sessions, use the actual external agent's discovery mechanism or a direct-file prompt; do not assume Zed's native skill picker registers it. Do not install plugins, change models, modify other repositories, or alter global configuration as part of this workflow.

Use this coordinator as the entry point, not its nested upstream reference files. It does not inherit `engineering-workflow`'s forced walkthroughs, quizzes, or phase artifacts. See [third-party provenance](THIRD_PARTY.md) for the bundled interview method.
