# Agentic workflows

Personal engineering workflows to install **locally in another project's checkout**. Choose the review style you want:

| Workflow | Review style |
| --- | --- |
| [local-pr-workflow](skills/local-pr-workflow/SKILL.md) | `grill-me` requirements → one tested, uncommitted slice → manual review in Zed and questions at will → explicit approval → local commit/checkpoint |
| [engineering-workflow](skills/engineering-workflow/SKILL.md) | Requirements → technical design → plan → one implementation slice → paced code walkthrough → final verification, with phase artifacts and understanding checks |

Both require explicit human approval at their defined gates. `STOP` means the assistant ends its turn and waits. These are model instructions, not hard permission controls. The existing `engineering-workflow` remains available unchanged; the new workflow has its own lighter review contract.

## Install in another project

Keep this repository as your source library. Do not install it globally, add it as a team dependency, or copy its entire checkout into a team repository.

1. Clone this private repository somewhere outside the target project:

   ```sh
   git clone https://github.com/BoofSmoofer/agentic-workflows.git /path/to/personal/agentic-workflows
   ```

2. Choose the workflow and agent and pass the **other project's Git root**. Python 3.9+ and Git are required. Preview first:

   ```sh
   python3 /path/to/personal/agentic-workflows/scripts/install-local.py \
     --project /path/to/your-project --client codex --skill local-pr-workflow --dry-run
   python3 /path/to/personal/agentic-workflows/scripts/install-local.py \
     --project /path/to/your-project --client codex --skill local-pr-workflow
   ```

   Use `--skill engineering-workflow` for the original workflow; omitting `--skill` preserves that default for existing commands. Each invocation installs only the selected skill, so both can coexist. Use `--client claude` for Claude Code. For both clients, run once for each. The installer puts the selected skill under `.agents/skills/<skill>/` for Codex or `.claude/skills/<skill>/` for Claude Code. Each copy contains its bundled references and licenses.

   For Zed or another ACP host, discovery depends on the active agent and adapter. Use the matching installed path with the direct-file prompt below if command discovery is unavailable. The workflow itself is provider-neutral Markdown; it does not require a particular model or provider-specific Skill tool.

3. The installer first protects only the selected skill directory and `/.agent-work/` using Git's local `info/exclude` (located with `git rev-parse --git-path info/exclude`). It preserves existing rules and refuses tracked target paths, existing installations, symlinked installation parents, and install rules overridden by project ignore rules. It never changes shared `.gitignore`, `AGENTS.md`, `CLAUDE.md`, global agent settings, or the index. In linked worktrees, Git's local exclude file may be shared with the main checkout; the skill files themselves are copied only to the chosen checkout.

4. Verify from the target project:

   ```sh
   git check-ignore -v .agents/skills/local-pr-workflow/SKILL.md .agent-work/example/handoff.md
   git ls-files -- .agents/skills/local-pr-workflow .agent-work
   git status --short
   ```

   For Claude, substitute `.claude` for `.agents`; for the original workflow, substitute `engineering-workflow` for `local-pr-workflow`. `git ls-files` should return nothing for these personal paths, and `check-ignore` should name the local exclude file. Ignored files can still be force-added; keep them out of team commits. Ignoring a tracked file never untracks it: the installer refuses that case rather than editing your index.

The installer performs no network requests, model calls, feature work, or global installation. Nothing has been installed into your other projects merely by adding this library to GitHub.

## Use local-pr-workflow

In a conversation rooted in the target checkout, invoke `$local-pr-workflow Add searchable session history` in Codex, or `/local-pr-workflow Add searchable session history` in Claude Code when supported. The portable fallback for Zed, ACP agents, and other repository-capable clients is:

```text
Read .agents/skills/local-pr-workflow/SKILL.md and follow it for this feature: Add searchable session history. Use the bundled grill-me for requirements, implement one agreed slice, then stop with an uncommitted diff for my review in Zed. Wait for explicit approval before committing or starting the next slice.
```

Use `.claude/skills/...` if installed there. Confirm the agent read the actual file. The nested upstream skills are references, not separately registered commands. No global installation or agent configuration changes are needed.

The interview resolves requirements and acceptance criteria, then the agent proposes a short slice outline. Confirm shared understanding and authorize slice 1. Prefer cohesive vertical slices, roughly **100–400 changed lines** as a soft guideline including tests; smaller or larger changes are fine when justified by coherence. Never split mechanically or add unrelated refactors to fill a slice.

Each slice includes relevant tests/checks and a concise PR-style summary: behavior and rationale, review scope and baseline, actual validation results, risks, and the proposed next slice. The agent then ends its turn with the diff uncommitted and unstaged, preserving any pre-existing work. Inspect it in Zed and ask questions freely. There are no automatic quizzes or forced walkthroughs.

| Your reply at review | What happens |
| --- | --- |
| `Why did you change this function?` | Answer, then wait at the same review gate |
| `Fix this edge case in slice 1` | Correct this slice, rerun affected checks, present the revised diff, then wait again |
| `Approve slice 1; commit it` | Commit only that reviewed slice and report its hash, then wait |
| `Approve slice 1; commit it and implement slice 2` | Commit the approved slice, then implement only the presented slice 2 and stop for its review |

Approval of the diff alone does not authorize a commit or the next slice. Each approved and explicitly authorized commit is a local checkpoint; no remote PR or push is implied. The agent must isolate slice changes from pre-existing staged/unstaged work, including mixed files, and stop if it cannot do so safely. A feature branch or worktree is optional.

For session or provider changes, use one compact handoff with requirements, decisions, actual checkout/branch/HEAD, completed checkpoints, pending diff and its baseline, remaining slices, test results, and the pending approval. Chat is sufficient; one locally ignored `.agent-work/<feature>/handoff.md` is optional. The new agent inspects the real tree and verifies human authorization before acting. Handoffs do not grant approval, and no phase-document bundle is required.

## Use engineering-workflow

The following invocation, approval sequence, and context sections describe the original workflow only.

In Codex, start a fresh conversation rooted in your project:

```text
$engineering-workflow Add searchable session history
```

In Claude Code:

```text
/engineering-workflow Add searchable session history
```

If your client doesn't expose that syntax, send:

```text
Read .agents/skills/engineering-workflow/SKILL.md and follow it for this feature: Add searchable session history. Start with requirements discovery. Stop at every approval gate.
```

Use `.claude/skills/...` when that's where you installed it. In a fresh session, confirm the actual skill file was read. The bundled upstream methods are reference files, not separately registered `/grill-me` or `$writing-plans` commands. Use the coordinator as the entry point.

### Engineering approval sequence

| Work presented | Example explicit reply | What it authorizes |
| --- | --- | --- |
| Requirements | `Approve requirements` | Design only |
| Design | `Approve design` | Planning only |
| Plan and slice 1 scope | `Approve plan; implement slice 1` | Slice 1 only |
| Slice N diff and checks | `Review slice N` | Read-only walkthrough |
| Finished walkthrough and understanding check | `Approve slice N; implement slice N+1` | One next slice |
| Last slice walkthrough | `Approve slice N; run final verification` | Final checks and understanding check |
| Final evidence | `Approve completion` | Completion report |

Equally unambiguous wording is valid; approval must identify the current presented artifact/action. `Approve plan` alone does not authorize a slice. A question during a walkthrough holds the current section; `Next` advances just one section. A changed artifact or diff needs renewed approval. The [skill](skills/engineering-workflow/SKILL.md) contains the complete contract, including corrective slices and separate authorization for commits, pushes, publication, and deployment.

### Engineering context and switching models

Feature memory lives under the target project's locally ignored `.agent-work/<feature>/`: `requirements.md`, `design.md`, `plan.md`, `tickets/slice-N.md`, `state.md`, `handoff.md`, and scoped baseline evidence. Documents are created only as their phases are reached. Approval records name exact versions/hashes and human evidence; summaries cannot grant approval.

Requirements and design may share a conversation with a gate between them. After approved design, a fresh planning conversation is usually useful for substantial features. Keep implementation and walkthrough together for one slice when context permits; reassess between slices and before final verification.

Use an exposed context meter if available; otherwise state that usage is unavailable and assess phase size, accumulated history, and reasoning quality conservatively. 60–70% is a handoff planning heuristic, not a universal cutoff, and 150K tokens is not a universal failure point. Handoffs work across providers because they use Markdown and the actual source tree. They preserve pending gates and require verifiable human approval or reconfirmation.

The agent prepares a resolved continuation prompt and stops; the human opens the fresh conversation. See [handoff procedure and phase-specific prompts](skills/engineering-workflow/references/session-handoff.md). Skills cannot guarantee context measurement, prevent client compaction, or launch fresh sessions in every harness.

## Update or remove

Copies do not auto-update. Review library changes, back up your installed skill directory outside the project, remove only that exact directory after checking for personal edits, and rerun the installer. Do not remove `.agent-work/` as part of an upgrade. If both clients are installed, update both copies.

To uninstall, remove only the selected installed workflow directory you verified. Retain feature artifacts if wanted. Remove only its specific installer-added skill exclude rule after removing the corresponding personal files; retain `/.agent-work/` while artifacts remain or another workflow/client uses them. Other skills, local exclusions, and global configuration should remain untouched. Fresh clones, remote environments, and worktrees need their own verified local installation.

## Sources and validation

The engineering coordinator and handoff guide were developed in the referenced “Vibe coding meaning” conversation and the user's local Sessions workflow, then generalized for other projects. The local PR workflow adds the user's manual Zed review and per-slice commit design. No feature code or personal run artifacts are included.

Pinned upstream snapshots retain original bytes and MIT notices: Matt Pocock's `grill-me`, `grilling`, and `codebase-design`; Jesse Vincent's Superpowers `writing-plans`; Test Double's Han `code-walkthrough`, explanation helper, and shared references. See [attribution, exact revisions, and compatibility adaptations](skills/engineering-workflow/THIRD_PARTY.md) and the [hash manifest](skills/engineering-workflow/vendor/manifest.json). This is a curated reference bundle, not a full upstream plugin distribution. Third-party licenses apply to their respective files; this repository does not add a blanket license for the original coordinator.

The local PR package reuses only the existing pinned `grill-me`, `grilling`, and MIT license, with its own [attribution](skills/local-pr-workflow/THIRD_PARTY.md) and [subset manifest](skills/local-pr-workflow/vendor/manifest.json). Neither workflow requires the other to be installed.

Run from this library's root:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Validation checks both workflows' paths, local Markdown links/anchors, pinned file hashes, and frontmatter. Installer tests use disposable Git repositories for both workflows, including linked worktrees, unsafe destinations, coexistence, and preservation of staged/unstaged work. These checks do not prove a live model will honor instructions; no end-to-end model or ACP behavior is claimed.
