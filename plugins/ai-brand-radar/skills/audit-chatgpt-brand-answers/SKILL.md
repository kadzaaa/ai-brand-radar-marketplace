---
name: audit-chatgpt-brand-answers
description: Audit how ChatGPT answers 50 high-intent questions about a real brand, which sources it cites, where competitors replace the brand, whether product information is correct and complete, and what exact website changes could improve future ChatGPT answers. Use for ChatGPT brand visibility audits, citation audits, answer-engine optimization, competitor answer comparisons, website content-gap analysis, post-update rechecks, and comparisons with a previous AI Brand Radar scan. Do not use this skill to claim access to global ChatGPT analytics or internal OpenAI ranking data.
---

# Audit ChatGPT Brand Answers

Run an evidence-backed, controlled audit centered on one outcome: help users receive accurate, useful information about the brand when they ask ChatGPT commercially important questions. Treat every result as an observation from the current research run, never as global ChatGPT telemetry.

## Default language

Communicate with the user in Russian by default, including onboarding, progress updates, headings, metric names, definitions, interpretations, source notes, confidence labels, gap labels, reports, tables, and recommendations. Write all free-text research fields in Russian, even when the researched sources are in another language.

Use the GEO language only for the exact 50 ChatGPT prompts and their verbatim recheck versions. Keep URLs, registered brand and product names, and machine-readable schema keys unchanged. Summarize or translate source evidence into Russian instead of switching the report language.

Switch the report language only when the user explicitly requests another language. The report language and prompt language are separate settings: a Russian-speaking user may receive a fully Russian report about English-language prompts for the United Kingdom.

## Required resources

Read these files before the corresponding phase:

- Before generating prompts or scoring results, read `references/methodology.md`.
- Before starting or resuming a project brief, read `references/brief.md`.
- Before writing the report, read `references/report-spec.md`.
- Before analyzing regulated categories, claims, privacy, or competitor content, read `references/safety.md`.
- Use `assets/project-input.template.json` when creating a reusable project profile.
- Use `assets/scan.template.json` as the scan data contract.
- Use `assets/report.template.md` when the user requests a saved Markdown report.
- Run `scripts/score_scan.py` for final metrics and scan comparisons. Do not calculate final percentages by estimation.

## Operating modes

Choose the narrowest mode matching the request:

- **Full audit:** run exactly 50 scenarios and produce the complete report.
- **Prompt panel only:** generate 50 scenarios without researching answers.
- **Page opportunity:** analyze one answer gap and create a page brief.
- **Recheck:** rerun selected prompts after a website change.
- **Compare scans:** compare two completed scan JSON files.

If the user requests a full audit, do not silently reduce the panel below 50. If time or tool access prevents completion, save partial observations and label the audit incomplete; do not publish final visibility percentages.

## Step 1: Build the brand profile

Start with the guided brief unless the user has already provided all required project data. Follow `references/brief.md`. First explain what the audit will do, say that the user will answer a few short questions, and end with the CTA **«Начнём?»**. After the user agrees, ask one numbered step at a time in Russian. Never present the entire questionnaire as one large form.

Open a new brief with:

```text
Проведу аудит 50 популярных и коммерчески значимых запросов пользователей в ChatGPT, оценю представленность и цитируемость бренда, а затем дам конкретные рекомендации по контенту и страницам сайта, которые могут повысить вероятность появления бренда в ответах ChatGPT.

Сначала нужно ответить на несколько коротких вопросов о бренде, сайте и рынке. Аудиторию, целевое действие, конкурентов, проверяемые факты и приоритетные страницы я определю самостоятельно.

Начнём?
```

After the user agrees, collect only these three user-input blocks:

- brand name and canonical domain;
- market and prompt language;
- product, category, and any user-stated product priority.

Infer the target audience and conversion goal from the brand's activity, product, site, and GEO. Select two to five relevant competitors for that GEO and label the selection as a research assumption. Independently determine the product facts to verify, outdated or prohibited claims to avoid, and priority pages and topics. For regulated categories, include licensing or legal availability, eligibility, promotions, payments, safety, and responsible-use information when relevant.

Do not ask the user to supply competitors, audience, conversion goal, required facts, prohibited claims, priority pages, Search Console, FAQ, support data, or a previous audit. Use any such material when the user volunteers it, but do not block the audit on it.

After the user answers the third block, do not ask whether the brief is correct and do not request approval of the 50-scenario panel. State the inferred assumptions briefly as a progress update and immediately begin the audit. Ask an extra question only when a missing fact makes the brand, canonical site, or GEO impossible to identify safely.

Verify the canonical site and current product facts from first-party pages. Do not treat review sites or model output as the source of truth for pricing, limits, security, availability, or legal claims.

## Step 2: Generate the 50-scenario panel

Follow the exact cluster counts in `references/methodology.md`. Generate prompts in the user's target language, while preserving natural phrasing used by the intended audience.

Prioritize prompts using, in order:

- user-provided Search Console or internal-search evidence;
- visible autocomplete, related questions, forums, reviews, and competitor FAQs;
- commercial relevance and product fit;
- common category, comparison, feature, pricing, trust, and implementation intents.

Call the panel `high-intent` unless reliable demand data supports `popular`. Never invent ChatGPT prompt volume.

Separate prompts into:

- 40 generic prompts that do not contain the target brand;
- 10 branded, comparison, alternative, migration, or accuracy prompts.

Show the panel to the user before a full audit only when the user explicitly asks to approve it. Otherwise proceed, preserving a copy in the scan output.

## Step 3: Research each scenario neutrally

Use web search for a real-brand audit. If web search is unavailable, use only sources supplied by the user and label the run incomplete unless all 50 scenarios have sufficient evidence.

For each generic prompt:

1. Research the prompt without adding the target brand to the query.
2. Draft the concise answer a user would need.
3. Record the brands and sources that naturally surface.
4. Only then score the target brand.
5. Verify any product claim against first-party pages.

For branded prompts, evaluate accuracy, completeness, citations, and whether the answer distinguishes facts from marketing claims.

Do not reuse one answer as evidence for several prompts without checking that it resolves each intent. Preserve URLs and short paraphrased evidence; avoid long quotations.

## Step 4: Record observations

Create one record per scenario using the schema in `assets/scan.template.json`. Required judgments include:

- brand mentioned;
- brand recommended, not merely named;
- first position when the response ranks products;
- owned-domain citation;
- canonical target-page citation;
- answer correctness against verified facts;
- answer completeness for the user's intent;
- competitor substitution;
- whether the brand site's current content is sufficient to answer the intent directly and accurately;
- whether a named competitor has materially stronger content for the same intent;
- missing information;
- exact target URL and recommended website change;
- confidence and evidence.

Use `null` when correctness or position is not applicable. Do not convert unknown values to `false`.

## Step 5: Diagnose answer gaps

Classify every incomplete or incorrect answer as one or more of:

- `missing_page`;
- `missing_direct_answer`;
- `conflicting_first_party_facts`;
- `outdated_external_source`;
- `weak_entity_definition`;
- `feature_ambiguity`;
- `pricing_ambiguity`;
- `trust_or_privacy_gap`;
- `comparison_gap`;
- `insufficient_evidence`;
- `product_gap_not_content_gap`.

Recommend a content change only when content can plausibly address the gap. Label missing functionality, availability, price, or integrations as product gaps when appropriate.

Every website recommendation must specify:

- target URL: update an existing page when possible;
- direct answer to add near the top;
- facts, tables, examples, or evidence required;
- internal links and canonical relationships;
- relevant structured data only when truthful;
- the exact prompt used to recheck the change;
- a measurable success condition.

Do not recommend generic keyword stuffing, mass article generation, fake reviews, fabricated citations, or copying competitor text.

## Step 6: Score deterministically

Save the completed observation set as JSON and run:

```bash
python3 scripts/score_scan.py path/to/scan.json --strict-50
```

For a comparison:

```bash
python3 scripts/score_scan.py new-scan.json --strict-50 --compare previous-scan.json
```

Use the script output for all reported counts and percentages. If validation fails, correct the observation data before reporting.

## Step 7: Produce the report

Follow `references/report-spec.md`. Deliver the user-facing report as Russian prose and Markdown, never as raw JSON. Lead with a concise main message that states:

1. the most popular or commercially important query themes about the brand and its category;
2. representative exact prompts in the GEO language;
3. how many of the 50 intents the current brand-site content can support;
4. where competitors have stronger pages or replace the brand in observed answers;
5. the site changes most likely to close those gaps;
6. how to verify improvements with the same prompts.

Call prompts `popular` only when demand evidence supports that label. Otherwise call them `frequent themes according to public demand proxies` or `high-intent prompts`; state the supporting signal and never invent ChatGPT prompt volume.

Render **Итоговые метрики** as explanatory bullet paragraphs. For every metric, give the Russian name, result, denominator, plain-language definition, and one-sentence interpretation for this brand. Do not paste the scoring JSON.

Render **Приоритетные изменения страниц** as an explained P0/P1/P2 editorial backlog. Explain what the section means and why the priorities were assigned. For every page, write the URL, problem, exact change, affected prompts, competitor evidence, expected user benefit, and recheck condition as prose or bullets. Do not output page recommendations as JSON.

Include methodology and limitations. Use the Russian label «Присутствие бренда в наблюдаемых ответах ChatGPT», not global `ChatGPT market share` or `share of voice` without qualification.

## Step 8: Save reusable outputs

When file creation is available, save:

```text
ai-brand-radar-output/
├── project.json
├── prompts.json
├── scan.json
├── report.md
├── final-metrics.md
└── priority-page-changes.md
```

Do not overwrite a prior scan. Use an ISO date or unique run identifier. When files cannot be created, provide the report in the conversation.

Treat JSON files as internal calculation and reproducibility artifacts. Do not show or offer raw JSON by default; provide it only when the user explicitly asks for a technical export. The primary deliverable is the Russian text report.

## Completion standard

A full audit is complete only when:

- exactly 50 scenarios are recorded;
- every eligible scenario has evidence;
- final metrics come from `score_scan.py`;
- every eligible scenario records site-content readiness and competitor-content advantage when scorable;
- factual product claims are verified from first-party sources;
- every answer gap has a page-level action or is labeled non-content-addressable;
- every recommended change has a recheck prompt;
- the report discloses that it is a controlled current-run observation, not internal ChatGPT analytics.
