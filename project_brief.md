# My agent: Content Repurposer Agent
One-liner: A conversational agent that helps marketers adapt raw content or URLs into platform-native posts (LinkedIn, X, TikTok scripts) while maintaining a strict brand persona and avoiding AI clichés.

Tool coverage:
- Memory: Remembers brand persona, tone of voice, target audience, and "banned words" (anti-slop prose rules) across sessions.
- Tools: A tool to fetch/scrape raw content from a given URL or text input.
- Catalog/UI: A draft queue or content catalog where generated posts (LinkedIn, X, Scripts) are displayed as visually rich UI cards.
- Image gen: Generates accompanying visual mockups or thumbnails for the repurposed social media posts.
- Sandbox: Evaluates "hook scores" or calculates engagement metrics using Python scripts.

Recommended for every project: memory, storage, tools, image generation, A2UI
Agent-specific / stretch (pick what fits): Code sandbox for calculating viral hook scores, external API integration for actual web scraping (e.g., using crawl4ai or similar).
