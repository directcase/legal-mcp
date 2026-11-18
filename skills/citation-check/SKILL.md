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

A DirectCase account works in one jurisdiction at a time; `legal-search:get_entitlements`
gives it in `country`. You check the law and case law of that country, plus
EU law. A citation of another country's law gets the status
`other jurisdiction`; never report it as missing.

## Workflow

1. **Collect the citations by type.** Read the whole document and sort what
   it cites into provisions, case numbers or ECLIs, and case names without a
   number. Each tool below takes up to 20 items per call, so one call per
   type usually covers a document; split longer lists into calls of 20. For
   every citation keep:
   - the sentence that relies on it, with the paragraph around it,
   - whether the document puts the source's words in quotation marks,
   - the date the document's facts relate to (today if it gives none).
2. **Provisions.** Send all provisions in one `legal-search:get_law_detail` call, each
   with `date` set to the date from step 1 and the provision in `fragment` in
   the notation of the country. Law of the account's country goes without
   `jurisdiction`; EU acts go with `jurisdiction: "eu"` and `lang` (the
   document's language). Take the wording from `text` and the link from
   `viewer_url`, or `url` where there is no `viewer_url`.
   - For each reference with `found: false`, call `legal-search:get_law_provision` with the
     citation as written (for EU law with `country: "eu-<lang>"`) to learn
     why. `reason: node_not_found` means the act exists without that
     provision: offer the existing provision in `closest` where the result
     has it, otherwise the paths in `nearest`. With `act_not_found` or
     `unparsed`, rephrase once with the act's number or full title.
3. **Past wording.** When the date from step 1 lies in the past, check for
   each act whether the result really comes from a version in force on that
   date: the version date in `iri`, or `effective_from` (`valid_from`) on or
   before the date with `effective_to` (`valid_to`) empty or after it.
   - If it does, the past wording is available. Repeat the call once without
     `date` and note every provision whose wording has changed since.
   - If the result carries no such date, or a later one, only the current
     wording is available for that act. Check against the current wording
     and give today's date in `Wording as of`. If the user explicitly asked
     for a past date, open the answer with a warning that historical wording
     of that act is not available, so the check used the current wording.
4. **Decisions.** Send all case numbers and ECLIs in one `legal-search:search_identifier`
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
   - For case names without a number use `legal-search:search_keyword` with the name in
     quotation marks, plus the court if the document names it.
   - Link every decision with `url` from the result.
5. **Read and compare.** Open the decisions with `legal-search:get_document` (up to 20
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
- **Link:** `viewer_url` or `url` from the tool result.

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
