# Power Up Raffle · draw tool

The electronic raffle tool for the Solviva Power Up Raffle Promo (Oct 2026 to Jan 2027).
One HTML file, no server. It runs in Chrome or Edge on the operator's laptop and is
screen-shared on the Zoom webinar.

## Hosted copy (nothing to download)

**https://solvivaenergy.github.io/raffle-draw-tool/** is this same tool served from GitHub
Pages. Open it in Chrome or Edge, click **Open live view** for the window to share in Zoom
(or open the same address with `#live` at the end). The entry list you load never leaves
your browser; the page only serves the tool itself. The session is remembered per browser,
so run the real draw on the laptop you rehearsed on.

The hand-over below is for running it from a local folder instead, which also works offline.

## Hand-over: running it on your own laptop

Nothing to install. You need Chrome or Edge and this folder, unzipped, kept together. Internet
is needed only for the fonts and for reading `.xlsx` files; a `.csv` list works offline.

1. Unzip `raffle-draw-tool.zip` anywhere, for example your Desktop.
2. Double-click `index.html`. That is the **operator view**. Keep it on your own screen.
3. Click **Open live view**. A second window opens; that is the one to share in Zoom. If the
   browser blocks the pop-up, allow it once, or open `index.html` again in a new window and add
   `#live` to the end of the address. The two windows stay in sync on their own.
4. Fill in Draw details. The draw number and date are picked up from the file when it holds one draw.
5. **Choose file** under Verified entries and pick the export from Odoo. For a dry run use
   `sample/odoo-export-dummy-20.xlsx` (20 made-up entries, 10 per prize pool).
6. Press **Draw**, confirm or set aside, repeat through the six picks.
7. **Export log (CSV)** and **Print draw report**. Keep both with the draw record.

Draw-night checklist:

- The Odoo export carries the **Promo Prize** and **Eligible** columns (see below). Without
  Promo Prize the tool loads the file but cannot draw, and says so.
- The counts on the Verified entries card match what Marketing expects (5 kWh pool, 16 kWh
  pool, won earlier, needs review). Anything under "needs review" is explainable.
- Winners of earlier draws are loaded under "Already won in earlier draws", or come through as
  Status = Winner in the export.
- DTI representative and permit number are filled in before the first pick.
- The live window, not the operator window, is the one being shared.
- After the draw, someone sets each winner's status in Odoo from the exported log.

If something goes wrong mid-draw: the session is saved in the browser, so closing the window
by mistake loses nothing. Reopen `index.html`, the list and the log come back. **Reset session**
clears everything and asks twice.

## Run it

1. Keep the three things together: `index.html`, the `assets/` folder, and your list files.
2. Double-click `index.html`. This is the **operator view**. Keep it off the screen share.
3. Click **Open live view**. A second window opens. Share **that** window in Zoom.
4. Fill in the draw details (draw number, date, DTI representative, permit number, your name).
5. Load the verified list exported from Odoo. Optionally load the winners of earlier draws.
6. Press **Draw**. The live window rolls the reels and reveals the pick. Confirm it, or set it
   aside with a reason and draw again.
7. After the six picks, **Export log (CSV)** and **Print draw report**. Keep both with the draw record.

Internet is only needed for the fonts and for reading `.xlsx` files. Save the list as `.csv`
and everything works offline.

## Export from Odoo (production)

The draw list comes from the **Promo Participation** records in Odoo. Two ways, same columns.

**A. From the Odoo screen (anyone with the Promo app)**

1. Open the Promo app, list view of Promo Participation.
2. Filter **Draw Number = 1** (or 2, 3). Do not filter on status; the tool decides what is
   drawable and shows why the rest is left out, which is what DTI wants to see.
3. Select all rows (tick the header box, then "Select all N").
4. Action menu, **Export**. Tick **"I want to update data"** off. Format: CSV or XLSX, both load.
5. Pick these fields, in this order, and **Save the template as "Raffle draw tool"** so the next
   draw is one click:

   | # | Field in the export dialog | Header in the file |
   | --- | --- | --- |
   | 1 | Reference | Reference |
   | 2 | Draw Number | Draw Number |
   | 3 | Draw Date | Draw Date |
   | 4 | Full Name | Full Name |
   | 5 | Customer | Customer |
   | 6 | Last Name | Last Name |
   | 7 | First Name | First Name |
   | 8 | Middle Name | Middle Name |
   | 9 | Mobile | Mobile |
   | 10 | Email | Email |
   | 11 | Street | Street |
   | 12 | City | City |
   | 13 | Status | Status |
   | 14 | Eligible | Eligible |
   | 15 | Promo Prize | Promo Prize |
   | 16 | Opportunity › System Size (kWp) | Opportunity/System Size (kWp) |

   The last one is a sub-field: expand **Opportunity** in the dialog and tick System Size (kWp).
   Fields 13 to 15 are the ones the default export misses and the tool cannot draw without.

**B. From the command line (Digital team, read-only API key)**

In the `solviva-inquiry` folder:

    ./py.cmd tools/raffle.py programs
    ./py.cmd tools/raffle.py --format csv participants --draw 1 > scratch/draw1.csv

The first prints the three programs with their dates and counts; the second writes the same
16 columns as the saved Odoo template. `--joined` keeps only Status = Joined, `--env staging`
reads the staging copy. Nothing in it writes to Odoo. The file holds customer names and
contacts, so keep it in `scratch/` and delete it after the draw record is filed.

Either way, load the file under **Verified entries**. Checked on 13 Nov 2026 against the real
Draw 1 export from production: every column mapped, every row got a name and a pool, and the
tool listed 3 drawable entries (all 5 kWh), 45 not yet joined, 5 joined but not ticked Eligible,
1 under 5 kWp.

## The verified list

Two export shapes are accepted. Header names are matched loosely and the order does not matter.

**Odoo "Promo Participation" export** (the promo module in Odoo, Oct 2026). In Odoo open
Promo Participation, select the rows, Export, and include these fields:

| Column | Used for |
| --- | --- |
| Reference | the entry number, e.g. `BATTERYPROMO-0003` (auto-numbered by Odoo per promo) |
| Draw Number | rows for other draws are left out of the pool (the tool picks the draw from the file when it holds only one) |
| Draw Date | prefills the draw date |
| Full Name, Customer, or First / Middle / Last Name | the name shown on screen: Full Name (as typed on the signup form) first, then the Odoo Customer, then the name parts |
| Street, City, Email, Mobile | shown on screen; email and mobile identify the customer for the one-win rule |
| **Promo Prize** | **required**: decides the pool from names like "Pylontech 5kwh Battery (2)" or "Pylontech 16kwh Battery (0)". Without it nothing can be drawn and the tool says so |
| Status | only **Joined** rows go into the draw; **Winner** rows count as already won; anything else is left out |
| Eligible | if present, only ticked rows go into the draw |
| Opportunity/System Size (kWp) *(optional)* | if present it is shown and cross-checked against the prize; a mismatch is flagged |

The default export (Reference, Draw Number, Draw Date, Customer, names, Mobile, Email, Street,
City, Status) loads but cannot be drawn from, because it carries no prize pool. Use the saved
"Raffle draw tool" template from the section above, or `tools/raffle.py`.

**Plain list** (the earlier layout):

| Column | Used for |
| --- | --- |
| Full Name | shown on screen and in the log |
| Street | export only |
| City | shown on screen |
| Email | identifies the customer for the one-win rule |
| Phone/Mobile | identifies the customer for the one-win rule |
| System Size | decides the prize pool: 5 to 14.99 kWp → 5 kWh package, 15 kWp and up → 16 kWh package |
| Entry No *(optional)* | if present it is used as the entry number |

**Entry numbers.** If the file has no entry-number column, the tool assigns a six-digit number to
each row when the file is loaded. The assignment is deterministic (the same row always gets the
same number) so reloading the same file after a browser crash gives the same numbers. Use
**Export entries with numbers** and keep that file with the draw record so every number can be
traced to a row. If Odoo generates the entry number when the raffle entry is saved, include it in
the export and the tool will use it, which is the better arrangement because the customer can be
told their number in the confirmation email.

On load the tool also:

- computes the SHA-256 checksum of the file and shows the first characters next to the file name;
- splits the entries into the two prize pools;
- flags rows with no name, no system size, or a system under 5 kWp (no prize pool) and leaves
  them out;
- flags exact duplicate rows (same name, email, phone, street and size) and leaves the copies out;
- marks entries whose email or phone matches a winner of an earlier draw and leaves them out.

Two entries from the same customer (two contracts) are both kept, as the FAQ allows. Once one of
them wins, the other is excluded for the rest of the session.

## How the draw works

- The pick order is fixed by the mechanics: 5 kWh winner 1, 5 kWh winner 2, 16 kWh winner, then one
  reserve for each prize in the same order. Six picks per draw.
- Each pick is a uniformly random choice from the eligible pool using the browser's cryptographic
  random source (`crypto.getRandomValues`). The number is chosen before any animation starts; the
  reels only roll to it.
- By default each pick draws only from entries that qualify for that prize, with already-won
  customers excluded. Tick the **literal reading** box in Draw details to draw from all verified
  entries instead and have the tool flag a pick that does not qualify, which the operator then sets
  aside, as the mechanics text describes.
- Reserve picks are drawn with the DTI representative but are **not shown on the live screen**.
  The live window shows a holding card while they happen. Their names are in the log and the
  report.
- Every pick, confirmation and set-aside is logged with the time. Set-asides carry a reason.
- The session is saved in the browser as you go, so a closed tab or a crash does not lose the log.
  **Reset session** clears it (two clicks).

## What to put in the DTI package

- **Step 10 front end:** a screenshot of the live window during a reveal.
- **Step 10 back end:** a screenshot of the operator window with the verified list loaded, showing
  the file name, the row count, the checksum and the prize pool counts.
- After each draw: the exported log CSV, the exported entries CSV (if numbers were assigned by the
  tool), and the printed draw report signed by the operator and the DTI representative.

## Troubleshooting

| What you see | What it means |
| --- | --- |
| "The spreadsheet reader did not load" | No internet, so `.xlsx` cannot be read. Save the list as `.csv` in Excel and load that. |
| Red banner about "Promo Prize" | The export has no prize column. Re-export from Odoo with Promo Prize (and Eligible) added. |
| Draw button stays grey | No eligible entries for this pick: check the draw number in Draw details and the pool counts. |
| Live window shows "Waiting for the first draw" after a pick | It was opened before the operator window loaded the list. Press Draw again or reload the live window. |
| Second window did not open | Pop-up blocked. Allow it, or open `index.html` in a new window with `#live` at the end of the address. |
| Print shows the report but no dialog | Only happens in the hosted demo; printing works from the local file. |

## Changing prize names or dates

Prize names, the pool rule and the pick sequence are at the top of the script in `index.html`
(`PRIZES` and `STEPS`). The large package is written as 16 kWh, following Mechanics v4; the brief
and FAQs say 20 kWh. Change the label in one place when Marketing settles it.

## Samples

- `sample/odoo-export-sample.csv`: 40 made-up rows in the exact layout of the Odoo export plus
  Promo Prize and Eligible. Start here.
- `sample/odoo-participation-export-sample.csv`: 60 rows in a wider participation layout.
- `sample/verified-entries-sample.csv` (312 made-up rows in the plain layout, including a few the
  tool should flag) and `sample/previous-winners-sample.csv` (three earlier winners, two of whom
  are in that list).

Regenerate with `python make-samples.py`. Every name, email and number is fictional.
