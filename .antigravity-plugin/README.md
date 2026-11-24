# DirectCase Legal Search for Google Antigravity

Legal research over national and EU law. DirectCase finds the relevant
legislation and court decisions and links each result to its document.

## What it does

- Searches legislation, case law and regulatory decisions: national courts,
  including supreme and constitutional courts where available, EU legislation,
  the Court of Justice of the EU and the European Court of Human Rights.
  Coverage varies by country and plan.
- Returns the wording of a provision held for a given date.
- Looks up decisions by case number or ECLI and opens their full text.
- Compares the citations in a document with DirectCase sources and flags the
  ones it cannot find.

No local data is ever changed. All tools read, except the hearing watch: when
you ask for it, it saves the case to your DirectCase profile and e-mails you
when a hearing changes.

## Install

```
agy plugin install https://github.com/directcase/legal-mcp
```

When the MCP server connects, Antigravity opens the DirectCase sign-in in your
browser (OAuth 2.0 with PKCE). A DirectCase account is required; new accounts
start free.

## Contents

| Path | Purpose |
| --- | --- |
| `.antigravity-plugin/plugin.json` | Plugin manifest |
| `mcp_config.json` | Remote MCP server `https://mcp.directcase.ai/` (Streamable HTTP) |
| `skills/legal-question/SKILL.md` | A legal question answered from legislation and case law, with linked sources |
| `skills/citation-check/SKILL.md` | Every citation in a document checked against DirectCase sources, as a table |
| `skills/legal-memo/SKILL.md` | A structured legal memo with linked sources |
| `assets/logo.png` | Plugin icon |

## Links

- Documentation: https://www.directcase.ai/gb/en/docs/mcp/
- Website: https://www.directcase.ai/
- Support: support@directcase.ai
- Privacy policy: https://www.directcase.ai/gb/en/privacy-policy/
- Terms: https://www.directcase.ai/gb/en/terms/
