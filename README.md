# alacrime.com — public website (Baldwin County, Alabama)

Static site built from one JSON file per day. The daily Claude scheduled task does the research and drops
`edition-YYYY-MM-DD.json` into the public Google Drive folder "alacrime feed".
Every 10 minutes, the "Pull new editions from Google Drive" GitHub Action copies any new
file into `data/editions/`, rebuilds the site and deploys it to GitHub Pages.
Any push to main also rebuilds.

```
data/editions/2026-09-27.json   one file per day (the record)
data/corrections.json           append-only corrections log
build.py                        generator, no dependencies  ->  public/
static/                         CSS + JS
scripts/import_drive.py         pulls new editions from the Drive folder
.github/workflows/deploy.yml    build + deploy on push
.github/workflows/sync-from-drive.yml   hourly Drive pull -> commit -> deploy
CNAME                           your domain (create when you have one)
```

## Pages generated
Home (latest edition) · `/editions/YYYY-MM-DD/` for every day · Archive · Open cases ·
Search (client-side, all editions) · Corrections · About · RSS `/feed.xml` · sitemap.

## One-time setup
1. Upload these files to the GitHub repo planetsurplus/alacrime (include the hidden `.github` folder).
2. Repo → Settings → Pages → Source: **GitHub Actions**; Custom domain: `www.alacrime.com`; Enforce HTTPS.
3. DNS at the registrar: A records for @ → 185.199.108.153 / .109.153 / .110.153 / .111.153; CNAME www → planetsurplus.github.io.
4. Google Drive: folder **alacrime feed** → Share → General access: **Anyone with the link — Viewer**.
5. Repo → Actions → "Pull new editions from Google Drive" → **Run workflow** once to test.

## Edition JSON format
```jsonc
{
  "date": "2026-09-28",              // must match file name
  "compiled": "2026-10-26T15:40:00-05:00",  // Central time
  "window": "Sep. 26–28, 2026",
  "summary": "One or two plain sentences on the day's main items.",
  "commentary": null,                // or {"title": "...", "body": ["para", "para"]} -> side column
  "entries": [{
    "id": "short-slug",              // unique within the edition
    "date": "2026-09-27",            // incident / filing date
    "time": "20:10",                 // optional
    "place": "Fairhope",
    "agency": "Fairhope Police",
    "category": "violent | property | dui | drug | court | other",
    "severity": "felony | misdemeanor | other",
    "cases": ["Bkg #254993"],
    "title": "Plain factual headline",
    "body": ["Paragraph.", "Paragraph."],
    "tags": [],                      // optional extra chips
    "sources": [{"label": "BCSO jail roster", "url": "https://..."}]
  }],
  "filings": {"window": "Oct. 19–25",                    // JAIL BOOKINGS (not court filings)
              "courts": [{"court": "Baldwin County Sheriff", "count": 93}],   // by arresting agency, last week
              "new": [{"case": "Bkg #254993", "defendant": "Name, 44", "agency": "Fairhope PD",
                       "date": "2026-10-26", "arrest": "10/26/2026 02:04", "charges": "...", "released": false}],
                                                          // every non-immigration booking, ~8 days; feeds the Charge-O-Meter
              "new_list": [ ...same shape... ],           // the bookings shown on the page (last 72 h)
              "list_note": "..."},
  "city_arrests": [{"agency": "Daphne Police", "window": "Oct. 19–26",
                    "rows": [{"name": "...", "when": "10/25 06:10", "offense": "...", "where": "block-level location"}]}],
  "open_cases": [{"case": "...", "defendant": "...", "level": "Class B felony", "charges": "...",
                  "next": "...", "agency": "...", "last_docket": "2026-10-26"}],
  "sources": [{"name": "...", "url": "...", "status": "read | stale | not reached | not working | paid", "note": "..."}]
}
```

## Public-site rules (straight tone)
- Plain factual language. No jokes or opinion in entries — opinion goes only in `commentary`.
- No dates of birth, no race. No victim names. DV/sex/child entries: only what an official record states.
- Immigration detainers are counted, never listed by name.
- Never publish Baldwin content to dickwheel.com / fairbankscrime.com, or Fairbanks content here.
- Everyone is "arrested" or "charged", never implied guilty.
- Corrections are appended to `corrections.json`, never deleted.

## Local preview
`python3 build.py && python3 -m http.server -d public 8000` → http://localhost:8000
