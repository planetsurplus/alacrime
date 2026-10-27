---
name: "baldwin-blotter"
description: "Run the daily Baldwin County, Alabama crime report for www.alacrime.com: read the primary Baldwin records directly (jail roster, city arrest logs, federal, state and DA releases), verify every date, upload the edition JSON to the alacrime feed Drive folder, and update the working artifact in place."
---

# Baldwin County Crime Record

A daily crime scan for Baldwin County, Alabama — Bay Minette to Orange Beach, Spanish Fort to Elberta — built from primary records rather than news coverage. Sister project to the Fairbanks Crime Record; same discipline, different county, and one big structural difference: **Alabama has no free court charge file.** Read "The court gap" below before anything else.

> DRAFT — written 2026-10-26 from a source survey. Items marked **[verify on first run]** were not confirmed end to end and must be checked, then this note removed.

## The artifact — read this first, every run

**Working page (private artifact): `https://claude.ai/artifact/W8WbHvM7rG2wZ5EzgmgtAQ` — "Baldwin County Crime Record"** (first edition Oct. 26, 2026).

**Always publish with `url` set to it. Never publish without it. Never create a new artifact.** A new URL is a fork, not an edition; the reader loses the history. (Fairbanks lost a full day this way on Sep. 24.)

## The public website — www.alacrime.com

The public site is **www.alacrime.com**, built by GitHub Pages from the repo **planetsurplus/alacrime** (local copy of the builder and README there). **Never publish Baldwin content to dickwheel.com or fairbankscrime.com,** never copy Baldwin items into the Fairbanks Drive feed, and never put Fairbanks items here.

**How an edition reaches the site:** write one JSON file per day, named `edition-YYYY-MM-DD.json` (a re-run the same day is `edition-YYYY-MM-DD-r2.json`; the highest rN wins), and upload it to the public Google Drive folder **"alacrime feed"** (folder ID `1YNOJzRqyTrgPNJewOEwBwIe2IyJzT0Co`). Upload with `create_file`: `parentId` = that folder, `contentMimeType` `application/json`, `disableConversionToGoogleType` true, the minified JSON as `textContent`. A GitHub Action checks the folder every 10 minutes, commits the file to `data/editions/`, rebuilds and deploys. Check the site about 15 minutes later; if the edition is not there, look at the repo's Actions tab for a red run.

**The JSON format is in the repo README** (`https://github.com/planetsurplus/alacrime`) — read it every run rather than from memory. The essentials:
- `date` must match the file name; `compiled` as ISO with offset (`2026-10-27T05:40:00-05:00`, `-06:00` in winter); `window` like "Oct. 26–27, 2026"; `summary` one or two plain sentences.
- `entries[]`: `id`, `date`, `time`, `place`, `agency`, `category` (violent | property | dui | drug | court | other), `severity` (`felony` only when an official source states it, else `other`), `cases` (booking or case numbers), `title` in "Category: Name" form, `body[]`, `tags[]` (Domestic, Sentenced, Pleaded guilty), `sources[]` with real URLs.
- `filings` holds **jail bookings**, not court filings: `courts[]` = bookings by arresting agency for the last Mon–Sun week; `new[]` = every non-immigration booking for about the last 8 days, each with `case` ("Bkg #254993"), `defendant` ("Name, 44"), `agency`, `date` (booking date, ISO), `arrest`, `charges`, `released` — this feeds the Charge-O-Meter, so keep it complete; `new_list[]` = the bookings shown on the page (last 72 hours); `list_note`.
- `city_arrests[]`: one block per city log (Daphne, Fairhope) with `rows[]` of `name`, `when`, `offense`, `where`.
- `open_cases[]`: `case`, `defendant`, `level`, `charges`, `next`, `agency`, `last_docket` (ISO date of last check).
- `sources[]`: `name`, `url`, `status` (read | stale | not reached | not working | paid), `note` with the count seen.
- Corrections: add a `corrections` list to the edition file (`[{"date": "...", "edition": "YYYY-MM-DD", "text": "..."}]`); the importer appends them to the site's permanent log.

Validate the JSON (it must parse, ids unique, every entry has title/date/body) before uploading. A malformed file turns the sync run red and the day never appears.

**Never publish to the site:** dates of birth, race, booking photos, victims' names, immigration-detainee names, juveniles' names. The public site uses the straight news voice described below.

The cloud workspace is wiped between runs. Recover the page with `Artifact` action `read` on the canonical URL, copy the saved file to `/home/claude/baldwin-crime-record.html`, and **Read every line** before republishing — a republish is refused otherwise.

## Before anything else

Run `TZ=America/Chicago date`. Baldwin County is on **Central time**; the user is in Fairbanks (Alaska time, three hours behind). Every date on the page is a Central date. Never trust a remembered date.

## Daily run, in order

1. `TZ=America/Chicago date`. Load the Claude in Chrome tools in one ToolSearch call.
2. Read every source below, in the order of the Summary table. Record the count seen for each.
3. Re-read the two preceding days on the roster and the city logs.
4. Write the edition JSON (format above), check it parses, and upload it to the "alacrime feed" Drive folder.
5. Update the working artifact with the same edition.
6. About 15 minutes later, load www.alacrime.com and confirm the new date is on the home page.

If Chrome is not connected, follow "When the browser is down" and still publish what the cloud can reach, with every browser source marked *Not reached*. A scheduled run has nobody to ask: never spend money on Alacourt, never publish anything the handling rules forbid, and leave anything uncertain out with a note in the sources table.

## The voice

Follow **fairbankscrime.com** (format adopted 2026-10-26): terse, neutral news-brief writing throughout, heavy on attribution and the accusation-not-conviction framing. The wry edge lives only in the brand tagline ("Allegedly, these crimes occurred, but maybe not.") and in the Commentary panel, which stays "Commentary column coming soon." until the user says otherwise. No commentator voice in entries, section headings, tables, notes or the footer.

## The rule that matters most

**A run that reports a day without having seen a result count has read nothing, not zero.** The jail roster's "Last 24 Hour Admits" must show its record count, or the day is *not read*. No day is ever "closed": a zero read means nothing was posted at the time of reading. Re-read the two preceding days every run.

Every date gets verified against its source before it goes on the page. The roster carries old bookings (people held since July sit beside last night's admits) — **the booking date and arrest date on each record are the only dates that count**, never position on the page.

## The court gap — why this county is different

Fairbanks reads charges from the court's own free PDFs. **Baldwin cannot.** Alabama's statewide case system, Alacourt, charges per search (see Sources). So in this county:

- **The jail roster is the charge record**, and it is **arrest-grade**: it lists what the arresting agency booked, not what the District Attorney filed or a grand jury indicted. Write "booked on" / "charged by [agency] with", never "indicted" and never a felony class unless an official source states it.
- **Court-grade facts come only from** U.S. Attorney releases, Alabama Attorney General releases, District Attorney statements quoted in news, or a paid Alacourt look-up the user has approved.
- **Never spend money on Alacourt.** Paid look-ups are the user's decision, case by case. Add it to Open cases with the note "worth a paid court look-up" and stop there.

## The coverage area

All of Baldwin County, Alabama. **In:** Bay Minette, Daphne, Spanish Fort, Fairhope, Loxley, Robertsdale, Silverhill, Summerdale, Foley, Elberta, Magnolia Springs, Gulf Shores, Orange Beach, Perdido Beach, Lillian, Stapleton, Stockton, Belforest, Point Clear, Seminole, plus I-10 and I-65 within the county. **Out:** Mobile County (Mobile, Saraland, Theodore, Prichard), Escambia County AL and FL (Pensacola, Atmore, Brewton). Mobile TV stations cover all of these; filter every newsroom item by place.

**Arresting agencies on the jail roster that are inside the county** (agency name and ORI as the roster prints them):

| Agency | ORI |
|---|---|
| Baldwin Co SO | `AL0050000` |
| Bay Minette PD | `AL0050100` |
| Fairhope PD | `AL0050200` |
| Foley PD | `AL0050300` |
| Gulf Shores PD | `AL0050400` |
| Robertsdale PD | `AL0050500` |
| Loxley PD | `AL0050600` |
| Silverhill PD | `AL0050700` |
| Daphne PD | `AL0050800` |
| Summerdale PD | `AL0050900` |
| Elberta PD | `AL0051000` |
| Orange Beach PD | `AL0051200` |
| Spanish Fort PD | `AL0051300` |

Also on the roster: State Troopers (`ALAST0200`), ABI, DPS, Pardons & Parole, U.S. Marshals, FBI, DEA, ICE, and out-of-county sheriffs (Mobile, Escambia AL/FL, Monroe, Washington, etc.) whose prisoners are held in Bay Minette. An out-of-county agency's arrest is in scope only if the record or another source places the offence in Baldwin.

**Spring break (March–April) and big events** (Hangout Fest, July 4) swamp Gulf Shores and Orange Beach with minor-in-possession and public-intoxication bookings. Summarise those in aggregate; do not list each name.

## Sources, and how each one has to be read

Access tier for each, as tested 2026-10-26. **Cloud** = readable from the workspace with WebFetch. **Browser** = needs Claude in Chrome. **Paid** = paywalled. The workspace shell (curl) reaches **none** of these hosts — every request is refused by the network allowlist.

### Summary

| Source | Tier | What it gives |
|---|---|---|
| BCSO jail roster (Southern Software Citizen Connect) | **Browser** | Every booking at the county jail: name, booking/arrest date, arresting agency, booked charges |
| Daphne PD Citizen Connect (`AgencyID=DaphnePDAL`) | **Browser** | City arrests with offence and block location; daily report; city jail bookings; active calls |
| Fairhope PD Citizen Connect (`AgencyID=FairhopePDAL`) | **Browser** | City arrests with offence and block location |
| Baldwin County DA Facebook | **Browser** | Verdicts and sentences — the only free court-grade local source |
| U.S. Attorney, S.D. Alabama | **Browser** (WebFetch refuses justice.gov) | Federal charges, pleas, sentences |
| Alabama Attorney General news | Cloud-readable via search hits; index **[verify]** | State prosecutions, convictions |
| ALEA press releases | **Browser** — cloud copy is stale | Fatal crashes, SBI officer-involved shootings |
| BCSO Facebook + municipal PD Facebook pages | **Browser** (user is signed in) | Real-time incidents, wanted, death investigations |
| Alacourt docket list (Baldwin, LOC=05) | **Browser**, free — **not working** | Returned the blank form on 2026-10-26 |
| Alacourt case search | **Paid** — $9.99/search | Filed charges, dispositions |
| Baldwin DA "Latest News" | Cloud, free — **dead** (newest item ~2019) | Nothing current |
| FOX10 Baldwin section | Browser (fetch within page works) | Best newsroom for Baldwin crime narrative |
| WKRG | **Browser** — WebFetch fails on wkrg.com | Narrative, follow-ups |
| NBC15/WPMI, 1819 News | Cloud via search, free | Narrative, date-checks |
| Gulf Coast Media (local weeklies) | Browser; **subscription site** | Local narrative; some items metered |
| AL.com | Metered paywall **[verify]** | Narrative |
| PulsePoint | **[verify]** — no Baldwin agency confirmed | Fire/EMS only, if present |

### BCSO jail roster — `cc.southernsoftware.com/bookingsearch/index.php?AgencyID=BaldwinCoSOAL`
**The backbone of this page.** Linked from the sheriff's "Arrest Search" page (`sheriff.baldwincountyal.gov/home/arrest-search`). The Baldwin County Corrections Center in Bay Minette holds arrestees for **every** agency in the county, so this one roster covers BCSO, all 12 municipal PDs, troopers and federal holds.

Browser only — the workspace cannot reach the host and WebFetch refuses the URL. Searches are POST forms on the page (`searchtype=daterange`, `JMSAgencyID=AL0050000`); there is no GET URL for a result list, so click the buttons:

- **Get Last 24 Hour Admits** — the daily read. Record the count shown.
- **Get Last 7 Days Admits** — the backfill read, every run.
- **Admits by Date Range** / **Releases by Date Range** — for a specific past day (`begindate` / `enddate`, MM/DD/YYYY).
- **Arresting Agency** dropdown — to check one department's arrests.
- **Current Confinements** — the whole jail (~540 on 2026-10-26); not a daily feed, do not read it as one.

Each record shows name, age / race / sex, **date of birth**, booking date, arresting agency, arrest date/time, and numbered booked charges, with "View Full Details" (which adds nothing beyond the list). Charge wording is the jail's NIBRS-style text ("Simple Assault-Family", "Dangerous Drugs-…"), not the Code of Alabama — translate it plainly, do not invent a statute.

**How to read it (learned 2026-10-26):**
- Click the button with `setTimeout(()=>button.click(),50)` and read the page in the next call; the click navigates. A `fetch` POST of the same form returns an empty shell.
- Results page 20 at a time with client-side «/» links ("Showing page 1 of 9 (1 - 20 of 166 inmates)"). Click » in a loop, parse each page, and de-duplicate by booking number. Return results in chunks of about 30 rows — longer tool outputs are truncated.
- Released prisoners **do** stay in the date-range lists, marked "Released".
- Records can be incomplete: on Oct. 26 two bookings showed no agency and no charges. List them as "Not listed on roster", never guess.
- **The arresting-agency field can be wrong.** Greenly Marie Culbreth was booked under "BALDWIN CO SO" but Fairhope's own log shows a Fairhope arrest at the same minute. Cross-check city arrests against the city logs before naming the agency in an entry.
- Arrest dates can fall after the booking date (Fouad Magdy Marcos: booked Oct. 24, arrest stamp Oct. 26), usually a new charge added in custody. Report both dates as printed.
- "19 hours ago" stamps are relative to the server clock and disagree with the admit date. Use the dates, not the relative stamps.
- Immigration detainers (agency ICE) run 25–30 a week. They are not crimes: count them, never list names.
- City police in Daphne, Fairhope and Foley run their own jails, so most of their arrests never reach this roster. The weekly count says so.

The "Alerts Archive" page on the same portal was empty on 2026-10-26.

### City arrest logs — Daphne and Fairhope (Southern Software Citizen Connect)
`cc.southernsoftware.com/arrestsearch/index.php?AgencyID=DaphnePDAL` and `…AgencyID=FairhopePDAL`. Browser only. Set `begindate` / `enddate` (MM/DD/YYYY) with the native value setter, click Submit, read the next call. Each row gives case number, name, date/time, offence and a block-level location (house numbers and some road numbers are masked as "XX"). No ages on Fairhope's log.
- Daphne also has a **Daily Report** (`/dayreport_incident/`) with incidents, arrests and city-jail bookings by day — but its offence fields are blank, so use the arrest search for charges. It also offers Incident Search, Accident Search, Active Calls and Press Releases.
- These logs lag: Fairhope's had not posted an Oct. 26 2:04 a.m. arrest by mid-afternoon. And they are not complete: a Daphne aggravated-assault arrest on the county roster (Oct. 20) never appeared in Daphne's log.
- Foley, Gulf Shores, Orange Beach, Spanish Fort, Bay Minette, Robertsdale, Loxley, Summerdale, Elberta and Silverhill have **no** Citizen Connect portal (their AgencyIDs return the national directory). Foley PD redirects to the directory too.
- Misdemeanour city arrests go in the City arrests tables, not in entries.

### U.S. Attorney, Southern District of Alabama — `justice.gov/usao-sdal/pr`
Covers Baldwin (Mobile division). About 80–120 releases a year, a minority of them Baldwin. **Read it in the browser** — WebFetch refuses justice.gov URLs in this session. From the index page, `fetch('/usao-sdal/pr/<slug>')` reads each release's text. **Read the index teaser as well as the release:** the Oct. 6 Wooten release body never gives his full name or sentence; only the teaser on the index does. Transcribe every row in a rolling 30-day window and filter by Baldwin place names (Foley, Loxley, Daphne, "Baldwin County", etc.).

### Alabama Law Enforcement Agency — `alea.gov/press-releases`
Troopers work fatal crashes on I-10, I-65, US 98, AL 59 and county roads; the SBI investigates officer-involved shootings and in-custody deaths. **The cloud copy is stale** — on 2026-10-26 WebFetch returned a page whose newest release was July 2025. Read it in the browser. Individual releases sit at `alea.gov/news/<slug>`. Fatal-crash releases are not crimes unless a charge is stated; list them in a separate traffic-deaths block, plainly.

### Alabama Attorney General — `alabamaag.gov/news`
State-level prosecutions and convictions, occasionally Baldwin. Older releases appear in search results and are readable; read the index in the browser **[verify current index path]**.

### Facebook — BCSO and municipal departments
`facebook.com/SheriffOfBaldwin` loads fully in the user's Chrome, which is signed in to Facebook. Formal releases are headed "FOR IMMEDIATE RELEASE" in decorative Unicode letters — normalise text with `.normalize('NFKC')` before matching, and click each post's "See more" before reading. On 2026-10-26 the page carried two crime releases in a week among recruiting and community posts.

**`facebook.com/baldwincountydaoffice` — Baldwin County District Attorney.** Posts jury verdicts and sentences with defendant, charge, judge and prosecutors (Sept. 25 capital murder verdict; Aug. 20 murder verdict with a sentencing date). This is the only free court-grade local source; read it every run.

Daphne PD `facebook.com/DaphnePoliceDept` — community posts only the week of Oct. 19; it does share DA verdicts. Foley, Fairhope, Gulf Shores, Orange Beach, Spanish Fort, Bay Minette and Robertsdale PD pages **[still to be located]**. Arrest-report grade only. Date-check against the post timestamp — pinned posts sit at the top for months. If a login wall appears, mark *not reached*, not *read, nothing*.

City websites are not a substitute: Daphne's "Police News" on `daphneal.com` is grants, awards and retirements.

### Alacourt — `pa.alacourt.com`
- **Docket list, free:** `pa.alacourt.com/frmDocketListsearch.aspx?LOC=05` (Baldwin is county `05`; the DA's site links it as "Daily Dockets"). Pick a setting date (today plus four days are offered) and optionally a last name; blank returns the whole docket. **Not working as of 2026-10-26:** a search with and without a last name returned the blank form both times. Retry each run; if it returns rows, record what they show here.
- **Case search, paid:** name or case-number search **$9.99** each, including one case detail; each further detail $9.99; document images $5.00 for the first 20 pages then $0.50/page; v2.alacourt.com is a subscription. (Prices as published by Alacourt and reported second-hand; **[verify on the portal's own pricing page]**.) **Never search here without the user's explicit approval for that case.**

### Baldwin County District Attorney — `baldwincountyal.gov/government/district-attorney/latest-news`
Free and cloud-readable, and effectively **dead**: the newest item is an Attorney General op-ed from around 2019. The DA posts on Facebook instead (see above).

### Newsrooms
FOX10/WALA (`fox10tv.com/news/baldwin-county/` — read the index in the browser, then `fetch` each article path from that page; article URLs carry the date as `/2026/MM/DD/`), WKRG (`wkrg.com/baldwin-county/` — browser only, WebFetch fails; article bodies need a full page load), its mirror `digital-release.wkrg.com`, NBC15/WPMI (`mynbc15.com`, mirrored at `weartv.com`), 1819 News (`1819news.com/tag/baldwin-county`), Gulf Coast Media (`gulfcoastmedia.com` — Baldwin's local weeklies; subscription prompts and a cookie banner, choose *Reject non-essential*), AL.com (metered). All are Mobile/Pensacola market outlets: **filter every item by place**, most of their crime is Mobile or Escambia. Use them for narrative and date-checks, and to catch what the roster hides (death investigations, unnamed juveniles, officer-involved shootings).

### PulsePoint — `web.pulsepoint.org`
**[verify on first run]** whether any Baldwin County fire/EMS agency is on PulsePoint (search "Baldwin", "Daphne", "Foley", "Gulf Shores", "Orange Beach"). If none, delete this section. If one is, the Fairbanks rules apply unchanged: fire/EMS only, rolling 24 hours, never infer a crime from a medical call.

### Not a source
Mugshot-aggregator and "jail view" SEO sites that scrape the roster. They are stale, unverified and full of filler; never cite them.

## When the browser is down

Almost everything here needs Claude in Chrome — the roster above all. If the extension is not connected, **do not publish a quiet edition.** Sweep what the cloud can reach (individual USAO releases surfaced through search, newsroom items), mark the roster and every browser source *Not reached* in Sources checked with the reason, and say at the top that the jail roster could not be read.

## Suicide — hold and ask, never publish

Standing instruction from the owner (set for the Fairbanks record Oct. 3, 2026; applies here too). An item is caught when a source **explicitly states** that a death or an attempt was a **suicide** or **self-inflicted** ("suicide", "self-inflicted", "took his/her own life", or a manner of death recorded as suicide). A death with no manner stated, or "no foul play suspected", is not caught.

When caught: do not publish it anywhere — not the artifact, not the Drive JSON, not a table row, not a correction — and do not paraphrase around it. Leave no identifying placeholder; where a count would otherwise be wrong, say only that one item is withheld pending review. Write it in full with its source and date to a local file `held-suicide-YYYY-MM-DD.md`, say in the run summary that an item is held, and send one PushNotification saying a suicide-related item is held pending permission (date and source only). Permission is per item, from the owner, in conversation; until then it stays held on every run.

## Handling rules

- Everyone is **arrested or charged, not convicted**, unless an official source says convicted or sentenced.
- Charges are **booked charges** from the jail. Never call one an indictment or give a felony class unless an official source does.
- **Never publish date of birth, race or the age/race/sex line** from the roster. Age may be given as stated in a news item, not computed from the DOB.
- Do not reproduce booking photographs.
- Do not list immigration holds (ICE, "INS Service" detainers) as crimes; an immigration detainer is not a criminal charge.
- **Do not compile non-crime biographical profiles of the people named here.** Private people, mostly misdemeanours, many dismissed. Answer bigger-picture questions in aggregate.
- Note coincidences without asserting connections the records don't support.
- Bound research on private individuals in minor matters to the roster and official releases.
- Juveniles are never named.

## Context for booked-only items

A roster record is a name, an agency and a charge line. Before an entry goes out bare, look for the event behind it — in this order, stopping when you have it:

1. **This record's own earlier items** — the arrest may already be on the page from a Facebook post or news item.
2. **The arresting agency's Facebook page**, booking date minus 1 to plus 2 days. Match on last name, then charge and place.
3. **Newsrooms — felonies only** — last name plus the town. Date-check every hit.

**Always add:** what the charge means in plain words, twelve words or fewer, from the roster's own text ("Simple Assault-Family — an assault charge against a family or household member"). Do not quote sentence ranges for a booked charge — the class is unknown until the DA files. When an official source states the class, you may add what Alabama law allows (Code of Alabama §§13A-5-6 and 13A-5-7): Class A felony 10 to 99 years or life, Class B 2 to 20 years, Class C 1 to 10 years; Class A misdemeanour up to 1 year, Class B up to 6 months, Class C up to 3 months — written as what the law allows, never what this person faces.

**Shape of an entry (fairbankscrime.com format):** headline in the form "Category: Name" ("Armed robbery arrest: [full name]", "Federal sentence, felon with a firearm: [full name]"; for roundups "Gulf Shores weekend: 6 booked, mostly DUI"); first paragraph is what police say, attributed; second is the booked charges with the plain-words meaning; optional third is the next court date if the free docket shows one. Leave docket and roster mechanics out of public entries — they belong in the Sources checked notes.

**Limits:** police narratives are allegations, attributed every time. No stitching two records together without name **and** date **and** place or charge matching. Domestic violence, sexual offences and child victims: only what an official source states; never a victim's name, relationship, age or address. Misdemeanours: context from police posts and the roster only, no news or social-media name searches. Budget: felonies first.

## The page

**The public site is generated, not hand-written:** `build.py` in the alacrime repo turns each edition JSON into the pages, so the JSON is what matters for www.alacrime.com. The layout below describes what that builder produces, and the working artifact mirrors it.

The working artifact is a single self-contained HTML file at `/home/claude/baldwin-crime-record.html`, republished to the working-page URL above. Build each day's version from the previous one (read it first), not from memory. The Motive Wheel lives only on the public site (`/wheel/`); its motives are in `wheel/index.html` in the repo.

**Tokens (same as fairbankscrime.com):** light `--paper #F6F7F9 --surface #ECEEF2 --ink #14181E --ink-soft #39414C --muted #646E7B --rule #DCE0E6 --rule-hard #BCC4CE --accent #0E5A58 --felony #A02B23 --caution #8A5A00 --ok #2E6647 --stamp #2F4A7A`; dark `--paper #0F1217 --surface #171C23 --ink #E7EBF1 --accent #63BFB8 --felony #E08A82 --caution #D6A44F --ok #7FC2A0 --stamp #8FB0E6`. Fonts: **Spectral 600** for the brand line only, **Public Sans** for everything else, **IBM Plex Mono** for the org line, nav, dateline, gutter, chips, table headers and source lines. Tokens on `:root`, redefined under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {...} }` and `:root[data-theme="dark"]`; explicit `body` background; a working Light / dark toggle in the footer.

**Structure, top to bottom:**
1. `header.site-head` — `.org` mono kicker "Baldwin County, Alabama · Compiled daily from primary records", `.brand` Spectral tagline.
2. `nav.top` sticky — Latest, Archive, Open cases, Search, Corrections, Motive Wheel, About, Contact.
3. `.layout` grid: `main` 692px + `aside.side` 340px, stacking under ~980px.
4. In `main`: `.ed-stamp` (rotated rubber-stamp "Morning Edition" / "Evening Edition") → `.dateline` (full date · Compiled HH:MM CDT · Covers date range) → `h1.page` "Today in Baldwin County" → `ul.highlights` anchor list of every entry headline → `.presumption` "Everyone named is arrested or charged, not convicted." → `.share` row.
5. **Charge-O-Meter** (`section.charge`, fixed dark instrument in both themes, gold numerals): **this week so far** — new jail bookings from Monday of the edition's week through the edition date (restarted Mon. Oct. 26, 2026 at the owner's request; `build.py` computes it from `filings.new`, so keep that list complete), a split line (city police · sheriff · troopers & others · flagged family/domestic), a proportional bar, eight tiles — Assault & threats, Drugs, Drunk driving, Theft burglary & damage, Broke a court order, Driving & licence, Everything else, **Warrants & holds** (replaces Fairbanks's "Charge not filed yet") — and a note naming the top category and saying booked charges are not filed charges. Each booking counts once, by its most serious-sounding booked charge.
6. **Entries** — filter buttons All / Violent / DUI·traffic / Courts / Other; each `article.entry` has a 130px mono `.gutter` (date, time, town, agency, ORI or case number) and a body with linked `h3`, `.chips` (agency always; `Felony` only when an official source states it; `Domestic`; `Sentenced` / `Convicted` for court outcomes), short paragraphs, and a mono `.src` line of linked sources. Federal and state outcomes and ALEA fatal crashes are entries too, filtered under Courts and DUI / traffic.
7. **Jail admits by agency** table (agency · ORI · bookings, last 24 hours) — Baldwin's stand-in for Fairbanks's court-filings table.
8. **Open cases** two-column `.card` grid: booking date, name, chips, one-line status, `dl.kv` with Next / Agency / Last check.
9. **Sources checked** table: Source (linked) · Status chip (Read / Not reached / Stale / Blocked) · Note with the count seen. Non-optional — it is how the page tells "nothing happened" from "I couldn't see."
10. `.daynav` previous-day link.
11. Sidebar: **This edition** 2×2 stats (Entries, Federal outcomes, Bookings 24 h, Open cases), **Commentary** placeholder panel, **Recent editions** list with entry counts and a Full archive link.
12. `footer.site-foot` — presumption-of-innocence paragraph adapted to Baldwin, including that jail charges are booked charges; corrections, contact, RSS and the theme toggle.

**Corrections stay published** as dated blocks on the corrections page, never silent edits. Before publishing, check tag balance (`<section>`, `<article class="entry">`, `<table>`, `<tbody>`, `<footer>`).
