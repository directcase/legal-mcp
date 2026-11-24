# Changelog

## 1.1.0 (2026-11-24)

- Plugin renamed from `legal-plugin` to `directcase-legal-search` in all manifests. Install commands for Claude Code and Codex change accordingly.
- MCP server renamed from `legal-search` to `directcase` (Codex: `codex mcp login directcase`); skills refer to its tools as `directcase:<tool>`.

## 1.0.1 (2026-11-23)

- Skills use the per-jurisdiction legislation tools (`get_law_<country>`, `search_law_<country>`, `get_law_eu`).

## 1.0.0 (2026-11-18)

- First public release.
- Plugin packages for Google Antigravity, Claude Code and OpenAI Codex.
- Skills: `legal-question`, `citation-check`, `legal-memo`.
