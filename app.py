import json
from pathlib import Path

import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

BASE = Path(__file__).parent
PROSPECTS = json.loads((BASE / "data" / "prospects.json").read_text())
SNIPPETS = json.loads((BASE / "data" / "knowledge-snippets.json").read_text())

app = Dash(__name__, external_stylesheets=["https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Space+Grotesk:wght@500&display=swap"])
app.title = "DealCast Control Surface"

app.layout = html.Div("DealCast placeholder")

if __name__ == "__main__":
    app.run(debug=True)
