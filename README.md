# AI Brand Radar for Codex

AI Brand Radar audits how ChatGPT answers 50 high-intent questions about a real brand and recommends concrete website content changes that can improve the brand's visibility and citability in future ChatGPT answers.

The plugin communicates in Russian by default. Questions used for a geographic market are written in the language of that market; the research, explanations, metrics, and recommendations remain in Russian.

## Install in Codex

Add this public marketplace:

```bash
codex plugin marketplace add kadzaaa/ai-brand-radar-marketplace --ref main
```

Install the plugin:

```bash
codex plugin add ai-brand-radar@ai-brand-radar-public
```

Restart Codex if the plugin does not appear immediately. Then choose **AI Brand Radar** and start the audit.

## What the user receives

- A short onboarding flow for the brand, website, geography, language, and product category.
- An audit of 50 realistic ChatGPT user scenarios.
- A comparison with relevant competitors selected for the target market.
- Plain-text summary metrics with explanations.
- A prioritized list of page and content changes, also in plain text.
- Recommendations for titles, descriptions, FAQ blocks, page copy, and structured data.

## Important limitation

AI Brand Radar does not have access to global ChatGPT analytics, internal OpenAI ranking data, or the real prompts of other users. It performs a reproducible research audit using ChatGPT and public web sources. Results are a visibility proxy and may vary over time.

## Privacy and access

This version contains a Codex skill only. It does not connect to a private MCP server, does not require API keys, and does not automatically publish changes to a website.
