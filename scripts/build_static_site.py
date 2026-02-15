from __future__ import annotations

import json
from pathlib import Path
from string import Template
import textwrap


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DIST_DIR = BASE_DIR / "dist"


def load_data() -> tuple[list[dict], list[dict]]:
    prospects = json.loads((DATA_DIR / "prospects.json").read_text())['prospects']
    snippets = json.loads((DATA_DIR / "knowledge-snippets.json").read_text())['documents']
    return prospects, snippets


def build_snippet_cards(snippets: list[dict]) -> str:
    cards = []
    for snippet in snippets:
        cards.append(
            f"""
        <div class=\"snippet-card\">
          <div class=\"snippet-title\">{snippet['title']}</div>
          <p class=\"snippet-body\">{snippet['snippet']}</p>
          <div class=\"snippet-footnote\">{snippet['path']}</div>
        </div>
        """.strip()
        )
    return "\n".join(cards)


def build_options(prospects: list[dict]) -> str:
    return "\n".join(
        f"<option value=\"{prospect['companyName']}\">{prospect['companyName']}</option>"
        for prospect in prospects
    )


def build_css() -> str:
    return textwrap.dedent(
        """
        body {background:#05060a;margin:0;font-family:'Inter', sans-serif;color:#e8e9ee;}
        .app-shell {min-height:100vh;padding:32px 48px;box-sizing:border-box;background:radial-gradient(circle at top,#10121c,#05060a 60%);} 
        .hero {display:flex;justify-content:space-between;align-items:flex-end;gap:24px;margin-bottom:32px;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:24px;}
        .hero-title {font-family:'Space Grotesk', sans-serif;font-size:48px;margin:4px 0;color:#f8f9ff;}
        .eyebrow {text-transform:uppercase;letter-spacing:0.3em;font-size:12px;color:#a3a7d1;}
        .hero-copy {color:#cfd2ff;font-size:16px;max-width:520px;}
        .selector label {display:block;margin-bottom:8px;color:#9ba1c5;font-size:13px;text-transform:uppercase;letter-spacing:0.14em;}
        #prospect-select {color:#05060a;}
        .layout-grid {display:flex;gap:24px;}
        .column {flex:1;display:flex;flex-direction:column;gap:20px;}
        .left {flex:0.9;}
        .right {flex:1.1;}
        .stat-grid {display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;}
        .stat-card {padding:18px;border:1px solid rgba(255,255,255,0.08);border-radius:16px;background:rgba(255,255,255,0.02);} 
        .stat-label {font-size:12px;text-transform:uppercase;letter-spacing:0.16em;color:#8f93b8;margin-bottom:6px;}
        .stat-value {font-size:20px;font-weight:600;color:#f8f9ff;}
        .section-card {padding:22px;border:1px solid rgba(255,255,255,0.08);border-radius:20px;background:rgba(11,13,23,0.9);box-shadow:0 10px 30px rgba(3,4,8,0.6);}
        .section-title {font-size:15px;text-transform:uppercase;letter-spacing:0.2em;color:#7e85b5;margin-bottom:16px;}
        .bullet-list {padding-left:20px;margin:0;display:flex;flex-direction:column;gap:8px;color:#e4e6ff;}
        .bullet-list li {line-height:1.4;}
        .tech-grid {display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;}
        .tech-card {padding:16px;border-radius:14px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.04);} 
        .tech-label {font-size:13px;font-weight:500;color:#b2b7e4;margin-bottom:8px;}
        .tech-value {font-size:15px;color:#f7f8ff;line-height:1.4;}
        .persona-grid {display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;}
        .persona-card {padding:18px;border-radius:18px;background:rgba(23,25,45,0.9);border:1px solid rgba(255,255,255,0.05);} 
        .persona-name {font-size:18px;font-weight:600;color:#fff;margin-bottom:4px;}
        .persona-title {font-size:14px;color:#9ba1c5;margin-bottom:10px;}
        .persona-bio {margin:0;color:#d8dbff;line-height:1.5;font-size:14px;}
        .chip-row {display:flex;flex-wrap:wrap;gap:8px;}
        .chip {padding:6px 12px;border-radius:999px;background:rgba(126,133,181,0.18);font-size:13px;color:#c5c8f2;border:1px solid rgba(197,200,242,0.3);}
        .snippet-grid {display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;}
        .snippet-card {padding:16px;border-radius:14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);}
        .snippet-title {font-size:15px;font-weight:600;margin-bottom:8px;color:#fdfdff;}
        .snippet-body {margin:0;color:#d5d8ff;font-size:14px;line-height:1.5;min-height:72px;}
        .snippet-footnote {margin-top:12px;font-size:12px;color:#8a8fb4;}
        @media(max-width:1024px){.hero{flex-direction:column;align-items:flex-start;}.layout-grid{flex-direction:column;}}
        """
    ).strip()


def build_html(prospects: list[dict], snippets: list[dict]) -> str:
    template = Template(
        """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>DealCast Control Surface</title>
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />
  <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500&display=swap\" rel=\"stylesheet\" />
  <style>$css</style>
</head>
<body>
  <div class=\"app-shell\">
    <div class=\"hero\">
      <div>
        <div class=\"eyebrow\">DealCast</div>
        <h1 class=\"hero-title\">Control Surface</h1>
        <p class=\"hero-copy\">Wire prospects, knowledge snippets, and personas into one glance for live show prep.</p>
      </div>
      <div class=\"selector\">
        <label for=\"prospect-select\">Prospect Roster</label>
        <select id=\"prospect-select\">
          $options
        </select>
      </div>
    </div>
    <div class=\"layout-grid\">
      <div class=\"column left\">
        <div id=\"company-meta\"></div>
        <div id=\"tech-stack\"></div>
        <div id=\"personas\"></div>
      </div>
      <div class=\"column right\">
        <div id=\"challenges\"></div>
        <div id=\"buying-triggers\"></div>
        <div id=\"competitive-notes\"></div>
        <div class=\"section-card\">
          <div class=\"section-title\">Knowledge Signals</div>
          <div class=\"snippet-grid\">
            $snippets
          </div>
        </div>
      </div>
    </div>
  </div>
  <script>
    const PROSPECTS = $prospects_json;
    const PROSPECT_LOOKUP = Object.fromEntries(PROSPECTS.map(p => [p.companyName, p]));

    function buildStat(label, value) {
      return '<div class="stat-card">\n        <div class="stat-label">' + label + '</div>\n        <div class="stat-value">' + value + '</div>\n      </div>';
    }
    function buildListSection(title, items) {
      const itemsMarkup = items.map(item => '<li>' + item + '</li>').join('');
      return '<div class="section-card">\n        <div class="section-title">' + title + '</div>\n        <ul class="bullet-list">' + itemsMarkup + '</ul>\n      </div>';
    }
    function buildTechStack(tech) {
      const cards = Object.entries(tech).map(([lane, value]) => {
        const label = lane.charAt(0).toUpperCase() + lane.slice(1);
        return '<div class="tech-card">\n          <div class="tech-label">' + label + '</div>\n          <div class="tech-value">' + value + '</div>\n        </div>';
      }).join('');
      return '<div class="section-card">\n        <div class="section-title">Tech Stack Lanes</div>\n        <div class="tech-grid">' + cards + '</div>\n      </div>';
    }
    function buildPersonas(personas) {
      const cards = personas.map(persona => {
        return '<div class="persona-card">\n          <div class="persona-name">' + persona.name + '</div>\n          <div class="persona-title">' + persona.title + '</div>\n          <p class="persona-bio">' + persona.personaBio + '</p>\n        </div>';
      }).join('');
      return '<div class="section-card">\n        <div class="section-title">Personas</div>\n        <div class="persona-grid">' + cards + '</div>\n      </div>';
    }

    function hydrate(companyName) {
      const prospect = PROSPECT_LOOKUP[companyName];
      const meta = [
        ['Industry', prospect.industry],
        ['HQ', prospect.headquarters],
        ['Revenue', prospect.annualRevenue],
        ['Stage', prospect.growthStage]
      ].map(([label, value]) => buildStat(label, value)).join('');
      document.getElementById('company-meta').innerHTML = '<div class="stat-grid">' + meta + '</div>';
      document.getElementById('tech-stack').innerHTML = buildTechStack(prospect.techStack);
      document.getElementById('personas').innerHTML = buildPersonas(prospect.personas);
      document.getElementById('challenges').innerHTML = buildListSection('Challenges in Play', prospect.challenges);
      document.getElementById('buying-triggers').innerHTML = buildListSection('Buying Triggers', prospect.buyingTriggers);
      document.getElementById('competitive-notes').innerHTML = buildListSection('Competitive Notes', prospect.competitiveNotes);
    }

    const selector = document.getElementById('prospect-select');
    selector.addEventListener('change', (event) => hydrate(event.target.value));
    hydrate(selector.value || PROSPECTS[0].companyName);
  </script>
</body>
</html>
        """
    )

    snippets_html = build_snippet_cards(snippets)
    options_html = build_options(prospects)
    css = build_css()

    return template.substitute(
        css=css,
        options=options_html,
        snippets=snippets_html,
        prospects_json=json.dumps(prospects, ensure_ascii=False)
    )


def main() -> None:
    prospects, snippets = load_data()
    html = build_html(prospects, snippets)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "index.html").write_text(html)
    print(f"Wrote {DIST_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
