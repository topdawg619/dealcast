# DealCast Agent Prompt & Orchestration Reference

This playbook codifies how the three DealCast copilots (Intel Scout, Playbook Crafter, Call Studio) should blend structured knowledge snippets with fresh LLM reasoning. All three agents share a common data contract so upstream collectors and downstream renderers stay in sync.

## Shared Data Contract

```yaml
request_id: dc-2026-02-15-001          # UUID or timestamp slug
session_context:                        # Optional high-level notes from producer
  host: "Chris"
  show_block: "Segment B"
  priority: "IPO desk"

knowledge_snippets:                    # Ordered, highest-signal first
  - id: src-01
    source: "Brave Search"
    type: "news"
    title: "CloudForge announces $250M Series D"
    excerpt: "CloudForge closed $250M Series D led by Horizon Peaks, valuing the firm at $2.3B. Funds earmarked for AI infrastructure and EMEA GTM hires."
    url: "https://example.com/story"
    freshness: "2026-02-15T16:20:00Z"
  - id: src-02
    source: "Internal CRM"
    type: "note"
    title: "Prospect pain point"
    excerpt: "CIO flagged multi-cloud cost overruns, remote workforce security gaps."
    url: null
    freshness: "2026-02-10T21:04:00Z"

llm_responses: []                      # Populated per agent with primary + alternates
aux_config:
  tone: "CNBC-meets-Operator"
  reading_time_seconds: 35
  compliance_flags: []
```

Common guardrails (baked into every template):

1. Always cite snippets inline using `[src-id]` tokens instead of URLs.
2. If a needed fact is missing, surface a gap note instead of hallucinating.
3. Keep outputs under the allocated token budget; prefer bullet hierarchies over long prose.

---

## Agent 01 — Intel Scout

**Mission**: Rapidly synthesize the freshest snippets into a scout brief the producer can drag directly into the broadcast rundown.

**Inputs**
- `session_context`
- `knowledge_snippets` (required)
- Optional `follow_up` instructions (e.g., "emphasize valuation comps")

**Outputs**
```json
{
  "headline": "GrowthCloud reopens IPO window",
  "why_now": "Series D at $2.3B signals liquidity appetite despite muted IPO tape.",
  "signal_stack": [
    {"label": "Funding", "detail": "CloudForge raises $250M Series D led by Horizon Peaks [src-01]"},
    {"label": "Pain", "detail": "CIO fighting multi-cloud cost overruns [src-02]"}
  ],
  "risk_flags": ["Valuation premium vs comps is 1.8×"],
  "gaps": ["Need confirmation on lockup expiration"]
}
```

### Prompt Template
```
<System>
You are Intel Scout, the DealCast recon analyst. Blend hard intel with tactical commentary.
Obligations:
- Only use facts present in the provided knowledge snippets.
- Surface why the signal matters for go-live decisions.
- Flag missing intel under "Gaps" instead of inventing.
- Style: sharp, newsroom-grade, <= 120 words total.
</System>

<User>
Session context:
{{session_context | default("None provided.")}}

Knowledge snippets:
{% for snippet in knowledge_snippets %}
[{{snippet.id}}] {{snippet.title}} — {{snippet.excerpt}}
Source: {{snippet.source}} • Freshness: {{snippet.freshness}}
Link: {{snippet.url | default("N/A")}}
{% endfor %}

Focus request: {{follow_up | default("None")}}

Produce JSON with keys: headline, why_now, signal_stack (array of {label, detail}), risk_flags, gaps.
</User>
```

### Pseudocode
```python
def run_intel_scout(payload):
    assert payload["knowledge_snippets"], "Intel Scout requires at least one snippet"

    prompt = render_template("intel_scout_prompt.txt", payload)

    llm_output = call_llm(
        model="openai/gpt-4o-mini",
        temperature=0.2,
        max_tokens=450,
        prompt=prompt
    )

    data = json.loads(llm_output)
    enforce_fields(data, required=["headline", "why_now", "signal_stack", "risk_flags", "gaps"])
    attach_metadata(data, agent="intel_scout", request_id=payload["request_id"])

    payload.setdefault("llm_responses", []).append({
        "agent": "intel_scout",
        "primary": data,
        "raw_prompt": prompt,
        "raw_completion": llm_output
    })

    return data
```

---

## Agent 02 — Playbook Crafter

**Mission**: Convert Intel Scout output + deeper snippets into an actionable engagement playbook (talking points, CTAs, overlays).

**Inputs**
- `session_context`
- `knowledge_snippets` (recommended ≥2)
- `intel_scout_brief` (output from Agent 01)
- Optional `audience_profile` (e.g., "CIO + CFO panel")

**Outputs**
```json
{
  "opening_angle": "Lead with liquidity momentum and AI infra spend",
  "talk_tracks": [
    {
      "title": "Funding momentum",
      "beats": [
        "Series D at $2.3B shows Horizon Peaks confidence [src-01]",
        "Tie into our hybrid-cloud accelerator offer"
      ],
      "overlay": "lt.deal_velocity"
    }
  ],
  "cta_blocks": [
    {"label": "Book desk walk-through", "microcopy": "Drop /slot IPO"}
  ],
  "producer_notes": "Have lower-third template ready; confirm lockup date once gap closes."
}
```

### Prompt Template
```
<System>
You are Playbook Crafter, DealCast's segment architect. Build a concise on-air playbook using the intel brief plus curated snippets. Respect snippet provenance and keep the flow punchy.
Rules:
- Mirror the audience's lens (boardroom, sales floor, etc.).
- Every talk track beat must cite a snippet id when referencing facts.
- Suggest overlays / kit assets where they reinforce the narrative.
- Output JSON exactly as specified.
</System>

<User>
Session context: {{session_context}}
Audience profile: {{audience_profile | default("General business viewers")}}

Intel Scout brief:
{{intel_scout_brief | to_pretty_json}}

Supporting snippets:
{% for snippet in knowledge_snippets %}
[{{snippet.id}}] {{snippet.title}} — {{snippet.excerpt}}
{% endfor %}

Deliver JSON with keys: opening_angle, talk_tracks (array of {title, beats[], overlay?}), cta_blocks (array of {label, microcopy, asset?}), producer_notes.
</User>
```

### Pseudocode
```python
def run_playbook_crafter(payload, scout_output):
    payload = payload.copy()
    payload["intel_scout_brief"] = scout_output
    prompt = render_template("playbook_crafter_prompt.txt", payload)

    llm_output = call_llm(
        model="openai/gpt-4o",
        temperature=0.35,
        max_tokens=650,
        prompt=prompt
    )

    data = json.loads(llm_output)
    validate_talk_tracks(data["talk_tracks"])

    payload.setdefault("llm_responses", []).append({
        "agent": "playbook_crafter",
        "primary": data,
        "raw_prompt": prompt,
        "raw_completion": llm_output
    })

    return data
```

---

## Agent 03 — Call Studio

**Mission**: Transform the playbook into ready-to-read host copy + cue sheet instructions for the live call, keeping cadence within the producer's timing window.

**Inputs**
- `session_context` (must include countdown, target duration)
- `knowledge_snippets`
- `playbook` (Agent 02 output)
- Optional `voice_profile` (e.g., "Anchor: Maya — fast, authoritative")

**Outputs**
```json
{
  "host_script": [
    {
      "timestamp": "T+00",
      "copy": "Maya: "CloudForge just snagged $250M from Horizon Peaks, cracking open the IPO window again." [src-01]",
      "delivery": "confident, 130wpm"
    },
    {
      "timestamp": "T+25",
      "copy": ""That cash is earmarked for AI infra build-outs — exactly where our hybrid desk goes on offense."",
      "delivery": "lean-in"
    }
  ],
  "cue_sheet": [
    {"time": "T+05", "action": "Push lower-third lt.deal_velocity"},
    {"time": "T+18", "action": "Roll b-roll package broll_energy_02"}
  ],
  "safety_checks": ["No financial advice language detected"],
  "fallback_line": "If news breaks mid-read, pivot to valuation context: 'Investors are paying 1.8× growth comp multiples.'"
}
```

### Prompt Template
```
<System>
You are Call Studio, the DealCast line producer. Convert playbooks into tight host copy + cue calls. Maintain pacing, cite snippet ids, and inject contingency lines for live pivots.
Constraints:
- Keep total script length within {{target_duration_seconds}} seconds (assume 145 wpm default).
- Tag each line with timestamp markers (T+00 etc.).
- Cue sheet actions must map to existing kit assets cited in the playbook.
- Include a "safety_checks" array noting compliance/language scans.
</System>

<User>
Session context: {{session_context}}
Voice profile: {{voice_profile | default("Neutral anchor")}}
Target duration (seconds): {{target_duration_seconds}}

Playbook JSON:
{{playbook | to_pretty_json}}

Reference snippets:
{% for snippet in knowledge_snippets %}
[{{snippet.id}}] {{snippet.title}} — {{snippet.excerpt}}
{% endfor %}

Produce JSON with keys: host_script (array of {timestamp, copy, delivery}), cue_sheet (array of {time, action}), safety_checks, fallback_line.
</User>
```

### Pseudocode
```python
def run_call_studio(payload, playbook_output):
    payload = payload.copy()
    payload["playbook"] = playbook_output
    assert payload.get("target_duration_seconds"), "Call Studio needs a timing target"

    prompt = render_template("call_studio_prompt.txt", payload)

    llm_output = call_llm(
        model="openai/gpt-4o-mini",
        temperature=0.25,
        max_tokens=700,
        prompt=prompt
    )

    data = json.loads(llm_output)
    enforce_timestamps(data["host_script"], payload["target_duration_seconds"])

    payload.setdefault("llm_responses", []).append({
        "agent": "call_studio",
        "primary": data,
        "raw_prompt": prompt,
        "raw_completion": llm_output
    })

    return data
```

---

## Hand-off Expectations

1. **Intel Scout → Playbook Crafter**: pass `headline`, `why_now`, `signal_stack`, `gaps`.
2. **Playbook Crafter → Call Studio**: pass full playbook plus resolved kit asset ids.
3. **Central logger**: after each agent run, append `llm_responses[*]` for traceability (prompt + completion) to simplify on-air audits.
4. **Gap handling**: if Intel Scout surfaces unresolved gaps, Playbook Crafter must either (a) route them to producer_notes, or (b) mark talk track as "conditional"; Call Studio should include fallback language referencing the gap.

With these templates + pseudocode in place, each DealCast surface can chain outputs reliably while staying grounded in vetted knowledge snippets.
