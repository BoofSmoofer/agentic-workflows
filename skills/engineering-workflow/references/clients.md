# Clients, discovery, and mixed providers

Read when installing, changing clients/providers, or resuming in another environment. Documentation checked 1 November 2026; client and adapter versions vary. No dependency on a particular model, subscription, plugin registry, or proprietary conversation history is required.

| Environment | Local install in the target project | Invocation and caveats |
| --- | --- | --- |
| Codex CLI / IDE | `.agents/skills/engineering-workflow/` | `$engineering-workflow ...` or select through `/skills`. If unavailable, explicitly request reading the installed SKILL.md. Confirm the resolved file. |
| Claude Code | `.claude/skills/engineering-workflow/` | `/engineering-workflow ...`. This bundle uses direct-file adaptations; it does not load Han plugin namespaces or Superpowers execution tools. |
| Zed external Codex ACP | `.agents/skills/engineering-workflow/` in the agent's actual working checkout | Discovery is owned by Codex and its adapter. `$` mentions and `/skills` may vary with the integration. Use a direct-file prompt if unavailable. |
| Zed external Claude ACP | `.claude/skills/engineering-workflow/` in the agent's actual working checkout | Use the external agent's supported command mechanism or a direct-file prompt. Zed's native skill list does not establish external discovery. |
| Zed native agent | `.agents/skills/engineering-workflow/` | Use its skill picker/slash command when supported; otherwise request reading the file. Native provider settings are separate from ACP agents. |
| Other LLM/harness | Project-local location it can read, protected with local Git exclusions before copying | Ask it to read the actual SKILL.md and current phase references. A plain chat without repository read/write access needs artifacts supplied through its supported file mechanisms; do not pretend it inspected code. |

Codex discovery/invocation is documented in [Build skills](https://learn.chatgpt.com/docs/build-skills). Claude's project paths and `/skill-name` invocation are documented in [Claude Code skills](https://code.claude.com/docs/en/skills). Zed documents [native skills](https://zed.dev/docs/ai/skills) separately from the [external-agent configuration boundary](https://zed.dev/docs/ai/external-agents). Discovery can be disabled by local or managed settings; diagnose the actual environment without changing global settings for this workflow.

## Bundled upstream instructions are methods, not commands

Read them only when routed by the parent skill. Nested `SKILL.md` files under `vendor/` are pinned references; they are not intended as independent installations. If a client lists them recursively, select the coordinator by its full installed path rather than invoking an upstream entry point alone. Do not flatten or separately register the bundle: that can bypass its gates or collide with existing skills.

- Matt's `grill-me` delegates to `grilling` using Claude's Skill mechanism. Read both files; ask one decision question per turn under this workflow.
- Superpowers `writing-plans` references further execution and worktree skills. They are not dependencies of this coordinator. Replace that handoff/header and default artifact path as directed in the parent SKILL.md. Do not automatically execute, commit, install tools, or dispatch future tasks.
- Han uses `!` command preprocessing, `${CLAUDE_PLUGIN_ROOT}`, namespaced skills, an explorer agent, and personal/plugin configuration lookup. This bundle supplies the teaching method, format, explanation helper and shared references. Do not evaluate the preprocessing or run those native plugin calls, even in Claude. Trace the actual code with the host's available file/search tools and apply the parent overrides. Full native Han plugin execution is outside this package.

Report which adaptation was used. Never claim plugin execution merely because a SKILL.md was read. Existing repository/host instructions govern tool access; no skill file supplies credentials or new runtime permissions.

## Moving between providers

The transfer unit is the approved requirements/design/plan, relevant ticket, state, handoff, baseline evidence and actual code. A possible sequence is Codex requirements/design → Claude planning → another repository-capable agent implementing one slice. It is a choice, not a recommendation that one provider is universally better.

On another machine or worktree, verify the skill and private artifacts are present at actual accessible paths. Ignored documents are absent from normal clones and remote sessions. Transfer only the needed material using the user's chosen mechanism; do not publish it to a shared repo to make it accessible. Re-resolve paths, source symbols, hashes, HEAD and uncommitted work. Read only the relevant phase and validate current human approval evidence; request reconfirmation if unavailable. Changing the provider, opening a new session, or pasting a saved prompt never approves anything.
