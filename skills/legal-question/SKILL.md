---
name: legal-question
description: >-
  Answers a legal question only from DirectCase sources (legislation, case
  law, regulators and EU bodies), with every source linked. Use for any legal
  question that needs research. To check the citations in a document use
  citation-check; for a written memo use legal-memo.
---

# Legal question

Answer only from what DirectCase tools return. Do not use web search, web
fetch or your own memory for legal content, and never cite a provision or
decision that a tool did not return. If DirectCase holds nothing on a point,
say so.

## 1. Scope the question

Before searching, settle four things:

- the legal area and the precise issue;
- the jurisdiction: the account's country (`legal-search:get_entitlements` shows it) and
  whether EU law applies;
- the date that matters: when the facts happened;
- which sources the question needs: legislation, case law, regulatory
  practice, or several.

If the issue, the jurisdiction or the date of the facts is not clear from the
conversation, ask the user one short question covering what is missing and
wait for the answer. Do not ask about anything the context already settles.

## Legislation tools

Statute tools are named per jurisdiction: `get_law_<country>` returns the
wording of one provision and `search_law_<country>` finds provisions by their
words, where `<country>` is the account's country code (for example
`get_law_cz`, `get_law_sk`). Accounts in EU member states also have
`get_law_eu` and `search_law_eu` for EU law. `get_entitlements` lists the exact
names in `available_tools`.

- Name the act and the provision with the parameters the tool's schema
  lists; they follow the citation units of that law (for example `zakon` and
  `paragraf`, or `celex` and the article for EU law).
- Pass `as_of` for a past date and `history: true` for earlier wordings. For
  EU law pass `language` for the language of the wording.
- Take the wording from `text`, its validity from `valid_from` and
  `valid_to`, and the link from `url`.
- If the account has no `get_law_` tool for a jurisdiction, quote the
  legislation from `search_law_parallel` results and link their `url`.

## 2. Search

| Source | Find with | Read and cite with |
| --- | --- | --- |
| Legislation | `legal-search:search_law_parallel` or `search_law_<country>` | `get_law_<country>` (EU law: `get_law_eu`) |
| Case law | `legal-search:search_caselaw_parallel` | `legal-search:get_document` |
| Regulators and EU bodies (decisions, guidelines, opinions, Q&A) | `legal-search:search_regulatory_parallel` | `legal-search:get_document` |

- Call only the search tools the question needs. Each of them can be called
  once per conversation, so send two to four focused `queries` in one call,
  in the language of the jurisdiction and in English. If a tool was already
  used, reuse its results and continue with `legal-search:search_keyword`,
  `legal-search:search_similar`, `search_law_<country>`, or `legal-search:search_identifier` for a known case
  number or ECLI.
- Search summaries (`collection_summaries`) are leads, not sources. Open every decision or regulatory document you
  rely on with `legal-search:get_document` (pass `mongo_uuid` and `collection` from the
  result) and quote statutes from `get_law_<country>`.
- If `legal-search:get_document` returns `truncated: true`, read on with `char_start` set
  to `next_char_start` until you reach the court's own reasoning; do not cite
  a decision from its opening part alone.
- EU law: use `get_law_eu` and `search_law_eu` with `language`.

## 3. Date of the law

Use today's wording unless the facts lie in the past; then pass that date as
`date` to `legal-search:search_law_parallel` and as `as_of` to the `get_law_` and
`search_law_` tools.
State in every answer which wording you used:

- "Current wording as of <today's date>", or
- "Historical wording, valid from <valid_from> to <valid_to>", with the dates
  from the tool result.

## 4. Answer

- Open with a short answer in two or three sentences. Then give the
  legislation, the case law and the regulatory practice, and end with the
  open points.
- Start the case law with the highest courts (for example the constitutional
  and supreme courts, the CJEU and the ECtHR), then add the arguments of lower
  courts. Say so when decisions conflict.
- For every decision give the case number, the date and the DirectCase link.
- If the question concerns the law of a country other than the account's
  jurisdiction, say that the account works with one jurisdiction at a time,
  offer what EU law covers, and do not fill the gap from memory.
- If the user wants a written memo, continue with `legal-memo`.
- Link every legal statement to its source with the `url` of the tool
  result.
- The answer supports a lawyer's work; it is not legal advice.
