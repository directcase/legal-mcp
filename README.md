# Legal MCP server for national and EU law: DirectCase Legal Search

DirectCase Legal Search is a hosted legal MCP server
([Model Context Protocol](https://modelcontextprotocol.io)) for lawyers,
in-house counsel and legal teams. It connects Claude, ChatGPT, Microsoft
Copilot, Gemini and other AI assistants to legislation, case law and
regulatory decisions of national and EU law, and links every result to its
source document in DirectCase. It also returns the wording of a provision for
a given date and looks up decisions by case number or ECLI.

This repository holds the connection details and the plugin packages for
Google Antigravity, Claude Code and OpenAI Codex. It contains no server code.

| | |
| --- | --- |
| Server URL | `https://mcp.directcase.ai/` |
| Transport | Streamable HTTP |
| Sign-in | OAuth 2.0 with PKCE; Dynamic Client Registration and Client ID Metadata Documents supported |
| Access | All tools read, except the hearing watch, which saves the cases you follow to your DirectCase profile |
| Docs and tool reference | https://www.directcase.ai/gb/en/docs/mcp/ |
| MCP Registry | `ai.directcase/directcase` |

> DirectCase supports legal work. It does not give legal advice and does not
> replace a lawyer's judgment.

## What it covers

Coverage varies by country and plan; see the coverage list at
https://www.directcase.ai/gb/en/docs/mcp/

- **Legislation:** national acts and regulations and EU legislation, with the wording held for a chosen date and, where available, its history.
- **Case law:** national courts, including supreme and constitutional courts where available, the Court of Justice of the EU and the European Court of Human Rights.
- **Regulatory decisions** and guidelines of supervisory authorities.
- **Exact lookup** by case number, file number or ECLI, and full texts of decisions.
- **Citation checks:** compare the decisions cited in a document with DirectCase sources and flag the ones that need a closer look.

## Examples

- "What did the Court of Justice of the EU decide in C-131/12 (Google Spain), and how does it relate to Article 17 GDPR?"
- "When can a company rely on legitimate interests under Article 6(1)(f) GDPR? Cite the CJEU case law."
- "Can an employer read an employee's work email? Answer from the legislation and case law, with links."
- "Is a non-compete clause enforceable after the employment ends? Summarise the leading decisions."
- "Check the case citations in this brief against DirectCase sources."

## Connect

A DirectCase account is required; new accounts start free at https://www.directcase.ai/.

### Google Antigravity

```
agy plugin install https://github.com/directcase/legal-mcp
```

### Claude Code

```
/plugin marketplace add directcase/legal-mcp
/plugin install legal-plugin@directcase
```

### OpenAI Codex

```
codex plugin marketplace add directcase/legal-mcp
codex plugin add legal-plugin@directcase
codex mcp login legal-search
```

The last command opens the DirectCase sign-in in your browser. To add only the
MCP server without the skills:

```
codex mcp add directcase --url https://mcp.directcase.ai/
codex mcp login directcase
```

### Claude, ChatGPT, Microsoft Copilot, Gemini Enterprise and other MCP clients

Add a custom (remote) MCP connector with the URL `https://mcp.directcase.ai/`
and sign in with your DirectCase account. Some clients need an administrator
to allow custom connectors. Guides per client:
https://www.directcase.ai/gb/en/docs/mcp/

## Skills

Skills tell the agent how to use the tools well. They load on demand, from a
plain request or as a slash command (in Claude Code: `/legal-plugin:legal-question`).

| Skill | Use it for |
| --- | --- |
| `legal-question` | A legal question answered from legislation and case law, with links to the sources |
| `citation-check` | Every citation in a brief, contract or draft checked against DirectCase sources, as a table |
| `legal-memo` | A structured legal memo: conclusion first, then legislation, case law and assessment, with linked sources |

New skills are listed in [CHANGELOG.md](CHANGELOG.md).

## Tools

The server groups its tools into search (case law, legislation, regulatory
decisions, keyword, semantic, exact identifier), documents (full text, the
wording of a provision at a date, legislative changes where available),
registries (company and insolvency registers where available) and a hearing
watch. The current
list with parameters is at https://www.directcase.ai/gb/en/docs/mcp/

## FAQ

### What is a legal MCP server?
A legal MCP server connects an AI assistant to legal sources through the Model
Context Protocol, so its answers rest on legislation and case law with links
instead of the model's memory. DirectCase Legal Search is a legal MCP server
for national and EU law, used from Claude, ChatGPT, Microsoft Copilot, Gemini
and other MCP clients.

### Is there an MCP server for EU law?
Yes. DirectCase Legal Search covers EU legislation, the Court of Justice of
the EU and the European Court of Human Rights, together with the national law
of EU member states.

### Which countries does the DirectCase legal MCP cover?
Most EU member states: their national law together with EU law. Coverage
differs by country and plan; the current list is at
https://www.directcase.ai/gb/en/docs/mcp/. Each account works with the law of
its country together with EU law.

### How is DirectCase different from asking ChatGPT directly?
A general assistant answers from its training data and the open web, which
can produce citations that do not exist. DirectCase Legal Search answers from
a legal database built for the task: every cited source links to its
document, and DirectCase knows how documents relate, such as the provisions a
decision applies, landmark rulings and similar decisions. It also holds
decisions that are hard to find on the open web, such as lower court
decisions in the countries where DirectCase indexes them.

### Which AI assistants work with DirectCase?
Most clients that support remote MCP servers over Streamable HTTP with OAuth,
for example Claude, ChatGPT, Microsoft Copilot, Gemini Enterprise, Google
Antigravity and Claude Code.

### Can it give the wording of a law on a past date?
Yes. Pass a date and the agent returns the version DirectCase holds for it
and says which version that is.

### Can it check citations in a contract or brief?
Yes. The agent looks up each cited decision in DirectCase sources and flags
the ones it cannot find, so you can check them.

### Does it change any data?
No local data is ever changed. All tools read, except the hearing watch: when
you ask for it, it saves the case to your DirectCase profile and e-mails you
when a hearing changes.

### Is there a free tier?
New accounts start free. Plans and prices: https://www.directcase.ai/

## Repository layout

| Path | Used by |
| --- | --- |
| `.antigravity-plugin/` and `mcp_config.json` | Google Antigravity |
| `.claude-plugin/` | Claude Code (MCP server defined in `plugin.json`) |
| `.codex-plugin/` | OpenAI Codex (MCP server in `mcp_servers.json`) |
| `skills/<name>/SKILL.md` | Shared skills for all clients |
| `scripts/validate.py` | Manifest and skill checks, also run in CI |

## Support

- Support: support@directcase.ai
- Privacy policy: https://www.directcase.ai/gb/en/privacy-policy/
- Terms: https://www.directcase.ai/gb/en/terms/
- Website: https://www.directcase.ai/

## License

Copyright 2026 DirectCase s.r.o.

The configuration and skill files in this repository are licensed under the
[Apache License 2.0](LICENSE). Use of the DirectCase service is governed by
the DirectCase terms at https://www.directcase.ai/gb/en/terms/

DirectCase and the DirectCase logo are trademarks of DirectCase s.r.o. The
license does not grant permission to use them, except to describe the origin
of this repository.
