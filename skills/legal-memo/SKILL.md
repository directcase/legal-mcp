---
name: legal-memo
description: >-
  Writes a legal memo on a defined question: the conclusion first, then the
  national and EU legislation, the case law and a legal assessment, with
  every source linked through DirectCase. Use when the user asks for a memo,
  a research note or a written analysis of a legal issue.
---

# Legal memo

The memo weighs the arguments of both sides and says how a court or
authority would most likely decide. It is an internal assessment, not a
submission for one party. Every legal statement rests on a source a tool
returned.

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

1. **Scope.** Confirm the question, the jurisdiction, the relevant date and
   the facts the memo may assume. If a fact that changes the answer is
   missing, list it as an assumption.
2. **Research.** Search all three source types, each with one call of two
   to four focused `queries`:
   - legislation with `directcase:search_law_parallel` (with `date` for past facts),
   - case law with `directcase:search_caselaw_parallel`,
   - regulators with `directcase:search_regulatory_parallel` when the matter falls in
     a regulated area (for example energy, competition, financial services
     or data protection).

   Each of these tools can be called once per conversation. If one was
   already used in this conversation, reuse its results and continue with
   `directcase:search_keyword`, `directcase:search_similar` and `search_law_<country>`.
3. **Verify.** Read the wording of every provision you will cite with
   `get_law_<country>` or, for EU law, `get_law_eu` (with `as_of` for past
   facts), and link it with `url`. Find each decision known by its case number or ECLI with
   `directcase:search_identifier`, and open every decision you rely on with
   `directcase:get_document`. Search summaries are leads, not sources.
4. **Weigh the sources.** They do not carry the same weight. Legislation
   comes first, case law interprets it, and regulators' decisions and
   guidelines show how an authority applies it in practice. When they
   point in different directions, say so and let the higher source lead.
5. **Write.** Follow the structure below in the user's language, quoting
   sources in their original language. Keep the assessment tied to the
   sources; mark open points and conflicting decisions honestly.

## Structure

1. **Question** (as agreed in step 1, with the jurisdiction and the
   relevant date)
2. **Conclusion** (two to four sentences, with the main condition it
   depends on)
3. **Facts and assumptions**
4. **Legal framework** (national legislation first, then EU law where it
   applies; each provision quoted briefly, with its link)
5. **Case law** (national courts, then the CJEU and the ECtHR where
   relevant; each decision: court, date, case number or ECLI, its holding
   in one sentence, link)
6. **Regulatory practice** (only in a regulated area: the authority, date,
   reference, what it decided or recommends, link)
7. **Legal assessment** (apply the law to the facts in the order of the
   sources above, weigh the arguments of both sides, and say where EU law,
   the case law or a regulator points the other way)
8. **Risks and open questions**
9. **Sources** (the DirectCase link of every source used)

If a source is not found in DirectCase sources, say so in the memo instead of
citing from memory. The memo supports a lawyer's work; it is not legal
advice.
