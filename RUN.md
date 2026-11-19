# Run engine

Read this file right after the first section of `SETUP.md`. Where this file and `SETUP.md` disagree, this file wins.

## The three rules of a run

1. **Do not end the session before the search is finished.** Finished means every work unit in the queue is `færdig`, `ufuldstændig` or `blokeret`. Not "most of it", not "a good part of it". A run takes many hours, and that is expected. Do not write a final answer, summary or "next steps" while units are open. Your turn ends only when section 9 is done.
2. **One platform at a time.** Finish a platform (search, verify, write, availability check) before you start the next one. If a platform fails, mark it `blokeret` and go on to the next platform. Never stop the run because of one platform.
3. **Everything goes through the queue.** The queue is the truth about how far the run is. Anyone reading it, including you after a lost thread, can see exactly what is done and what is left.

## Why it is built this way

A full search does not fit in one agent's context. It covers all active rows, every search string, every result page and every listing, plus a thumbnail image for every new find. Earlier runs stopped at page 1–3 and never wrote `searched`, so every run started from scratch. So:

- The work is split into small units. Each unit is done by a fresh subagent with its own context.
- **You are the conductor. You hold the queue and nothing else.** You do not search, you do not open listings, you do not paste long files into prompts, and you do not handle listing details, images or thumbnails. Details go between subagents as files in the working directory. You only see short status lines. That is what lets you keep going for hours.
- The queue is stored twice: in the run document in the database (for the page and for the next session) and in `queue.json` in the working directory (for you). If you lose track, for example after your context is compacted, read `RUN.md` and `queue.json` again and continue from there.

## 1. Start

1. **Tool check.** Check that the browser tools (Claude in Chrome) are there and that you can write to the run document. If the browser is missing, see section 10.
2. Read `requests/search` and the newest documents in `runs`, ordered by `date` descending.
3. **Continue an open run.** If a run document has `status: "kører"`:
   - If its `heartbeat` is less than 2 hours old, another session is running it. Write nothing, and stop.
   - Otherwise, take it over. Set `heartbeat` to now and set units with status `kører` back to `åben`. Rebuild `queue.json` from the run document, and go to section 4.
4. **Start a new run** if `requests/search` is `bestilt`, if the user asked for a search, or if no run has started in the last 20 hours. Go to section 2.
5. Otherwise there is nothing to do. Write nothing, and stop.

## 2. Build the queue

Do the start-of-run gate in `SETUP.md` section 1 (categories, targets, platforms, time window). Create `runs/<YYYY-MM-DD-HHMM>` with these fields:

- `status: "kører"`
- `heartbeat`
- `searched: {}`
- `platformOrder`
- `progress`
- `units`

Write the queue before any searching, and set `requests/search` to `kører`.

**How to find a unit's cutoff.** Read every document in `runs`, not only the newest ones: older runs hold valid cutoffs. For a row R in category C on platform P, the cutoff is the **latest timestamp** among these values:

- `searched["P|R"]` in a run document whose `category` is C or `alle`.
- `searched["P"]` (old form, platform only) in a run document whose `category` is C or `alle`. If that document has a `rows` list, the value counts only when R is in the list.

Compare the timestamps themselves, not the run documents' `date` fields, which use mixed formats. If no value is found, the unit has no cutoff (`"ingen"`), and the row is searched on the whole platform. Write the cutoff into each unit when you build the queue, so it is visible on the page.

**Platform order.** Edit this list to change it. Platforms missing from it go last, in alphabetical order.

DBA, Tradera, Vinted, Klein Anzeigen, Lauritz, Palsgaard, Woxholt, Bidstrup, Sikö, Catawiki, Gul og Gratis, Reshopper, Facebook Marketplace

Facebook Marketplace is last because it is the most likely to hit a login wall.

**Units.** Each platform covers the rows of every category. At the start of a platform, create its `search` and `check` units. `verify` and `write` units are created as results come in.

| Unit id | Agent | Work | Size |
|---|---|---|---|
| `search|<platform>|<targetId>` | search agent | One target row: all its search strings, every page to the end | 1 row |
| `search|<platform>|<targetId>|<k>` | search agent | Part k of a large row (more than 6 search strings, or a search known to hit a page cap) | Some search strings |
| `verify|<platform>|<n>` | verifier | Independent verification (`SETUP.md` section 4) | Max 15 candidates |
| `write|<platform>|<n>` | writer | Decide and write the finds of one verify unit, thumbnails included (`SETUP.md` sections 5–6) | 1 verify unit |
| `check|<platform>|<n>` | availability agent | Check active finds, in fixed order by `id` | Max 40 links |
| `write|<platform>|check-<n>` | writer | Apply the result of one check unit (`SETUP.md` section 6, "Known finds") | 1 check unit |

`<targetId>` is the `targets` document id, for example `lamper-row-21`.

Each unit is `{"status": "åben", "attempts": 0, "cutoff": "<ISO or 'ingen'>", "resumeFrom": null, "note": ""}`. The status values are:

- `åben`: not started
- `kører`: in progress
- `færdig`: done
- `ufuldstændig`: could not be completed; the reason is in `note`
- `blokeret`: a real block, such as a login wall, 403, Cloudflare/Akamai or an unreachable host

## 3. Brief files: written once per platform

Before the first unit of a platform, write these files in the working directory. Each one holds the full text of the files listed, unchanged:

| File | Contents |
|---|---|
| `brief-search-<platform>.md` | `agents/platform-searcher.md`, `agents/qualification-rules.md`, the platform file |
| `brief-verify-<platform>.md` | `agents/verifier.md`, `agents/qualification-rules.md`, the platform file |
| `brief-check-<platform>.md` | `agents/availability-checker.md`, the platform file |
| `brief-write.md` | `SETUP.md` sections 5 and 6, `templates/FIND_SCHEMA.md`, and section 7 of this file |

In file names, replace `|` in a unit id with `_`, for example `cand-search_DBA_lamper-row-21.txt`.

Subagents share the working directory. Each prompt is then short, for example:

> Read `brief-search-DBA.md` and follow it. Unit: `search|DBA|lamper-row-21`. Cutoff: … resumeFrom: … Target block: …

This replaces "pasted verbatim" in `SETUP.md`. The content is the same, but it is written once instead of copied into hundreds of prompts.

## 3a. Models for the subagents

Set the model on every subagent you start (the `model` field of the Agent tool). Most of the run's cost is in the subagents, because they browse and look at pages. So the cheap model does the work that is mechanical, and the stronger model does the judgement.

| Agent | Model | Why |
|---|---|---|
| search (`search` units) | `haiku` | Runs the searches, pages through results, and notes candidates. The verifier checks its work. |
| availability (`check` units) | `haiku` | Opens links and reads whether the listing is still for sale. |
| writer (`write` units) | `haiku` | Follows fixed rules and writes to the database. |
| verifier (`verify` units) | `sonnet` | Decides identity, colour, price and date. It is the safeguard against the search agent's mistakes. |

**Escalation.** If a Haiku unit comes back unusable, start it again once with `sonnet` and say so in the unit's `note`. Unusable means one of these:
- The answer is not in the format in section 6.
- `read af total` is missing.
- It stops with `ikke færdig` at the same `resumeFrom` twice.

## 4. Run one platform

1. Set the platform to `kører` in `progress`.
2. Run the units in rounds of up to **3 subagents** at the same time, each in its own browser tab. A platform file can set a lower number under `Samtidighed`, for example 1 for a platform that blocks quickly. `write` units do not use the browser and can always run alongside the others.
3. **Start a round's subagents in one message, and wait for them there.** Do not start them in the background. If your turn ends while subagents run in the background, an unattended session can end with them, and the work is lost.
4. Order within the platform:
   1. `search` units.
   2. A `verify` unit as soon as it holds 15 candidates.
   3. The `write` unit for it right after.
   4. When the searches are done: the remaining `verify` and `write` units.
   5. The `check` units, each followed by its `write` unit.
5. **After each round:** update `queue.json`, and write the units' status, `progress` and `heartbeat` to the run document. Pin each write with `if_version`.
6. The platform is done when none of its units is `åben` or `kører`. Write one line for it in `progress`, for example: `DBA: færdig. 31/31 rækker, 4 nye fund, 212 fund tjekket.` Then go to the next platform.

## 5. Handle a unit result

**Search unit**

- **Complete:** every search string has been read to the end, after splitting where needed. Set the unit to `færdig`, and **write `searched["<platform>|<row>"]` with the unit's start time at once.** This moves the cutoff, so the next run is small.
- **Candidates:** the search agent writes its candidate lines to `cand-<unit>.txt` and returns only the count. Add the candidates (URL + row) to the platform's open `verify` unit. At 15, start a new `verify` unit.
- **Not finished** (lost the tab, ran out of room): save `resumeFrom`, add 1 to `attempts`, and set the status back to `åben`. After 3 attempts, set `ufuldstændig` with the reason. An unfinished unit never writes `searched`.
- **Page cap even after splitting:** set `ufuldstændig` with the numbers (`read af total`).
- **Blocked:** set `blokeret` with the reason. If the block applies to the whole platform (a login wall, or a 403 on the search page), set every open `search` and `check` unit of the platform to `blokeret` with the same reason. Then finish its `verify` and `write` units if they can still run, and go to the next platform.

**Verify unit**

The verifier writes its full blocks to `verify-<unit>.md` and returns only `<n> bekræftet / <n> forbehold / <n> afvist`. Create the `write` unit for it.

**Write unit**

The writer reads `cand-*.txt` and `verify-<unit>.md` for the candidates, decides per `SETUP.md` section 5, and writes the finds per `SETUP.md` section 6, thumbnails included. It returns `skrevet: <n> nye, <n> opdateret, <n> udeladt`. Thumbnails and listing details never pass through you.

**Check unit**

The availability agent writes its result to `check-<unit>.md` and returns `<n> til salg / <n> væk / <n> reserveret / <n> uklar`. Create the `write` unit for it. The writer applies the updates (`SETUP.md` section 6, "Known finds").

**A subagent cannot write to the database** (`network_off` or a missing tool): mark the unit `blokeret` with "kan ikke skrive til siden" and keep its files. Do not write the finds yourself.

**A subagent cannot be started at all:** do the unit yourself with the same brief. Keep only the short result in your context.

## 6. What a subagent returns to you

Max 10 lines:

```
Unit: <unit id>
Status: færdig | ikke færdig (resumeFrom: "<term>", side <n>) | blokeret (<reason>)
Resultat: <the count line from section 5>
Fil: <the file with the details>
```

Search agents add one coverage line per search term: `"<term>": <read> af <total>, slut nået: ja/nej`. No narration.

## 7. Platforms without a listing date

These rules replace the date requirement in `SETUP.md` section 5, for these platforms only.

- **Vinted and Facebook Marketplace.** The relative age ("for 3 dage siden") is the evidence. Set `listedAt` to the run time minus that age, and set `check` to "dato ud fra relativ alder". If only "Sidst set" is shown, set `listedAt` = null and `check` = "oprettelsesdato ikke vist".
- **Gul og Gratis and any other platform with no date.** Set `listedAt` = null and `check` = "oprettelsesdato ikke vist".
- **What counts as new.** A listing is new if its find id is not already in `finds`. Every page is still read to the end.
- A missing date is **not** a reason to drop a find or to call a search incomplete.

## 8. Your own context

- Never read the content of `cand-*`, `verify-*` or `check-*` files yourself. The subagents read them.
- Do not repeat results in your messages. Write them to `queue.json` and the run document.
- If you notice that you have lost track, read `RUN.md` and `queue.json` and continue with the first open unit.

## 9. Ending the run

Only when no unit in the whole queue is `åben` or `kører`:

1. Set the run document's `status` to `færdig` if every unit is `færdig`, otherwise to `delvis`. Write the coverage note (`SETUP.md` section 6, item 4) as `sections`. Start with one line per platform: `færdig`, `delvis (x/y rækker)` or `blokeret (<reason>)`.
2. Set `requests/search` to `færdig` with `finishedAt` and a one-line summary.
3. Send the summary as a notification if a notification tool is available.

The next run first creates new units for every combination that ended `ufuldstændig` or `blokeret`, with the old cutoffs, since their `searched` value never moved.

## 10. When the run cannot go on

- **Browser missing at the start:** write a run document with every unit `blokeret` ("browser ikke tilgængelig"). Set `requests/search` to `færdig` with the note "IKKE SØGT: browser ikke tilgængelig", so the button works again. Then stop. This is the only case where a run stops early.
- **Browser lost during the run:** wait 2 minutes and try again, up to 3 times. If it is still gone, mark the platform's open browser units `blokeret` and go to the next platform. If every platform is then blocked, go to section 9.
- **Session ends anyway** (a limit outside your control): the queue is saved after every round. The next session takes over after 2 hours without `heartbeat` (section 1, step 3) and continues where you stopped. This is the safety net, not the plan.
