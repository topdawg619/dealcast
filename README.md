# DealCast Control Surface

Dash-powered dashboard that fuses the prospect roster, personas, and
knowledge snippets the DealCast crew uses before each show. The app can
run as a standard Dash server for rapid iteration, and we also ship a
static, JavaScript-only build so it can live on Pages.

## Run the Dash app locally

1. **Install dependencies** (one-time):
   ```bash
   cd projects/dealcast
   python3 -m venv .venv            # optional but recommended
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Start the dev server**:
   ```bash
   python app.py
   ```
3. Visit <http://127.0.0.1:8050> and use the dropdown to cycle through
   prospects. Dash reloads automatically whenever you change `app.py` or
the JSON data under `data/`.

## Deploying to Pages (static build)

Pages expects a static bundle, so we flatten the Dash layout into pure
HTML/CSS/JS driven by the JSON sources. The helper script writes that
bundle to `dist/` (git-ignored) and mirrors all of the styling from the
live app.

1. Build the static snapshot:
   ```bash
   cd projects/dealcast
   python scripts/export_static.py
   ```
   The script reads `data/prospects.json` and
   `data/knowledge-snippets.json`, then writes `dist/index.html` with the
   full layout plus inline JavaScript to hydrate the dropdown.
2. **Publish to Pages** using whichever workflow you prefer:
   - **Manual:** copy the contents of `dist/` into the branch that Pages
     serves (for example `docs/` on `main`), commit, and push. In the
     repo settings, point Pages to that branch/path.
   - **GitHub Actions:** set the Pages workflow’s build command to
     `python scripts/export_static.py` and upload
     `projects/dealcast/dist` as the artifact.
3. Once the Pages deploy turns green, refresh
   `https://<user>.github.io/<repo>/projects/dealcast/` (or your custom
   domain). The dropdown and persona panes will work client-side with no
   backend.

> Tip: regenerate the static bundle whenever the JSON data changes so the
> Pages build stays in sync with the latest prospects/snippets.
