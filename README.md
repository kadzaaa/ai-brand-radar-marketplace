# AI Brand Radar for Codex and Claude

AI Brand Radar audits how an AI assistant answers 50 high-intent questions about a real brand and recommends concrete website content changes that can improve the brand's visibility and citability in future answers.

The plugin communicates in Russian by default. Questions used for a geographic market are written in the language of that market; the research, explanations, metrics, and recommendations remain in Russian.

## Install in Claude Code

Run these commands inside Claude Code:

```text
/plugin marketplace add kadzaaa/ai-brand-radar-marketplace
/plugin install ai-brand-radar@ai-brand-radar-claude
/reload-plugins
```

Start the skill with `/ai-brand-radar:audit-brand-answers` or ask Claude to audit a brand across 50 answer scenarios.

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
- An audit of 50 realistic user scenarios for the installed AI platform.
- A comparison with relevant competitors selected for the target market.
- Plain-text summary metrics with explanations.
- A prioritized list of page and content changes, also in plain text.
- Recommendations for titles, descriptions, FAQ blocks, page copy, and structured data.

## Important limitation

AI Brand Radar does not have access to global AI analytics, internal ranking data, or the real prompts of other users. Each platform version performs a reproducible, controlled research audit using the current assistant and public web sources. Results are a visibility proxy and may vary over time.

## Privacy and access

The repository contains separate skills for Codex/ChatGPT and Claude. Neither version connects to a private MCP server, requires API keys, or automatically publishes changes to a website.
