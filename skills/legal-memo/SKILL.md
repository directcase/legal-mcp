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

## Workflow

1. **Scope.** Confirm the question, the jurisdiction, the relevant date and
   the facts the memo may assume. If a fact that changes the answer is
   missing, list it as an assumption.
2. **Research.** Search all three source types, each with one call of two
   to four focused `queries`:
   - legislation with `legal-search:search_law_parallel` (with `date` for past facts),
   - case law with `legal-search:search_caselaw_parallel`,
   - regulators with `legal-search:search_regulatory_parallel` when the matter falls in
     a regulated area (for example energy, competition, financial services
     or data protection).

   Each of these tools can be called once per conversation. If one was
   already used in this conversation, reuse its results and continue with
   `legal-search:search_keyword`, `legal-search:search_similar` and `legal-search:search_law_text`.
3. **Verify.** Read the wording of every provision you will cite with
   `legal-search:get_law_provision` (with `date` for past facts; `eu-<language>` for EU
   law). Find each decision known by its case number or ECLI with
   `legal-search:search_identifier`, and open every decision you rely on with
   `legal-search:get_document`. Search summaries are leads, not sources.
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
