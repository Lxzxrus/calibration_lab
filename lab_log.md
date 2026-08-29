# calibration_lab — Lab Log

*Append-only. Newest first. Raw measurements and what happened, dated.*


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