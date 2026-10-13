# `calibration_lab` — Handoff

*Operational snapshot. Drop this + the pre-registration into a fresh chat and say hello — that's enough to resume.*

**Last updated:** 2026-10-12 · **Synthesized against commit:** `28a33de` · **Status:** **Both-must-hold decided and on the page (2026-10-12, `28a33de`)** — AUROC is computed separately for P(True) and verbalized confidence, each held to its own noise floor, overall verdict the weaker of the two (prereg line 31; split-verdict table lines 66–86). Template B is therefore in the pilot of record and **B's grader-side parser is on the critical path**. **Repo PUBLIC** since 2026-10-11 — `github.com/Lxzxrus/calibration_lab`. **Runner COMPLETE** (steps 1–7, 2026-09-20); the 300-row harness-validation run at `4254e66` is **not the pilot and is deleted unopened before it**. Next: the remaining pre-pilot rules, the grader, the pilot. **Freeze date not set** — waiting on real REU deadlines; "mid-December" turned out to be an unverified placeholder.

*Session protocol lives in `SESSION_PROTOCOL.md`. Open by running its §B block.*

---

## 0. YOU ARE HERE

**The plan changed on 2026-08-31. Read this before anything else.**

Prereg prose is **paused**. Harness construction is the active work. The exception is the
set of prereg items that must exist before the pilot runs (below). The elicitation-method
rule, which several of them depended on, landed 2026-10-12. Everything else in §5c waits.

### Why

The pilot requires a harness. §5's `p_weak` / `p_strong` / `N` blanks can only be filled
by pilot data, and H2a's and H2b's thresholds are *defined* against pilot-measured noise
floors. Freeze was gated on code that did not exist. This was not previously understood
and it is the single most important correction in this file.

September 21 is the start of fall quarter — a capacity cliff, not a soft target. Calculus
plus two other courses, and a baby in November. Prose survives fragmented time; code does
not. So the last uninterrupted weeks go to the harness, and the prose moves into the
fragments where it will still work.

### Revised timeline

- **Sept 21 target: harness complete and debugged. Pilot deferred past the 21st — 2026-09-12.**
  Reasoning: the pilot is largely autonomous — start it, attend a school day, return to
  results — so it does not need the uninterrupted block. The runner and grader do.
  Consequence: §11's rule and §8's procedure stop being pre-21st and become pre-*pilot*,
  landing in the fragments exactly where this re-plan wanted the prose. Not freeze.
- **Cut line decided 2026-09-18, deadline met 2026-09-20.** Laz set runner completion as the
  hard deadline, leaving the grader for the fragments — the grader is transcription from a
  complete §6 spec and fragment-tolerant; the runner was construction and was not.
  **Checked 2026-10-08: half-landed.** Neither 09-18 lab-log entry records the reasoning; the
  09-20 entry states the deadline only. Recorded as such in the 10-08/10-10 entry. The 19th
  produced no session (house work). Step 5's last piece, step 6, and step 7 all landed on the
  20th, with the close starting at 8:30 pm rather than past midnight.
- ~~**Freeze mid-October**~~ — **overtaken.** No sessions ran 2026-09-21 → 10-07; the gap
  was zero sessions per week, the variable the estimate below already named. **A new freeze
  date needs setting, by Laz, accounting for November.**
- **2026-10-08 / 10-10: public release.** Open checks passed at `da50cea`; one discussion-only
  day (10-08), then one committing session (10-10 into 10-11) producing `94430cf`: README,
  LICENSE, CITATION.cff, two prereg amendments, handoff placeholders, lab log. Pushed to a
  new GitHub remote and made public 2026-10-11.
- **2026-10-12: elicitation-method rule decided and written** (`28a33de`). Both-must-hold,
  per-method floors, opt-for-weaker split verdicts; seven §D amendments, all logged in the
  10-12 lab-log entry.
- **Slice 4 deferred to October by design** — offline analysis against saved JSONL, no
  live state, the most fragment-tolerant work in the project. Half of it already exists
  in `ece_test.py`.
- ~~**Diagrams by end of October.** Treat November and December as near-zero work months;
  the mid-December REU application should read from a finished thing.~~ **Superseded
  2026-10-12.** Laz's stated pace goal is **three sessions a week, November included**
  (worst case one a week); two ran the week before 10-12. And "mid-December" was never a
  verified REU deadline — a July placeholder repeated as fact, this file included. REU
  sites set their own dates, many January–April; Laz is checking a shortlist, CRA DREU
  first. PNNL CCI, early January 2027, is the dated gate, and the recommenders are for CCI.
- **Harness estimate: ~12–19 sessions, now counted in work-days (see §0b). Slice 1 came in at two. Slice 2 is budgeted 6–10; its runner half is done.** Runner steps 5–7 took two work-days (09-18, 09-20) once the prereg blockers were cleared in the first half of 09-18. Roughly nine harness sessions spent against 12–19 (count carried from the 09-20 rewrite; 10-10 and 10-12 were release and prereg work, not harness), with the grader the remaining Slice 2 work.
- **The estimate is not what broke.** With roughly nine of 12–19 spent, 3–10 remain — the harness number is holding. *(Until 2026-10-12 this bullet said "roughly seven" while the one above said "roughly nine" — a stale figure left beside its update.)* What has been mis-estimated the whole time is **sessions per week**, and that variable gets materially worse on the 21st. Re-planning a date teaches nothing; naming which variable the estimate got wrong is the thing that makes the next estimate better.
- **Whole-study estimate, 2026-10-12 — Claude's, logged in the 10-12 entry as an estimate:**
  12–20 sessions to freeze, 8–15 more from freeze to posted results, roughly 45–55% of the
  way to posted results. The error lives in the §8 noise-floor procedure and the grader. At
  three sessions a week freeze is roughly 4–7 weeks out; at one a week, 12–20. Laz sets the
  freeze date once real REU deadlines are known.

### Pre-pilot mandatory items

Template B dropped from pre-21st scope — 2026-09-10

**Partly reversed 2026-09-20, at the runner level only.** Step 6 was built with all three
templates. B rows — each carrying the full top-10 candidate list for every generated token —
are in the validation run, and one was checked against the prereg's Template B text
(now lines 210–214, verbatim) and `top_logprobs = 10` (now line 246): position 0 held `False` at −0.1057 and `True` at
−3.1908, plus the `FALSE` and ` False` variants the parsing rule counts. What did **not**
change: B's parser is grader work and is still unbuilt. **Settled 2026-10-12: B is in the pilot of
record** — both-must-hold makes P(True) a verdict method, and its noise floor has to be measured. The reversal's reasoning is on the page in
Laz's words — the 09-20 lab-log entry, "Template B's reversal, and why" (verified 2026-10-08).
The 09-10 reasoning below is kept as history.

A completion threshold was set at the start of the 09-09/10 session: runner steps 3–6 done and step 7 started, or Template B leaves the pre-21st build. The session reached step 4. The pilot runs Template C only. Template B lands in October.

The cost, stated rather than discovered later: B's parser is the hard one — position 0 fixed, affirmative/negative mass summed and renormalized, retained mass logged, the empty-token-with-absent-bytes edge case — and it now gets built in fragmented time alongside coursework and a newborn.

*(Superseded 2026-10-12, kept as history.)* What survives intact: a C-only pilot still yields p_weak, p_strong, an AUROC floor, and a debugged harness, which is what §8 says the pilot is for. The spread floor and H2b are unaffected — they need the roster, not the second method.

1. **§11's interpretation rule** (the AUROC-flat-while-ECE-degrades case). Written after
   the pilot, it is post-hoc even though pilot data is discarded.
2. **§8's noise-floor procedure.** Sharper: the procedure defines *how* the floor is
   measured, and `2 × floor` is H2a's and H2b's threshold. Written after seeing a floor,
   a resample structure that yields a smaller number cannot be *proven* unchosen. Same
   standard already applied to grader-rule changes. **Three questions it must answer
   (found 2026-10-12):** how the 50-item pilot floor scales to the main-study N; whether
   the floor is for a single AUROC or for a difference of AUROCs (H2a's steps and H2b's
   spread are differences on the same items); and how H2b's spread floor is measured when
   the pilot runs two cells and the spread uses four. Per method under both-must-hold.
3. ✅ **Which elicitation method decides each verdict — LANDED 2026-10-12 (`28a33de`).**
   Both-must-hold: separate AUROCs, each against its own floor (prereg line 31); overall
   verdict the weaker per-method verdict, with the 15-row table (lines 66–86); per-method
   verdicts always reported. Averaging ruled out on line 372's precedent.
4. **§9's refusal pattern list.** Line 360 says "matches refusal patterns"; no list
   exists anywhere. The grader cannot implement the rule, and a list written after seeing
   pilot refusals is a new rule, not a code fix — the grader-rule declaration's own test.
5. **Tie-rate statement, descriptive only** — in §7 or the exclusion table. Must exist
   before any ties are seen, and must say it never changes a verdict.
6. **§10's saturation entry (line 398) extended to verbalized confidence.** It names
   P(True) only; verbalized now decides verdicts and is the larger tie risk (probe 2:
   9 of 10 Template C responses on the 12b were `100`).

### Next actions, in order

*The 2026-09-12 review gate is **discharged** — executed 2026-09-17/18, sixteen findings,
~20 amendments landed. It worked: two contradictions that would otherwise have reached
freeze were caught. Do not re-add it; the next scheduled review is a judgment call, not a
standing gate.*

0. ✅ **Elicitation-method rule** — landed 2026-10-12. **Freeze date** — still unset; Laz
   sets it once real REU deadlines are known.
1. **Pre-pilot prose, fragment-sized** — refusal pattern list, tie-rate statement, line
   398's saturation entry, §11's rule, §8's procedure (the pre-pilot list above). Also the
   B-blind resume clause at line 269 — a §D amendment naming B and C.
2. **Slice 2 — grader, now including B's parser.** Boundary matching over the union of
   normalized_value and normalized_aliases, negation detection, Template C's parser, and
   P(True)'s — position 0, renormalization, retained mass, the empty-token-with-absent-
   `bytes` case. Reads the runner file and writes the second file described at prereg
   lines 314–330. Rejoins to items_pilot.jsonl on question_id — the runner does not carry
   the answer key. Not pure transcription any more: the refusal rule needs its list first.
3. **Pilot analysis code** — per-cell, per-method AUROC, accuracy, and the floor
   computation. The pilot's six outputs are computed values, so this slice of Slice 4 is
   pre-freeze.
4. **Small runner close-outs** — resume robustness and the whitespace-only answer (§5c,
   open list). None block the grader.
5. **Pilot.** Delete `pilot_runner_log.jsonl` first, **unopened** — provenance commitment
   2026-10-12: the 300 validation rows are the pilot items on the pilot models, so they are
   not opened for any pre-pilot rule. Line 271's keep-first check hard-stops any
   `run_pilot.py` start while the file is present regardless.
6. **Then** Slice 3 (full roster), the remaining §5c prose, OSF registration, freeze.

### Estimate check — 2026-09-05

Slice 1 was the calibration probe: **1–2 sessions holds the estimate, 4+ triggers a
re-plan.** It came in at **two sessions.** The ~12–19 session harness estimate survives its
first test and remains the working number. Next checkpoint is Slice 2, budgeted at 6–10
sessions across runner and grader.

### Standing

No study data has been run. Harness code is draw_pilot.py (complete) and run_pilot.py (complete, steps 1–7, verified 2026-09-20). The 300 rows in `pilot_runner_log.jsonl` (gitignored) are harness validation at `4254e66` — not study data, not the pilot. **Not to be opened for any pre-pilot rule, and deleted unopened before the pilot of record** (2026-10-12; they were inspected 09-20 for counts, duplicates, provenance and schema only — no grading, no AUROC). Probe scripts — three probe*.ps1 plus probe4_endpoint_logprob_diff.py — and ece_test.py remain environment characterization and learning artifacts. All Ollama calls so far are environment characterization.

**Division of labor (2026-08-31; restated publicly in the README 2026-10-10).** Laz types
every line of the code, the prereg and the lab log, and accepts, rewrites or rejects every
proposal. Claude explains concepts and code, reviews for errors, and proposes text. The
handoff is written primarily by Claude, with occasional small edits by Laz (header hash,
review). Reading is both. *Corrected 2026-10-11:* this line previously read "lab log —
mostly Laz, Claude adds and edits," which contradicts the 09-20 lab-log entry ("Same rule
that's held for the prereg and this log since the start of the project") and the public
README. Laz's own statement governs. **2026-10-12, per Laz:** lab-log entries do not restate
authorship each session; the division of labor lives in the README, this file and his briefs.
Claude's 10-12 claim that the 09-20 entry set a per-entry rule was wrong — that entry was a
one-time statement about step 6.

**Recorded 2026-09-20, verified 2026-10-08:** step 6 was built in a separate ~2-hour session
with Sonnet. The 09-20 lab-log entry states it in Laz's words: "I wrote it. Every line,
every character in run_pilot.py is mine, typed in myself." On 2026-10-10 Laz added that the
same entry's "drafted proposed text for me to type" overstates it — Sonnet showed and
explained Python, which he then adapted. Not in the 10-10 entry draft Claude reviewed; the
log is append-only, so any clarification goes in a new entry.

---

## 0b. Working protocol

**Moved to `SESSION_PROTOCOL.md` (adopted 2026-08-29).** That file is now the single
home for session discipline: closing checklist, the opening `git` block, what Claude
verifies on open, the harness-phase prereg-drift rule, and the post-freeze
`git diff` integrity check.

Do not restate its rules here. If handoff and protocol ever disagree, the protocol file
governs on process; the prereg governs on content.

**Known failure mode, still live:** decisions get logged in the handoff as *landed* when
they were only *decided*. §5c is the list that catches it. Verification is against the
page, in both directions.

Protocol defect found 2026-08-31 — VERIFIED FIXED 2026-09-07. §C.1 now reads "header hash plus exactly one handoff-only commit vs HEAD," which is the corrected condition. The 08-31 protocol commit did land it. Item closed.

§E amended 2026-09-09 — the session is the work-day, not the chat. One session = one lab-log entry + one commit, daily. The handoff stays chat-scoped and is rewritten when the chat closes, which may cover several days. A work-day counts as a session only if it produces a commit; the OPEN/WORK split was retired but the committed-artifact requirement was kept. The 12–19 estimate carries over unchanged — the unit changed name, not duration.

Reasoning on the page: §F's two failures were conversation and disk drifting apart, not chats running long. The new hazard the amendment names is specific — at the end of a long chat the lab log gets written from the conversation instead of from the page, which is the 2026-08-26 failure in different clothing, and it will not feel like it, because the whole discussion is sitting right there reading like fresh recall. Same-day entries are the guard. Adopted three days late and in practice before it was written down; recorded as such.

---

## 1. What this project is

A standalone research study measuring **calibration** — whether a model's confidence matches its accuracy — on small, quantized, instruct-tuned models running on consumer hardware.

Conceptual replication of **Kadavath et al. 2022** (arXiv 2207.05221, *Language Models (Mostly) Know What They Know*), whose cleanest results were on **base pretrained** models from 800M to 52B. This study asks whether that picture survives quantization and small scale. Every roster model is instruct-tuned, so instruct-tuning is held constant, not tested — a cross-study difference from Kadavath (prereg §10), not an axis here.

**Dual audience, deliberately:** an academic portfolio artifact (a professor sees someone learning to navigate research) *and* a community finding (a reader with 8GB of VRAM learns which model at which quantization is actually trustworthy). Neither is the afterthought. This framing drives most scope decisions below.

**Research identity it serves:** *"I study whether AI systems know what they know and how humans stay meaningfully in control when they don't."*

**Timeline:** the original "first reliability diagrams by September 2026" target is overtaken (see §0). Self-imposed either way. The dated external gate is **PNNL CCI, early January 2027** — the recommenders are for CCI. The REU's "mid-December" was an unverified placeholder; real site deadlines are pending (§0).

**Public since 2026-10-11** at `github.com/Lxzxrus/calibration_lab`. The README is the front door: status banner, design at a glance, repository map, how-this-was-built disclosure, reproducing steps, TriviaQA licensing note. Public name: Nathaniel (Nate) Campbell; "Laz" in the process documents is the same person, stated in the README.

---

## 2. Frozen decisions — and why

*These are settled. The rationale is the part that doesn't survive a context reset, so it's recorded here.*

**Standalone repo, entirely separate from ARIA.** `C:\Users\legen\Projects\calibration_lab\`, own git repo, own venv. Reason: the August ARIA decision leans toward a *curated public research mirror* rather than full open-source. If `calibration_lab` lived inside ARIA, publishing it later would require history surgery on a repo containing a gitignored personal memory store. Ollama is shared, but as a service on `127.0.0.1:11434`, not a code dependency. **The harness talks to Ollama directly, never through ARIA** — ARIA's vault injection could silently prepend material to a frozen prompt template.

**Own venv, and free to pin a different Python.** ARIA is on 3.14; the scientific stack may not have 3.14 wheels. Check before committing; drop to 3.12/3.13 if needed.

**gemma3 family only.** All three hypotheses are within-family. Holding family and training recipe fixed is what makes the scale claim clean. Cross-family replication is deferred to a follow-up study, explicitly post-September.

**TriviaQA only; MMLU dropped.** Free-form trivia is closer to how people actually use models. **Consequence — load-bearing:** MC logprobs requires lettered options, so dropping MMLU drops it. Two elicitation methods remain: **P(True)** and **verbalized confidence**.

**The MMLU and `nocontext` decisions are one principle applied twice: never hand the model material that lets it succeed without knowing the fact.** Context supplies the answer to read; multiple choice supplies the answer set to pick from. The MC-specific harm is **recognition vs. recall** — with distractors, partial knowledge can produce a correct answer by elimination, so a correct MC response is *ambiguous evidence*. Under MC, confidence can track distractor quality rather than the model's own knowledge, which is a different quantity than the one AUROC is supposed to read. Free-form has no guessing floor.

**Config: `unfiltered.nocontext`, validation split.** `rc` drops questions whose retrieved evidence documents don't contain the answer, which selects for facts with strong web documentation — plausibly correlated with training-data over-representation, biasing every cell in the same direction and invisibly. `unfiltered` does not *solve* contamination; it avoids compounding it. Validation because test-set answers aren't publicly released. **Verified on HuggingFace 2026-08-16** (`mandarjoshi/trivia_qa`, validation, 4.39 MB parquet).

**Identical item set across all nine cells.** Sample once with a recorded seed, freeze to `items.jsonl`, every cell reads that file in fixed order. **Seed and file do different jobs:** the seed is provenance; the file is the guarantee. `items.jsonl` is **committed to the repo** — NOT YET DONE, see §5c.

**C = 200, held regardless of the N it implies.** Puts the AUROC noise floor around 0.02–0.03 (Hanley–McNeil), keeping `2 × floor` around 0.04–0.06. **The escape hatch was deliberately removed** — an earlier "if runtime exceeds 8 hours I'll adjust" clause triggers precisely when p_weak is lowest, i.e. when the items are most needed. Any change to C post-freeze is a §12 deviation.

**N is two-sided: `N = 200 / min(p_weak, 1 − p_strong)`, +10% exclusion margin.** AUROC needs both classes populated. The strongest cell's *incorrect* count is its thin class, so the binding constraint can silently flip ends of the roster.

**Forced response, not permitted refusal.** Permitting "I don't know" gives clean refusals, but §9 excludes refusals and the 1b would refuse far more often — differential exclusion straight into H1 and H2b. Forced guessing pollutes the correct class with lucky hits instead, but free-form has **no guessing floor**, so the pollution is small *and uniform across cells*.

**Prompt constraint over a smart grader.** A smart grader is a second measuring instrument whose errors land unevenly across cells (small models produce messier prose, so a lenient grader rescues more of the 1b's answers than the 12b's). Prompt constraint moves the burden somewhere identical across cells and makes compliance a *measurable* property. **Design: constrain hard, then a small, mechanical, auditable grader on top — never a smart one.**

**Non-compliance is counted, not eliminated.** Hedging and degenerate output at 1b are real model properties that correlate with size. They become per-cell *reported rates*. Same move applied four times now: negation, compliance, truncation, retained mass.

**Negation is detected, never corrected.** A "not"-near-alias handler has no natural stopping point, and each rule misfires more often on messy prose, i.e. more often on the 1b — rebuilding the differential-grader problem in a subtler form. Flag, log, report the rate, never touch the score.

**Grader: token-boundary matching over `normalized_value` + all `normalized_aliases`.** Not exact-match, not raw substring (short aliases hit inside longer words — `exile` inside `exiled`). **No article stripping, no prefix stripping** — boundary matching absorbs leading scaffolding for free.

**P(True): renormalize over affirmative+negative, and log the retained mass per row.** Raw True-mass conflates *uncertainty about the answer* with *failure to follow the format*, and format-following scales with model size — a size effect riding inside the measurement, and H1 is a size hypothesis. Renormalizing removes it; logging the retained mass preserves the format-following signal as a reported statistic.

**P(True): fixed position 0, exact match, no floor** (settled 2026-08-21/26, full rule now in §6).
- **Position 0, no exceptions.** Scanning forward for a matching position would rescue more items on the 1b than the 12b — differential exclusion — and searching for the position where you find what you want is a degree of freedom. Probe confirmed position 0 carries the answer at both roster extremes.
- **Strict format compliance: exact match against `{true}` / `{false}` only**, after strip-and-lowercase. Reversed an earlier lean toward prefix/stem matching: the probe showed `Truth` at 0.00024 matching `tru*` as a false positive, and showed the real variant set is narrow (`True`/`TRUE`/`true`/`[sp]True`). The prompt names two tokens, so two tokens count; semantic enumeration (`Yes`, `Correct`, `Right`) has no natural stopping point. **Empirical reversal, not aesthetic.**
- **Affirmative mass is the SUM** over all candidates normalizing to `true`. Four surface variants collapsing to one string is the normal case, not an edge case.
- **Single letters excluded.**
- **Zero retained mass → unparseable → §9 exclusion.** 0.5 manufactures a value the model never expressed; 0 treats absence of `true` as evidence for `false`.
- **No minimum-mass floor.** Structurally identical to the minimum-alias-length knob already rejected: a number with nothing to justify it from. Handled by reporting per-cell mean retained mass instead, with the instability named in §10.
- **Computed from raw logprobs at full precision** — concentrated mass can round the denominator to zero.

**P(True) framing is non-self-referential — a deliberate deviation from Kadavath.** Every call is stateless; the model has no memory of producing the answer, so "your answer" would assert something false about the context.

**Verbalized confidence: strict integer, permissive normalization** (settled 2026-08-26).
- Entire response must parse as an integer after stripping **whitespace, then trailing `%`, then leading zeros**, in that order. Divided by 100 to put it on [0,1], because ECE, Brier score and the reliability diagrams compare confidence against accuracy, a proportion. **Not** for AUROC, which is rank-only and unchanged by rescaling — this file and the prereg both carried the wrong reason until 2026-10-12 (now prereg line 236).
- **Leading zeros stripped, not rejected.** `int("085")` is total and unambiguous — no judgment, no stopping-point problem, unlike the `Yes` case. Also a reporting argument: excluding would bury a formatting artifact in the same bucket as refusals, inflating a rate the exclusion table reports as a finding.
- **`done_reason: "length"` → flag, never exclude.** The strict entire-response-is-an-integer rule plus the [0,100] bound mean a truncated response almost always fails parsing on other grounds. The flag is a check that the hazard didn't materialize, not a caveat on the numbers. **The strict rule and the flag-don't-exclude decision are load-bearing on each other.**
- Exclusion-on-`length` was considered and rejected: it fires on a *risk* rather than an absent value, and would land disproportionately on the 1b. Rejected because it buys nothing, NOT because "we can't afford differential exclusion" — that reasoning would also have kept refusals in.

**`num_predict` = 25 / 5 / 10 for A / B / C, all below 32.** On `gemma3:1b-it-q8_0`, one TriviaQA item producing degenerate repeating output returned `done: false` with **no metadata fields** at `num_predict ≥ 32`, and returned normally with `done_reason: "length"` at ≤ 31. Confirmed on Ollama 0.32.6 and 0.32.14, same digest. **Observed on a single item — two versions makes the boundary stable, not general.** Staying below it means degenerate items return cleanly with usable metadata. Above that floor, each value gives headroom over a compliant response: C's worst case is three digit tokens for `100` plus a stop token, four total. **The prompt bounds the output space, so the parser only handles what the prompt permits** — same principle as prompt-constraint-over-smart-grader.

**Grader-rule development against pilot outputs is permitted, with a stated test** (settled 2026-08-26).
- **May change:** code that fails to implement a written rule.
- **May not change:** the rules themselves. Not because changing them "skews data" — because after seeing outputs you cannot *prove* a change wasn't chosen for its effect on results.
- **The test:** does the fix make the code do what §6 already says, or does it change what §6 says? Adding `hasn t` to the negation list is a fix (§6 says detect negation; the list is the implementation). Loosening boundary matching to catch more of the 1b's prose is a rule change (§6 specifies boundary matching).
- Pre-freeze rule changes: amend and record. Post-freeze: §12 deviation, and should be near-nonexistent because the pilot runs pre-freeze precisely so the grader is debugged by then.

**KV cache `f16`, and the decision is overdetermined.** *A priori:* a quantized attention cache adds a second noise source on top of the weight quantization H2a is about, and the probabilities are the dependent variable. *A posteriori:* measured **faster** than q8_0 at all three sizes — at `num_ctx=2048` the cache is small enough that per-token dequantization overhead outweighs bandwidth savings. KV quantization pays off at 32K–128K context, the opposite regime from this study. **Those comparison numbers are from the old driver and are scoped as such in §6.**

**Flash attention: enabled, pinned, verified from the server log** — not assumed from the environment variable, since Ollama falls back silently if hardware or model doesn't support it (AMD/ROCm especially). Mathematically equivalent to standard attention but not bit-identical, so it's pinned under "inherit nothing," same as `top_k`/`top_p`. Held constant across all nine cells, so it cannot produce a differential.

**`keep_alive` replaces the `ollama stop` subprocess.** Generous within a cell, `keep_alive: 0` on the final call to each model, `ollama ps` as verification. The request field travels in the body — in code, in version control, logged per run — where an env var needs a tray restart and can silently fail to reach the running server. `keep_alive: 0` on *every* call would be wrong: it defeats the loop order and cold-loads constantly, breaking the warm-up guarantee.

**Digest and version verification, hard stop on mismatch.** Ollama tags are mutable pointers. Verify each model's digest at load against §4's frozen values; read the Ollama version at process start. Hard stop rather than warning — a warning scrolls past on a multi-hour run, and a cell computed across two different sets of weights is uninterpretable in a way no §12 disclosure repairs. **Observed once already**, when Ollama auto-updated 0.32.6 → 0.32.14 unprompted.

**AUROC is the primary metric.** All three hypotheses rest on it. Chosen over ECE because the practitioner question is "can I *trust* this model's confidence" — discrimination, not calibration. Side effect: AUROC is bin-independent, so the binning debate can't touch the hypotheses.

**Both-must-hold across elicitation methods (decided and landed 2026-10-12, prereg lines 31 and 66–86).** Every cell yields a P(True) AUROC and a verbalized AUROC; until 10-12 §3 named neither, so a verdict could have been read off whichever supported it. Averaging rejected on line 372's precedent (constructs a value the model never expressed). Primary-plus-secondary was the alternative (precedents: line 38's rung, line 334's binning). **The rule:** each method clears the hypothesis's bar against **its own** pilot-measured floor; the overall verdict is the weaker per-method verdict (H1 confirmed > suggestive > falsified; H2a supported > falsified; H2b supported > not evaluable > falsified); per-method verdicts always reported. **Accepted in advance:** verbalized saturation on the 12b can falsify H1 on that method; a tie rate may be reported, descriptively, never verdict-changing. **For the write-up:** both AUROCs share items and answers, so the methods are correlated — stricter than one, not two independent confirmations. **Consequences:** B in the pilot of record, B's parser on the critical path, six pilot outputs (line 149).

**ECE as co-primary: considered and DECLINED (2026-08-26).** The vulnerability is real — AUROC is invariant under monotonic transformations, so if quantization compresses confidence while preserving rank, AUROC reports a null that is true and misleading. Four options were weighed; **option four adopted**: keep AUROC confirmatory, and pre-register an interpretation rule in §11 stating that AUROC-flat-while-ECE-or-Brier-degrades is reported as a named finding rather than a null. Costs no new confirmatory threshold and no third noise floor; lands in §11, which needs rewriting anyway. **Only works if written before the pilot.** Co-primary was declined against the timeline; that goes in §10 as considered-and-rejected, which is judgment rather than omission.

**Accuracy measured per cell as a control.** Free, and it's the instrument that adjudicates the open mechanistic question — see §4.

**Published quants only; asymmetric ladders accepted.** Laz's reasoning, verbatim: *"What is available to me via an ollama shell command is also available to anyone reading my paper in the future."* Methodological principle, not a fallback.

**Δ for H2b is defined over q8_0 → q4_K_M**, not fp16 → q4_K_M. **`gemma3:12b` has no published fp16.** Using fp16 as the top rung would mean the 12b's Δ spans 8→4.8 bits while the 1b/4b span 16→4.8 — the 12b would show a smaller Δ *because it was compressed less*, artifactually confirming H2b. **Re-derived three separate times after evaporating between sessions — now in the prereg's Definitions block.**

**Within-model vs. across-model rung rule.** Within-model (H2a) uses every rung available at that size; across-model (H1, H2b) uses only the rung or rung pair that exists at every size.

**H1's primary quantization rung is q4_K_M.** Both exist at all three sizes, so "same quantization" left a free post-hoc choice. q4_K_M because a bare `ollama pull` resolves to it — what the target reader actually runs. **q8_0 is a declared robustness check.** **Cost, must land in §10:** at q4_K_M every model is compressed, so the headline size effect is scale *and* compression entangled.

**H2b uses endpoints, not strict monotonicity.** Three points in the predicted order occur ~17% of the time under pure noise, and a difference-of-differences is three subtractions deep. Δ(4B) is measured and **declared descriptive context, not part of the verdict**.

**H2b has a sign precondition.** All-negative Δs can satisfy `Δ(1B) > Δ(12B)` while contradicting the premise. Evaluated only if Δ(1B) > 0; otherwise **not evaluable**, not falsified. *Not evaluable* and *falsified* are distinct verdicts throughout §3. (Since 2026-10-12 the labels are confirmed / suggestive / falsified for H1 and supported / falsified (+ not evaluable for H2b) for H2a and H2b; "not supported" is retired from §3.)

**k = 2 for both H2a and H2b, committed blind 2026-08-01.** Multiplication, not subtraction — the floor is in AUROC units, k is a bare count of noise-widths. Identical k because **the differing noise floors already account for the differing noise**; a larger k on H2b would charge it twice for the same fact.

**H1 keeps hardcoded thresholds; H2a/H2b use the formula.** **Where you have judgment, use it; where you don't, defer to the instrument.**

**H2a's verdict rule: supported only if all three per-model checks hold**, with per-model verdicts reported individually regardless. A 2-of-3 outcome is a genuine finding and must not vanish under a bare "falsified" (the label since 2026-10-12).

**H2a's magnitude threshold is per-step, not total span.** The claim is that each drop in precision costs something.

**QAT arm is exploratory.** `gemma3:4b-it-qat` is **Q4_0**; the standard 4b is **Q4_K_M**. Different schemes, so the comparison moves two variables. **The QAT/non-QAT scheme split is structural across the whole family** — verified 2026-08-09 — so no bit-matched control exists anywhere in gemma3. Ollama's quantizer also refuses Q4_0.

**10 bins for ECE, dual scheme.** Equal-width primary, equal-mass robustness check. Declaring primacy in advance is required, or reporting two ECEs is a fresh degree of freedom.

**Thresholds (H1): ≥0.1 confirms · 0.05–0.1 suggestive · <0.05 falsifies.** Chosen by decision relevance, not statistical convention. **Total gap now defined** as `AUROC(12B) − AUROC(1B)`.

**Exclusion rules are mechanical, per-item decision procedures.** The "items where all models fail" rule was **deleted** — data-dependent, and it would delete the hardest, most informative items.

---

## 3. Hypotheses (§3 COMPLETE — locked 2026-08-02, amended 2026-10-12)

**Definitions block.** Δ(M) = AUROC(M, q8_0) − AUROC(M, q4_K_M). Uniform at all three sizes. fp16 rungs serve only H2a's within-model check and never enter Δ. **Both-must-hold (2026-10-12):** AUROC per elicitation method, each against its own pilot-measured floor.

**H1 (confirmatory).** As parameter count increases across gemma3 1B → 4B → 12B — same family, all sizes at q4_K_M, same prompts — AUROC increases monotonically.
*Rationale:* a larger model has capacity to store both the facts it was trained on and how reliably it holds each one; a smaller model's capacity goes to the facts themselves. So a larger model's confidence **varies** with how well it knows a given fact, while a smaller model's is comparatively flat — and that variation is what AUROC reads.
*Rationale history — do not let this regress:* drafts 1–2 circular; draft 3 named the wrong cause (knowledge → accuracy, not discrimination); draft 5 (current) cut the accuracy material and replaced "knows more of what it doesn't know" with the capacity mechanism. **Two failure modes: accuracy creep, and circularity.** Test: could you delete the rationale and lose any information beyond H1's statement?
*Prediction:* AUROC(1B) < AUROC(4B) < AUROC(12B), total gap `AUROC(12B) − AUROC(1B)` ≥ 0.1 confirming. *Band:* 0.05–0.1 suggestive. *Falsifier:* non-monotonic ordering, or total gap < 0.05.

**H2a (confirmatory, main effect).** Within each model, AUROC decreases monotonically as precision drops. Three separate per-model checks, not one interleaved chain.
*Rationale:* the confidence signal lives in fine-grained logit differences; quantization noise corrupts those before it touches the argmax.
*Prediction:* stated orderings, each step independently ≥ 2 × pilot noise floor, across all five comparisons.
*Falsifier:* any ordering other than predicted, or **any per-step gap** below the magnitude threshold. (Corrected 2026-08-26 — previously said "the change (Δ)", which misused Δ.)
*Verdict label:* "falsified" on a break at any size (was "not supported" until 2026-10-12).

**H2b (confirmatory, interaction — the most original claim).** Δ(1B) > Δ(12B).
*Rationale:* larger models have enough weights to absorb compression; smaller models have no slack.
*Precondition:* evaluated only if Δ(1B) > 0.
*Prediction:* spread ≥ 2 × the pilot-measured floor **for the spread** — a different number from H2a's.

**Split verdicts (2026-10-12, lines 66–86).** Overall verdict = the weaker of the two per-method verdicts; a 15-row table covers every pair; per-method verdicts always reported.

**E1 (exploratory, labeled).** Sweet-spot map: calibration and throughput against memory footprint. **NOT YET IN §3 — see §5c.**

---

## 4. The open mechanistic question

Does quantization degrade **the stored knowledge** or **the confidence signal that tracks it**?

The accuracy control reads out the mixture:
- AUROC drops **and** accuracy drops in lockstep → knowledge decay
- AUROC drops **but** accuracy barely moves → signal fragility
- both degrade at different rates → gray, and the ratio is measurable

---

## 5. Section status — pre-registration file

*Verified against commit `99a126d`, 2026-08-29. §4, §5, §6, §10 read directly from the file this session; §1–3 and §7–13 carried forward from the 2026-08-27 pass — re-verify next session.*

§9 re-verified against the file 2026-09-07. Two entries in this table were stale in the "logged as pending but already landed" direction and are corrected below.

**Every row below re-verified against the file 2026-09-18**, during the full prereg review. That pass read §1–§13 directly; no row here is carried forward from an earlier session.

**2026-10-08/10:** the prereg was read in full on 10-08 against `da50cea` (unchanged since `6779746`). Two §D amendments landed in `94430cf`, both logged in the 10-08/10-10 lab-log entry: line 4's author changed from "Laz" to "Nathaniel Campbell", and line 368's probe pointer corrected to `probe*.ps1 and probe4_endpoint_logprob_diff.py at the repo root; raw CSVs and probe 4's two warm-run JSON files in probe_out/`. Both were in-place edits, so no line numbers shifted. Rows below updated only where those or the new §3 gap touch them.

**2026-10-12 (`28a33de`):** seven §D amendments, all logged in the 10-12 entry — line 31 (both-must-hold + per-method floor), line 48 (H2a "not supported" → "falsified", "supported or not" → "supported or falsified"), line 58 (H2b "confirmed" → "supported"), lines 66–86 (split verdicts), line 149 (six pilot outputs), line 236 (division-by-100 reason), line 350 (per-method collision). Lines shifted +1 after line 31, +23 after the table, +24 after line 149. **Every prereg line number in this file was re-mapped against `28a33de` on 2026-10-12.**

| § | Status | What's left |
|---|---|---|
| Header | ⚠️ stale | **Half fixed 2026-09-18:** `instruct-tuning` removed from the "Study:" list — nothing tests it, every roster model is instruct-tuned, and §10 correctly calls it a confound. **Still stale:** the `frontier-scale` half, which is factually wrong rather than merely dated and needs the overlap-not-absence rework (§5c, header *frontier-scale*). `Drafted: [7-15-2026]` is a filled value inside brackets; a pre-freeze bracket scan will false-positive on it. **2026-10-10:** author line now "Nathaniel Campbell", matching README and `CITATION.cff`. |
| 1. Research question | ✅ fine | Names AUROC, scoped to gemma3 + consumer hardware. *Corrected 2026-10-12:* this row still said "stale premise — rewrite before anything else" six weeks after the 2026-08-31 correction (§5c) found §1 carries no such claim. The stale text is the header's *frontier-scale*. |
| 2. Background | ❌ unwritten | 3–5 sentences. Kadavath on base models, Tian 2023 on verbalized confidence, why small/quantized/instruct-tuned might differ, the community motivation. The stray 3×3-cell note belongs in §8 or §11. |
| 3. Hypotheses | ✅ COMPLETE | Locked 2026-08-02. H2a falsifier and H1 total-gap fixed 2026-08-26. Δ verified 2026-08-29 as the `q8_0 → q4_K_M` pair, present at all three sizes — H2b is testable. **E1 missing entirely.** Check H1's rationale for the old "uncharted" framing. Elicitation-method gap (found 10-08) **closed 2026-10-12** — both-must-hold, lines 31 and 66–86; H2a/H2b labels unified (lines 48, 58). |
| 4. Models | ✅ COMPLETE | Locked 2026-08-08. Amended 2026-08-29: the one-family line now states the recipe is fixed across all nine with QAT carrying an additional training stage. |
| 5. Datasets | ✅ COMPLETE | Runtime block rebuilt from probe data 2026-08-28; probe date corrected and load/unload figures de-duplicated 2026-08-29. **2026-09-18:** bare `seed` renamed `draw_seed` at all three draw-context mentions, ending the collision with §6's generation `seed = 42`; integrity rule added (now line 152) — fixed before `draw_main.py` first runs, recorded in `items_manifest.json`, and the first draw at that seed is the draw. Three brackets outstanding (`p_weak`, `p_strong`, `N`) — pilot fills them. **`draw_seed`'s value does not exist anywhere yet.** **2026-10-12:** pilot outputs four → six (line 149). |
| 6. Procedure | ✅ **COMPLETE** | Content, structure, consistency. Findings block, `load_duration` threshold line, and loop-order block rewritten 2026-08-29 to cite rather than restate. Templates fenced 2026-09-10, prompt text byte-identical. **2026-09-18:** `top_logprobs` pinned (now line 246, Template B only) and logged per row · `attempt_count` added (now line 320) · exclusion reason added to the Grader Spec per-row list · runner/grader split stated once, generally (line 263) · three more restate-vs-cite duplications killed (Truncation detector, Compliance detector, and the contamination/`load_duration` pair) · contamination source 1 relabelled `first-in-loop`, resolving an apparent contradiction with the mid-run-reload check · "never analyzed" → "never enters the study's results". **Landed 2026-09-18 evening (`6779746`):** the four §D blockers plus three issues the page surfaced — elicitation-method values `'answer'`/`'p_true'`/`'verbalized'` (line 320); model tag, digest and quantization per row; keep-first dedup with a commit-hash/Ollama-version hard stop, `run_id` considered and declined (line 271); dirty-tree hard stop with gitignored logs (line 283); runner file / grader file split (lines 314–330); `timed_out` (line 322); resume on any well-formed row, success or failure (line 267); terminal-A-failure resume clause (line 269). **New gap 2026-09-20:** line 269 names only the C call; B now runs too (§5c, resume clause). **2026-10-12:** line 236's division-by-100 reason corrected; line 236 also states the leading-zero rule twice (consistency review). |
| 7. Metrics | 🟡 partial | No throughput or memory-footprint metric, so nothing feeds E1. Tie-rate statement (descriptive only) owed here or in §9's table — pre-pilot. Line 338 names no method; line 31 now governs. |
| 8. Analysis plan | 🟡 partial | Needs the per-hypothesis walkthrough **and the noise-floor measurement procedure**. **Landed 2026-09-18:** the H1-versus-measured-floor collision is now disclosed rather than silent — if `2 × floor` meets or exceeds H1's fixed 0.1, H1 keeps its threshold (an intentional design choice, not an oversight) but the verdict is reported alongside a note that H1 and H2a/H2b no longer share a comparable standard of evidence. **2026-10-12:** the collision rule is now per method (line 350, "either method's"). The procedure itself is still unwritten; the three questions it must answer are in §0. |
| 9. Exclusion rules | ✅ **COMPLETE** | Timeout filled at 90s. no_valid_response is done: false only. Mean-retained-mass and truncation-rate columns exist. **2026-09-18:** `excluded-no_valid_response` column added (exclusion table now at line 366) — the table had carried three reason-code columns against §9's four codes since a much earlier session, and survived two prior passes. **Gap found 2026-10-12:** the refusal rule (line 360) has no pattern list — pre-pilot. |
| 10. Confounds | ✅ near-complete | **Rewritten 2026-09-18.** All four template scaffold bullets replaced with real content; the orphan fragment became a real differential-exclusion entry citing §8's mechanism and bias direction; contamination bullet rewritten (concedes magnitude scales with size, follows it into AUROC, threatens H1 specifically, spares H2a/H2b on the shared-baseline argument); quantization-confounded-with-scale added; instruct-tuning reframed from a false within-roster claim to the real cross-study one; extrapolation limit split. `qwen3`/MMLU gone. **Two small things left:** the instruct-recipe fact is stated twice (lines 390 and 400), and bullet formatting is mixed. ECE resolved as *not* §10 — it is §11's unwritten rule. **2026-10-10:** the replicator pointer (now line 392) corrected (probe 4 is `.py`; `probe_out/` also holds JSON). **2026-10-12:** the saturation entry (line 398) covers P(True) only; extend to verbalized — pre-pilot. |
| 11. Null result | ❌ **placeholder** | Records the ECE decision but not the rule — it announces a rule for the AUROC-flat-while-calibration-degrades case and never states it. Needs full redesign — three hypotheses can null independently, and H2b can come back *not evaluable*. Option-four interpretation rule lands here. |
| 12. Deviations | ✅ ready | Empty by design until freeze. |
| 13. Freeze | ⏳ blocked | Three §5 brackets until the pilot. `items.jsonl` not yet committed. **OSF (decided 2026-10-12):** register the prereg on OSF at freeze, post results to the OSF project at completion; nothing registered yet. Line 432's mechanics name only the git tag — add the OSF step before freeze. |

---

## 5b. §6 contents (COMPLETE — reference map)

Order: **environment → findings → templates → parsing rules → parameters → throughput → harness → negation → grader spec → grader-rule declaration → logging**

- **Environment** — hardware spec, display config, Ollama version, KV cache (full, with driver-scoped numbers), flash attention
- **Findings** — probe results · logprobs raw not temperature-scaled · `top_k` doesn't truncate reporting · cold ≠ warm · degenerate generation · `num_ctx` pinning cost (driver-scoped)
- **Templates** — A/B/C, Kadavath non-self-referential note, flag/exclusion lines
- **Parsing rules** — P(True), then verbalized confidence
- **Parameters** — `num_predict` 25/5/10 with the 32-boundary justification, `num_ctx` 2048, temperature 0, `top_k` 64, `top_p` 0.95, seed 42
- **Throughput** — Conditions / Table / Readings / Contamination sources
- **Harness requirements** — 11 entries
- **Negation marker list** — 17 markers, 4-word window, observational
- **Grader spec** — normalize, match, four flags with parallel definitions
- **Grader-rule declaration** — may/may-not change, the test, pre- vs post-freeze, pilot isolation
- **Logging** — per run (11 fields), per row (5 categories)

---

## 5c. DECIDED BUT NOT YET WRITTEN — and OPEN

*Items leave these lists only by landing on the page, or — for the open list — by being decided, "considered and declined" included. Nothing else.*

**Restructured 2026-10-12.** Until now one numbered list held both decided-but-unwritten items and genuinely open decisions, which is how the elicitation-method question sat under "decided" for four days. Now two lists, items named by content. **Numbering retired** — the numbers meant nothing on Laz's side. The closed records below are history and still cite the old numbers; landed items have been removed from the lists, and their records stand.

**Closed 2026-08-29:** §5 runtime paragraph (landed). §10 ECE-declined entry (**resolved as not §10** — §7 already reports ECE with its binning spec, so nothing is hidden from a reader; the real gap is §11's unwritten rule, now item 6). Lab-log placement (**committed**). Template C `eval_count` (measured — four tokens, §6's reasoning confirmed).

**Closed 2026-08-31:** none. Prereg untouched — the session was environment and harness.

Closed 2026-09-10 (both pre-pilot, both landed on the page, both logged as §D intentional amendments same session):

§6 templates fenced. A/B/C moved into fenced code blocks with labels and list bullets outside the fence. The two-space continuation indentation on B and C was markdown list-continuation, not prompt content, and is gone. Prompt text is byte-identical before and after, verified by repr() on the raw file lines — a formatting change, not a §12 candidate. Motivation: the document could not previously prove which reading was intended, so the frozen prompt was not unambiguously specified.
§6 whitespace-strip rule. Raw Template A output is stripped of leading and trailing whitespace only — no punctuation removal, no case folding, no article stripping — before entering the [Answer] slot in Templates B and C. Reasoning on the page: whitespace behavior correlates with model size, so a whitespace-sensitive prompt would put a size effect inside the instrument on a size hypothesis; and .strip() is total and unambiguous, no threshold to pick and no stopping-point problem — the same test that permitted leading-zero stripping and rejected the alias-length knob.

**Closed 2026-09-18** — items 2, 3, 4, 5, 7, 9, 12 and 16, plus six findings that were never on this list. All §D intentional amendments, all recorded in `lab_log.md` the same session:

§10 rewritten end to end — four scaffold bullets replaced with real content, the orphan fragment resolved into a differential-exclusion entry citing §8, contamination bullet rewritten, quantization-confounded-with-scale added, instruct-tuning reframed, extrapolation limit split. §9's exclusion table gained its fourth reason-code column. `top_logprobs` pinned and logged per row. `attempt_count` and exclusion reason added to the row schema. `draw_seed` named and given an integrity rule. The runner/grader split stated once, generally. Three restate-vs-cite duplications killed. Two contradictions resolved — `load_duration` and the pilot's "never analyzed". The post-study TODO moved out of §12 into `POST_STUDY_TODO.md`, committed.

**Closed 2026-09-18 evening (`6779746`), all §D intentional amendments:** the four §D blockers (elicitation-method values, digest/model-tag/quantization scope, harness commit hash + keep-first with `run_id` declined, dirty-tree hard stop) and three found by reading the page instead of this file — runner/grader field split, the resume rule's re-roll hole ("completed" → "every well-formed row, success or failure"), and the A-failure resume clause. Plus item 22 below. Two internal line-number references removed from the prereg in favour of named references.

**Closed 2026-09-20:** none on the page — code-only session. Items 22 (code side) and 21 (partially) moved in `run_pilot.py`.

**Closed 2026-10-10 (`94430cf`):** none of the numbered items below. Two unlisted §D amendments landed — prereg line 4 (author) and line 368 (probe pointer) — both logged the same session. **Considered and declined:** a fallback for running `run_pilot.py` outside a git checkout (line 31's `git rev-parse HEAD` crashes on a ZIP download). Documented in the README as a requirement — clone with git — rather than changed in the harness, since a run with no commit hash would have no provenance.

**Corrections to this list, 2026-08-31 (verified against the file):**

- **Item 1 was mis-scoped.** §1's research question (line 19) contains no "uncharted"
  claim; it scopes to consumer hardware, which is true. The only stale text is the header
  **Study:** line — *"Does **frontier-scale** calibration behavior survive…"* Kadavath
  topped out at 52B. That is a **one-line fix**. The overlap framing has no home in §1;
  it belongs in **§2, which is empty**. Item 1 was filed as a §1 rewrite and is actually a
  one-line §1 edit plus a §2 authoring job.
- **Item 5 is partly void.** No `[others]` placeholder exists in §10. The four scaffold
  bullets (lines 331–334) are still there.
- **The "~2.3s is gone from the document entirely" claim is false** — in this file's §0
  as of 08-29 and in the 08-29 lab-log entry. §5 line 122 carries "~2.3 seconds
  (prompt_eval, eval and server_slack summed across the nine cells)." Different quantity
  from the dead one — the 1b cold-load figure generalized to the roster — same digits.
  The sweep killed the load figure; the runtime component is live and correct.

**Closed 2026-10-12 (`28a33de`):** the elicitation-method rule (old 37) and B in the pilot of record (old 29), decided and written — both-must-hold, per-method floors, split verdicts, seven §D amendments. Removed from the list body as already landed: old 2, 3, 4, 5, 7, 9, 12, 16 (closed 09-18) and 22 (closed 09-18/20).

### Decided, not yet written

**Pre-pilot:**
- **§11's option-four interpretation rule.** Currently a placeholder that announces a rule and never states it. Post-hoc if written after the pilot.
- **Tie-rate statement, descriptive only** (decided 2026-10-12). Location open: §7 or the exclusion table. Must say it never changes a verdict.
- **§10's saturation entry extended to verbalized confidence** (line 398, decided 2026-10-12). Verbalized now decides verdicts and is the larger tie risk.
- **Resume clause names only the C call** (line 269). Since 2026-09-20 the runner also makes a B call per item and skips it on a terminal A failure — code ahead of the page. Line 259 already says the answer feeds "both Template B and C". §D amendment: make 269 say B and C, and check the page for other C-only phrasings written while B was deferred.

**Before freeze:**
- **Header *frontier-scale* and §2's overlap framing.** Line 3 still says *frontier-scale*; Kadavath topped out at 52B, and the roster's 1b and 12b overlap two of his four sizes. A one-line header fix plus authoring §2 (empty) around overlap, not absence. Read Proskurina et al. 2024 first (below). `instruct-tuning` already came out of the line on 2026-09-18.
- **Proskurina et al. 2024**, *When Quantization Affects Confidence of Large Language Models?* (NAACL Findings 2024, arXiv 2405.00632). Not yet read. Found 2026-10-10. Directly on quantization and confidence, so it belongs in §2 and bears on how the contribution is framed (one family, three sizes, published consumer quants, crossed design, pre-registered falsifiers — not "nobody has looked"). Check its method overlap before citing.
- **§3: E1, and §7: throughput + memory-footprint metrics** to feed it.
- **`items.jsonl` committed** — §5 promises it (line 139).
- **OSF step in §13** (decided 2026-10-12). Line 432 names only the git tag; add the OSF registration and a place for its DOI.
- **`qf_1637` needs two entries.** (a) §5: one line stating the row is dropped at draw time, by id, as a source defect — question and answer entity do not correspond (a roadrunner question wired to static-library answers), `value` is the fragment `'(a'`, `normalized_value` blank. Dropped before any model runs, so it is **not** a §9 exclusion and must not enter the exclusion table. (b) §10: rows mis-wired *without* blanking a field are undetectable mechanically — an unquantifiable dataset-quality limitation, uniform across cells, with `qf_1637` as the existence proof.
- **§10's off-label entry, with its measured number.** Alias-set size across the validation split: **min 1, max 214, mean 11.7.** The 214 is `sfq_9993` — every Google country-code domain plus scraped typos (`gogole com`, `giigke cin`). No cap applied: an alias-count threshold is the same unjustifiable free parameter already rejected for minimum alias length and minimum retained mass.
- **§10: TriviaQA construction artifacts are a pattern, not three coincidences.** Three distinct fields carry leftover machinery from dataset construction: the **answer wiring** (`qf_1637` — a valid answer entity attached to the wrong question), the **`value` field** (`'(a'` on qf_1637, `"A: Basketball"` on tc_543), and the **`question` field** (`qw_402` — CSV escaping never stripped: the whole question wrapped in quotes with `""` doubled around an internal title). Written as one dataset-quality entry with three instances, alongside the off-label alias entry above. All uniform across cells, so none can produce a differential.
- **§5: `draw_pilot.py`'s output is destructive on re-run.** The script opens `items_pilot.jsonl` and `items_manifest.json` in `'w'` mode. Harmless while `DRAW_SEED` and `PILOT_N` are fixed — same inputs, same output — but a live risk if either changes. Git catches it; the hazard is worth one line where §5 describes the frozen item set. **Extended 2026-10-10:** even at the same seed, a re-run always dirties the tree — `items_manifest.json` records a fresh `datetime.now()` timestamp, while `items_pilot.jsonl` is rewritten byte-identical. The dirty-tree check (line 283) then refuses the pilot until `git checkout -- items_manifest.json`. The README's Reproducing section documents the restore step; the prereg does not yet.
- **§10 states the instruct-recipe fact twice** (lines 390 and 400), introduced by the 2026-09-18 rewrite; bullet formatting in that section is mixed.
- **§11's closing sentence trails off mid-thought**, no terminal punctuation. Separate from the option-four rule, which is the unwritten rule itself.
- **Line 236 states the leading-zero rule twice** — once in the opening sentence, again as "Leading zeros are stripped." before the 085 example. Keep the reasoning, drop the restatement. Consistency review (noted 2026-10-12).
- **The 08-28 lab-log line** saying scripts and CSVs are both under `probe_out/` — the scripts are at repo root. The log is append-only, so the correction goes in a new entry.
- *Optional:* §10's roster-asymmetry entry could be reworded — "the shape across the two steps on the 1b and across the two steps on the 4b" is clumsy. Content is correct.
- *Optional:* re-run the three 1b cells at higher `num_predict` for a longer timing window, so every row in the throughput table means something.

### Open — not yet decided

**Pre-pilot:**
- **§9's refusal pattern list** (line 360; found 2026-10-12). No list exists. The grader cannot implement the rule without one, and a list written after seeing pilot refusals is a new rule.
- **§8's noise-floor procedure.** Unwritten. Must answer: how the 50-item pilot floor scales to the main-study N; single-AUROC floor vs difference-of-AUROCs floor; how H2b's spread floor is measured when the pilot runs two cells and the spread uses four (more pilot cells — cheap at ~4 min per 300 calls — or a derived floor with a stated assumption). Per method, so twice.
- **G: does a terminal Template A failure need a fifth §9 reason code?** Open since the 2026-09-12 lab log. §9's codes all describe the confidence call; an A failure removes the item from the B and C cells with no code saying so. Grader-session decision.
- **Whitespace-only Template A answer.** `.strip()` gives `""`, which is not `None`, so B and C run with an empty `[Answer]`. Arguably correct — the runner records, the grader's compliance detector decides — but no text on the page has considered the case.

**Before freeze:**
- **The freeze date.** Laz sets it once real REU deadlines are known (§0).
- **`draw_seed`'s value.** The integrity rule is at line 152; the number exists nowhere. Not blocking — `draw_main.py` can't be written until the pilot reports p_weak and p_strong — but the value is arbitrary and could be chosen now, which would make the commitment checkable rather than declared.
- **§6: KV cache has no verification path.** Line 168 pins f16 with a methodological reason — quantizing the cache adds a second noise source on top of the weight quantization H2a is about, and the probabilities are the dependent variable. Line 318 lists KV cache type as a per-run logged field. The Ollama version and the digest each get a hard stop (line 283) for a weaker version of the same risk, and KV cache is a server-level setting — the same class of thing that already drifted once. Whether the API reports cache type is unchecked; line 170 solves the analogous problem for flash attention by reading the server log at model load. **Finding 1 of the 2026-09-18 review.** **Partly moved 2026-09-20:** `run_pilot.py` now declares `KV_CACHE_TYPE = 'f16'` and writes it on every row. Still no verification path — the code comment says "verified via server log," but nothing in the code reads the log. The row records what was *set*.
- **Digest verified at startup, not "at the point of load, once per model"** (line 283). `run_pilot.py` checks `/api/tags` for both models before any call. Defensible, since nothing can change the weights mid-process without the hard stops firing on the next run, but the code and the line disagree. Move one of them.
- **`keep_alive: '5m'` on measurement calls** equals Ollama's default. Line 281 says "generous within a cell." The validation run had zero mid-cell reloads, so it held at pilot size; whether 5m is the frozen value is undecided.
- **Warm-up and unload prompt text** (`'Hello'`, `num_predict` 1) is harness detail with no home on the page. Line 261 says "output is discarded" and nothing more. Probably fine as code-only, but that is a decision, not a default.
- **Template text is duplicated between §6 (now lines 204–226) and `run_pilot.py`'s `prompt_a` / `prompt_b` / `prompt_c`, with no automated equality check.** B joined the duplication 2026-09-20; its text was checked by hand. Code must hold the literal string, so there is no citing out of this one. Byte-matched by hand 2026-09-12; the only guard is a comment. Same shape as the digest-prefix check and strictly more load-bearing.
- **Digest prefix equality check in `run_pilot.py`** — deferred deliberately 2026-09-18. §4's table carries 12-character prefixes, the code carries full 64-character digests. Optional hardening, not a live bug.

**Before the main sweep (not the pilot):**
- **The keep-first commit-hash stop collides with daily commits** (found 2026-10-08). Line 271 hard-stops a resume onto rows from a different commit; SESSION_PROTOCOL §E requires a commit every work-day; line 283 hard-stops on any uncommitted edit. So an interrupted run becomes un-resumable once the repo changes before resume — a commit trips 271, an uncommitted edit (a lab-log note typed while the run is down) trips 283. The main sweep (2–5 h, §5) is exposed; the pilot (~4 min) effectively isn't. The obvious fix — hash the harness files instead of HEAD — undoes the 09-12 reasoning that the repo-level hash is what pins the prereg's template text. **A decision, not a bug fix.**
- **Resume robustness.** A line that parses as JSON but lacks a key (`question_id`, `raw_response`, `harness_commit_hash`) raises a `KeyError` and stops resume, rather than being discarded like a malformed line. Found 2026-09-20; not hit in any run. Code fix; the open part is whether such a line is discarded or is itself a hard stop.

---

## 5d. §10 accumulated list

benchmark contamination (gemma3 has likely seen TriviaQA) · quantization confounded with scale · **H1's primary rung is q4_K_M, so the headline size effect is measured on compressed models throughout** · vision asymmetry (1b text-only; 4b/12b multimodal) · context asymmetry (32K vs 128K) · differential exclusion across cells threatening H1/H2b · thin positive class on the weakest cells · **floor compression: if the 1b's AUROC at q8_0 is near 0.5 it has little room to fall, squeezing Δ(1B) and biasing against H2b** · **saturation: the 12b pinning near 1.0 risks ties in P(True); ties push AUROC toward 0.5, biasing against H1 for reasons unrelated to the capacity mechanism — the mirror of floor compression, different mechanism, different hypothesis; **on the page for P(True) only — extend to verbalized confidence, the larger tie risk and now verdict-deciding (2026-10-12)**** · **both AUROCs share items and answers: the methods are correlated, so passing both is not two independent confirmations (2026-10-12)** · **the k × noise-floor rule is a heuristic; bootstrapped CIs are the clean version, and if not implemented that must be stated** · QAT arm not bit-matched · **extrapolation limit, driver-aware version** (landed 2026-09-18) · H1's "bluffs less" contested in literature · **cold-load logprob variance observed once (n=1)** · **the AUROC noise floor is estimated via Hanley–McNeil pre-pilot; the pilot's measured floor governs** · **`unfiltered` avoids compounding contamination but does not remove it** · **degenerate generation at 1b: some "incorrect" answers are non-answers rather than wrong facts** · **forced response puts lucky guesses in the correct class; uniform across cells** · **TriviaQA used off-label** — built as a reading-comprehension benchmark, so its Wikipedia-harvested aliases are deliberately permissive; closed-book generation makes that permissiveness a false-positive hazard · **the `value` field carries scraping artifacts** (`"A: Basketball"` on tc_543) — `normalized_value` is canonical · **throughput numbers are only valid on an otherwise-idle GPU with the previous model unloaded** · **low retained mass produces a renormalized value computed from tail probabilities, less stable than the same value from dominant ones; a minimum-mass threshold was considered and rejected as an unjustifiable free parameter** · **ECE co-primary considered and declined against the timeline** · **throughput measured on one driver version; a driver update moved the largest cell from spilling to resident**

---

## 5e. Harness state

### Environment — committed 2026-08-31

Python **3.12.8** (`AppData\Local\Programs\Python\Python312`), `.venv` in repo root.
ARIA's Python deliberately not used — §2 already frees this repo to pin its own. All
packages installed as **prebuilt wheels, no source builds**: requests, datasets, pandas
3.0.5, pyarrow, numpy 2.5.2, scikit-learn, matplotlib. `requirements.txt` frozen.
`.gitignore` covers `.venv/`, `__pycache__/`, `*.pyc`, `.env`, and `tempCodeRunnerFile.py`.
The `data/` rules were removed 2026-09-06 as structurally dead — see §11. PowerShell
execution policy `RemoteSigned`, `CurrentUser` scope.

**pandas 3.0 is a major release** — most examples online are written for 2.x. Unexpected
errors from copied tutorial code have this as a likely cause.

### Dataset facts (measured 2026-08-31)

Validation split, `unfiltered.nocontext`: **11,313 rows**, `question_id` unique across all
of them and used as the key. `entity_pages` and `search_results` empty — `nocontext`
confirmed by observation, not by config name.

Pool math against `N = 200 / min(p_weak, 1 − p_strong)` +10%: p_weak 0.10 → N ~2,200 ·
0.05 → ~4,400 · 0.03 → ~7,330 · 0.02 → ~11,000. Pool after pilot withdrawal is **11,262**.
Comfortable unless the 1b lands near 2% accuracy.

### `items.jsonl` — design frozen 2026-08-31

**Five fields per row:** `question_id`, `question`, `normalized_value`,
`normalized_aliases`, `value`.

- **`value` kept on self-containment, not audit.** It is a verbatim copy that cannot go
  stale, and it is the field that reveals corruption (`'(a'` on qf_1637, `"A: Basketball"`
  on tc_543). Without it the frozen artifact is not gradeable or inspectable without
  re-fetching the source.
- **`answer.type` dropped.** Nothing uses it. Carrying it creates unlabeled exploratory
  optionality, which cuts against E1 being the only labeled exploratory.
- **Draw index dropped.** The file is committed and frozen, so `git diff` already catches
  reordering. An index field is a second, weaker version of a guarantee already held —
  same reasoning that killed the minimum-mass floor.

**Provenance goes in a sidecar `items_manifest.json`, not a JSONL header line.** Header was
preferred initially for readability; JSONL's one-object-per-line rule forces the manifest
onto a single ~400-character line — the least skimmable form — and every consumer would
have to special-case line 1 (`for line in f` breaks; line counts go N+1). Same commit,
same tag keeps the two files together. Manifest contents: date and time first, then
dataset, config, split, draw label, `draw_seed`, source row count, skipped ids,
items drawn.

**Pilot exclusion is subtraction, not rejection sampling.** Drop `qf_1637` → draw 50 with
`draw_seed` → **remove those ids from the pool** → draw N later from the remainder.
Deterministic, no collision possible, no loop.

**Pilot is one draw of 50, run on both extremes** (`1b-q4_K_M`, `12b-q8_0`) — mirrors the
identical-item-set design and makes `p_weak` and `p_strong` directly comparable. Settles
the ambiguity in §8's wording.

**`items_pilot.jsonl` must be committed before the pilot runs.** The main draw reads it to
build the exclusion list. Uncommitted, "these 50 were withheld" rests on memory.

**Two scripts** (`draw_pilot.py`, `draw_main.py`), duplication hazard accepted and named:
the row shape will live in two places, and a change to one that misses the other produces
mismatched shapes that fail late in the grader rather than crashing. Fix when it bites —
shared logic in a third file, imported.

**`draw_seed` is distinct from §6's generation seed 42** and named `draw_seed` in the
manifest so no one later thinks one number did both jobs. **Value not yet chosen.**
Note: at temperature 0 decoding is greedy, so seed 42 does approximately nothing —
it is pinned under "inherit nothing," not because it is load-bearing.

### `draw_pilot.py` — COMPLETE 2026-09-05

Runs end to end: loads the split, filters `qf_1637` by id, shuffles with `DRAW_SEED`,
selects `PILOT_N`, reshapes each row to five fields, writes `items_pilot.jsonl` and
`items_manifest.json`. Constants at top (`DRAW_SEED = 8`, `PILOT_N = 50`, `DATASET`,
`CONFIG`, `SPLIT`, `DRAW`), an `assert` after each stage, and comments carrying reasoning
rather than mechanics.

**`DRAW_SEED = 8`**, chosen before any item was seen. **Reproducibility verified:** three
consecutive runs returned `odql_4374` at index 0. That is the evidence behind every
replication claim about this file — a replicator running seed 8 gets the same 50 items,
not a similar sample.

**Order is load → filter → shuffle → select.** Shuffling before selection is what makes the
draw a random sample rather than TriviaQA's storage order; filtering before shuffling is
what makes `qf_1637` unselectable.

**Filtered by id, not by blank `normalized_value`:** the blank is a symptom. If the source
is ever revised, a symptom-based filter silently changes what it removes.

**`.select(range(PILOT_N))` over `shuffled[0:50]`.** `.select()` returns a Dataset;
bracket-slicing returns a **dictionary of columns** — five parallel lists, not 50 rows.
The write step walks rows, so rows are the shape to keep. Re-zipping parallel lists by
index is where off-by-one misalignment between questions and answers would come from.
Third encounter with the row/column split (also `dataset[0]` vs `dataset['question_id']`,
and `row['answer']['normalized_value']` vs the column form).

**Committed artifacts:** `items_pilot.jsonl` (50 lines, verified on disk) and
`items_manifest.json`. The manifest's nine fields are all **derived from the run**, never
typed — a hand-entered seed that disagrees with `DRAW_SEED` is worse than no manifest.
`items_pilot.jsonl` is what `draw_main.py` will read to build its exclusion list.

**Manifest as written 2026-09-05:** timestamp `2026-09-05T21:10:50`, dataset
`mandarjoshi/trivia_qa`, config `unfiltered.nocontext`, split `validation`, draw `pilot`,
`draw_seed` 8, `source_rows` 11313, `skipped` `["qf_1637"]`, `items_drawn` 50.

run_pilot.py — steps 1–7 COMPLETE, 2026-09-20

*Described from the `run_pilot.py` uploaded mid-session on 2026-09-20. **Re-checked
2026-10-08 against the committed file at `da50cea`** (unchanged through `94430cf`; `28a33de` was meant to carry only the prereg and lab log — confirm at next open): strip on
both live and resume paths (lines 106, 275), `KV_CACHE_TYPE` declared and never verified
(line 28), `keep_alive: '5m'` (line 153), the item-30 `KeyError` exposure (lines 103, 106,
107) and the item-31 whitespace case (line 275) — all as described below.*

Separate script from draw_pilot.py by design: the draw produces a frozen artifact from fixed inputs and opens its outputs in 'w'; the runner reads that artifact and appends. Fusing them would re-run the draw on every debug cycle and rewrite the committed item set.

Step 1 — read. Opens items_pilot.jsonl in 'r', json.loads per line, keeps question and question_id only. Answer fields dropped deliberately: the grader rejoins on question_id against the frozen file, so the answer key has one home. Asserts 50 against PILOT_N.

Step 2 — version and digest hard stop. GET /api/version against a frozen OLLAMA_VERSION; GET /api/tags for the roster. Nested search with a per-model flag and break; distinct exits for wrong digest and model absent. Full 64-char digests. The *observed* digest is stored and logged, not the frozen constant — the runner records what it saw.

Steps 3–4 — the A→B/C chain. Now inside `run_call` (below). The answer is stripped before entering `[Answer]`, in both the live path and the resume path. **The strip was lost once in the step-6 refactor** and 300 rows were generated with unstripped answers before it was caught in review; they were deleted and re-run.

Step 5 — one row per call. `per_run_fields` (the nine per-run fields) is built once and copied into every row, then identity, response, timing and raw fields are added. `top_logprobs` is `None` on A and C, `10` on B. On a timeout, `done`, `done_reason`, timing and raw response are left out entirely rather than written as null (line 322). On `done: false`, each response field is logged if present — line 322 only promises absence on a timeout. One shared `base_options` object feeds both the request and the row, so the row cannot claim a value that wasn't sent. 90-second timeout, one retry, `attempt_count` recorded, `done` checked before anything else is read, Ollama error responses crash loudly as harness faults. Rows appended and the file closed per row.

Step 6 — the loop. Outer loop over models, inner over items (line 277). One warm-up per model on every start and resume, output discarded, checked for `done`. A → B → C per item; a terminal A failure skips B and C. Resume collects triples from every well-formed row and skips them; a malformed line is discarded. After each model's items, `unload()` sends `keep_alive: 0` and polls `/api/ps` up to five times until the model is gone, else hard stop. Measurement calls carry `keep_alive: '5m'` explicitly.

Step 7 — startup checks. `git status --porcelain` must be empty or the run hard-stops (line 283); the gitignored log does not appear in it. If the output file already has rows, their commit hashes and Ollama versions must all equal this process's, or hard stop (line 271).

**Tests, 2026-09-20, all passed per Laz.** Forced timeout (`timeout=0.001`): A row with `timed_out: true`, `attempt_count: 2`, no B or C row for the item. Dirty tree: stops on an edited tracked file, proceeds when reverted. Hash mismatch: refused to resume onto rows from an older commit.

**Validation run at `4254e66`, verified 2026-09-20 by Laz's pasted output:** 300 rows · 100 each of `answer` / `p_true` / `verbalized` · 0 rows with `timed_out: true`, `done: false` or `attempt_count: 2` · 0 rows with a 10+-digit `load_duration` (no mid-cell reload, line 273) · row `harness_commit_hash` equal to HEAD. First row's `load_duration` 0.23 s against a 3.52 s cold load measured 2026-09-18 — the warm-up works. Position 1 of the first B row contains a candidate with an empty token string and no `bytes` key — the edge case line 275 says the parser must tolerate, now observed in real data. **Provenance, 2026-10-12:** these rows are the 50 pilot items on the two pilot models — pilot data in everything but name. Not opened for any pre-pilot rule; deleted unopened before the pilot of record.

**False-provenance incident, 2026-09-20.** An earlier 300-row run at 17:20 was stamped `ffd3e78` (the 09-18 step-5 commit) while the whole step-6 loop was uncommitted. Every row claimed code that did not produce it. Found in review the same evening, before the dirty-tree check existed — line 283's reason, measured rather than argued. Those rows were deleted.

Dedup rule for the append-only output: keep-first — on the page since 2026-09-18 (line 271), enforced in code since 2026-09-20. First occurrence wins; a re-run never replaces an observation already made, which closes the "re-run until it looks better" degree of freedom. Precondition: only valid within an unchanged harness, so the row must carry enough to prove that — digest, Ollama version, generation parameters, and the harness's own git commit hash. Rows from two harness versions are a discard-and-re-run question, not a dedup question. Append order is itself arrival order, so the rule is executable without a timestamp.

Endpoint: /api/chat — settled with evidence 2026-09-10

/api/chat, not /api/generate. Two reasons, neither numerical: every §6 logprob finding was measured on /api/chat, and the roster is entirely -it, so chat templating is what the models were tuned on. /api/generate also returns a context field of raw token ids that /api/chat does not.

The probe that settled it, and its correction. A first comparison showed every logprob diverging between endpoints on identical text and was written up as a finding. It was cold-load contamination: load_duration 2.52 s on the generate call against 0.24 s on chat — a cold load against the ~215.5 ms warm constant. Re-run warm-vs-warm, logprobs were bit-identical at all 12 positions. So the endpoints agree numerically on a warm model, and the endpoint choice rests entirely on the two arguments above.

Two things this bought. §6's finding #3 (cold ≠ warm) reproduced independently on a different model, a different prompt and a different quantity — the original was n=1 on the cold side. And the discarded warm-up call gained a second justification, which matters because it costs 100 calls across the pilot.

Third instance of cold-load producing clean-looking wrong numbers, after the first-in-loop throughput reading and the keep-alive stacking case. Pattern, not coincidence. Script committed as probe4_endpoint_logprob_diff.py; outputs renamed *_warm.json after the first run's identical filenames destroyed the cold-run evidence by 'w'-mode overwrite.

### Two artifacts found in the written file (2026-09-05)

**`\uXXXX` escapes throughout the alias lists — not corruption.** `json.dumps` defaults to
`ensure_ascii=True`, rewriting non-ASCII as escapes. `\u0430\u043b\u044f\u0441\u043a\u0430`
is *аляска*, Alaska in Cyrillic; Arabic and emoji also appear. Valid JSON, round-trips
exactly through `json.loads`. **Default kept deliberately:** pure-ASCII output cannot be
misread regardless of a reader's encoding settings — same self-containment argument that
kept the `value` field.

**`qw_402` carries unstripped CSV escaping.** The question text is wrapped in quotes with
`""` doubled around an internal title. One of 50. Reaches the model as mild prompt noise,
identical across all nine cells. Not repaired — a de-escaping rule would need to
distinguish artifact quotes from legitimate quoted titles, which is the unjustifiable free
parameter rejected for minimum alias length, minimum retained mass, and alias caps.

Together with `qf_1637` and tc_543, these make **three distinct fields** carrying
construction artifacts. See §5c, the construction-artifacts entry.

### Remaining in Slice 1's family

`draw_main.py` — not written, and cannot be until the pilot reports `p_weak` and
`p_strong`. Reads `items_pilot.jsonl`, subtracts those ids from the pool, draws N with a
**different seed**. Duplication hazard stands: the five-field row shape will exist in two
files.

### Concepts landed (don't re-explain; do check for regression)

**2026-08-31:** `import` brings in code, function calls fetch data · variables and `=` as a
command that stores vs `==` as a question that compares · `len()` · dictionary access
`row['key']` · dataset row access `d[0]` vs column access `d['col']` · `lambda` ·
`.filter()` returns a new dataset and does not mutate · `assert` as a hard stop, written as
a *relationship* (`len(dataset) - 1`) rather than a hardcoded 11312 · `#` comments ·
comments carry *why*, code carries *what*.

**2026-09-05:** `.shuffle(seed=)` and why a seed is fixed-and-recorded rather than
unpredictable · `.select()` vs bracket-slicing · `for` loops, and indentation as block
structure rather than decoration · building dictionaries with `{}` · empty list `[]` and
`.append()` (mutates in place, returns nothing — never `items = items.append(x)`) ·
`with open(...) as f` and automatic close · `json.dumps` (returns a string, needs
`+ '\n'`) vs `json.dump` (writes to a file, takes `indent=`) · explicit `encoding='utf-8'`
as "inherit nothing" applied to file I/O · constants in ALL_CAPS so one fact has one home ·
chained method calls use `.`, not `,`.

**Error classes met:** `NameError` (name never created) · `KeyError` (asked a dictionary
for a label it lacks) · `'X' object is not callable` (parentheses after something that
isn't a function) · `IndentationError`. And the silent class, which is the dangerous one:
`['question_id']` without `row` builds a one-item list that compares unequal to every
string, filters nothing, and does not crash; a wrong key on the *left* of a colon writes a
wrongly-named field into all 50 lines without error (caught as `'question_'`).

**Failure modes demonstrated rather than explained:** a comment left stale when the code
under it moved · a fix that existed in conversation but not in the file that was run ·
adapting a working block into a context with a different shape (the JSONL write loop
reached for when the manifest needed a single object, written once).

**Autocomplete disabled in VS Code** (`quickSuggestions`, `parameterHints`,
`inlineSuggest`, `acceptSuggestionOnEnter`) at Laz's request — a parameter hint had
already offered `huggingface/c4` in place of the TriviaQA arguments. Error squiggles and
the Problems panel are unaffected.

---

## 6. Environment

- **Hardware:** AMD Ryzen 7 9850X3D (8C/16T, 4.70 GHz) · 32 GB (2×16 GB) G.Skill F5-6000J3636F16G DDR5-6000, EXPO enabled, verified at 3003.4 MHz CL36 · XFX Swift Radeon RX 9070 XT, 16 GB GDDR6, reference clocks (2400 MHz game clock), 644 GB/s bandwidth, PCIe 5.0 x16 · Windows 10 22H2
- **Displays:** 4 × 1440p (2 @ 60 Hz, 1 @ 75 Hz, 1 @ 180 Hz), all on the 9070 XT. Framebuffer allocation eats into the margin on the largest cell.
- **AMD Adrenalin 26.8.1**, driver `32.0.31041.1004`. **Auto-update disabled 2026-08-26** — re-enable post-study.
- **Ollama 0.32.14** — drifted from 0.32.6 via auto-update, discovered 2026-08-16. Auto-update now disabled. §13 freezes on 0.32.14.
- **KV cache `f16`** — set via `OLLAMA_KV_CACHE_TYPE` in System Properties, then **quit Ollama from the tray and relaunch**; a shell `set` never reaches the running server. Verify it applied.
- **Flash attention on**, verified from the server log (`%LOCALAPPDATA%\Ollama\server.log`, grep "flash"), not assumed from the env var.
- **PowerShell chains with `;`, not `&&`.** cmd has **no `#` comments**. `curl` is aliased to `Invoke-WebRequest`; use `Invoke-RestMethod` or `curl.exe`.

### Logprob check — COMPLETE 2026-08-08

Run against `gemma3:1b-it-q8_0` via `/api/chat`, `logprobs: true`, `top_logprobs: 10`.

1. **Logprobs are RAW, not temperature-scaled.** Temp 0 vs temp 2: True −0.0310 vs −0.0324, False −4.3070 vs −4.3420. **Temperature does not change the measured quantity**, though it does change generation.
2. **`top_k` does NOT truncate the returned distribution.** `top_logprobs: 10` with `top_k: 5` returned 10 candidates. Independent knobs.
3. **Cold-load ≠ warm-load. PROCEDURE REQUIREMENT.** First call after load differed at identical temp/seed (TRUE −5.1499 vs −4.9346, tail reordered); three warm calls at *differing* temp/`top_k` were bit-identical. **Every model gets a discarded warm-up call.** Caveat: n=1 on the cold side.
4. **Parser edge case.** A candidate with an empty token string and **no `bytes` key**. Present at position 0 on the 12b, not just position 1.

### P(True) probe — 2026-08-21

Template B, hand-written question (not a TriviaQA item, so no draw-pool contamination), both roster extremes.

- **Position 0 carries the answer.** `1b-q4_K_M`: `True` 0.94765, `False` 0.04254, retained mass 0.99493, renormalized P(True) 0.95724. `12b`: `True` ~1.0, retained mass ~1.0.
- **Observed variants:** `True`, `TRUE`, `true`, `[sp]True`, `Yes`.
- **`Truth` matched `tru*`** — the false positive that killed prefix matching.
- **`Correct` in the tail**, unmatched — a semantically affirmative but format-noncompliant response, correctly outside retained mass.
- **Empty-token candidates with absent `bytes` at position 0** on the 12b.
- **12b saturated** at ~1.0 → the tie/AUROC risk now in §10.

### Throughput — re-measured 2026-08-26 on driver 26.8.1

Conditions: `num_ctx=2048`, KV f16, warm, previous model unloaded, no other GPU consumers, one item per cell. tok/s from `eval_count / eval_duration`, both server-side.

| cell | tok/s |
|---|---|
| `gemma3:1b-it-q8_0` | 248.7 |
| `gemma3:1b-it-q4_K_M` | 234.3 |
| `gemma3:1b-it-fp16` | 184.4 |
| `gemma3:4b-it-qat` | 134.4 |
| `gemma3:4b` (q4_K_M) | 132.5 |
| `gemma3:4b-it-q8_0` | 110.6 |
| `gemma3:4b-it-fp16` | 67.8 |
| `gemma3:12b` (q4_K_M) | 66.0 |
| `gemma3:12b-it-q8_0` | **43.9** |

**THE SPILL WAS A DRIVER ARTIFACT.** On the previous driver, `12b-it-q8_0` measured 15.4 tok/s — ~31% of the 644 GB/s ceiling, which is what spilling looks like. On 26.8.1 it is **fully resident at 43.9, ~89% of ceiling**. The q8_0→q4_K_M step is now **1.49×** against a ~1.6× file-size ratio: ordinary bandwidth scaling. That cell is now **~25% of sweep runtime**, not 48%. The old "4× step / VRAM ceiling / 48%" reading is superseded and must not be reintroduced.

**The 1b cells are within run-to-run noise.** Two runs put the ordering in opposite directions, ~6% either way. A 22-token generation is too short a timing window. **Do not read the ordering between them.**

**QAT 134.4 beside the standard 4b at 132.5** — near-identical bit budgets, consistency check passes.

**VRAM:** peak 15474 MB against 16304 MB available, 2256 MB desktop baseline (PowerShell + Adrenalin only). It fits with under 1 GB of margin.

**Desktop applications cost nothing measurable.** With Discord in a call, Claude, VS Code, PowerShell and Adrenalin open: 44.2 tok/s on the critical cell vs 43.9 closed — 0.7%, inside noise. Baseline 2866–2874 MB, peak 16002 MB. **Discord was never poisoning the numbers.**

**⚠ Three contamination sources, all of which produced clean-looking numbers:**
1. **Cold-load / first-in-loop.** `1b-q4_K_M` read 57.9 tok/s leading the loop, ~239 in isolation.
2. **Keep-alive stacking.** `OLLAMA_KEEP_ALIVE` defaults to 5m; nine models called inside five minutes all stay resident, stacking exhausts VRAM, later cells spill. Degradation scaling with model size is the tell.
3. **Other GPU consumers.** A game in the background cost `4b-q8_0` 31.5 vs 105.2.

**None showed up in `load_duration`** — every bad run reported ~0.23s. No automatic check exists, so the protection is procedural.

### `localhost` vs `127.0.0.1` — measured 2026-08-16

5 calls: `localhost` 5,855 ms · `127.0.0.1` 1,338 ms → ~900 ms per call. Windows resolves `localhost` to IPv6 first; Ollama binds IPv4. At 27 calls per item that's ~24 s/item of pure latency. **The throughput table is unaffected** — tok/s comes from server-side fields.

### Degenerate generation — confirmed on 0.32.6 AND 0.32.14

`gemma3:1b-it-q8_0` (digest `0fdb9c7fefee`, unchanged across versions), one TriviaQA item — *"Which Lloyd Webber musical premiered in the US on 10th December 1993?"* — produces degenerate repeating asterisks. `num_predict ≥ 32` → `done: false`, **no metadata**. ≤ 31 → normal, `done_reason: "length"`. Re-verified 2026-08-21: `np=25` and `31` returned `done=True`; `np=32/64/100` returned `done=False`.

**Process note.** An ARIA background task reported this as "no longer reproduces on 0.32.14." Re-running the *original* item disproved it — the probe had used a trivial prompt. **A non-reproduction is only evidence if it reproduces the original conditions.**

### `num_ctx` pinning cost throughput

Dropping `num_ctx` 131072 → 2048 cost the 12b throughput (35.9 → ~20 tok/s at the time). Counterintuitive and unexplained. **Both numbers are from the old driver and have not been re-checked on 26.8.1** — scoped as such in §6.

---

## 7. Sources gathered

- **Kadavath et al. 2022** — arXiv 2207.05221. The paper being replicated.
- **Tian et al. 2023** — *Just Ask for Calibration*. Verbalized-confidence-beats-logits.
- **Leng et al. 2025** — arXiv 2410.09724, *Taming Overconfidence in LLMs* (ICLR 2025). **Scope carefully:** about *verbalized* confidence under RLHF, so a prediction about one elicitation method, not a refutation of H1. Also the cite for why "more confident" ≠ "better calibrated."
- **"Mind the Confidence Gap"** — OpenReview, Sept 2025. Large RLHF-tuned models can be *more* miscalibrated on easy queries; small models remain significantly miscalibrated.
- **Dunning-Kruger paper** — arXiv 2603.09985 (2026, read critically). **This is H1's rationale in different words** — chase the primary source.
- **arXiv 2311.13240** — *On the Calibration of LLMs and Alignment*. Finds *no* significant ECE degradation from RLHF atop instruction tuning. Cite alongside Leng to show the field disagrees with itself.

---

## 8. Slice roadmap

- **Slice 0** — pre-registration. **PAUSED mid-draft 2026-08-31.** §3, §4, §6, §7 done.
  Blockers now split: §11's rule and §8's noise floor are **pre-pilot mandatory**;
  §10's transcription and §2 are post-pilot, pre-freeze.
- **Slice 1** — dataset loader. **COMPLETE 2026-09-05**, two sessions.
- Slice 2 — runner + grader. ← here. **Runner complete 2026-09-20** — both pilot models, all three templates, append-only JSONL, resume, warm-up, verified unload, startup hard stops. Grader not started. Template B **in** the pilot of record (decided 2026-10-12); B's parser is grader work and now on the critical path.
- **Public release — 2026-10-11**, between slices: README, LICENSE, CITATION.cff, full history pushed. Not a slice; recorded so the date is findable.
- **Slice 3** — the full nine-model roster, and B's grader side. The runner half of "second method" landed early, in step 6.
- **Slice 4** — analysis. **Deferred to October by design**, as the most fragment-tolerant
  work in the project.

**Pilot: one draw of 50 items, run on both extremes**, before freeze, data discarded.
**Different seed**, and **pilot items removed from the main draw pool by subtraction**
(see §5e).

Determines **six** numbers (since 2026-10-12, line 149): p_weak, p_strong, and an AUROC noise
floor and a spread noise floor **per elicitation method**. **A materially wider measured floor is a §12 disclosure**, stated in advance.

**Scope risk, restated 2026-08-31 with the correct emphasis:** the document is nearly done
and the harness is where the deadline actually turns. The prereg is the visible pile and
the smaller one. Sessions spent on §10's wording are sessions not spent on the thing the
timeline depends on.

**Freeze mechanics:** `git tag -a prereg-frozen -m "Slice 0 frozen"`. Record the hash in the header. **Before tagging, hash the file you edited and confirm it matches the commit** — a stale handoff costs a session; a stale freeze costs the claim. **Plus OSF (decided 2026-10-12):** register the frozen prereg on OSF at freeze — a timestamped, immutable registration a reviewer outside git can check — and record its DOI in §13 beside the commit. Results go to the OSF project at completion. Prereg line 432 names only the git tag; add the OSF step there before freeze.

**Scope risk worth naming:** the document is nearly done; the harness doesn't exist. Slices 1–4 are where beginners lose months. If something must be cut for time, cut there — drop the QAT arm, or run at smaller N and disclose — not from the parts that make the study interpretable.

---

## 9. Working process

**Division of labor.** Laz writes the research content — hypotheses, rationales, thresholds, predictions, falsifiers. Claude's job is adversarial review: unfalsifiable phrasing, circular rationales, data-dependent exclusions, metrics that don't answer the stated question, contradictions between sections. Claude **declined** to draft the hypotheses; that's load-bearing, because the pre-registration *is* the research identity.

**Explanation protocol.** Name the term, state the problem it exists to solve, show the concrete failure it prevents — then apply it to the file. Don't slow down; decompress. Worked examples with actual numbers land far better than definitions.

**Concepts explained and confirmed landed** (don't re-explain from scratch; do check they haven't regressed): threshold = k × floor is multiplicative · bootstrapping is resampling *with replacement* · more resamples don't reduce uncertainty, only N does · *not evaluable* vs *not supported* · `num_ctx` vs `num_predict` · raw vs renormalized mass · **digest = cryptographic hash, same thing as a git commit hash** · **a priori vs a posteriori** · **AUROC = P(random correct ranks above random incorrect), ties count 0.5, which is why saturation degrades it** · **AUROC is computed within one cell; rank-only, so rescaling cannot change it; undefined only when a cell has no correct or no incorrect items (2026-10-12)** · **saturation = confidence piling up at the scale's top whether right or wrong; not always an artifact — it can be genuine overconfidence (2026-10-12)**.

**Manual mile.** ARIA is ~5% Laz / 95% Claude by his own assessment. `calibration_lab` is the corrective — small enough to write alone, the artifact he can put his name on without an asterisk. The bar: rebuild the harness solo from a blank editor by OSU arrival. **Deprecated — in need of review.** The bar itself still holds; its deadline is anchored to a transfer plan no longer being pursued. Noted rather than ignored, and it needs re-anchoring to a date that still exists.

**Progress note, 2026-08-26.** Longest session yet. Four things worth recording as evidence. (1) **He caught the stale handoff himself** at the top of the session — noticed the date was wrong and stopped the session rather than working from it. That prevented hours of work built on false premises. (2) **The P(True) probe reopened a decision he'd already made**, and he took the reversal on evidence rather than defending the earlier call. (3) **He questioned whether the driver mattered**, which surfaced that the throughput table predated it — and chose re-measurement over disclosure, which turned out to invalidate a mechanism he'd have otherwise frozen into the document. (4) He asked "should we hold the number accountable to both value and format?" on leading zeros — the right frame, and he reached the correct answer via his own precedent rather than by being told.

**The recurring correction pattern — his stated achilles heel.** Drafts contain the *evidence* for a claim without the claim itself. Diagnosis: curse of knowledge, not a comprehension gap. Rereading won't fix it because his brain supplies the missing inference. **The mechanical check: after writing a justification, ask whether a reader who doesn't know the answer could reconstruct it from the page — and run it on the last sentence of each block specifically**, since the conclusion is what gets dropped. Note the variation observed 2026-08-26: he began keeping the conclusion and dropping the *provenance* instead (the quantity without the observation that produced it). Same root, different half.

**Register.** Trend is real and improving: the throughput block took three passes, P(True) took five, `num_predict` took three, and he caught more himself each time. Two months from precalculus to a pre-registered study with locked hypotheses and empirically-grounded parameters.

**Tone that works:** direct pushback with reasoning; flagging the crack rather than smoothing it; handing back the rows that must be his. He asks to be graded honestly and uses it well. He'll say "unpack that" when vocabulary outruns him — and does, reliably.

**Claude's failure mode — 2026-09-12/14.** Four false claims shipped in one session, all one
mechanism: reasoning against a *summary* of the file instead of the file. §9 line 322 defines
`no_valid_response` — claimed absent after reading lines 304–320 and stopping two lines short,
then repeated two turns later without reopening. §6 line 286 had already specified the row
schema — repeated the handoff's claim that it was open design work, which would have cost a
session designing something already written down. Claimed the resume mechanism had broken under
the no-C-row design when it had not. Claimed `elicitation_method` discriminates at runner level
when line 265's fields are grader outputs. Three of the four surfaced because Laz asked a
question, not from review.

**Standing rule — adopted 2026-09-14.** Any claim about what a file says arrives as a line
number plus verbatim text — "check prereg line 322" — or it arrives as "I haven't checked
that." Never "your prereg says X." Partial reads are the specific hazard: a `sed` range chosen
for convenience is not the section, and a range ending on a round number is not a boundary the
document agreed to.

**The rule held, 2026-09-18.** Full §1–§13 pass, sixteen findings, every one cited to a line
and quoted — no false claims about the file that session, against four the session before.
Two of the sixteen were contradictions that would otherwise have reached freeze. It also
caught a defect in Claude's own draft header for *this* handoff, which claimed step 5 was
unblocked when four amendments were verifiably still unlanded. **Apply the rule to your own
drafts, not only to Laz's text** — that is where it failed twice this week and where it will
fail next.

**2026-09-18/20, two small misses, both caught.** Verified line 259's paragraph without
flagging its internal "(line 116)" reference, the same defect fixed two lines up; caught on
the next pass. And told Laz to park G "in §5c" without saying §5c lives in this file, not
the prereg, so G went nowhere until this rewrite (§5c item 32). Reading the page instead of
this file at session open found three blockers this file had missed.

**2026-10-08/11, two misses, both caught.** (1) Referred to "§B" and "§C" without naming the
file. With the prereg, this handoff and `SESSION_PROTOCOL.md` all sectioned, a bare section
sign is ambiguous; Laz could not find "the §B opening block." **Name the file with the
section — `SESSION_PROTOCOL §B` — every time.** (2) Asked Laz to decide item 29 (B in the
pilot of record) before noticing that item 29 depends on a gap nobody had found — which
method decides the verdicts (item 37). Caught one turn later, when he asked what "B" meant
and the answer required checking §3. **Before asking for a decision, check what it depends
on.** Separately, the 2026-10-08 open caught this file's own §0 asking Claude to check an
entry it hadn't read — the reading-the-page rule working as intended.

**2026-10-12, five misses, all caught.** (1) The REU's "mid-December" deadline was carried as fact since July with no site ever named — a planning placeholder. **A date in this file needs a source.** (2) This file's verbalized-confidence bullet and the prereg both said dividing by 100 was for AUROC; AUROC is rank-only. Claude carried the error in its own document. (3) Told Laz the 09-20 lab-log entry set a standing per-entry authorship rule; it was a one-time statement — a precedent overstated from memory, the 09-12 failure in small. (4) Claude's amendment table said line 48 changed "twice"; it was two different phrases, and the error reached Laz's log draft before review caught it. (5) Called the unwritten §8 procedure "three gaps", implying a paragraph exists. **Process change, per Laz:** this file's item numbers meant nothing on his side — refer to everything by content. §5c's numbering retired the same day. Also found at open: §5's row for §1 still said "stale premise — rewrite before anything else" six weeks after the 08-31 correction voided it.

---

## 10. Living-doc gap — the reason this file exists

`calibration_lab` had **no home** in the doc system, so it fell through the gap and evaporated from awareness during midterms.

**The leak is real and measured.** Six settled decisions had to be re-derived from scratch — the Δ rung pair (three times), the definitions block, Δ(4B)'s role, the threshold rule, H2a's verdict rule, the endpoints choice. All were transfer failures between conversation and disk.

**Second failure mode, identified 2026-08-26:** the handoff recorded decisions as *landed* when they were only *decided*. Fixed by §0b's protocol and §5c's list.

**Companions:**
- ✅ **Lab log** — `lab_log.md`, created 2026-08-26, tracked as of 2026-08-29. Placement decided and committed 2026-08-29 (§5c, closed list).
- ✅ **README / LICENSE / CITATION.cff** — added 2026-10-10. The README is the public map of every tracked file; keep its repository table current when files are added.
- ✅ **Session protocol** — `SESSION_PROTOCOL.md`, adopted 2026-08-29.
- ⬜ **Decisions log** — what was chosen and why. §2 here is doing this job informally.

Repo holds the pre-registration and data. Vault holds interpretation. **Canonical prereg copy in the repo only** — a frozen artifact in a mutable store isn't frozen.

---

## 11. Git state

```
28a33de  2026-10-12 Both-must-hold decided; §3 split verdicts; prereg (seven §D amendments) + lab log 10-12 (exact message: git log -1 28a33de)
032ba89  2026-10-11 Handoff rewritten against 94430cf
94430cf  2026-10-10/11 public-release prep — README, LICENSE, CITATION.cff, prereg lines 4 + 368, handoff placeholders, lab log 10-08/10-10 (exact message: git log -1 94430cf)
da50cea  2026-09-20 Updated handoff
09c815e  2026-09-20 Appended lab log: 2026-09-20 Steps 5-7 done: run_pilot.py hardened, resumed, and verified clean
b9a25be  2026-09-20 Lab log entry: 2026-09-20 Steps 5-7 done: run_pilot.py hardened, resumed, and verified clean
4254e66  2026-09-20 TEST: reverted back to original state - timeout = 90
a2bf59a  2026-09-20 TEST: temporary timeout=0.001 for forced-timeout verification
de90f21  2026-09-20 step 6 hardening: strip fix for B/C prompts, warm-up/unload verified via /api/ps, explicit keep_alive, dirty-tree and keep-first startup checks
8253911  2026-09-20 step 6: full loop, warm-up, unload, resume, all three templates; 300 verified rows.
ffd3e78  2026-09-18 step 5 of runner mostly complete and usual log entry
6779746  2026-09-18 finishing prereg fixes landed and step5 of the runner unblocked
eb83167  2026-09-18 updated handoff
e4f28e4  2026-09-18 Prereg review: ~20 amendments, lab log, POST_STUDY_TODO.md
80287c6  2026-09-14 updated handoff
9f87f53  2026-09-14 lab log 09-12/09-14
ea5699f  2026-09-10 Updated handoff 09-10-2026
ff7df62  2026-09-10 runner steps 2-4 completed and updated 2 things in the prereg.
2d73604  2026-09-05  Slice 1 finished and deferred lab log entry resolved
207f989  2026-09-01  Handoff: re-plan to harness-first, §5e harness state, three §5c corrections
cb92a94  2026-08-31  Slice 1: TriviaQA loader with corrupted-row filter; log entry deferred
99a126d  2026-08-29  08-29-2026 another small post-session fix
101b7db  2026-08-29  08-29-2026 quick fix post-session
a213298  2026-08-28  (last verified hash of the 08-28 session)
23e58ee  2026-08-27  S6: reorder + throughput re-measurement on driver 26.8.1
a37c996  2026-08-27  S6: parsing rules, throughput, logging, grader-rule declaration, verification requirements
8438601  2026-08-09  section 5 completed in prereg
f8a12b4  2026-08-01  Section 3 completed
3496554  2026-06-24  pre-registration template WIP
```

Verified 2026-10-12:

Open check: `git log --oneline 94430cf..HEAD` returned only `032ba89 (HEAD -> master, origin/master)`; tree clean; prereg unchanged since `94430cf`. `28a33de` was committed by Laz with the prereg and the 10-12 lab-log entry; its file list was **not** shown to Claude — next open, run `git diff --stat 032ba89 28a33de` and expect exactly those two files. Per Laz's git check (10-12 entry), origin held 44 commits after the second 10-11 push (`032ba89`). Whether `28a33de` and this handoff are pushed is not recorded here.

**This handoff should be the only file past `28a33de`.**

Verified 2026-10-08 → 10-11:

Open checks at `da50cea`, both 10-08 and 10-10: tree clean, `git diff --stat 09c815e HEAD` showed only this handoff, `git diff --stat da50cea HEAD` empty. `94430cf` carries all of the 10-10 work in one commit. Tracked files (`git ls-files`, 10-10) match the README's repository map plus the three new files; `.venv/`, `pilot_runner_log.jsonl` and `tempCodeRunnerFile.py` exist on disk and are ignored.

**Remote added 2026-10-11:** `origin` = `https://github.com/Lxzxrus/calibration_lab.git`, branch `master`, tracking set with `push -u`. There was **no remote before this** — the repo had never been pushed. Full history (43 commits at push) is public. **Any other machine must clone fresh from GitHub**; an older local copy shares no history with it.

**Commit email:** this repo's `user.email` is now the GitHub noreply address (`…+Lxzxrus@users.noreply.github.com`), from `94430cf` on; GitHub blocks pushes exposing the private address. Commits before `94430cf` keep the personal address — accepted, since rewriting history would change every hash the lab log cites.

**Pre-publication audit, 2026-10-08:** commit authors — one name, one email; `pilot_runner_log.jsonl` never committed; no token patterns in history.

(At the time: this handoff the only file past `94430cf` — confirmed 2026-10-12.)

Verified 2026-09-20:

`4254e66`: working tree clean, `pilot_runner_log.jsonl` 300 rows, every row stamped `4254e66`.
`ffd3e78` against `6779746`: `.gitignore`, `lab_log.md`, `run_pilot.py` only — prereg untouched.
`6779746`: prereg and lab log together, satisfying §D. The prereg has not moved since.
`pilot_runner_log.jsonl` is gitignored (confirmed by a clean status with the file present).
Line 259 requires the grader's log to be ignored too once it exists — not yet checked, since it doesn't. (At the time: this handoff the only file past `09c815e` — confirmed 2026-10-08.)

Verified 2026-09-18:

`e4f28e4` carries the prereg (~20 §D amendments), the 09-17/18 lab-log entry, and
`POST_STUDY_TODO.md`. `run_pilot.py` **unchanged this session** — no code was written.
Working tree clean at close. This handoff is the only file that moved after `e4f28e4`, so
next session's §C.1 should find exactly one handoff-only commit against it.

`POST_STUDY_TODO.md` is **committed, not ignored** — decided 2026-09-18 against gitignoring
it. A gitignored reminder lives on one machine, reaches neither the laptop nor any backup,
and the file is two lines. Holds re-enabling Ollama and AMD driver auto-update, and reverting
KV cache to q8_0.

Earlier, verified 2026-09-10:

run_pilot.py — steps 1–4 of 7, committed.
probe4_endpoint_logprob_diff.py and its two *_warm.json outputs — committed.
.gitignore — data/ and !data/items.jsonl removed. The exception was structurally dead: git cannot re-include a file inside an excluded directory, confirmed by git check-ignore -v. Both pilot artifacts live at repo root, so the rules were speculative and never applied. A stray CR left by a hand-edit went with them.
lab_log.md — two entries, 09-06/09-09 and 09-09/09-10.
Prereg moved during a harness session, twice, both §D-intentional and both recorded in lab_log.md the same session: templates fenced, strip rule added. Expect this in next session's --stat; it is not an anomaly.
SESSION_PROTOCOL.md — §E amended (see §0b).

Carried from 2026-08-31: `SESSION_PROTOCOL.md` committed with Laz's `cd` line in §B;
`.gitignore` created (first in the repo); `requirements.txt` pinned from `pip freeze`.

Commit messages are now descriptive with reasoning in the body where the diff doesn't
carry it. Adopted after `quick fix post-session` proved unfindable.

`core.autocrlf` set to false to stop LF→CRLF conversion, so the bytes on disk match the
bytes in the commit — relevant because the freeze mechanic is "the hash is my witness."

Commit messages for the last two are `quick fix post-session` / `another small
post-session fix`. Accurate for what they contain, but the session's substantive work is
only findable through `lab_log.md`. Worth more descriptive messages going forward.
