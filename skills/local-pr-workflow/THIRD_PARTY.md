# Third-party source

This skill reuses the existing library's pinned Matt Pocock `grill-me` and `grilling` snapshots from `mattpocock/skills`, revision `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`. Their original bytes and [MIT notice](vendor/mattpocock-skills/LICENSE) are preserved. Exact source paths, revision, and hashes are in [vendor/manifest.json](vendor/manifest.json).

Only the two interview instructions and license are bundled, so installation is self-contained without depending on an installed `engineering-workflow`. The coordinator adapts provider-specific skill calls to direct file reads and delegation to the host's available permissions/tools. It adds manual diff review and explicit local commit gates; the upstream interview does not authorize implementation automatically.

For updates, deliberately select and review a revision, preserve its notices, update the selected files and manifest together, and run the library validator. Do not follow a moving upstream branch automatically. The original workflow instructions are not part of the upstream MIT snapshot.
