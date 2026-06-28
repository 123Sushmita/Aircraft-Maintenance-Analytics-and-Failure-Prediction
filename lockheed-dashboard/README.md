# Lockheed Aerospace Dashboard — fixed

## What was actually broken

Your charts, design, and chatbot all failed for the **same reason**: `style.css`
and `app.js` were sitting next to `index.html` instead of inside a folder
named `static/`. Flask only auto-serves files from `static/` (at the URL
`/static/...`) — anything else 404s silently.

Result: the browser got an unstyled HTML page (no charts, no layout), and
since `app.js` never loaded, `loadDashboard()` never ran and `ask()` was
undefined — so nothing on the page worked, including the chat button.

## Folder structure (this matters in Flask)

```
lockheed-dashboard/
├── app.py
├── query_map.py
├── requirements.txt
├── templates/
│   └── index.html        ← references {{ url_for('static', filename=...) }}
└── static/
    ├── style.css
    └── app.js
```

`templates/` and `static/` are Flask's two reserved folder names — keep the
file names and locations exactly as they are here.

## Setup

```bash
pip install -r requirements.txt
```

Then just run it:

```bash
python app.py
```

Visit `http://localhost:5000`.

## What changed besides the path fix

- **KPI panel** now shows MAX and MIN cost too (your SQL already computed
  them, the frontend just wasn't displaying them).
- **Chat** runs entirely on your own machine — no external API key needed.
  Every question triggers real SQL queries (KPI/KRI/maintenance/status), and
  a keyword-based rule engine picks which numbers to answer with. Covers:
  total/average/max/min cost, failure rate, high-risk jobs, maintenance type
  breakdown, status breakdown, busiest aircraft, and aircraft-specific
  questions (mention an ID like "AC-0002" and it pulls that aircraft's real
  log). Won't understand free-form phrasing as flexibly as an LLM would, but
  it works instantly with zero setup.
- Chat UI now shows a "thinking..." state, clears the input box, supports
  pressing Enter, and disables the Send button while waiting.
- History table now shows a friendly message when an aircraft has no logs,
  and the dropdown has a "select aircraft" placeholder.
- DB credentials moved to environment variables instead of being hardcoded.

## If something still doesn't render

Open your browser's DevTools → Network tab and reload. If `style.css` or
`app.js` show as 404, double check they're inside `static/` (not `public/`
or the project root) and that `templates/index.html` is the one using
`{{ url_for(...) }}`, not a copy with plain `href="style.css"`.
