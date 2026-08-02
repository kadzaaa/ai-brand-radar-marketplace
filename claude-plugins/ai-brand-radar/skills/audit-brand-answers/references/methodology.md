# Methodology

## Purpose

Measure whether a controlled set of high-intent questions receives accurate, complete, useful answers in Claude and determine which website changes could improve those answers. The method does not measure global Claude usage or internal ranking.

## Required 50-scenario composition

Generate exactly 50 scenarios:

| Cluster | Count | Purpose |
|---|---:|---|
| Category discovery and recommendation | 8 | Test generic product selection |
| Pricing, plans, and value | 8 | Test commercial facts and affordability |
| Audience and use cases | 8 | Test fit for important customer segments |
| Features and workflows | 7 | Test task-level product capabilities |
| Trust, privacy, safety, and accuracy | 9 | Test confidence-building facts |
| Implementation, integrations, and migration | 5 | Test adoption questions |
| Branded comparisons and alternatives | 5 | Test competitive accuracy |
| **Total** | **50** |  |

At least 40 prompts must be generic and must not name the target brand. Up to 10 may be branded, comparisons, alternatives, migrations, or direct accuracy checks.

## Demand labels

Use one of these labels for each prompt:

- `observed`: supported by user-provided Search Console, internal search, analytics, support, or sales data;
- `public_proxy`: supported by autocomplete, related questions, forums, reviews, or competitor FAQs;
- `editorial`: included because it is commercially important despite limited demand evidence.

Never invent Claude search volume. Call the panel `high-intent` unless observed demand data justifies stronger language.

In the Russian report, translate these labels as:

- `observed` — «подтверждено данными бренда»;
- `public_proxy` — «подтверждено публичными сигналами спроса»;
- `editorial` — «коммерчески важный редакционный сценарий».

Use «популярный запрос» only for prompts supported by `observed` or sufficiently strong `public_proxy` evidence. Otherwise use «типовой высокоинтентный запрос». Report the evidence class, not fabricated Claude volume.

## Neutral research protocol

For generic prompts, do not add the target brand to the query. Research and answer the user's need first, then score brand presence. This reduces target-brand contamination.

Prefer source types in this order:

1. official product, pricing, policy, documentation, and support pages for product facts;
2. authoritative independent comparisons or reviews for market framing;
3. credible community discussions for user-language discovery, not definitive facts;
4. low-authority aggregators only as evidence that misinformation exists.

Verify volatile facts, including pricing, limits, models, availability, security, integrations, and legal claims, on the date of the scan.

## Scenario scoring

Record these booleans or nullable judgments:

- `brand_mentioned`: the answer names the target brand.
- `brand_recommended`: the answer affirmatively presents it as a fit for the prompt.
- `owned_citation`: at least one cited URL uses the canonical brand domain.
- `canonical_source`: the intended best first-party page is cited.
- `answer_correct`: verifiable claims are consistent with current first-party facts; `null` when not applicable.
- `answer_complete`: the answer resolves the intent without a material missing fact; `null` when not scorable.
- `competitor_substitution`: a competitor is used to answer an intent the brand plausibly serves while the target brand is absent or unsupported.
- `site_content_ready`: the brand site contains a current, discoverable page with enough direct facts and evidence to answer the prompt accurately, whether or not Claude cited it in this run; use `null` when the site cannot be assessed.
- `competitor_content_advantage`: at least one named competitor has a materially clearer, more complete, or better-evidenced page for the same intent; use `null` when competitor pages cannot be assessed.

`first_position` is one-based when the answer presents a ranked or ordered set. Use `null` for prose without a meaningful order.

## Core metrics

- Answer Presence = eligible scenarios mentioning brand / eligible scenarios.
- Recommended Brand Share = eligible scenarios recommending brand / eligible scenarios.
- First-party Citation Coverage = scenarios with owned citation / citation-eligible scenarios.
- Correct Answer Rate = correct scenarios / scenarios where correctness is scorable.
- Complete Answer Rate = complete scenarios / scenarios where completeness is scorable.
- Competitor Substitution Rate = substitution scenarios / eligible scenarios.
- Canonical Source Rate = canonical-source scenarios / citation-eligible scenarios.
- Website Answer Readiness = scenarios where `site_content_ready` is true / scenarios where site readiness is scorable.
- Competitor Content Advantage Rate = scenarios where `competitor_content_advantage` is true / scenarios where competitor content is scorable.
- Answer Gap Count = scorable scenarios where correctness or completeness is false.
- Average First Position = mean of non-null first positions.

Also calculate weighted versions using `intent_weight * commercial_priority`. Weights must be integers from 1 to 5 and must be assigned before answer research.

## Confidence

- `high`: direct first-party evidence and clear answer behavior;
- `medium`: multiple credible sources but incomplete first-party evidence;
- `low`: ambiguous response, weak sources, or unstable facts.

Low-confidence observations may remain in the appendix but must not support a strong executive conclusion without qualification.

## Recheck protocol

After a site change:

1. preserve the exact original prompt;
2. rerun it in the same target language and market context;
3. record new answer, brands, claims, and citations;
4. compare correctness, completeness, owned citation, and canonical source;
5. avoid claiming causality from one improved answer;
6. require repeated observations before calling an improvement stable.
