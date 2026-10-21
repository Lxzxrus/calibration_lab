# `calibration_lab` — Handoff

*Operational snapshot. Drop this + the pre-registration into a fresh chat and say hello — that's enough to resume.*

**Last updated:** 2026-10-20 · **Synthesized against commit:** `556b441` · **Status:** **Grader spec complete on the page; grader not started.** Between 10-16 and 10-20 the refusal rule, tie rate, saturation extension, terminal-A cascade, the normalizer, the match boundary and the negation window all landed in the prereg (four sessions, ~30 §D amendments). `fixtures/items.jsonl` exists (52 cases); the fixture runner rows and expected rows do not. **Runner COMPLETE** since 2026-09-20. **Repo PUBLIC** since 2026-10-11. Pre-pilot prose still unwritten: **§8's noise-floor procedure** and **§11's interpretation rule**. **Freeze date: not set, by Laz's decision.**

*Session protocol lives in `SESSION_PROTOCOL.md`. Open by running its §B block.*

*Rewritten 2026-10-20 against the files as attached at the 10-20 close, not from the previous handoff: the prereg, `lab_log.md`, `run_pilot.py`, `draw_pilot.py`, `triviaqa_normalize.py`, `build_fixture_items.py`, `README.md`, `SESSION_PROTOCOL.md`, `.gitignore`, `.gitattributes`. Superseded history was condensed to pointers into the lab log. **Prereg locations are now cited by section and bullet name, not line number** — line numbers went stale after every amendment session; get them with a search at session time.*

---

## 0. YOU ARE HERE

### Critical path, in order

1. **Fixtures, the remaining two files** — `fixtures/runner_log.jsonl` and `fixtures/expected.jsonl` for fx_001–fx_052. Full spec in §5e. Expected values are computed by hand from the prereg, independently of any grader.
2. **`grade_pilot.py`** (name not yet fixed) — transcription of §6's Grader Spec and §9's exclusion rules. Imports `triviaqa_normalize.py`. Reads the runner file and joins `items_pilot.jsonl` on `question_id`. Writes the grader file. Done when it reproduces every expected row in the fixtures **and** passes the whole-split test (grade every gold value against its own keys; only `qf_1637` may fail).
3. **§8's noise-floor procedure** — pre-pilot, unwritten. Four questions it must answer, per method under both-must-hold:
   - how the 50-item pilot floor scales to the main-study N
   - floor for a single AUROC or for a difference of AUROCs (H2a's steps and H2b's spread are differences on the same items)
   - how H2b's spread floor is measured when the pilot runs two cells and the spread needs four
   - whether the k × floor rule is stated as a heuristic, with bootstrapped CIs as the clean alternative
4. **§11's option-four interpretation rule** — pre-pilot. AUROC flat while ECE or Brier degrades is reported as a named finding, not a null. Post-hoc if written after the pilot.
5. **Pilot analysis code** — per cell and per method: AUROC, accuracy over retained items, tie rate, retained mass, flag rates, and the floor computation. The pilot's six outputs are computed values, so this is pre-freeze.
6. **Pilot of record.** Delete `pilot_runner_log.jsonl` first, **unopened** (provenance commitment, 2026-10-12: those 300 validation rows are the pilot items on the pilot models). The runner's keep-first check hard-stops on the file anyway.
7. **Then:** fill §5's brackets → choose `draw_seed` → `draw_main.py` (pin the dataset revision) → Slice 3 (full roster) → pre-freeze prose (§5c) → OSF registration → freeze.

**Ordering rule, unchanged since 2026-08-31:** code goes in the uninterrupted blocks, prose in the fragments. Items 1, 2 and 5 are code. Items 3 and 4 are fragment-sized prose and can land in any gap before the pilot.

### Estimate

- **Whole-study estimate, 2026-10-12 (Claude's, logged as an estimate):** 12–20 sessions to freeze, 8–15 more to posted results.
- **Since then:** four sessions (10-16, 10-18, 10-19, 10-20), all prereg and grader-spec work plus the fixtures items file. 12–20 minus 4 leaves **8–16 to freeze**, by subtraction, not re-estimation.
- **The variable that has broken every prior estimate is sessions per week, not sessions per task.** Pace goal: three a week.
- The dated external gate is **PNNL CCI, early January 2027**; the recommenders are for CCI. REU deadlines are per-site and unconfirmed; "mid-December" was a July placeholder.

### Standing

No study data has been run. The 300 rows in `pilot_runner_log.jsonl` (gitignored) are harness validation at `4254e66`: not study data, not the pilot. They are not to be opened for any pre-pilot rule, and they are deleted unopened before the pilot of record. On 09-20 they were inspected for counts, duplicates, provenance and schema only — no grading, no AUROC.

**All model calls since 09-20 are environment characterization:**
- probe 5 (10-16): 20 calls, hand-written non-pool questions
- one Template B call (10-19): "capital of France", checked absent from the pool, nothing saved

**Division of labor** (2026-08-31; restated publicly in the README):
- Laz types every line of the code, the prereg and the lab log, and accepts, rewrites or rejects every proposal.
- Claude explains concepts and code, reviews for errors, and proposes text.
- This handoff is written primarily by Claude; Laz edits the header hash and reviews it.
- Lab-log credit lines name the model (Opus, Fable, Sonnet) by content. This file says "Claude".

**This file is public.** It carries no personal scheduling detail, by Laz's decision (2026-10-18).

---

## 0b. Working protocol

**`SESSION_PROTOCOL.md` is the single home for session discipline:** closing checklist, the opening `git` block, what Claude verifies on open, the harness-phase prereg-drift rule, and the post-freeze integrity check. Do not restate its rules here. If this file and the protocol disagree, the protocol governs on process; the prereg governs on content.

**§E, in one line:** the session is the work-day. Each work-day gets one lab-log entry and at least one commit. This handoff is chat-scoped and is rewritten when a chat closes.

**Known failure modes, all still live:**
- **Decided logged as landed.** §5c is the list that catches it; verify against the page, in both directions.
- **A number carried from an earlier entry without being re-run.** The 10-18 figures 156 and 4 were repeated on 10-19 and proposed for the prereg on 10-20; neither reproduced (now 151 or 527 depending on the definition, and 3). Before any figure enters the prereg, re-run the committed script that produced it.
- **A conclusion inferred from content and written as if tested.** The hyphen-side figure was stated as all 141 items matching no key, from key content alone, without running the Match test; run, it is 138 of the 141.
- **A fixture testing a state the data never has.** An article in an alias: zero of 131,861 aliases contain one.

**Open protocol question, parked 10-16:** whether §E should exempt housekeeping commits (the 10-14 `FUNDING.yml` commit made §C.1's "exactly one handoff-only commit" condition false, benignly).

---

## 1. What this project is

A standalone research study measuring **calibration** — whether a model's confidence matches its accuracy — on small, quantized, instruct-tuned models running on consumer hardware.

It is a conceptual replication of **Kadavath et al. 2022** (arXiv 2207.05221, *Language Models (Mostly) Know What They Know*), whose cleanest results were on **base pretrained** models from 800M to 52B. This study asks whether that picture survives quantization and small scale. Every roster model is instruct-tuned, so instruct-tuning is held constant, not tested — a cross-study difference from Kadavath (prereg §10), not an axis here.

**Dual audience, deliberately:** an academic portfolio artifact (a professor sees someone learning to navigate research) *and* a community finding (a reader with 8GB of VRAM learns which model at which quantization is actually trustworthy). Neither is the afterthought. This framing drives most scope decisions below.

**Research identity it serves:** *"I study whether AI systems know what they know and how humans stay meaningfully in control when they don't."*

**Public since 2026-10-11** at `github.com/Lxzxrus/calibration_lab`. The README is the front door. Public name: Nathaniel (Nate) Campbell; "Laz" in the process documents is the same person, as the README states.

---

## 2. Frozen decisions — and why

*These are settled. The rationale is the part that doesn't survive a context reset, so it's recorded here. Entries marked **(rebuilt 10-xx)** replaced an earlier version that is now wrong; the lab log carries the history.*

### Repository and environment

**Standalone repo, entirely separate from ARIA.** `C:\Users\legen\Projects\calibration_lab\`, own git repo, own venv. Reason: ARIA is leaning toward a *curated public research mirror* rather than full open source. If `calibration_lab` lived inside ARIA, publishing it later would require history surgery on a repo containing a gitignored personal memory store. Ollama is shared, but as a service on `127.0.0.1:11434`, not a code dependency. **The harness talks to Ollama directly, never through ARIA** — ARIA's vault injection could silently prepend material to a frozen prompt template.

**Own venv, free to pin its own Python.** Python 3.12.8, because the scientific stack may not ship wheels for the newest version.

### Data

**gemma3 family only.** All three hypotheses are within-family. Holding family and training recipe fixed is what makes the scale claim clean. Cross-family replication is deferred to a follow-up study.

**TriviaQA only; MMLU dropped.** Free-form trivia is closer to how people actually use models.
- **Consequence, load-bearing:** MC logprobs require lettered options, so dropping MMLU drops that method. Two elicitation methods remain: **P(True)** and **verbalized confidence**.

**The MMLU and `nocontext` decisions are one principle applied twice: never hand the model material that lets it succeed without knowing the fact.**
- Context documents supply the answer to read.
- Multiple choice supplies the answer set to pick from. The MC-specific harm is **recognition vs. recall**: with distractors, partial knowledge can reach a correct answer by elimination, so a correct MC response is *ambiguous evidence*, and confidence can track distractor quality rather than the model's own knowledge.

**Config: `unfiltered.nocontext`, validation split.**
- `rc` drops questions whose retrieved evidence documents don't contain the answer, which selects for facts with strong web documentation. Those facts are plausibly over-represented in training data, which would bias every cell in the same direction, invisibly.
- `unfiltered` does not *solve* contamination; it avoids compounding it.
- Validation because test-set answers aren't public.
- Dataset revision `0f7faf33a3908546c6fd5b73a660e0f8ff173c2f`, recorded 10-19 and pinned in the measurement scripts. **`draw_pilot.py` does not pin it** — `draw_main.py` must.

**Pool rule (on the page in §5 since 10-18).** `qf_1637` is dropped by id before any draw, as a source defect: its question (roadrunner) and answer entity (static libraries) don't correspond, `value` is `'(a'`, and `normalized_value` is blank. No model ever sees it, so it is not a §9 exclusion. The blank field is a symptom, which is why the filter is on the id.

**Identical item set across all nine cells.** Sample once with a recorded seed, freeze the file, and every cell reads it in fixed order.
- **Seed and file do different jobs:** the seed is provenance; the file is the guarantee.
- The main items file is **not yet committed** (it can't exist before the pilot).
- §5 still says "items.jsonl" generically, against the actual `items_pilot.jsonl`. Open in §5c.

**C = 200, held regardless of the N it implies.** It puts the AUROC noise floor around 0.02–0.03 (Hanley–McNeil), keeping `2 × floor` around 0.04–0.06. **The escape hatch was deliberately removed.** An earlier "if runtime exceeds 8 hours I'll adjust" clause would trigger precisely when p_weak is lowest, which is exactly when the items are most needed. Any change to C post-freeze is a §12 deviation.

**N is two-sided: `N = 200 / min(p_weak, 1 − p_strong)`, plus a 10% exclusion margin.** AUROC needs both classes populated. The strongest cell's *incorrect* count is its thin class, so the binding constraint can silently flip ends of the roster.

### The prompt side

**Forced response, not permitted refusal.** Permitting "I don't know" gives clean refusals, but §9 excludes refusals and the 1b would plausibly refuse more often — differential exclusion straight into H1 and H2b. Forced guessing puts lucky hits in the correct class instead. Free-form has no guessing floor, which should keep that small.
- **Rebuilt 10-18:** this entry used to say the pollution is "uniform across cells." That was unsupported, and §10's forced-response bullet now says explicitly that the rate is not measured and not claimed equal across cells.
- Probe 5 (10-16): **zero refusals in 20 forced-guess calls at both extremes.** Entities that don't exist got invented answers at both sizes.

**Prompt constraint over a smart grader.** A smart grader is a second measuring instrument whose errors land unevenly across cells: small models produce messier prose, so a lenient grader rescues more of the 1b's answers than the 12b's. Prompt constraint moves the burden somewhere identical across cells and makes compliance a *measurable* property. **Design: constrain hard, then put a small, mechanical, auditable grader on top — never a smart one.**

**Whitespace strip before `[Answer]`.** Raw Template A output is stripped of leading and trailing whitespace only before it enters B and C. Whitespace behavior correlates with size, and `.strip()` is total and unambiguous.
- **Empty after the strip (decided 10-19, on the page):** scored incorrect, not excluded. It enters B and C as a non-answer, by the same mechanism §9 excludes refusals for. The inconsistency is named on the page, and no code is invented for an unobserved case. The pilot counts the rate (raw word count = 0).

**`num_predict` = 25 / 5 / 10 for A / B / C, all below 32.**
- On `gemma3:1b-it-q8_0`, one TriviaQA item producing degenerate repeating output returned `done: false` with **no metadata** at `num_predict ≥ 32`, and returned normally with `done_reason: "length"` at ≤ 31.
- Confirmed on Ollama 0.32.6 and 0.32.14, same digest. Single item: two versions make the boundary stable, not general.
- Staying below it means degenerate items return cleanly with usable metadata.

**P(True) framing is non-self-referential — a deliberate deviation from Kadavath.** Every call is stateless and the model has no memory of producing the answer, so "your answer" would assert something false about the context.

### The grader

**Grader: TriviaQA's own normalizer, whitespace-delimited matching over `normalized_value` plus every `normalized_aliases` entry. (rebuilt 10-19/10-20)**

- **Normalize** is `normalize_answer` from TriviaQA's evaluation script (`mandarjoshi90/triviaqa`, commit `51b5359`), copied with the body unchanged into `triviaqa_normalize.py`. That file is under Apache-2.0, with a license copy at `third_party/triviaqa/LICENSE`.
  - **Reason:** the dataset's keys are already that function's output. It reproduces `normalized_value` on all 11,313 items, and `normalized_aliases` on all but five, where it yields an empty string the dataset drops. Any other function on the response side is a mismatch with the key side.
- **What it replaced, and the defect that forced it:**
  - The old rule (lowercase, punctuation→space, *no article stripping*) failed **389 of 11,313 gold answers against their own keys**. 387 of them have an internal article: *Fiddler on the Roof* against the key `fiddler on roof`.
  - The old rationale ("boundary matching absorbs leading scaffolding") was right for a leading article and false for an internal one. The internal case was never tested.
  - **Found by grading every gold answer against its own keys, not by reading the spec.** Article removal is now inherited from the dataset, not a grader choice.
- **Boundary: whitespace, not regex `\b`.** A key must be preceded and followed by a space or an end of the text.
  - Under literal `\b`, **9** gold answers fail against their own keys, because their keys begin or end with a non-word character (£, ellipsis, curly quote, a private-use glyph). Under whitespace, **1** fails (`qf_1637`, dropped).
  - **The cost, declared in §10:** a correct answer with a curly double quote, en or em dash, or ellipsis attached to it is missed.
- **One boundary rule in four places:** Match, negation markers, the multi-candidate `or`, and refusal phrases.
- **Not exact-match, not raw substring** (`exile` inside `exiled`). No prefix stripping.
- **An empty alias never matches.** No pool item has one, but a missing guard would score every response correct.
- **Every distinct hit is logged as a list:** `normalized_value` first, then `normalized_aliases` in stored order, deduplicated (the value sits inside the alias list on 11,312 of 11,313 items).
- **Characters the normalizer leaves alone** (en and em dashes, curly double quotes, ellipsis) are declared in §10. 135 items have an en dash in a key. A hyphen-for-en-dash response misses every key on 10 of those 135. Counts are in lab log 10-20.

**Non-compliance is counted, not eliminated.** Hedging and degenerate output at 1b are real model properties that correlate with size, so they become per-cell *reported rates*. This is now the same move five times: **negation, compliance, truncation, multi-candidate, retained mass.**
- **Refusal is the one exception** (below), with the reason stated on the page.

**Negation is detected, never corrected. (rebuilt 10-19/10-20)** A "not"-near-alias handler has no natural stopping point, and each rule misfires more often on messy prose, so more often on the 1b. That rebuilds the differential-grader problem in a subtler form.
- **The rule:** set when a marker lies **wholly within** the 4-word window preceding the **earliest match**, in the **normalized** response. False when nothing matched. Markers match as whole words and phrases under the Match bullet's boundary rule, so `no` doesn't fire inside `know`.
- The rule says "wholly within" because 13 of the 17 markers end in `t`, and a bare `t` would fire otherwise.
- **A high negation rate means the *alias* matcher is crediting negated answers.** The prereg's old phrase "substring matching" was a stale name for it.

**Compliance: true when raw word count ≤ 10, counted as `len(raw.split())` on the raw response. (decided 10-19)** Raw, because normalization splits words apart and drops articles. The word count is logged as an integer, which is what makes empty answers findable.

**Multi-candidate: set when `or` appears as a whitespace-delimited word in the normalized response. (10-18)** "Any match = correct" scores a response naming several candidates as correct if any one is an alias. That's a recognition-shaped hazard inside a free-form design.
- **Crude by design:** it misses comma and range lists (`13mm - 15mm, likely 13mm`), and it fires on gold answers containing `or`.
- Measured: 87 values and 164 items counting any alias.

**Refusal: closed declared list, *excluded*, not flagged. (decided 10-16, landed 10-18)**
- **Rule:** the normalized A response contains a list phrase **and** no alias matches → the item is excluded from **both** of that model's calibration cells, and `refusal` is logged on the A row and in both cells. An alias match governs, so refusal exclusion only removes items from the incorrect class.
- **Why exclusion when the other four are only counted:** a refusal changes what Templates B and C are asked about. The A output becomes B's and C's `[Answer]`, so the confidence calls are then about a non-answer.
- **Admission criterion for the 13-entry list:** a phrase must commit to not answering. Hedges (`not sure`, `probably`) are out, because Template A invites a hedged guess. Identity disclaimers (`as an ai`) are out too.
- **Two consequences, stated on the page:**
  - A wrong answer containing a list phrase is excluded. Separating it from a refusal would need a word cap, the same free parameter refused before.
  - A refusal the list misses is scored incorrect, and the table can't count it.
- **Measured collision:** 3 items have a key inside a refusal phrase (`i`, `no`, `know`). On those, "I don't know" matches the key and scores correct.

**Terminal Template A failure: no fifth code. (G, decided 10-18)** A `done: false` or timed-out A row after the retry removes the item from both cells, logged under the A row's own code in both. The grader writes synthesized B and C rows for those cells, which have no runner row. If A succeeded and its B or C row is missing, the grader stops.

**P(True): renormalize over affirmative + negative mass, and log the retained mass per row.** Raw True-mass conflates *uncertainty about the answer* with *failure to follow the format*, and format-following scales with model size. That puts a size effect inside the measurement, and H1 is a size hypothesis. Renormalizing removes it; logging the retained mass preserves the format-following signal as a reported statistic.

**P(True): fixed position 0, exact match, no floor** (settled 08-21/26; the full rule is in §6).
- **Position 0, no exceptions.** Scanning forward for a matching position would rescue more items on the 1b than the 12b (differential exclusion), and searching for the position where you find what you want is a degree of freedom.
- **Exact match against `{true}` / `{false}` only**, after strip and lowercase. The probe showed `Truth` matching `tru*` as a false positive, and showed the real variant set is narrow (`True`/`TRUE`/`true`/`[sp]True`). **An empirical reversal, not an aesthetic one.**
- **Affirmative mass is the SUM** over all candidates normalizing to `true`.
- **Zero retained mass → unparseable.** 0.5 manufactures a value the model never expressed; 0 treats the absence of `true` as evidence for `false`.
- **No minimum-mass floor:** it would be a number with nothing to justify it. Per-cell mean retained mass is reported instead.
  - *(The comparison to a "minimum-alias-length knob already rejected" appears only in this file and in no lab-log entry. Confirm it or drop it before the off-label bullet cites it — §5c.)*
- **Computed from raw logprobs at full precision**, because concentrated mass can round the denominator to zero.

**Verbalized confidence: strict integer via `int()`. (rebuilt 10-19)**
- **Rule:** strip whitespace, then **one** trailing `%`, then the whole remainder must parse with `int()`. `int()` accepts leading zeros: `085` → 85, `0` and `00` → 0. `85%%` is unparseable.
- **The defect fixed:** the old rule stripped leading zeros as a separate step, so `0` became the empty string and a zero-confidence answer was unparseable.
- **Divided by 100** because ECE, Brier and the reliability diagrams compare confidence against accuracy, which is a proportion. **Not** for AUROC, which is rank-only.
- **`done_reason: "length"` → flag, never exclude.** The entire-response-is-an-integer rule plus the [0,100] bound mean a truncated response fails parsing on other grounds. **The strict rule and the flag-don't-exclude decision are load-bearing on each other.**

**Grader-rule development against pilot outputs is permitted, with a stated test** (08-26).
- **May change:** code that fails to implement a written rule.
- **May not change:** the rules themselves. After seeing outputs, you cannot *prove* a change wasn't chosen for its effect on results.
- **The test:** does the fix make the code do what §6 already says, or does it change what §6 says?
- Pre-freeze rule changes: amend and record. Post-freeze: §12 deviation.

### Runtime environment

**KV cache `f16`, and the decision is overdetermined.**
- *A priori:* a quantized cache adds a second noise source on top of the weight quantization H2a is about.
- *A posteriori:* it measured faster at `num_ctx=2048`.
- The comparison numbers are from the old driver and are scoped as such in §6.

**Flash attention: enabled, pinned, verified from the server log**, not assumed from the environment variable. It is mathematically equivalent but not bit-identical, and it is held constant across all nine cells.

**`keep_alive` replaces the `ollama stop` subprocess.** Generous within a cell, `keep_alive: 0` on the final call to each model, `/api/ps` as verification. `keep_alive: 0` on every call would cold-load constantly and break the warm-up guarantee.

**Digest, version and clean-tree hard stops.**
- Ollama tags are mutable pointers. The 0.32.6 → 0.32.14 auto-update was observed once already.
- A warning would scroll past on a multi-hour run, and a cell computed across two sets of weights is uninterpretable.
- The dirty-tree stop exists because of a measured false-provenance incident on 09-20.

### Metrics and verdicts

**AUROC is the primary metric.** The practitioner question is "can I *trust* this model's confidence", which is discrimination, not calibration. It is bin-independent.

**Both-must-hold across elicitation methods (10-12; prereg §3 Definitions and the Split verdicts table).**
- Each method clears the hypothesis's bar against **its own** pilot-measured floor.
- The overall verdict is the weaker per-method verdict:
  - H1: confirmed > suggestive > falsified
  - H2a: supported > falsified
  - H2b: supported > not evaluable > falsified
- Per-method verdicts are always reported.
- **Averaging was rejected** on §9's ranges precedent: it constructs a value the model never expressed.
- **For the write-up:** both AUROCs share items and answers, so passing both is stricter than passing one, but not two independent confirmations. *(Not yet on the page — §5d.)*

**Tie rate (10-18, §7):** the fraction of **correct–incorrect pairs** with identical confidence, which are the pairs AUROC scores 0.5. Reported per cell for both methods, descriptively. It never changes a verdict.

**Accuracy over retained items (10-19, §7),** so accuracy and AUROC share one item set. Trade-off: a cell that refuses more shows higher retained accuracy, and its refusal rate sits beside it in the exclusion table.

**ECE as co-primary: considered and DECLINED (08-26).**
- The vulnerability is real: AUROC is invariant under monotonic transformations, so compressed-but-rank-preserving confidence reads as a null that is true and misleading.
- **Option four was adopted:** a pre-registered §11 interpretation rule. **Still unwritten — pre-pilot.**

**Accuracy measured per cell as a control.** It adjudicates the mechanistic question in §4.

**Published quants only; asymmetric ladders accepted.** Laz, verbatim: *"What is available to me via an ollama shell command is also available to anyone reading my paper in the future."*

**Δ for H2b is defined over q8_0 → q4_K_M**, not fp16 → q4_K_M, because `gemma3:12b` has no published fp16. An fp16 top rung would make the 12b's Δ smaller *because it was compressed less*, artifactually confirming H2b. This was re-derived three times after evaporating between sessions, and is now in the prereg's Definitions block.

**Within-model vs. across-model rung rule.** Within-model (H2a) uses every rung available at that size. Across-model (H1, H2b) uses only the rung or rung pair that exists at every size.

**H1's primary rung is q4_K_M** — what a bare `ollama pull` resolves to. q8_0 is a declared robustness check. The cost, on the page in §10: the headline size effect is scale *and* compression entangled.

**H2b uses endpoints, not strict monotonicity.** Three points fall in the predicted order ~17% of the time under pure noise. Δ(4B) is descriptive only.

**H2b has a sign precondition:** evaluated only if Δ(1B) > 0; otherwise **not evaluable**, not falsified.

**k = 2 for both H2a and H2b, committed blind 2026-08-01.** It is multiplicative. Identical k because the differing noise floors already account for the differing noise.

**H1 keeps hardcoded thresholds** (≥0.1 confirms · 0.05–0.1 suggestive · <0.05 falsifies); **H2a and H2b use the formula.** Where you have judgment, use it; where you don't, defer to the instrument.

**H2a: supported only if all three per-model checks hold**, with per-model verdicts reported regardless. Its magnitude threshold is per-step, not total span.

**QAT arm is exploratory.** Q4_0 vs Q4_K_M moves two variables at once, and no bit-matched control exists anywhere in gemma3.

**10 bins for ECE, dual scheme:** equal-width primary, equal-mass robustness check.

**Exclusion rules are mechanical, per-item decision procedures.** The "items where all models fail" rule was deleted: it was data-dependent and would delete the hardest items.

---

## 3. Hypotheses (§3 COMPLETE — locked 2026-08-02, amended 2026-10-12)

**Definitions block.** Δ(M) = AUROC(M, q8_0) − AUROC(M, q4_K_M), uniform at all three sizes. fp16 rungs serve only H2a's within-model check and never enter Δ. Both-must-hold: AUROC per elicitation method, each against its own pilot-measured floor.

**H1 (confirmatory).** As parameter count increases across gemma3 1B → 4B → 12B (same family, all at q4_K_M, same prompts), AUROC increases monotonically.
- *Rationale:* a larger model has capacity to store both the facts and how reliably it holds each one, while a smaller model's capacity goes to the facts themselves. So a larger model's confidence **varies** with how well it knows a fact, while a smaller model's is comparatively flat.
- *Rationale history — do not let this regress:* drafts 1–2 were circular; draft 3 named the wrong cause; the current draft uses the capacity mechanism. **Two failure modes: accuracy creep, and circularity.**
- *Prediction:* AUROC(1B) < AUROC(4B) < AUROC(12B), with total gap `AUROC(12B) − AUROC(1B)` ≥ 0.1 confirming. 0.05–0.1 is suggestive.
- *Falsifier:* non-monotonic ordering, or total gap < 0.05.

**H2a (confirmatory, main effect).** Within each model, AUROC decreases monotonically as precision drops. Three separate per-model checks.
- *Rationale:* the confidence signal lives in fine-grained logit differences, which quantization noise corrupts before it touches the argmax.
- Each of the five steps must be ≥ 2 × the pilot noise floor.
- A break at any size is "falsified".

**H2b (confirmatory, interaction — the most original claim).** Δ(1B) > Δ(12B), evaluated only if Δ(1B) > 0.
- The spread must be ≥ 2 × the floor **for the spread**, a different number from H2a's.

**Split verdicts:** a 15-row table in §3 covers every per-method pair.

**E1 (exploratory, labeled).** Sweet-spot map: calibration and throughput against memory footprint. **NOT YET IN §3, and §7 has no throughput or footprint metric to feed it — §5c.**

---

## 4. The open mechanistic question

Does quantization degrade **the stored knowledge** or **the confidence signal that tracks it**? The accuracy control reads out the mixture:
- AUROC and accuracy drop in lockstep → knowledge decay
- AUROC drops but accuracy barely moves → signal fragility
- both degrade at different rates → gray, and the ratio is measurable

---

## 5. Section status — pre-registration file

*Every row read against the prereg as attached on 2026-10-20, after the seven 10-20 amendments. No row is carried forward from the previous handoff.*

| § | Status | What's left |
|---|---|---|
| Header | ⚠️ stale | The `frontier-scale` half of the **Study:** line is factually wrong. Kadavath topped out at 52B, and the roster's 1b and 12b overlap two of his four sizes. Fix it with §2's overlap framing. `Drafted: [7-15-2026]` is a filled value inside brackets, so a pre-freeze bracket scan will false-positive on it. |
| 1. Research question | ✅ fine | Names AUROC, scoped to gemma3 + consumer hardware. |
| 2. Background | ❌ unwritten | Still a note plus `[ ]`. Write 3–5 sentences around overlap, not absence. Read Proskurina et al. 2024 first. The stray 3×3-cell note belongs in §8 or §11. |
| 3. Hypotheses | ✅ complete | **E1 missing.** |
| 4. Models | ✅ complete | — |
| 5. Datasets | ✅ complete except brackets | Pool Rule and draw-re-run paragraphs landed 10-18. `p_weak`, `p_strong`, `N` brackets wait for the pilot. `draw_seed` has an integrity rule and no value. Says "items.jsonl" generically. Its "Free-form has no guessing floor, so a correct answer means the model produced the fact" overstates against §10's forced-response bullet (open). |
| 6. Procedure | ✅ complete | **Changed 10-18 → 10-20:** resume clause names B and C; whitespace-empty answer rule; `int()` parsing rule; Normalize = TriviaQA's `normalize_answer`; Match = whitespace-delimited with the reason against `\b`, hits logged as a list, empty-alias guard; per-row logging gains matched aliases (list), raw word count (int), multi-candidate flag; compliance polarity and count; negation wholly-within / earliest match / normalized / marker boundary; multi-candidate detector; grader file writes synthesized rows and stops on a missing B/C. **Open wording:** Normalize says "copied verbatim into the grader", but the function lives in `triviaqa_normalize.py` (reword once the grader exists); two stray spaces before commas (Match bullet after `normalized_aliases`; the `127.0.0.1` paragraph). **Open decisions:** KV-cache verification path, digest-at-load wording, `keep_alive` 5m, warm-up text, template duplication check (§5c). |
| 7. Metrics | 🟡 partial | Tie rate and accuracy-over-retained landed. **No throughput or memory-footprint metric, so nothing feeds E1.** |
| 8. Analysis plan | 🟡 partial | Differential-exclusion reading and the per-method H1-collision rule are on the page. **Noise-floor procedure unwritten (pre-pilot, four questions in §0). Per-hypothesis walkthrough unwritten.** |
| 9. Exclusion rules | ✅ complete | Refusal rule, 13-entry list, provenance, two consequences, exclusion-not-flag reasoning, and terminal-A cascade all landed 10-18/19/20. Table has four reason-code columns plus retained mass, truncation, compliance, negation and multi-candidate rate columns. |
| 10. Confounds | 🟡 most landed | **Added 10-18 → 10-20:** forced response; refusal-exits-incorrect-class; saturation for both methods; multi-candidate; characters the normalizer leaves alone (both directions plus the attachment cost). Instruct-recipe restatement removed. **Still owed (§5c):** construction artifacts; off-label aliases with the recounted figures; the §5d items not on the page. |
| 11. Null result | ❌ placeholder | It announces a rule for AUROC-flat-while-calibration-degrades and never states it (**pre-pilot**). It needs a design for three hypotheses nulling independently, plus H2b's *not evaluable*. The closing paragraph has no main verb and no terminal punctuation; "noticably" is a typo. |
| 12. Deviations | ✅ ready | Empty by design until freeze. |
| 13. Freeze | ⏳ blocked | §5 brackets; main items file; **OSF step not added** (names only the git tag; where the DOI is recorded is undecided). |

---

## 5b. §6 contents (reference map)

Order: **environment → findings → templates → whitespace rule → parsing rules → parameters → throughput → harness requirements → negation marker list → grader spec → grader-rule declaration → logging**

- **Environment** — hardware, displays, Ollama version, KV cache, flash attention
- **Findings** — P(True) probe · logprobs raw · `top_k` doesn't truncate reporting · cold ≠ warm · degenerate generation · `num_ctx` pinning cost · load/unload table
- **Templates** — A/B/C fenced; Kadavath non-self-referential note
- **Whitespace strip rule** — plus the empty-answer sentence
- **Parsing rules** — P(True); verbalized via `int()`
- **Parameters** — `num_predict` 25/5/10, `num_ctx` 2048, temperature 0, `top_k` 64, `top_p` 0.95, seed 42, `top_logprobs` 10 on B only
- **Throughput** — conditions, table, readings, contamination sources
- **Harness requirements** — answer reuse, warm-up, runner/grader split, `done` first, resume, terminal-A resume clause, keep-first, `load_duration`, loop order, `127.0.0.1`, `keep_alive`, digest/version/clean-tree stops
- **Negation marker list** — 17 markers, 4-word window, observational
- **Grader spec** — normalize (TriviaQA), match (whitespace), per-row logging, compliance, truncation, negation, multi-candidate
- **Grader-rule declaration** — may/may-not change, the test, pre- vs post-freeze, pilot isolation
- **Logging** — runner file vs grader file, field by field

---

## 5c. DECIDED BUT NOT YET WRITTEN — and OPEN

*Items leave these lists only by landing on the page, or (for the open list) by being decided, "considered and declined" included. Referenced by content, never by number.*

### Closed since the last handoff (10-12 → 10-20), all on the page and logged

Refusal pattern list and rule · tie-rate statement · saturation extended to verbalized · resume clause B and C · G (no fifth code) · whitespace-only answer · leading-zero restatement (superseded by the `int()` rule) · instruct-recipe stated twice · §5 Pool Rule · §5 draw re-run · CRLF in the draw files (`5ce1f7b`, `8b87f92`) · the normalizer defect · match boundary · negation window and marker matching · multi-candidate detector · compliance polarity · synthesized grader rows · accuracy over retained items · measurement scripts committed · Apache-2.0 license for the copied function.

### Pre-pilot — unwritten prose

- **§8 noise-floor procedure.** Four questions, per method (§0).
- **§11 option-four interpretation rule.**

### Pre-pilot — code (critical path, §0)

- **Fixtures:** `runner_log.jsonl`, `expected.jsonl` (spec in §5e).
- **Grader:** plus the whole-split test.
- **Pilot analysis code.**
- **Grader output file:** name it, then add it to `.gitignore` (§6 requires it ignored).
- **Grader-session counts**, recorded alongside the pilot:
  - single-character keys: 151 items letter/digit, 527 any character
  - the 3 refusal-phrase collisions
  - the 153 items with left-alone characters
  - the rate of empty A answers
  - how often responses contain a curly double quote, en/em dash or ellipsis (the frequency §10 says is unmeasured)
- **Delete `pilot_runner_log.jsonl` unopened** before the pilot.

### Before freeze — decided, not yet written

- **§10 construction-artifacts bullet.** Three fields carry leftover dataset-construction machinery:
  - answer wiring: `qf_1637`, a valid answer entity on the wrong question
  - `value`: `'(a'` on `qf_1637`, `"A: Basketball"` on `tc_543`
  - `question`: `qw_402`, unstripped CSV escaping (one of the 50 pilot items)

  Uniform across cells. Mis-wiring that doesn't blank a field is mechanically undetectable; `qf_1637` is the existence proof.
- **§10 off-label alias bullet.** TriviaQA was built for reading comprehension, so its Wikipedia-harvested aliases are permissive, which is a false-positive hazard in closed-book use. Figures:
  - normalized alias-set size min 1, max 214 (`sfq_9993`), mean 11.66
  - single-character keys 151 (letter/digit) or 527 (any); **say which definition and why**
  - 3 refusal collisions

  No cap. **Before citing "rejected for minimum alias length", confirm it.** It is recorded only in this file.
- **§10, the 5d items not on the page:** decide placement for each (table in §5d).
- **Header *frontier-scale* + §2 overlap framing**, after reading **Proskurina et al. 2024** (*When Quantization Affects Confidence of Large Language Models?*, NAACL Findings, arXiv 2405.00632). Check method overlap before citing; the contribution is "one family, three sizes, published consumer quants, crossed design, pre-registered falsifiers", not "nobody has looked".
- **§3 E1 + §7 throughput and memory-footprint metrics.**
- **§13 OSF step,** and where the DOI is recorded.
- **§11 closing paragraph:** predicate, punctuation, typo.
- **§5** "items.jsonl" vs `items_pilot.jsonl`; §5's "no guessing floor" sentence against §10's forced-response bullet.
- **Two stray spaces** (§6 Match bullet; `127.0.0.1` paragraph), as a logged amendment.
- **Normalize bullet wording** once the grader exists.
- **README:**
  - repository map lacks `.gitattributes`, `.github/FUNDING.yml`, `CITATION.cff`, `probe5_refusal_phrasing.py`, `triviaqa_normalize.py`, `build_fixture_items.py`, `measure_normalizer.py`, `measure_boundary.py`, `fixtures/`, `third_party/`
  - the Data paragraph says TriviaQA's license is unknown, while TriviaQA's own README says Apache-2.0 covers code and data. If so, `items_pilot.jsonl` is redistributed under it and `third_party/triviaqa/LICENSE` covers it. Reconcile and point at that copy.
  - the status banner will need updating when the grader exists
- **08-28 lab-log line** placing the probe scripts under `probe_out/` (they are at repo root): correction goes in a new entry.
- **`run_pilot.py` stale comments** (checked against the file 10-20):
  - "12b gets used when the full sweep (Step 6+)…" (the 12b is used in the pilot)
  - `KV_CACHE_TYPE`'s comment says "verified via server log", but nothing reads the log
- *Optional:* reword §10's roster-asymmetry bullet; re-run the 1b throughput cells with a longer window.

### Open — not yet decided

**Before freeze:**
- **The freeze date.** Not set, by Laz's decision.
- **`draw_seed`'s value.** The integrity rule exists. Choosing it now would make the commitment checkable rather than declared.
- **KV cache verification path.** §6 pins f16 with a methodological reason and logs the *set* value; nothing verifies it. The flash-attention check (read the server log at load) is the analogous solution.
- **Digest checked at startup**, not "at the point of load, once per model" as §6 says. Defensible; move the code or the line.
- **`keep_alive: '5m'`** equals Ollama's default. Is it the frozen value?
- **Warm-up and unload prompt text** (`'Hello'`, `num_predict` 1) has no home on the page. Code-only is probably fine, but that is a decision.
- **Template text duplicated** between §6 and `run_pilot.py`'s f-strings, with no automated equality check (hand-checked 09-12 and 10-16).
- **Digest-prefix equality check:** optional hardening.

**Before the main sweep (not the pilot):**
- **Keep-first commit-hash stop vs daily commits.** An interrupted multi-hour run becomes un-resumable once the repo changes. Hashing harness files instead would undo the reasoning that the repo-level hash pins the prereg's template text. **A decision, not a bug fix.**
- **Resume robustness.** A line that parses as JSON but lacks a key raises `KeyError` (still true in the 10-20 file). Discard it, or hard stop?

---

## 5d. §10 coverage — the accumulated list against the page (checked 2026-10-20)

**On the page:**
- benchmark contamination (with `unfiltered`)
- quantization confounded with scale (with H1's q4_K_M rung)
- instruct-tuning (cross-study)
- extrapolation limit (driver-aware)
- differential exclusion (→ §8)
- forced response
- refusal exits the incorrect class
- degenerate output
- low retained mass
- saturation (both methods)
- QAT not bit-matched
- roster asymmetry
- multi-candidate
- characters the normalizer leaves alone
- ECE co-primary declined (in §11's first bullet)

**Not on the page — decide where each goes:**

| Item | Likely home |
|---|---|
| vision asymmetry (1b text-only; 4b/12b multimodal) | §10 |
| context asymmetry (32K vs 128K) | §10 |
| thin positive class on the weakest cells | §5 (N formula) or §10 |
| floor compression (1b near 0.5 at q8_0 squeezes Δ(1B), biases against H2b) | §10 |
| both AUROCs share items and answers (correlated methods) | §10 or §8 |
| k × floor is a heuristic; bootstrapped CIs are the clean version | §8 (with the procedure) |
| H1's "bluffs less" contested in the literature | §2 or §10 |
| Hanley–McNeil is the pre-pilot estimate; the measured floor governs | §5 or §8 |
| construction artifacts; off-label aliases | §10 (drafted, §5c) |

---

## 5e. Harness state

### Environment — committed 2026-08-31

Python **3.12.8**, `.venv` in repo root. Prebuilt wheels only: requests, datasets, pandas 3.0.5 (a major release; tutorial code written for 2.x is a likely error source), pyarrow, numpy 2.5.2, scikit-learn, matplotlib. `requirements.txt` frozen. PowerShell execution policy `RemoteSigned`, `CurrentUser`.

- **`.gitignore`:** `.venv/`, `__pycache__/`, `*.pyc`, `.env`, `tempCodeRunnerFile.py`, `pilot_runner_log.jsonl`. The grader output file is not named yet.
- **`.gitattributes`:** `items_pilot.jsonl`, `items_manifest.json` and `fixtures/*.jsonl` all `text eol=lf`. The machine's system git sets `autocrlf true`; the project overrides it to false.

### Dataset facts

Validation split, `unfiltered.nocontext`, revision `0f7faf33…`:
- 11,313 rows, `question_id` unique
- `entity_pages` and `search_results` empty
- 143,174 keys; 0 changed by re-applying `normalize_answer`
- 0 of 131,861 aliases and 0 of 11,313 values contain a standalone article
- 1,016 keys in 516 items begin or end with a non-word character

Pool math, `N = 200 / min(p_weak, 1 − p_strong)` + 10%: p_weak 0.10 → ~2,200 · 0.05 → ~4,400 · 0.03 → ~7,330 · 0.02 → ~11,000. Pool after pilot withdrawal: 11,262.

### Items files — design frozen 2026-08-31

- **Five fields per row:** `question_id`, `question`, `normalized_value`, `normalized_aliases`, `value`. `value` is kept for self-containment, since it is the field that reveals corruption. `answer.type` and a draw index were dropped as second, weaker versions of guarantees already held.
- **Provenance in a sidecar `items_manifest.json`**, not a JSONL header line.
- **Pilot exclusion by subtraction**, not rejection sampling.
- **Pilot is one draw of 50 on both extremes** (`1b-q4_K_M`, `12b-q8_0`).
- **Two draw scripts** (`draw_pilot.py`, `draw_main.py`). The duplication hazard is accepted and named.
- **`draw_seed` is distinct from §6's generation seed 42**, and its value is not chosen. At temperature 0, seed 42 does approximately nothing; it is pinned under "inherit nothing".

### `draw_pilot.py` — COMPLETE 2026-09-05; line endings changed 2026-10-19

- **Pipeline:** load → filter `qf_1637` by id → shuffle (`DRAW_SEED = 8`) → `.select(range(50))` → reshape → write.
- **Seed verified:** three runs returned `odql_4374` at index 0.
- **Outputs opened with `newline='\n'`** since `5ce1f7b`.
  - The committed files were converted CRLF → LF, terminators only: `items_pilot.jsonl` 25,660 → 25,610 bytes; manifest 274 → 262.
  - The ignore-CR diff was empty, and the original timestamp `2026-09-05T21:10:50.315940` was kept.
  - A re-run at seed 8 reproduces the items file byte for byte and the manifest except its timestamp. Restore it from git; never commit a re-run (§5).
- **No dataset revision pin.**

### `run_pilot.py` — steps 1–7 COMPLETE 2026-09-20 (re-read against the 10-20 upload)

Separate from the draw by design: the draw writes a frozen artifact in `'w'` mode; the runner reads that artifact and appends.

- **Startup:**
  - reads `items_pilot.jsonl`, keeping `question` and `question_id` (the grader rejoins the answer key)
  - asserts 50
  - Ollama version hard stop
  - `/api/tags` digest hard stop on both models, logging the *observed* digest
  - `git status --porcelain` clean or hard stop
  - resume scan of the output file
  - commit-hash and Ollama-version agreement across existing rows, or hard stop
- **`run_call`:**
  - `base_options` shared by the request and the row
  - 90 s timeout, one retry, `attempt_count`
  - Ollama error → crash
  - on a timeout, `done` and the timing and raw fields are omitted
  - otherwise each field is logged if present
  - `raw_logprobs` on B; row-level `top_logprobs` is the request value (10 on B, null on A and C)
  - appended, file closed per row
- **Loop:** models outer, items inner. Warm-up per model (`'Hello'`, `num_predict` 1, output discarded). A → B → C per item; a terminal A failure skips B and C. Answer `.strip()`ped on both the live and resume paths. `unload()` sends `keep_alive: 0` and polls `/api/ps` up to 5 times.
- **Measurement calls carry `keep_alive: '5m'`.**
- **Known gaps (§5c):**
  - `KeyError` on a well-formed-but-incomplete resume line
  - `KV_CACHE_TYPE` declared, never verified
  - two stale comments
- **Tests 09-20, all passed:** forced timeout, dirty tree, hash mismatch.
- **Validation run at `4254e66`:** 300 rows, 100 per method, 0 timeouts, 0 `done: false`, 0 retries, no mid-cell reload, warm-up working. Position 1 of the first B row showed the empty-token-no-`bytes` candidate in real data. **Sealed** (see §0, Standing).
- **False-provenance incident, 09-20:** rows stamped with a commit that didn't contain the code that wrote them. This is the measured reason for the dirty-tree stop.
- **Endpoint `/api/chat`, settled 09-10:** all §6 logprob findings were measured there, and the roster is `-it`. The first endpoint comparison was cold-load contamination; warm-vs-warm was bit-identical at all 12 positions. That is the third cold-load-looks-clean incident: a pattern, not a coincidence.

### Normalizer and measurement scripts — 2026-10-19/20

- **`triviaqa_normalize.py`:** TriviaQA's `normalize_answer`, body unchanged. SPDX Apache-2.0 header; license copy at `third_party/triviaqa/LICENSE` (SHA-256 `5CC54833…`). Do not edit the body.
- **`measure_normalizer.py`:** reproduces every 10-19 figure (reproduction check, five empty-string items, idempotence, articles, left-alone characters, refusal phrases and negation markers read from the prereg, self-match under the old rule and the function).
- **`measure_boundary.py`:** reproduces every 10-20 figure (`\b` vs whitespace, edge characters, dash and quote counts, the constructed-response boundary cost).
- **Both scripts:** run from the repo root, import `triviaqa_normalize.py`, write nothing, and pin the revision.
- **The two 10-18 figures that did not reproduce:**
  - 156 single-character aliases → **151** letter/digit, **527** any character
  - 4 refusal collisions → **3**: `bb_5892` i, `dpql_3356` no, `sfq_7794` know

### Grader — NOT STARTED; spec complete on the page

**Inputs:** the runner file and `items_pilot.jsonl`, joined on `question_id`.

**Output:** the grader file (gitignored once named), **one row per (item, model, method)**. That includes synthesized B and C rows for a terminal A failure. The grader stops if A succeeded and B or C is missing.

**Per-row fields:** the triple, `matched`, matched aliases (list), negation flag, raw word count, compliance, truncation, multi-candidate, and exclusion reason. P(True) rows add renormalized P(True), retained mass, and matched-token logprobs. Template C rows add the parsed integer and mapped confidence.

**Done when:** it reproduces every expected fixture row, and the whole-split test fails only `qf_1637`.

### Fixtures

**Done:** `fixtures/items.jsonl`.
- 52 rows, 8,353 bytes, SHA-256 `F24DFD1C…FC54FC`, LF endings, ASCII-escaped.
- Built by `build_fixture_items.py`: keys computed with `normalize_answer`, never typed.
- `question` is prefixed `Fixture:`.
- **One items row per case**, because the runner writes one A row per item per model and the grader joins on the triple.

**Still to write:** `fixtures/runner_log.jsonl` and `fixtures/expected.jsonl`.

**Rules:**
- Key names come from `run_pilot.py`'s row build (`question_id`, `model_tag`, `elicitation_method`, `raw_response`, `raw_logprobs`, `timed_out`, `done`, `done_reason`, `attempt_count`, …).
- `raw_logprobs` copies the shape seen 10-19: a list of positions, each with `token`, `logprob`, `bytes` and `top_logprobs`. The nested list holds 10 entries, sorted descending.
- **Every constructed candidate list sums to at most 1**: check with `math.exp`. fx_023 and fx_024 were first drafted at 1.055 and 1.27.
- Complete A, B and C rows for every item, except the failure cases.
- **Expected values are hand-computed from the prereg, never generated by the grader.**

**Cases** (A response unless noted; "✓" = matched true):

| id | key | response / runner state | expected |
|---|---|---|---|
| 001 | paris, paris france | `Paris, France.` | ✓, aliases [paris, paris france] |
| 002 | exile | `He was exiled.` | not matched |
| 003 | xiaowei yi | `**Xiaowei Yi**` | ✓ |
| 004 | o neil | `O’Neil` (curly) | ✓ |
| 005 | i | `I don't know` | ✓, no exclusion (documented collision) |
| 006 | paris | whitespace only | not matched, word count 0, no exclusion; B and C graded normally |
| 007 | paris | `not Paris` | ✓, negation true |
| 008 | vancouver | `never really truly said Vancouver` | negation true (4th word back) |
| 009 | vancouver | `never really truly once said Vancouver` | negation false (5th) |
| 010 | vancouver | `not Toronto` | not matched, negation false |
| 011 | chihuahua | `Possibly a terrier or chihuahua.` | ✓, multi true |
| 012 | 13mm | `13mm - 15mm, likely 13mm.` | ✓, multi false (documented miss) |
| 013 | orwell | `George Orwell` | ✓, multi false |
| 014 | paris | 11-word answer | compliance false |
| 015 | paris | `done_reason` length | truncation true, score unchanged |
| 016 | 1915 | `I don't know` | refusal on A, B, C |
| 017 | 1915 | `I cannot know, but probably 1915` | ✓, no exclusion |
| 018 | 1915 | `I cannot know, but probably 1914` | refusal (stated consequence) |
| 019 | lyon | `I'm not sure, maybe Paris` | not matched, no exclusion |
| 020 | paris | A `timed_out`, `attempt_count` 2, no B/C rows | A timeout; synthesized B and C timeout |
| 021 | paris | A `done` false, no B/C rows | `no_valid_response` cascade |
| 022 | paris | C `timed_out` | C timeout; B grades normally |
| 023 | paris | B pos 0: True, TRUE, False, Yes | sum the true variants; Yes outside retained mass |
| 024 | paris | B pos 0: Truth, False | Truth not counted; p_true 0.0 |
| 025 | paris | B pos 0: ` True`, `false` | both counted |
| 026 | paris | B pos 0: empty token without `bytes`, then True (+ False) | tolerated, excluded from mass |
| 027 | paris | B pos 0: no true/false candidate | retained 0 → unparseable |
| 028 | paris | B: True only at pos 1 | pos 0 only |
| 029 | paris | C `85` | 85, 0.85 |
| 030 | paris | C `85%` | 85 |
| 031 | paris | C `085` | 85 |
| 032 | paris | C `0` | 0, 0.0 |
| 033 | paris | C ` 100\n` | 100 |
| 034 | paris | C `80-90` | unparseable |
| 035 | paris | C `eighty-five` | unparseable |
| 036 | paris | C `150` | unparseable |
| 037 | paris | C `85 percent` | unparseable |
| 038 | paris | C `100`, `done_reason` length | 100, truncation true |
| 039 | paris | C empty | unparseable |
| 040 | fiddler on roof | `Fiddler on the Roof` | ✓ (internal article) |
| 041 | paris | C `85%%` | unparseable |
| 042 | paris | B `done` false | `no_valid_response` on p_true only |
| 043 | paris | 10-word answer | compliance true |
| 044 | truth or dare | `Truth or Dare` | ✓, multi true (documented false positive) |
| 045 | hague | `The Hague` | ✓ |
| 046 | paris + `""` | a wrong answer | not matched (guard) |
| 047 | 1939–1945 (en dash) | `1939-1945` | not matched (§10 key-side cost) |
| 048 | “casablanca” | `“Casablanca”` | ✓ (whitespace gains over `\b`) |
| 049 | vancouver | `couldn't ever be Vancouver` | negation true |
| 050 | vancouver | `couldn't ever really be Vancouver` | negation false (straddles the edge) |
| 051 | vancouver | `I know Vancouver` | negation false (`no` inside `know`) |
| 052 | casablanca | `“Casablanca”` | not matched (whitespace's cost) |

Fillers in the negation cases contain no articles, markers, whole-word `or`, or refusal phrases.

### Remaining in Slice 1's family

`draw_main.py` — can't be written until the pilot reports p_weak and p_strong. It must:
- read `items_pilot.jsonl`
- subtract those ids from the pool
- draw N with a **different** seed, chosen before it first runs
- pin the dataset revision

### Concepts landed (don't re-explain; do check for regression)

- **2026-08-31:** `import` vs function calls · `=` vs `==` · `len()` · dictionary access · row vs column access · `lambda` · `.filter()` returns new · `assert` as a relationship · comments carry *why*.
- **2026-09-05:** `.shuffle(seed=)` · `.select()` vs slicing · `for` and indentation · `{}` dicts · `.append()` mutates and returns nothing · `with open` · `json.dumps` vs `json.dump` · explicit `encoding='utf-8'` · ALL_CAPS constants.
- **2026-10-19/20:** a normalizer must be the one that built the keys · self-match (grade each gold answer against its own keys) as a test of a grading rule · `\b` vs whitespace boundaries, and why `\b` fails on a key that starts with `£` or `“` · `int()`'s tolerance (leading zeros, `+85`, `8_5`, full-width digits) · Apache-2.0 attribution for a copied function.
- **Error classes met:** `NameError`, `KeyError`, not-callable, `IndentationError`, and the silent class (a wrong key that writes or filters without crashing).

**Autocomplete disabled in VS Code** at Laz's request.

---

## 6. Environment

- **Hardware:** AMD Ryzen 7 9850X3D (8C/16T, 4.70 GHz) · 32 GB (2×16 GB) G.Skill F5-6000J3636F16G DDR5-6000, EXPO enabled, verified at 3003.4 MHz CL36 · XFX Swift Radeon RX 9070 XT, 16 GB GDDR6, reference clocks (2400 MHz game clock), 644 GB/s bandwidth, PCIe 5.0 x16 · Windows 10 22H2
- **Displays:** 4 × 1440p (2 @ 60 Hz, 1 @ 75 Hz, 1 @ 180 Hz), all on the 9070 XT. Framebuffer allocation eats into the margin on the largest cell.
- **AMD Adrenalin 26.8.1**, driver `32.0.31041.1004`. **Auto-update disabled 2026-08-26**; re-enable post-study (`POST_STUDY_TODO.md`).
- **Ollama 0.32.14.** It drifted from 0.32.6 via auto-update; auto-update is now disabled. §13 freezes on 0.32.14.
- **KV cache `f16`:** set via `OLLAMA_KV_CACHE_TYPE` in System Properties, then quit Ollama from the tray and relaunch. A shell `set` never reaches the running server.
- **Flash attention on:** verified from `%LOCALAPPDATA%\Ollama\server.log` (grep "flash"), not assumed.
- **PowerShell chains with `;`, not `&&`.** cmd has no `#` comments. `curl` is aliased to `Invoke-WebRequest`; use `Invoke-RestMethod` or `curl.exe`.

### Logprob check — 2026-08-08

1. **Logprobs are RAW, not temperature-scaled** (temp 0 vs 2: True −0.0310 vs −0.0324).
2. **`top_k` does NOT truncate the returned distribution.**
3. **Cold-load ≠ warm-load:** the first call after load differed; warm calls were bit-identical. **Every model gets a discarded warm-up call.** n=1 on the cold side.
4. **Parser edge case:** an empty-token candidate with no `bytes` key, at position 0 on the 12b.

### P(True) probe — 2026-08-21

- Position 0 carries the answer at both extremes. `1b-q4_K_M`: True 0.94765, False 0.04254, retained 0.99493, P(True) 0.95724. 12b ~1.0.
- Variants seen: `True`/`TRUE`/`true`/`[sp]True`/`Yes`.
- `Truth` matched `tru*`, the false positive that killed prefix matching.
- `Correct` appeared in the tail, unmatched.

### Template B shape — 2026-10-19

One call on `1b-q4_K_M` (hand-written question, not in the pool):
- each position has `bytes`, `logprob`, `token`, `top_logprobs`
- the nested list holds 10 entries, descending, total probability 0.994
- position 0: True −0.0629, False −3.3937, Yes −4.6845, TRUE −5.3292

### Probe 5 — 2026-10-16 (committed `17377bd`)

- 10 hand-written non-pool questions × both pilot extremes, Template A verbatim (repr-checked).
- **0 refusals in 20.**
- Every `load_duration` 0.22–0.24 s.
- A re-run with the version field came back byte-identical.
- Multi-candidate answers at both extremes; markdown bold on one 1b answer.

### Throughput — re-measured 2026-08-26 on driver 26.8.1

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

- **The spill was a driver artifact.** `12b-it-q8_0` was 15.4 tok/s (~31% of ceiling) on the old driver and is 43.9 (~89%) on 26.8.1. The old "4× step / VRAM ceiling / 48%" reading must not be reintroduced.
- The 1b cells are within run-to-run noise (~6%).
- VRAM peak is 15,474 MB of 16,304 MB.
- Desktop apps cost nothing measurable.
- **Three contamination sources produced clean-looking numbers** — first-in-loop, keep-alive stacking, other GPU consumers. None showed in `load_duration`, so the protection is procedural.

### Other measured facts

- **`localhost` vs `127.0.0.1`:** ~900 ms per call via `localhost` (IPv6 first, Ollama binds IPv4).
- **Warm `load_duration` is a fixed ~215.5 ms** per call (~72% of sweep runtime). What it is remains an open, parked question.
- **Runtime:** ~8.1 s per item across nine cells. N = 900 / 1500 / 2200 → 2.0 / 3.4 / 5.0 h.
- **Degenerate generation:** the Lloyd Webber item on `1b-q8_0` returns `done: false` at `num_predict ≥ 32`. **A non-reproduction is only evidence if it reproduces the original conditions.**
- **`num_ctx` pinning cost the 12b throughput** on the old driver; not re-checked.

---

## 7. Sources gathered

- **Kadavath et al. 2022**, arXiv 2207.05221. The paper being replicated.
- **Tian et al. 2023**, *Just Ask for Calibration*. Verbalized confidence beats logits.
- **Leng et al. 2025**, arXiv 2410.09724 (ICLR 2025). About verbalized confidence under RLHF: a prediction about one method, not a refutation of H1.
- **"Mind the Confidence Gap"**, OpenReview, Sept 2025.
- **Dunning-Kruger paper**, arXiv 2603.09985 (read critically). H1's rationale in different words; chase the primary source.
- **arXiv 2311.13240**, *On the Calibration of LLMs and Alignment*. No significant ECE degradation from RLHF; cite with Leng.
- **Proskurina et al. 2024**, arXiv 2405.00632, NAACL Findings. **Not yet read**; belongs in §2.
- **TriviaQA** (Joshi et al., ACL 2017); evaluation code at `mandarjoshi90/triviaqa` (Apache-2.0, commit `51b5359` for `normalize_answer`).

---

## 8. Slice roadmap

- **Slice 0** — pre-registration. Pre-pilot prose remaining: §8 procedure, §11 rule. Pre-freeze prose in §5c.
- **Slice 1** — dataset loader. **COMPLETE 2026-09-05**, two sessions.
- **Slice 2** — runner + grader. ← here.
  - Runner complete 09-20.
  - Grader spec complete on the page 10-20; fixtures items file built; grader not started.
- **Public release 2026-10-11** (not a slice).
- **Slice 3** — full nine-model roster.
- **Slice 4** — analysis. The pilot-analysis portion (AUROC, floors) is pre-freeze.

**Pilot:** one draw of 50 on both extremes, before freeze, data discarded. It determines **six** numbers: p_weak, p_strong, and per method an AUROC noise floor and a spread noise floor. **A materially wider measured floor is a §12 disclosure**, stated in advance.

**Freeze mechanics:**
1. Commit, then `git tag -a prereg-frozen -m "Slice 0 frozen"`.
2. Hash the file and confirm it matches the commit.
3. Register on OSF and record the DOI beside the commit. **§13 does not yet say this.**

**Scope risk:** if something must be cut for time, cut the QAT arm or run at smaller N and disclose. Never cut the parts that make the study interpretable.

---

## 9. Working process

**Division of labor.** Laz writes the research content: hypotheses, rationales, thresholds, predictions, falsifiers. Claude's job is adversarial review: unfalsifiable phrasing, circular rationales, data-dependent exclusions, metrics that don't answer the stated question, contradictions between sections. Claude **declined** to draft the hypotheses, and that is load-bearing: the pre-registration *is* the research identity.

**Explanation protocol.** Name the term, state the problem it exists to solve, show the concrete failure it prevents, then apply it to the file. Worked examples with real numbers land better than definitions.

**Concepts explained and confirmed landed:**
- threshold = k × floor is multiplicative
- bootstrapping resamples with replacement
- more resamples don't reduce uncertainty, only N does
- *not evaluable* vs *falsified*
- `num_ctx` vs `num_predict`
- raw vs renormalized mass
- digest = cryptographic hash
- a priori vs a posteriori
- AUROC = P(random correct ranks above random incorrect), ties count 0.5
- AUROC is computed within one cell, rank-only, undefined only with an empty class
- saturation can be genuine overconfidence

**Manual mile.** `calibration_lab` is the artifact Laz can put his name on without an asterisk. The bar: rebuild the harness solo from a blank editor. **Its deadline needs re-anchoring;** the original was tied to a transfer plan no longer being pursued.

**Laz's stated recurring correction pattern:** drafts contain the *evidence* for a claim without the claim itself, or keep the conclusion and drop the *provenance*. **The check:** could a reader who doesn't know the answer reconstruct it from the page? Run it on the last sentence of each block.
- **Seen on 10-18 and caught in review:** a line saying a re-run dirties the tree without saying why.

**Tone that works:** direct pushback with reasoning; flagging the crack rather than smoothing it; handing back the rows that must be his. He asks to be graded honestly and uses it well. He says "unpack that" when vocabulary outruns him.

**Standing rule (2026-09-14):** any claim about what a file says arrives as section and bullet plus verbatim text, or as "I haven't checked that." Never "your prereg says X." **Apply it to Claude's own drafts and to this file**; that is where it fails.

**Claude's misses, 10-16 → 10-20 (all caught, all logged):**
- Cited §10 from this file instead of the page: a forced-response entry that didn't exist.
- Called a correct-class effect and an incorrect-class effect "the same direction".
- Framed a fixture with an article in the alias as a "declared false negative". Nothing declared it, and the data has none.
- fx_023 and fx_024: candidate lists summing to 1.055 and 1.27, written without the arithmetic.
- Said fixture cases could share an items row.
- Listed four negation cases under three ids.
- Gave an example "unreachable" definition that contradicts itself, since a key always reaches itself.
- Repeated the 10-18 figures 156 and 4 and put them into proposed prereg text; neither reproduces.

**Rules added from those misses:**
- Re-run a figure before it enters the prereg.
- Compute fixture arithmetic.
- Check the data can produce the state a fixture tests.
- Before asking for a decision, check what it depends on.
- Name the file with the section: `SESSION_PROTOCOL §B`, not "§B".
- A date in this file needs a source.

**What worked, 10-19/10-20:** grading every gold answer against its own keys found the normalizer defect, which would otherwise have reached the pilot as a grader "bug". Committing the measurement scripts and re-running them caught two stale numbers before they reached the prereg. Measuring the data before writing the grader is now the method.

---

## 10. Living-doc gap — the reason this file exists

`calibration_lab` once had no home in the doc system and evaporated from awareness during midterms. **The leak was real and measured:** six settled decisions were re-derived from scratch. That was a transfer failure between conversation and disk. The second failure mode (decided logged as landed) is caught by §5c.

**Companions:**
- ✅ `lab_log.md` — the dated, append-only record; measurements and credits live there.
- ✅ `README.md`, `LICENSE`, `CITATION.cff` — the public front door. **Keep the repository map current** (behind as of 10-20; see §5c).
- ✅ `SESSION_PROTOCOL.md` — adopted 08-29.
- ✅ `POST_STUDY_TODO.md` — re-enable Ollama and driver auto-update; revert the KV cache.
- ⬜ A decisions log — §2 here is doing that job.

**Canonical prereg copy in the repo only:** a frozen artifact in a mutable store isn't frozen.

---

## 11. Git state

```
556b441  2026-10-20 Lab log 10-20 (header hash of this file)
1c2fa48  2026-10-20 Seven prereg amendments; fixtures/items.jsonl; triviaqa_normalize.py; build_fixture_items.py; measure_normalizer.py; measure_boundary.py; third_party/triviaqa/LICENSE; .gitattributes; README license line
3ff0833  2026-10-19 Lab log 10-19: normalizer defect found by measurement, int() and CRLF fixes, nine prereg amendments
3e429f0  2026-10-19 Nine prereg amendments (normalizer, int(), match list, compliance, negation, grader rows, accuracy, refusal on A)
8b87f92  2026-10-19 .gitattributes: eol=lf for the draw files
5ce1f7b  2026-10-19 draw_pilot.py newline='\n'; draw files CRLF→LF, terminators only
6d7ed5b  2026-10-18 Prereg prose amendments and lab log entry (thirteen amendments)
4d737e8  2026-10-16 Lab log 10-14 to 10-16: probe 5, refusal list settled, push status recorded
17377bd  2026-10-16 Probe 5
7f4c892  2026-10-14 GitHub Sponsors FUNDING.yml
b351c13  2026-10-12 Handoff rewritten against 28a33de
28a33de  2026-10-12 Both-must-hold decided; §3 split verdicts; prereg + lab log 10-12
032ba89  2026-10-11 Handoff rewritten against 94430cf
94430cf  2026-10-10/11 public-release prep — README, LICENSE, CITATION.cff, prereg author + probe pointer, lab log
da50cea  2026-09-20 Updated handoff
09c815e  2026-09-20 Appended lab log 09-20
b9a25be  2026-09-20 Lab log entry 09-20
4254e66  2026-09-20 TEST: reverted back to original state - timeout = 90
a2bf59a  2026-09-20 TEST: temporary timeout=0.001 for forced-timeout verification
de90f21  2026-09-20 step 6 hardening
8253911  2026-09-20 step 6: full loop, warm-up, unload, resume, all three templates
ffd3e78  2026-09-18 step 5 of runner mostly complete
6779746  2026-09-18 prereg fixes landed; step 5 unblocked
eb83167  2026-09-18 updated handoff
e4f28e4  2026-09-18 Prereg review: ~20 amendments, lab log, POST_STUDY_TODO.md
80287c6  2026-09-14 updated handoff
9f87f53  2026-09-14 lab log 09-12/09-14
ea5699f  2026-09-10 Updated handoff
ff7df62  2026-09-10 runner steps 2-4; two prereg updates
2d73604  2026-09-05 Slice 1 finished
207f989  2026-09-01 Handoff: re-plan to harness-first
cb92a94  2026-08-31 Slice 1: TriviaQA loader
99a126d  2026-08-29 another small post-session fix
101b7db  2026-08-29 quick fix post-session
a213298  2026-08-28 (last verified hash of the 08-28 session)
23e58ee  2026-08-27 S6: reorder + throughput re-measurement
a37c996  2026-08-27 S6: parsing rules, throughput, logging, grader-rule declaration
8438601  2026-08-09 section 5 completed
f8a12b4  2026-08-01 Section 3 completed
3496554  2026-06-24 pre-registration template WIP
```

**Verified in chat:**
- `032ba89..28a33de` = prereg + lab log only (10-16).
- `3ff0833` pushed, origin in sync (10-19).
- The order of `5ce1f7b`, `8b87f92`, `3e429f0` within 10-19 is as the log describes; confirm with `git log --oneline 6d7ed5b..3ff0833`.

**Reported by Laz, 10-20, without git output in chat:** `1c2fa48` (nine files) and `556b441` pushed; local, `origin/master` and GitHub all at `556b441`.

**Not verified:** the file names on the `1c2fa48` line. They come from the lab log; there are nine, matching the reported count. Confirm with `git show --stat 1c2fa48`.

**Next open (SESSION_PROTOCOL §C.1):** the header hash is `556b441`, and exactly one handoff-only commit is past it. Then `git status -sb` in sync with origin, `git show --stat 1c2fa48` against the line above, and `git grep -n WORK_COMMIT -- lab_log.md` returning nothing.

**Standing git facts:**
- Remote `origin` = `https://github.com/Lxzxrus/calibration_lab.git`, branch `master`. Any other machine must clone fresh.
- Commits from `94430cf` on use the GitHub noreply email; earlier commits keep the personal address (rewriting would change every hash the lab log cites).
- `core.autocrlf false` in the project; `.gitattributes` pins LF on the draw and fixture files.
- `POST_STUDY_TODO.md` is committed, not ignored.
- Commit messages are descriptive. "quick fix post-session" proved unfindable.
