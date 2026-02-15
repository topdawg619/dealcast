# DealCast Instant Kit Templates

These shells are pre-wired to accept structured outputs from the DealCast control surface (segments, tickers, inserts, AI quote packs). Swap any placeholder with the corresponding payload ID or manual edit before distribution.

---

## 1. Presentation Outline (Live or Same-Day Recap)

| Slide | Content Block | Notes / Placeholders |
| --- | --- | --- |
| 1 | **Title + Timestamp** | `{{dealcast.session.title}}` • `{{dealcast.session.datetime}}` • `{{dealcast.session.anchor}}` |
| 2 | **Open Hook / Why Now** | 2-sentence summary from `{{dealcast.broadcast.opening_hook}}` plus momentum stat from ticker `{{ticker.live.delta_pct}}`. |
| 3 | **Market Pulse Snapshot** | Use infographic snapshot `{{viz.sector_heatmap}}` or top 3 metrics from `{{instant.lower_third.metrics}}`. |
| 4 | **Deal Spotlight A** | `{{segment.A.headline}}`, key metric `{{segment.A.metric}}`, CTA `{{segment.A.cta}}`. |
| 5 | **Deal Spotlight B** | `{{segment.B.headline}}` with chart `{{segment.B.overlay_asset}}`. |
| 6 | **Expert Soundbite** | Quote from AI insert `{{ai.quote_pack.top_quote}}`, attribution `{{guest.primary.name}}`. |
| 7 | **Risks & Watchpoints** | Bulleted list from `{{producer.queue.watchpoints}}` or manual entry. |
| 8 | **Action Items / Next Steps** | Pull from `{{instant.kit.action_recs}}` or manual CTA with owner + due date. |
| 9 | **Appendix** | Reference ticker `{{ticker.stack.id}}` + link to full DealCast reel `{{assets.clip_url}}`. |

> **Presenter note field:** `{{notes.presenter}}` — automatically populated with IFB cues or producer annotations when exported.

---

## 2. Follow-Up Email (Post-Broadcast Touchpoint)

```
Subject: {{dealcast.session.short_title}} — Key takeaways & next steps

Hi {{recipient.first_name}},

Thanks for tuning into today's DealCast segment on {{dealcast.session.topic}}. Here are the highlights:

1. {{segment.A.headline}} — {{segment.A.key_stat}} (source: {{segment.A.source}})
2. {{segment.B.headline}} — {{segment.B.key_stat}}
3. {{ai.quote_pack.top_quote}} — {{guest.primary.name}}, {{guest.primary.title}}

What this means for you:
- {{analysis.implication_1}}
- {{analysis.implication_2}}

Recommended actions:
- **{{cta.one.label}}** → {{cta.one.description}} (owner: {{cta.one.owner}}, due: {{cta.one.due}})
- **{{cta.two.label}}** → {{cta.two.description}}

Resources:
- Replay: {{assets.on_demand_url}}
- Deck: {{assets.deck_url}}
- Ticker bundle: {{ticker.bundle_url}}

Let me know if you want a deeper dive or an intro to {{guest.primary.firm}}.

Best,
{{sender.name}}
{{sender.role}}
{{sender.contact}}
```

> **Automation hooks:** map `{{segment.*}}` to the broadcast feed JSON, `{{analysis.*}}` to DealCast's AI summary block, and `{{cta.*}}` to the producer desk task list.

---

## 3. Slack Digest (Executive Channel Drop)

```
:studio_microphone: *DealCast Pulse — {{dealcast.session.datetime_short}}*

• *Lead Story*: {{segment.A.headline}} _(Ticker: {{segment.A.ticker}}, Sentiment: {{segment.A.sentiment}})_
• *Secondary*: {{segment.B.headline}} + overlay {{segment.B.overlay_asset}}
• *Fast Stat*: {{instant.lower_third.stat_label}} — {{instant.lower_third.stat_value}}
• *Quote of the Day*: “{{ai.quote_pack.top_quote}}” — {{guest.primary.name}}
• *Watchlist*: {{producer.queue.watchpoints | join(', ')}}

*Next Actions*
> {{cta.one.label}} — {{cta.one.description}} _(Owner: {{cta.one.owner}}, ETA: {{cta.one.due}})_
> {{cta.two.label}} — {{cta.two.description}}

Links: Replay {{assets.on_demand_url}} • Deck {{assets.deck_url}} • Clips {{assets.clip_playlist}}
```

> **Channel tagging:** prepend `<!channel>` or `@deal-team` only when the producer toggles the "priority" flag in the Instant Kit export modal.
