#!/usr/bin/env python3
"""Check the plugin manifests, MCP configs and skills. Exit 1 on any error.

Checks: JSON parses; one version across all manifests, present in CHANGELOG;
Antigravity name, logo and Marketplace fields; the MCP server URL identical in
every config with the right key per client; marketplace entries point to
existing paths; Codex paths exist; every skill folder has SKILL.md whose
frontmatter name matches the folder; no dash used as sentence punctuation in
public Markdown or JSON text.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER_URL = "https://mcp.directcase.ai/"
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}
errors = []


def read(rel):
    p = ROOT / rel
    if not p.is_file():
        errors.append(f"{rel}: missing")
        return ""
    return p.read_text(encoding="utf-8")


def load(rel):
    text = read(rel)
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        errors.append(f"{rel}: invalid JSON ({e})")
        return {}


ag = load(".antigravity-plugin/plugin.json")
cl = load(".claude-plugin/plugin.json")
cx = load(".codex-plugin/plugin.json")
mk = load(".claude-plugin/marketplace.json")
ag_mcp = load("mcp_config.json")
cl_mcp = {"mcpServers": cl.get("mcpServers")} if isinstance(cl.get("mcpServers"), dict) else {}
cx_mcp = load(str(Path(cx["mcpServers"]))) if isinstance(cx.get("mcpServers"), str) else {}
if (ROOT / ".mcp.json").exists():
    errors.append(".mcp.json at the repo root: Antigravity strict validation rejects it; keep MCP config in the manifests")

# Versions
versions = {"antigravity": ag.get("version"), "claude": cl.get("version"), "codex": cx.get("version")}
if None in versions.values() or len(set(versions.values())) != 1:
    errors.append(f"versions missing or different: {versions}")
elif f"## {versions['antigravity']}" not in read("CHANGELOG.md"):
    errors.append(f"CHANGELOG.md has no entry for {versions['antigravity']}")

# Antigravity manifest
if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", ag.get("name", "")):
    errors.append("antigravity name must be lowercase kebab-case")
for f in ["name", "displayName", "description", "version", "logo", "author", "suggestedPrompts"]:
    if not ag.get(f):
        errors.append(f"antigravity manifest missing {f}")
if len(ag.get("suggestedPrompts", [])) > 3:
    errors.append("antigravity suggestedPrompts max 3")
if ag.get("logo") and not (ROOT / ag["logo"]).is_file():
    errors.append(f"logo not found: {ag['logo']}")
if re.match(r"(?i)(antigravity|gemini|claude|cursor)", ag.get("displayName", "")):
    errors.append("displayName must not lead with a client name")
if len({m.get("name") for m in (ag, cl, cx)}) != 1:
    errors.append("plugin name differs between manifests")

# MCP configs
for label, cfg, key, need_type in [
    ("mcp_config.json", ag_mcp, "serverUrl", None),
    (".claude-plugin/plugin.json mcpServers", cl_mcp, "url", "http"),
    (".codex-plugin mcpServers file", cx_mcp, "url", None),
]:
    servers = cfg.get("mcpServers") or {}
    if not servers:
        errors.append(f"{label}: no mcpServers")
    for name, srv in servers.items():
        url = srv.get(key) or (srv.get("url") if key == "serverUrl" else None)
        if url != SERVER_URL:
            errors.append(f"{label} {name}: expected {key} {SERVER_URL!r}, got {url!r}")
        if need_type and srv.get("type") != need_type:
            errors.append(f"{label} {name}: type must be {need_type!r}")

# Claude marketplace
for entry in mk.get("plugins", []) or [{}]:
    if entry.get("name") != cl.get("name"):
        errors.append(f"marketplace entry {entry.get('name')!r} does not match .claude-plugin name")
    if not (ROOT / entry.get("source", "\0")).exists():
        errors.append(f"marketplace entry source not found: {entry.get('source')!r}")

# Codex manifest
for f in ["skills", "mcpServers"]:
    if not cx.get(f) or not (ROOT / cx[f]).exists():
        errors.append(f"codex {f} path missing: {cx.get(f)!r}")
iface = cx.get("interface", {})
if not iface.get("displayName") or not iface.get("defaultPrompt"):
    errors.append("codex interface needs displayName and defaultPrompt")

# Skills
skills_dir = ROOT / "skills"
if not skills_dir.is_dir():
    errors.append("skills/ missing")
else:
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        md = skill_dir / "SKILL.md"
        if not md.is_file():
            errors.append(f"{skill_dir.name}: SKILL.md missing")
            continue
        m = re.match(r"---\n(.*?)\n---", md.read_text(encoding="utf-8"), re.S)
        fm = m.group(1) if m else ""
        nm = re.search(r"""^name:\s*["']?([^"'\s]+)["']?\s*$""", fm, re.M)
        if not nm or nm.group(1) != skill_dir.name:
            errors.append(f"{skill_dir.name}: frontmatter name must equal folder name")
        if not re.search(r"^description:", fm, re.M):
            errors.append(f"{skill_dir.name}: description missing")

# Dashes as punctuation in public copy (Markdown prose and JSON strings)
DASH = re.compile(r"[—–]| -- | - ")


def public_files(pattern):
    for p in ROOT.rglob(pattern):
        if not SKIP_DIRS.intersection(p.relative_to(ROOT).parts):
            yield p


for md in public_files("*.md"):
    in_code = False
    for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        text = re.sub(r"`[^`]*`", "", line)
        text = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", text)
        if text.strip().startswith("|") and set(text.replace("|", "").strip()) <= set("- :"):
            continue
        if DASH.search(text):
            errors.append(f"{md.relative_to(ROOT)}:{i}: dash used as punctuation")


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)


for js in public_files("*.json"):
    try:
        data = json.loads(js.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        continue
    for s in strings(data):
        if DASH.search(s):
            errors.append(f"{js.relative_to(ROOT)}: dash used as punctuation in {s[:60]!r}")

# Only expected files may be published (local junk is ignored via .gitignore)
ALLOWED = re.compile(
    r"^(README\.md|CHANGELOG\.md|LICENSE|\.gitignore|mcp_config\.json"
    r"|\.antigravity-plugin/(plugin\.json|README\.md)"
    r"|\.claude-plugin/(plugin|marketplace)\.json"
    r"|\.codex-plugin/(plugin|mcp_servers)\.json"
    r"|\.github/workflows/[a-z-]+\.yml"
    r"|assets/[a-z0-9_-]+\.(png|svg)"
    r"|scripts/validate\.py"
    r"|skills/[a-z0-9-]+/(SKILL\.md|references/[a-z0-9-]+\.md))$"
)
IGNORED = re.compile(r"(^|/)(\.DS_Store|\.claude/|\.git/|__pycache__/|\.venv/)|\.pyc$|^\.mcp\.json$")
for p in ROOT.rglob("*"):
    if p.is_file():
        rel = p.relative_to(ROOT).as_posix()
        if not IGNORED.search(rel) and not ALLOWED.match(rel):
            errors.append(f"unexpected file, not allowed to publish: {rel}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("ok:", ", ".join(f"{k} {v}" for k, v in versions.items()))
