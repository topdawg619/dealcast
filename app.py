import json
from pathlib import Path

from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc

BASE = Path(__file__).parent
PROSPECTS_DATA = json.loads((BASE / "data" / "prospects.json").read_text())
SNIPPETS_DATA = json.loads((BASE / "data" / "knowledge-snippets.json").read_text())

SCENARIO_FILES = {
    "NovaThera Labs • Audit Push": BASE / "data" / "call-studio-sample.json",
    "Federal Pulse • Security Consolidation": BASE / "data" / "dashboard-preload-sample.json",
}
SCENARIOS = {label: json.loads(path.read_text()) for label, path in SCENARIO_FILES.items()}

PROSPECT_MAP = {p["companyName"]: p for p in PROSPECTS_DATA["prospects"]}
DEFAULT_PROSPECT = PROSPECTS_DATA["prospects"][0]["companyName"]
DEFAULT_SCENARIO = next(iter(SCENARIOS.keys()))

FONT_LINK = "https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Space+Grotesk:wght@500&display=swap"

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_LINK],
    title="DealCast Control Surface",
)

PAGE_STYLE = {
    "backgroundColor": "#05060a",
    "color": "#f5f7ff",
    "fontFamily": "Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "minHeight": "100vh",
    "padding": "32px 32px 90px",
}

CARD_STYLE = {
    "background": "#0e111a",
    "border": "1px solid rgba(255,255,255,0.05)",
    "borderRadius": "16px",
    "padding": "20px",
    "marginBottom": "20px",
}

CHIP_STYLE = {
    "display": "inline-flex",
    "alignItems": "center",
    "gap": "8px",
    "background": "rgba(255,255,255,0.04)",
    "border": "1px solid rgba(255,255,255,0.07)",
    "borderRadius": "999px",
    "padding": "8px 16px",
    "fontSize": "13px",
    "fontWeight": "600",
}


def build_stat_grid(prospect: dict) -> html.Div:
    stats = [
        ("Industry", prospect["industry"]),
        ("HQ", prospect["headquarters"]),
        ("Revenue", prospect["annualRevenue"]),
        ("Stage", prospect["growthStage"]),
    ]
    return html.Div(
        [
            html.Div(
                [html.Div(label, className="stat-label"), html.Div(value, className="stat-value")],
                className="stat-card",
            )
            for label, value in stats
        ],
        className="stat-grid",
    )


def build_list_section(items, title):
    return html.Div(
        [
            html.Div(title, className="section-title"),
            html.Ul([html.Li(item) for item in items], className="bullets"),
        ],
        style=CARD_STYLE,
    )


def build_persona_cards(personas):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(person["title"], className="persona-title"),
                    html.Div(person["name"], className="persona-name"),
                    html.P(person["personaBio"], className="persona-bio"),
                ],
                className="persona-card",
            )
            for person in personas
        ],
        className="persona-grid",
    )


def build_tech_stack_cards(stack):
    return html.Div(
        [
            html.Div(
                [html.Div(label.title(), className="tech-label"), html.Div(value, className="tech-value")],
                className="tech-card",
            )
            for label, value in stack.items()
        ],
        className="tech-grid",
    )


def build_snippet_cards(snippets):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(snippet.get("title"), className="snippet-title"),
                    html.P(snippet.get("excerpt") or snippet.get("snippet"), className="snippet-body"),
                    html.Div(snippet.get("source") or snippet.get("path"), className="snippet-source"),
                ],
                className="snippet-card",
            )
            for snippet in snippets
        ],
        className="snippet-grid",
    )


def build_signal_stack(signals):
    return html.Ul(
        [
            html.Li(
                [
                    html.Span(signal["label"], className="chip"),
                    html.Span(signal["detail"], className="signal-detail"),
                ]
            )
            for signal in signals
        ],
        className="signal-stack",
    )


def build_talk_tracks(tracks):
    cards = []
    for track in tracks:
        cards.append(
            html.Div(
                [
                    html.Div(track["title"], className="talktrack-title"),
                    html.Ul([html.Li(beat) for beat in track.get("beats", [])], className = "bullets"),
                    html.Div(f"Overlay: {track.get('overlay')}", className="overlay-tag"),
                ],
                className="talktrack-card",
            )
        )
    return html.Div(cards, className="talktrack-grid")


def build_cta_blocks(ctas):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(cta["label"], className="cta-label"),
                    html.P(cta.get("microcopy"), className="cta-copy"),
                    html.Div(cta.get("asset"), className="cta-asset"),
                ],
                className="cta-card",
            )
            for cta in ctas
        ],
        className="cta-grid",
    )


def build_host_script(script):
    rows = []
    for row in script:
        rows.append(
            html.Div(
                [
                    html.Div(row.get("timestamp"), className="script-timestamp"),
                    html.Div(row.get("copy"), className="script-copy"),
                    html.Div(row.get("delivery"), className="script-delivery"),
                ],
                className="script-row",
            )
        )
    return html.Div(rows, className="script-table")


def build_cue_sheet(cues):
    return html.Ul([html.Li(f"{cue.get('time')}: {cue.get('action')}") for cue in cues], className="bullets")


app.layout = html.Div(
    [
        html.Div(
            [
                html.Div("DealCast Control Surface", className="hero-title"),
                html.Div("Control room ready view of prospects, signals, and scripted actions.", className="hero-subtitle"),
            ],
            className="hero",
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.Div("Prospect", className="field-label"),
                            dcc.Dropdown(
                                id="prospect-select",
                                value=DEFAULT_PROSPECT,
                                options=[{"label": p, "value": p} for p in PROSPECT_MAP.keys()],
                                clearable=False,
                                className="dropdown",
                            ),
                        ],
                        style=CARD_STYLE,
                    ),
                    md=6,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Div("Scenario", className="field-label"),
                            dcc.Dropdown(
                                id="scenario-select",
                                value=DEFAULT_SCENARIO,
                                options=[{"label": label, "value": label} for label in SCENARIOS.keys()],
                                clearable=False,
                                className="dropdown",
                            ),
                        ],
                        style=CARD_STYLE,
                    ),
                    md=6,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.Div(id="company-meta", style=CARD_STYLE),
                            html.Div(id="personas", style=CARD_STYLE),
                            html.Div(id="tech-stack", style=CARD_STYLE),
                            html.Div(id="challenges", style=CARD_STYLE),
                            html.Div(id="triggers", style=CARD_STYLE),
                            html.Div(id="competition", style=CARD_STYLE),
                            html.Div(id="snippet-feed", style=CARD_STYLE),
                        ]
                    ),
                    lg=5,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Div(id="intel-brief", style=CARD_STYLE),
                            html.Div(id="playbook", style=CARD_STYLE),
                            html.Div(id="call-studio", style=CARD_STYLE),
                        ]
                    ),
                    lg=7,
                ),
            ],
            className="g-4",
        ),
    ],
    style=PAGE_STYLE,
)


@app.callback(
    Output("company-meta", "children"),
    Output("personas", "children"),
    Output("tech-stack", "children"),
    Output("challenges", "children"),
    Output("triggers", "children"),
    Output("competition", "children"),
    Output("snippet-feed", "children"),
    Output("intel-brief", "children"),
    Output("playbook", "children"),
    Output("call-studio", "children"),
    Input("prospect-select", "value"),
    Input("scenario-select", "value"),
)
def refresh_view(prospect_name, scenario_label):
    prospect = PROSPECT_MAP.get(prospect_name) or next(iter(PROSPECT_MAP.values()))
    scenario = SCENARIOS.get(scenario_label) or next(iter(SCENARIOS.values()))

    knowledge_snippets = scenario.get("knowledge_snippets") or SNIPPETS_DATA.get("documents", [])

    company_meta = html.Div([
        html.Div("Company Capsule", className="section-title"),
        build_stat_grid(prospect),
    ])

    personas = html.Div([
        html.Div("Personas", className="section-title"),
        build_persona_cards(prospect["personas"]),
    ])

    tech_stack = html.Div([
        html.Div("Tech Stack", className="section-title"),
        build_tech_stack_cards(prospect["techStack"]),
    ])

    challenges = html.Div([
        html.Div("Challenges", className="section-title"),
        html.Ul([html.Li(item) for item in prospect["challenges"]], className="bullets"),
    ])

    triggers = html.Div([
        html.Div("Buying Triggers", className="section-title"),
        html.Ul([html.Li(item) for item in prospect["buyingTriggers"]], className="bullets"),
    ])

    competition = html.Div([
        html.Div("Competitive Notes", className="section-title"),
        html.Ul([html.Li(item) for item in prospect["competitiveNotes"]], className="bullets"),
    ])

    snippet_feed = html.Div([
        html.Div("Knowledge Snippets", className="section-title"),
        build_snippet_cards(knowledge_snippets),
    ])

    intel_section = scenario.get("intel_scout_brief", {})
    intel = html.Div(
        [
            html.Div("Intel Scout", className="section-title"),
            html.Div(intel_section.get("headline"), className="intel-headline"),
            html.P(intel_section.get("why_now"), className="intel-why"),
            html.Div("Signal Stack", className="subheading"),
            build_signal_stack(intel_section.get("signal_stack", [])),
            html.Div("Risks", className="subheading"),
            html.Ul([html.Li(risk) for risk in intel_section.get("risk_flags", [])], className="bullets"),
            html.Div("Gaps", className="subheading"),
            html.Ul([html.Li(gap) for gap in intel_section.get("gaps", [])], className="bullets"),
        ]
    )

    playbook_section = scenario.get("playbook", {})
    playbook = html.Div(
        [
            html.Div("Playbook Crafter", className="section-title"),
            html.P(playbook_section.get("opening_angle"), className="intel-why"),
            html.Div("Talk Tracks", className="subheading"),
            build_talk_tracks(playbook_section.get("talk_tracks", [])),
            html.Div("CTA Blocks", className="subheading"),
            build_cta_blocks(playbook_section.get("cta_blocks", [])),
            html.Div("Producer Notes", className="subheading"),
            html.P(playbook_section.get("producer_notes")),
        ]
    )

    call_section = scenario.get("call_studio", {})
    call = html.Div(
        [
            html.Div("Call Studio", className="section-title"),
            html.Div("Host Script", className="subheading"),
            build_host_script(call_section.get("host_script", [])),
            html.Div("Cue Sheet", className="subheading"),
            build_cue_sheet(call_section.get("cue_sheet", [])),
            html.Div("Safety Checks", className="subheading"),
            html.Ul([html.Li(item) for item in call_section.get("safety_checks", [])], className="bullets"),
            html.Div("Fallback", className="subheading"),
            html.P(call_section.get("fallback_line")),
        ]
    )

    return (
        company_meta,
        personas,
        tech_stack,
        challenges,
        triggers,
        competition,
        snippet_feed,
        intel,
        playbook,
        call,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
