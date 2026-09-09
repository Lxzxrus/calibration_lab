# calibration_lab — Lab Log

*Append-only. Newest first. Raw measurements and what happened, dated.*

## 2026-09-06 - 2026-09-09 run_pilot.py creation and work.

A forenote: I neglected this log for a couple days. I am making amends by combining three days of work into this entry - all work is done inside run_pilot.py

- Step 1:
draw_pilot.py is finished. it produced items_pilot.jsonl which I used here. Since run_pilot.py runs as its own separate program, none of draw_pilot.py's in-memory variables survive; the only thing that persisted across that script's exit was the file it wrote. So run_pilot.py opens items_pilot.jsonl in read mode, loops line by line, and uses json.loads() to turn each raw text line back into a real dictionary  Only question and question_id are kept per item - the answer fields (normalized_value/normalized_aliases/value) are deliberately dropped here, since the grader will re-open the frozen items_pilot.jsonl later and rejoin on question_id rather than carrying answer data through this pipeline. Asserts exactly 50 items came through.

- Step 2:
Ollama tags are mutable pointers, and the project had already been silently moved once before (Ollama 0.32.6 moved to 0.32.14),  so this step exists to refuse to generate any data if the environment has drifted, hard stopping rather than just warning. Used requests library (already a listed dependency, no fresh install needed) to make HTTP calls against Ollama's local server at 127.0.0.1:11434, not localhost. GET /api/version returns the running Ollama version; compared against a frozen OLLAMA_VERSION constant and hard-stops via sys.exit() with a message stating expected vs. received.
GET /api/tags returns metadata for every locally installed model as a list under a 'models' key. Built two frozen constants, MODEL_1B_Q4 and MODEL_12B_Q8 - the pilot's weak/strong model pair from the prereg's section 4 roster - each pairing an expected model name with its expected digest, combined into a MODELS list. Built a nested loop: outer loop over the two expected models, inner loop searching all installed models for a name match, then comparing digests on match (hard stop on mismatch). Used break to stop the inner search early once found, and a "found" flag (reset fresh per outer-loop pass) to catch the case where an expected model isn't installed at all. Found that ollama list's CLI digest column is truncated (12-character prefix, not the full SHA256). Retrieved the full digests and verified against full digests - machine accuracy, a human can tell the difference by reading the first few characters of the hash. Tested code thoroughly and did a full pass of comments - step 2 functionally complete and verified.

hand-edited .gitignore to add tempCodeRunnerFile.py (an artifact of my VScode extension "Code Runner") and found that data/ was structurally dead - git can't re-include a file inside an excluded directory - so I deleted both rules.

Some findings: 
- /api/tags casing investigation: a bug tripped me up here - 'model_name' 's value inside the two model constants at the top of run_pilot.py caused a "missing model" crash. Curious, I was certain I had the model. I printed the api tags and found that the name field was lowercase: "gemma3:1b-it-q4_k_m" and the quantization level field was uppercase: "q4_K_M"
- The digest length bug fired on a healthy model because I trusted the windows powershell command "ollama list" to give me the digest hash, but ollama truncated the full hash in that CLI environment. I pulled the full hashes from the tags and updated the constants. But it did prove that the hard stop works - the check refused to proceed on a mismatch.

An honest confusion: I was planning to write run_pilot.py inside of draw_pilot.py because I was confused on my next steps after having completed draw_pilot.py - Slice 2 had no step breakdown before starting the work like slice 1 did. A confusion caught before amending a finished draw_pilot.py, thankfully.

A good lesson from debugging: inspect a structure you didn't build before reaching into it. Both came from writing the reach before printing the shape.

## 2026-09-06

hand-edited .gitignore to add tempCodeRunnerFile.py, discovered the data/ exception was structurally dead, removed both data/ rules because the pipeline writes to root.

## 2026-09-05 - Harness Slice 1 finished and deferred lab log entry resolved.
To begin, I fixed the deferred lab log entry - see entry "2026-08-31 - Re-plan" for more.

I shuffled the questions out of the dataset from seed = 8, took 50 of them, and sorted through them with a for loop - pulling the 5 values needed from all 50 items, verifying there is actually 50 via assert function, then recording them to items_pilot.jsonl and also recording timestamp, dataset, config, split, draw, draw_seed, source_rows, skipped, and items_drawn into items_manifest.json. I did a once-over of the two generated files and found ASCII escaping standing in for UTF-8 characters. 

I ran the script three times and got odql_4374 as item 0 every time. That's the seed verified rather than assumed - supports my replication claims. A replicator using DRAW_SEED = 8 gets the exact same items I did.

\uXXXX escapes throughout the alias lists. Not corruption - json.dumps defaults to ensure_ascii=True, so non-ASCII gets escaped. \u0430\u043b\u044f\u0441\u043a\u0430 is аляска, Alaska in Cyrillic. Kept the default deliberately: pure-ASCII output can't be misread by anyone regardless of their editor's encoding.

qw_402 carries CSV escaping that was never stripped - the question is wrapped in quotes with "" doubled around The Gold Cup. One of 50. Reaches the model as prompt noise, uniform across cells, not fixed because a de-escaping rule is the unjustifiable-free-parameter knob again.

TriviaQA's construction artifacts now appear in three distinct fields: the answer wiring (qf_1637), the value field ('(a', "A: Basketball" on tc_543), and the question field (qw_402). Three independent instances is a dataset-quality limitation, not three coincidences. This needs to be a section 10 entry.

Slice 1 done in 2 sessions, 12-19 sessions estimate for completed harness is holding accurate. 

One hazard worth logging: draw_pilot.py opens in 'w' mode, so re-running it overwrites both committed artifacts. Harmless while the seed is fixed; a live risk if DRAW_SEED or PILOT_N ever changes.

I discovered that .select() returns a dataset while example[0:50] returns a column dictionary - I need rows, not columns, so I used .select()

 ## 2026-08-31 - Re-plan: prereg paused for harness. Environment built, Slice 1 steps 1–2.

*Entry written 2026-09-05. Deferred at session close on 08-31 (session ran late), then
deferred four days beyond the stated 09-01. Measurements recovered from the session
transcript, not from disk, the reason the deferral was a risk.*

 A few handoff claims failed the verification:
 - "~2.3s is gone from the document entirely" is false. section 5 line 122 carries "~2.3 seconds (prompt_eval, eval and server_slack summed across the nine cells)." Different quantity from the dead one (the 1b cold-load figure generalized to the roster), same digits. The 08-29 lab log entry states it wrong too — this entry corrects it.
 - Section 5c item 1 was mis-scoped. Section 1's research question has no "uncharted" claim. The only stale text is the header Study: line - "frontier-scale," when Kadavath topped out at 52B. One-line fix. The overlap framing belongs in Section 2, which is empty.
 - No [others] placeholder exists in section 10 (Section 5c item 5 says to delete it). Separately: section 10 line 331 reads "qwen3 has almost certainly seen MMLU and TriviaQA" but the roster is gemma3 and MMLU was dropped. Wrong on the page, not scaffolding.

The re-plan: the pilot requires a harness, and up to this point I had done nothing at all to build the harness. Section 5's p_weak, p_strong, and N blanks and H2a/H2b's noise floor thresholds all require pilot data. The harness is a hard roadblock to the freeze. I decided that September 21st was not a hard deadline, but more so a "capacity cliff" - my life gets considerably busy after Sep 21st and I will no longer have the hours to dedicate to this lab that it deserves. i.e: I should get as much done as possible before Sep 21st, and after the 21st I tidy things up and prepare for freeze. My rough new target is slices 1-3 and the pilot completed before the 21st, slice 4 and freeze in October. This re-plan mainly revolves around my personal life. I am logging it to show the change in direction of work and effort. 

Design Decisions: items.jsonl will have 5 fields: question_id, question, normalized_value, normalized_aliases, value. Dropped answer.type and a draw index. Sidecar manifest, not a JSONL header line. Pilot exclusion by subtraction. Pilot is one draw of 50 on both extremes. Two scripts, duplication hazard (Row shape lives in two seperate files, changing one and missing the other produces mismatched shapes that won't crash) accepted.

The Measurements: 
- Validation split: 11,313 rows - Train: 87,622 (from verifying the split argument).
- question_id is unique across all 11,313 so it is usable as a key.
- entity_pages and search_results fields are empty - this is the nocontext config verified.
- Alias set size (normalized_value and normalized_aliases): min 1, max 214, mean 11.7.
- I found exactly one row with an empty normalized_value.
- Pool math: N = 200 / min(p_weak, 1 - p_strong) +10%: p_weak 0.10 → ~2,200 · 0.05 → ~4,400 · 0.03 → ~7,330 · 0.02 → ~11,000. Pool after pilot withdrawal 11,262. Comfortable unless the 1b lands near 2% accuracy.

The two items I found:
- qf_1637: Question: "In the cartoon, what kind of bird is the roadrunner?" Answer entity: static libraries, .lib, .a, static linking, static compilation. value is the fragment '(a', which normalizes to nothing - that's why normalized_value is blank. The answer entity is internally coherent, just attached to the wrong question, which is why there's nothing to scan for. Dropped by id at draw time, before any model runs, so it's a source defect and not a section 9 exclusion. Open and unquantifiable: rows mis-wired without blanking a field are mechanically undetectable.
- sfq_9993: The 214 max. Question: "In computing, what started life at Stanford University as 'backrub'?" Answer is Google; aliases are every country code domain (google.ae, google.am, google.at, etc.) and scraped typos (gogole com, giigke cin). This is the remnants of a Wikipedia redirect table. I did not cap it though, I would have to invent an unjustifiable number - which I have already rejected doing twice before.

Pre-Pilot Exceptions: Section 11's interpretation rule and section 8's noise floor procedure must be written before the pilot or else they are post-hoc.

Environment Setup: Python 3.12.8, .venv, requirements.txt, .gitignore, execution policy. 3.12 was chosen over the newest Python because the scientific stack may not have wheels built for the newest version yet, and the study's own principle is that this repo pins its own environment rather than inheriting one.

Code: draw_pilot.py steps 1–2 of 5: loads split, prints count, filters qf_1637 by id, asserts len(kept) == len(dataset) - 1. Verified 11,313 → 11,312.

## 2026-08-29 - §5 runtime reconstruction, §6 number-home consistency sweep, §10 rework begun, Kadavath scale correction

Kadavath's roster is 800M/3B/12B/52B, base models. My 1b and 12b overlap two of his four sizes. section 1's "consumer scale is uncharted" framing was built on a wrong belief and needs rewriting - the stronger position is that my range overlaps published results, so differences trace to what I actually varied.

Kadavath found RLHF models poorly calibrated, largely repaired by T=2.5. Relevant to section 2 and possibly section 11. Parked.

section 4 repaired: qat is the same recipe plus a stage, not a different path; scheme not bit-budget.

section 10: qat clause and roster asymmetry landed. ECE and differential exclusion resolved as not section 10 - ECE is section 11's unwritten rule, differential exclusion is already in section 8 and needs one clause about direction of bias.

Still open in section 10: contamination rewrite, extrapolation split into three, differential exclusion line, verify probe_out/ path in the repo.

Section 6 reworked - findings post-table paragraph, load_duration threshold line rewritten to cite both sections rather than restate the warm and cold figures, and loop-order block updated. 

Consistency sweep - every measured number now has exactly one home - no more duplicates. ~2.3s is gone from the document entirely. ~51s exists only in section 6 and section 5's sentence rewritten to cite section 6 instead of restating the figure. Warm constant only in section 5. Done to eliminate the failure mode of a number going stale in two places at once. 

Protocol change. Todays session started with a one day old stale handoff and a secondary handoff - it should have been just one updated handoff. With harness work coming up soon as the prereg is nearing completion, document and git tracking and syncing is becoming absolutely imperative. SESSION_PROTOCOL.md will aid me in doing so. 

Section 4 QAT repair - Updated line "- Why only one family? It holds the training recipe fixed across all nine, with QAT carrying an additional training stage (which is why it's exploratory), so the claim is clean." in the prereg, making a note here that it was not a mistake, it was a genuine edit outside today's session scope. 

Small date fix in section 5 08-27 → 08-28. The stale 08-27 handoff still listed the runtime paragraph as unrecomputed, which means the probes could not have run before the 28th

Section 7 has no throughput or footprint metric to feed E1. Surfaced today, carried over from the 08-27 handoff.

## 2026-08-28 — Runtime probes: per-call overhead, prompt eval, load/unload

Why: §5's runtime paragraph had been stale across three generations of numbers and was
flagged in three consecutive handoffs. Recomputing it from the current throughput table
surfaced a gap — `tok/s` is derived from `eval_count / eval_duration`, both server-side,
so it measures generation only. It excludes prompt eval, HTTP round trip, and any
per-call constant. At 27 calls per item (3 templates × 9 cells), anything per-call gets
multiplied ~40,000× at N=1500. Chose to measure rather than estimate.

Three PowerShell probes written and run. Scripts and CSVs committed under `probe_out/`.

### Probe 1 — per-call overhead

20 calls each on `gemma3:12b-it-q8_0` and `gemma3:1b-it-q4_K_M`, warm, Template B with
`logprobs: true` / `top_logprobs: 10`. Distinct hand-written questions per call (NOT
TriviaQA — draw pool untouched) because identical prompts hit Ollama's prompt cache and
collapse `prompt_eval_count`. Three priming calls discarded per model, covering both
model warm-up and client-side .NET/HTTP initialization.

| | 12b-q8_0 | 1b-q4_K_M |
|---|---|---|
| load_ms (warm) | 215.73 | 215.39 |
| prompt_eval_ms | 61.61 | 15.66 |
| eval_ms | 24.95 | 12.31 |
| server_slack_ms | 14.93 | 7.44 |
| client_ms (wall − total) | 0.65 | 0.71 |
| wall_ms | 317.86 | 251.52 |

**Main finding: `load_duration` on a warm call is a fixed ~215.5 ms.** A 12.6 GB model
and an 835 MB model report the same value to within 0.4 ms. Range across all 60 calls in
probes 1 and 2: 212.8–227.2 ms. Invariant across model size, quantization, template,
prompt length, and `logprobs`.

It is not loading anything — a genuine cold load of the 12b is 11,930 ms, two orders of
magnitude away. It is a fixed per-request cost that Ollama reports under `load_duration`.

At 27 calls per item that is 5.82 s/item, ~72% of projected sweep runtime.

**Client-side overhead is 0.65 ms.** HTTP and JSON serialization are free. The earlier
268 ms/call figure from the `127.0.0.1` measurement was this same constant plus
generation, not transport cost. Nothing in the harness can reduce this; it is server-side.

### Probe 2 — prompt eval by template, 12b-q8_0

10 items × Templates A/B/C, transcribed verbatim from §6 so `prompt_eval_count` is the
sweep's actual prompt length.

| template | prompt_tok | prompt_eval_ms | eval_tok | eval_ms | wall_ms |
|---|---|---|---|---|---|
| A | 44.0 | 62.30 | 4.10 | 75.31 | 365.81 |
| B | 38.8 | 62.07 | 2.00 | 25.12 | 318.61 |
| C | 76.8 | 75.63 | 3.90 | 71.42 | 389.55 |

Mean wall-clock for one item's full A+B+C on 12b-q8_0: **1074 ms**.

**§5c item 12 settled.** Template C `eval_count`: `100` → 4 tokens, `95` → 3 tokens.
Digits are emitted individually plus a stop token. §6 *reasoned* that C's worst case was
three digit tokens plus a stop, four total. Measured at exactly four. `num_predict = 10`
has ample headroom. Prediction confirmed by measurement — status upgraded, wording
unchanged.

**Saturation flag (weak, not actioned).** 9 of 10 Template C responses on the 12b were
`100`. These were easy questions with correct answers supplied, so this is weak evidence
and no change was made. But §10's saturation entry currently scopes the tie risk to
P(True) only; this hints the same hazard may exist in verbalized confidence, where it
would degrade AUROC by the same mechanism. Pilot should look at the C distribution.

### Probe 3 — cold load and unload, all nine cells

| model | cold load | VRAM | unload |
|---|---|---|---|
| 1b-q4_K_M | 2.15 s | 835 MB | 42 ms |
| 1b-q8_0 | 2.19 s | 1086 MB | 51 ms |
| 1b-fp16 | 2.94 s | 1979 MB | 73 ms |
| 4b-q4_K_M | 4.45 s | 2740 MB | 100 ms |
| 4b-qat | 4.28 s | 3376 MB | 119 ms |
| 4b-q8_0 | 5.46 s | 4305 MB | 145 ms |
| 4b-fp16 | 8.20 s | 7774 MB | 243 ms |
| 12b-q4_K_M | 8.21 s | 7670 MB | 247 ms |
| 12b-q8_0 | 11.93 s | 12642 MB | 391 ms |

Nine cold loads: 49.8 s. Nine unloads: 1.41 s. Total ~51 s.

**§6's "nine model loads at ~2.3s each" was the 1b's figure generalized to the roster.**
Wrong for eight of nine models, off by 5× at the top. The *conclusion* survives — 51 s
against a multi-hour sweep is negligible — but the number behind it did not.

Cold load scales with model size; unload scales with resident VRAM.

**Caveat on the unload figures.** `unload_polls` was 0 on every row, meaning the poll loop
never slept — it broke on the first `/api/ps` check. Each unload figure is therefore the
latency of a single `/api/ps` call, not a polled interval. Two readings fit: either
`/api/ps` blocks on the scheduler lock while teardown runs (likely, given the clean
scaling with VRAM), or unload is instant and `/api/ps` latency coincidentally scales with
model size (no mechanism proposed). Probably genuine, not proven. Immaterial to the 51 s
conclusion either way.

**4b-q4_K_M loads slower than 4b-qat** (4.45 s vs 4.28 s) despite being 636 MB smaller.
Single measurement per model, no repeat, so no spread — cannot distinguish a real
inversion from run-to-run variation. Not claimed as noise; the ~6% figure from the
throughput runs is a different quantity and does not transfer. Three repeat loads per
model would settle it. Nothing depends on it.

### Recomputed runtime (now in §5)

Per item across all nine cells: 5.82 s fixed (27 calls × 215.5 ms) + ~2.3 s
model-dependent (prompt_eval, eval, server_slack summed across cells) = **~8.1 s/item**.

| N | runtime |
|---|---|
| 900 | 2.0 h |
| 1500 | 3.4 h |
| 2200 | 5.0 h |

The old "4-6+ hours" figure was accidentally close for two wrong reasons that partially
cancelled: it attributed ~half the runtime to a spill that turned out to be a driver
artifact, and it omitted the largest single component entirely. Its provenance cannot be
reconstructed from any surviving table — no token-count assumption reproduces it.

### Open question (parked, not on the critical path)

**What is the 215.5 ms?** It is 72% of sweep runtime. It is uniform across all nine cells,
so it threatens no hypothesis, and the sweep is affordable at 2–5 h either way — not
chasing it before September 21. One hypothesis worth testing when there's time: it may be
tied to specifying `keep_alive` in every request body, since that touches Ollama's
scheduler on each call. Test `/api/generate` vs `/api/chat`, and with `keep_alive` omitted.

If sweep runtime ever needs cutting, three quarters of it is here.

## 2026-08-26 — Throughput re-measurement

Throughput re-measurement - 2026-08-26

Why: Adrenalin 26.8.1 released 8-17-26. Original table predated it, so the frozen driver and the measured driver didn't match. I chose to re-measure rather than just disclose.

Original table (superseded, old driver): 239.2 / 233.8 / 175.4 / 127.2 / 126.9 / 105.2 / 64.6 / 61.1 / 15.4

Run 1: normal desktop (Discord in call, Claude desktop app, VS Code, PowerShell, Adrenalin). VRAM baseline 2866–2874 MB, peak 16002 MB:
244.7 / 217.3 / 179.8 / 131.8 / 131.4 / 110.4 / 67.5 / 65.7 / 44.2

Run 2: PowerShell and Adrenalin only. VRAM baseline 2256 MB, peak 15474 MB:
234.3 / 248.7 / 184.4 / 134.4 / 132.5 / 110.6 / 67.8 / 66.0 / 43.9

Findings:

- 12b-q8_0 went 15.4 → 43.9. Not contamination - run 1 had more open and was still ~3x the old number. Driver change.

- 15.4 was ~31% of the 644 GB/s ceiling (spilling); 43.9 is ~89% (fully resident).

- Desktop applications cost ~0.7% on the critical cell (44.2 vs 43.9), inside noise. Discord was never poisoning anything.

- 1b cells inverted between runs - q4_K_M above q8_0 in run 1, below in run 2, ~6% either way. 22-token window too short.

- Peak 15474 MB against 16304 MB available. Fits with under 1 GB of margin on four 1440p displays.

Actions: AMD driver auto-update disabled 08-26-26, re-enable post-study. Run 2 frozen into section 6. Section 5 runtime paragraph and section 10 extrapolation entry both need updating.