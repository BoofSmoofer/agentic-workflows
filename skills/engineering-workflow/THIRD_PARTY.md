# Third-party sources and adaptations

The files under `vendor/` are curated, unmodified snapshots. Exact per-file source paths, Git blob IDs, SHA-256 hashes, and upstream commits are recorded in [vendor/manifest.json](vendor/manifest.json). Original copyrights and MIT license texts are included beside each source tree.

| Source and author | Pinned revision | Included methods | License |
| --- | --- | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills), Matt Pocock | [4ae2317ddb22b046e26455e4f9c9b3aaaf62212d](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d) | `grill-me`, its `grilling` delegate, `codebase-design` and its design references/metadata | [MIT](vendor/mattpocock-skills/LICENSE) |
| [obra/superpowers](https://github.com/obra/superpowers), Jesse Vincent | [2ce8aa15d05bd57213e6f746f953aafb7ded7a8b](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b) | `writing-plans` | [MIT](vendor/superpowers/LICENSE) |
| [testdouble/han](https://github.com/testdouble/han), Test Double, Inc. | [abba73a773528905a8f3d15956029394746e5c7f](https://github.com/testdouble/han/tree/abba73a773528905a8f3d15956029394746e5c7f) | `code-walkthrough`, its format, `explanation-guidance`, shared configuration/explanation/readability/voice references | [MIT](vendor/testdouble-han/LICENSE) |

The original coordinator and session handoff guide are derived from the user's approved workflow development, not copied from an upstream orchestrator. They impose the requested human gates, local artifacts, conservative context decisions, and deliberate handoffs. Upstream files remain unchanged; adaptations are stated in the coordinator and [client guide](references/clients.md). The bundle is not endorsed by the upstream authors.

Compatibility adaptations: one decision question per turn; no interview-to-implementation jump; explicit named artifact approvals; technical architecture beyond vocabulary; planning only with a personal artifact path and replacement execution handoff; one authorized implementation slice; paced, read-only teaching of its actual incremental diff; final checks and teach-back; manual-file routing instead of Claude plugin machinery. Missing upstream siblings are not silently installed or invoked.

To update a source, choose an explicit commit, review its changed methods and dependencies against the coordinator, copy the selected files with original notices, regenerate all affected manifest hashes/blob IDs, validate links, and repeat gate/resume scenarios. Do not follow moving `main` versions automatically or substitute a fork without recording provenance. Keep this file and licenses in every installed copy.
