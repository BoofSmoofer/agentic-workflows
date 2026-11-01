# Agentic workflows

Personal engineering workflows to install **locally in another project's checkout**. Start with [engineering-workflow](skills/engineering-workflow/SKILL.md): requirements → technical design → plan → one implementation slice → paced code walkthrough → final verification.

Every transition requires explicit human approval. Answering interview questions, passing tests, finishing a walkthrough, “yes”, and “continue” never approve a phase. `STOP` means the assistant ends its turn and waits. These are model instructions, not hard permission controls.

## Install in another project

Keep this repository as your source library. Do not install it globally, add it as a team dependency, or copy its entire checkout into a team repository.

1. Clone this private repository somewhere outside the target project:

   ```sh
   git clone https://github.com/BoofSmoofer/agentic-workflows.git /path/to/personal/agentic-workflows
   ```

2. Choose the agent and pass the **other project's Git root**. Python 3.9+ and Git are required. Preview first:

   ```sh
   python3 /path/to/personal/agentic-workflows/scripts/install-local.py \
     --project /path/to/your-project --client codex --dry-run
   python3 /path/to/personal/agentic-workflows/scripts/install-local.py \
     --project /path/to/your-project --client codex
   ```

   Use `--client claude` for Claude Code. For both clients, run once for each. Codex and Zed's native agent use `.agents/skills/engineering-workflow/`; Claude Code uses `.claude/skills/engineering-workflow/`. Each copy contains all bundled references and licenses. Zed **external** ACP discovery depends on the external agent, not Zed's native skill catalog; see [client compatibility](skills/engineering-workflow/references/clients.md).

3. The installer first protects only the selected skill directory and `/.agent-work/` using Git's local `info/exclude` (located with `git rev-parse --git-path info/exclude`). It preserves existing rules and refuses tracked target paths, existing installations, symlinked installation parents, and install rules overridden by project ignore rules. It never changes shared `.gitignore`, `AGENTS.md`, `CLAUDE.md`, global agent settings, or the index. In linked worktrees, Git's local exclude file may be shared with the main checkout; the skill files themselves are copied only to the chosen checkout.

4. Verify from the target project:

   ```sh
   git check-ignore -v .agents/skills/engineering-workflow/SKILL.md .agent-work/example/state.md
   git ls-files -- .agents/skills/engineering-workflow .agent-work
   git status --short
   ```

   For Claude, substitute `.claude` for `.agents`. `git ls-files` should return nothing for these personal paths, and `check-ignore` should name the local exclude file. Ignored files can still be force-added; keep them out of team commits. Ignoring a tracked file never untracks it: the installer refuses that case rather than editing your index.

The installer performs no network requests, model calls, feature work, or global installation. Nothing has been installed into your other projects merely by adding this library to GitHub.

## Start a feature

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

## Approval sequence

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

## Context and switching models

Feature memory lives under the target project's locally ignored `.agent-work/<feature>/`: `requirements.md`, `design.md`, `plan.md`, `tickets/slice-N.md`, `state.md`, `handoff.md`, and scoped baseline evidence. Documents are created only as their phases are reached. Approval records name exact versions/hashes and human evidence; summaries cannot grant approval.

Requirements and design may share a conversation with a gate between them. After approved design, a fresh planning conversation is usually useful for substantial features. Keep implementation and walkthrough together for one slice when context permits; reassess between slices and before final verification.

Use an exposed context meter if available; otherwise state that usage is unavailable and assess phase size, accumulated history, and reasoning quality conservatively. 60–70% is a handoff planning heuristic, not a universal cutoff, and 150K tokens is not a universal failure point. Handoffs work across providers because they use Markdown and the actual source tree. They preserve pending gates and require verifiable human approval or reconfirmation.

The agent prepares a resolved continuation prompt and stops; the human opens the fresh conversation. See [handoff procedure and phase-specific prompts](skills/engineering-workflow/references/session-handoff.md). Skills cannot guarantee context measurement, prevent client compaction, or launch fresh sessions in every harness.

## Update or remove

Copies do not auto-update. Review library changes, back up your installed skill directory outside the project, remove only that exact directory after checking for personal edits, and rerun the installer. Do not remove `.agent-work/` as part of an upgrade. If both clients are installed, update both copies.

To uninstall, remove only the installed `engineering-workflow` directory you verified. Retain feature artifacts if wanted. Remove only the two specific installer-added exclude rules after removing the corresponding personal files; retain `/.agent-work/` while artifacts remain or another client uses them. Other skills, local exclusions, and global configuration should remain untouched. Fresh clones, remote environments, and worktrees need their own verified local installation.

## Sources and validation

The coordinator and handoff guide were developed in the referenced “Vibe coding meaning” conversation and the user's local Sessions workflow, then generalized for other projects. No feature code or personal run artifacts are included.

Pinned upstream snapshots retain original bytes and MIT notices: Matt Pocock's `grill-me`, `grilling`, and `codebase-design`; Jesse Vincent's Superpowers `writing-plans`; Test Double's Han `code-walkthrough`, explanation helper, and shared references. See [attribution, exact revisions, and compatibility adaptations](skills/engineering-workflow/THIRD_PARTY.md) and the [hash manifest](skills/engineering-workflow/vendor/manifest.json). This is a curated reference bundle, not a full upstream plugin distribution. Third-party licenses apply to their respective files; this repository does not add a blanket license for the original coordinator.

Run from this library's root:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Validation checks paths, local Markdown links/anchors, pinned file hashes, and frontmatter. Installer tests use disposable Git repositories, including linked worktrees and unsafe destinations. These checks do not prove a live model will honor instructions; no end-to-end model or ACP behavior is claimed.
