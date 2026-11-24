---
name: citation-check
description: >-
  Checks every legal citation in a document (brief, contract, opinion, memo or
  AI draft) against DirectCase sources: is each provision or decision found,
  does it say what the document makes of it, and does quoted wording match.
  Trigger it for requests to verify or check the citations in a text.
---

# Check the citations in a document

You go through a document citation by citation and report what you found in
DirectCase sources, each with a link to the source. Report like an auditor:
say what you found and what discrepancies you noted, never that a citation
is correct. You do not rewrite the document unless asked.

## Jurisdiction

A DirectCase account works in one jurisdiction at a time; `directcase:get_entitlements`
gives it in `country`. You check the law and case law of that country, plus
EU law. A citation of another country's law gets the status
`other jurisdiction`; never report it as missing.

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

## Workflow

1. **Collect the citations by type.** Read the whole document and sort what
   it cites into provisions, case numbers or ECLIs, and case names without a
   number. `search_identifier` and `get_document` take up to 20 items per
   call; split longer lists into calls of 20. Provisions are read one per
   call. For every citation keep:
   - the sentence that relies on it, with the paragraph around it,
   - whether the document puts the source's words in quotation marks,
   - the date the document's facts relate to (today if it gives none).
2. **Provisions.** Read each provision with `get_law_<country>` (EU acts:
   `get_law_eu` with `celex` and `language` set to the document's language),
   with `as_of` set to the date from step 1. Take the wording from `text`
   and the link from `url`.
   - If the result has `exists: false`, the act was found without that
     provision: the status is `no such provision`.
   - If the act is not recognised, find it with `search_law_<country>` (EU:
     `search_law_eu`) and repeat the call once with its `code`.
3. **Past wording.** When the date from step 1 lies in the past, check for
   each act whether the result really comes from a version in force on that
   date: `valid_from` on or before the date and `valid_to` empty or after it.
   - If it does, the past wording is available. Repeat the call once without
     `as_of` and note every provision whose wording has changed since.
   - If the result carries no such date, or a later one, only the current
     wording is available for that act. Check against the current wording
     and give today's date in `Wording as of`. If the user explicitly asked
     for a past date, open the answer with a warning that historical wording
     of that act is not available, so the check used the current wording.
4. **Decisions.** Send all case numbers and ECLIs in one `directcase:search_identifier`
   call and match the results back to the inputs:
   - Compare case numbers after removing spaces and dots, ignoring case:
     `Pl. ÚS 19/93` matches `Pl.ÚS 19/93`.
   - Match an ECLI through the `ecli` field where a result has one. An ECLI
     contains the case number; if the ECLI returns nothing, also search the
     case number.
   - Drop repeated `uuid`s and treat the same `ecli` in several language
     collections as one decision; link the copy in the document's language.
   - One case number can cover several documents (orders, an Advocate
     General's opinion, the judgment). Pick the one whose date, ECLI or type
     matches the citation; for a bare case number take the decision that
     closed the case and list the others in Note. Report `several matches`
     only when this still leaves more than one.
   - For case names without a number use `directcase:search_keyword` with the name in
     quotation marks, plus the court if the document names it.
   - Link every decision with `url` from the result.
5. **Read and compare.** Open the decisions with `directcase:get_document` (up to 20
   UUIDs, pass `collection`; continue with `char_start` when `truncated`) and
   find the passage the sentence relies on. For provisions you already have
   `text`.
   - **Words in quotation marks** must appear in the source exactly. Ignore
     line breaks, extra spaces, the provision's own number and heading, and
     an ellipsis marking an omission; any other difference gives
     `quote not in source`.
   - **A paraphrase** is judged by meaning, not by words. Read the passage
     with what surrounds it: an exception, a condition, the next sentence,
     or the fact that the court is restating a party's argument or a view it
     goes on to reject. If the paraphrase states something else, the status
     is `meaning differs`. If the cited words are there but their context
     narrows or reverses them, the status is `taken out of context`. Say in
     one sentence what the source actually says.
6. **No result.** When a citation cannot be found, report it as not in
   DirectCase sources.

## Usage limits

If a tool refuses a call because the account's usage limit is reached, stop
calling it. Open the answer with a warning that the limit was reached and
how many citations remain unchecked, mark those rows `not checked`, and
finish the table with what you have.

## Output

Warnings (usage limit, historical wording not available) come first. Then one
table, one row per citation, in the order of the document:

| # | Citation as written | Status | Wording as of | Note | Link |
| --- | --- | --- | --- | --- | --- |

- **Wording as of:** for a provision, the date whose wording you checked
  (today's date when only the current wording is available), with "changed
  since" when today's wording differs; for a decision, the decision date.
- **Link:** `url` from the tool result.

Status:
- `found, no discrepancy noted`: the source was found and the passage read
  showed no discrepancy with the sentence
- `quote not in source`: the quoted words are not in the source
- `meaning differs`: the paraphrase says something the source does not
- `taken out of context`: the words are there, their context changes them
- `no such provision`: the act exists without the cited provision; name the
  closest one
- `not in DirectCase sources`
- `several matches`: more than one decision fits the citation
- `other jurisdiction`: law of a country other than the account's
- `not checked`: the usage limit was reached first

After the table, list every row with a discrepancy or without a result,
starting with `no such provision`, `quote not in source`, `meaning differs`
and `taken out of context`, each with what the lawyer should do about it.
Close with three points: "no discrepancy noted" covers the passages read,
it does not certify a citation; for decisions the check covers the decision
and its content, not how later case law dealt with it; this supports a
lawyer's work and is not legal advice.
