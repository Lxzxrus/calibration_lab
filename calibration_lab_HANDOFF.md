# `calibration_lab` — Handoff

*Operational snapshot. Drop this + the pre-registration into a fresh chat and say hello — that's enough to resume.*

**Last updated:** 2026-08-27 · **Synthesized against commit:** `23e58ee` · **Status:** Slice 0 (pre-registration) in draft, not frozen

---

## 0. YOU ARE HERE

**§6 (Procedure) is COMPLETE** — content, structure, and internal consistency. Every block written, every decision recorded, reordered into a navigable shape, committed as `23e58ee`. That was the longest-running open section on the project.

**Pre-session brief (written 2026-08-27, end of the 08-26 session):**

Last session ran long and did three things. (1) Closed §6 entirely: both parsing rules, the grader-rule development declaration, logging split into per-run/per-row, digest and version verification, flash attention, and the environment block including a full hardware spec. (2) Discovered mid-session that the throughput table predated the current AMD driver, re-measured all nine cells, and found the `12b-it-q8_0` spill was a **driver artifact, not a hardware limit** — that cell went 15.4 → 43.9 tok/s and is now fully resident. The old table would have frozen a false mechanism into the document. (3) Repaired seventeen days of uncommitted git history and stood up `lab_log.md`.

**Next actions, in order:**
1. **§5's runtime paragraph.** Still carries `~166 / ~36 tok/s` and "4-6+ hours" and the spill claim. Now stale against *three* generations of numbers. Recompute from the current table. **This has been flagged for three consecutive sessions — do it first, it takes two minutes.**
2. **§10 transcription.** Delete the stale qwen3/MMLU bullets, fill `[others]` from the accumulated list below, rewrite the extrapolation-limit entry around the driver finding, add the ECE-declined entry.
3. **§11 redesign.** The current text is a placeholder recording the ECE decision, not the rule. Needs the full null-result structure plus the option-four interpretation rule.
4. **§8's noise-floor procedure** — blocking, two floors required.
5. **§1 header line, §2 background** — transcription of material already articulated.
6. **E1 is missing from §3 entirely**, and §7 has no throughput or footprint metric to feed it.

**No study data has been run.** No harness code exists except a synthetic ECE/reliability-diagram experiment (`ece_test.py`) written for learning. All Ollama calls so far are environment characterization.

---

## 0b. Working protocol (adopted 2026-08-26)

Established after a stale handoff caused a session to open on false premises and produced three incorrect corrections.

- **One chat = one session = one handoff update = one commit.** A single chat holding several days of work is what produced the date confusion and the drift.
- **Commit before uploading.** The uploaded file is then the committed file by construction.
- **Upload the prereg AND handoff together**, with `git log -1 --format="%h %ad %s"` and `git status --short`. The hash proves which version; a clean status proves nothing was edited after.
- **Claude synthesizes the handoff against the actual file** and reports every claim that doesn't verify. A handoff composed from conversation rather than from the page is how six settled decisions evaporated.
- **The handoff header records the commit it was synthesized against.** Next session opens by checking that against `HEAD`.
- **Open-but-undecided items get their own section** (§5c below) and leave it only by being decided — including "considered and declined."
- **The prereg governs where prereg and handoff disagree.**
- Handoff stays descriptive. Reasoning that belongs in the prereg gets written by Laz, into the prereg, in his words.

**Known failure mode, still live:** decisions get logged in the handoff as *landed* when they were only *decided*. Every mismatch found on 2026-08-26 was of this kind. §10's fix #2 — a running "decided but not yet written" list at the bottom of the section being worked — was adopted in August and never actually maintained. §5c is that list.

---

## 1. What this project is

A standalone research study measuring **calibration** — whether a model's confidence matches its accuracy — on small, quantized, instruct-tuned models running on consumer hardware.

Conceptual replication of **Kadavath et al. 2022** (arXiv 2207.05221, *Language Models (Mostly) Know What They Know*), whose cleanest results were on large **base pretrained** models. This study asks whether that picture survives instruct-tuning, quantization, and small scale.

**Dual audience, deliberately:** an academic portfolio artifact (a professor sees someone learning to navigate research) *and* a community finding (a reader with 8GB of VRAM learns which model at which quantization is actually trustworthy). Neither is the afterthought. This framing drives most scope decisions below.

**Research identity it serves:** *"I study whether AI systems know what they know and how humans stay meaningfully in control when they don't."*

**Timeline:** first reliability diagrams by September 2026. Note: this is self-imposed. The real external gates are the REU in mid-December and PNNL CCI in January.

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
- Entire response must parse as an integer after stripping **whitespace, then trailing `%`, then leading zeros**, in that order. Divided by 100 to put both methods on [0,1] so AUROC can compare them.
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

**ECE as co-primary: considered and DECLINED (2026-08-26).** The vulnerability is real — AUROC is invariant under monotonic transformations, so if quantization compresses confidence while preserving rank, AUROC reports a null that is true and misleading. Four options were weighed; **option four adopted**: keep AUROC confirmatory, and pre-register an interpretation rule in §11 stating that AUROC-flat-while-ECE-or-Brier-degrades is reported as a named finding rather than a null. Costs no new confirmatory threshold and no third noise floor; lands in §11, which needs rewriting anyway. **Only works if written before the pilot.** Co-primary was declined against the timeline; that goes in §10 as considered-and-rejected, which is judgment rather than omission.

**Accuracy measured per cell as a control.** Free, and it's the instrument that adjudicates the open mechanistic question — see §4.

**Published quants only; asymmetric ladders accepted.** Laz's reasoning, verbatim: *"What is available to me via an ollama shell command is also available to anyone reading my paper in the future."* Methodological principle, not a fallback.

**Δ for H2b is defined over q8_0 → q4_K_M**, not fp16 → q4_K_M. **`gemma3:12b` has no published fp16.** Using fp16 as the top rung would mean the 12b's Δ spans 8→4.8 bits while the 1b/4b span 16→4.8 — the 12b would show a smaller Δ *because it was compressed less*, artifactually confirming H2b. **Re-derived three separate times after evaporating between sessions — now in the prereg's Definitions block.**

**Within-model vs. across-model rung rule.** Within-model (H2a) uses every rung available at that size; across-model (H1, H2b) uses only the rung or rung pair that exists at every size.

**H1's primary quantization rung is q4_K_M.** Both exist at all three sizes, so "same quantization" left a free post-hoc choice. q4_K_M because a bare `ollama pull` resolves to it — what the target reader actually runs. **q8_0 is a declared robustness check.** **Cost, must land in §10:** at q4_K_M every model is compressed, so the headline size effect is scale *and* compression entangled.

**H2b uses endpoints, not strict monotonicity.** Three points in the predicted order occur ~17% of the time under pure noise, and a difference-of-differences is three subtractions deep. Δ(4B) is measured and **declared descriptive context, not part of the verdict**.

**H2b has a sign precondition.** All-negative Δs can satisfy `Δ(1B) > Δ(12B)` while contradicting the premise. Evaluated only if Δ(1B) > 0; otherwise **not evaluable**, not falsified. *Not evaluable* and *not supported* are distinct verdicts throughout §3.

**k = 2 for both H2a and H2b, committed blind 2026-08-01.** Multiplication, not subtraction — the floor is in AUROC units, k is a bare count of noise-widths. Identical k because **the differing noise floors already account for the differing noise**; a larger k on H2b would charge it twice for the same fact.

**H1 keeps hardcoded thresholds; H2a/H2b use the formula.** **Where you have judgment, use it; where you don't, defer to the instrument.**

**H2a's verdict rule: supported only if all three per-model checks hold**, with per-model verdicts reported individually regardless. A 2-of-3 outcome is a genuine finding and must not vanish under a bare "not supported."

**H2a's magnitude threshold is per-step, not total span.** The claim is that each drop in precision costs something.

**QAT arm is exploratory.** `gemma3:4b-it-qat` is **Q4_0**; the standard 4b is **Q4_K_M**. Different schemes, so the comparison moves two variables. **The QAT/non-QAT scheme split is structural across the whole family** — verified 2026-08-09 — so no bit-matched control exists anywhere in gemma3. Ollama's quantizer also refuses Q4_0.

**10 bins for ECE, dual scheme.** Equal-width primary, equal-mass robustness check. Declaring primacy in advance is required, or reporting two ECEs is a fresh degree of freedom.

**Thresholds (H1): ≥0.1 confirms · 0.05–0.1 suggestive · <0.05 refutes.** Chosen by decision relevance, not statistical convention. **Total gap now defined** as `AUROC(12B) − AUROC(1B)`.

**Exclusion rules are mechanical, per-item decision procedures.** The "items where all models fail" rule was **deleted** — data-dependent, and it would delete the hardest, most informative items.

---

## 3. Hypotheses (§3 COMPLETE — locked 2026-08-02)

**Definitions block.** Δ(M) = AUROC(M, q8_0) − AUROC(M, q4_K_M). Uniform at all three sizes. fp16 rungs serve only H2a's within-model check and never enter Δ.

**H1 (confirmatory).** As parameter count increases across gemma3 1B → 4B → 12B — same family, all sizes at q4_K_M, same prompts — AUROC increases monotonically.
*Rationale:* a larger model has capacity to store both the facts it was trained on and how reliably it holds each one; a smaller model's capacity goes to the facts themselves. So a larger model's confidence **varies** with how well it knows a given fact, while a smaller model's is comparatively flat — and that variation is what AUROC reads.
*Rationale history — do not let this regress:* drafts 1–2 circular; draft 3 named the wrong cause (knowledge → accuracy, not discrimination); draft 5 (current) cut the accuracy material and replaced "knows more of what it doesn't know" with the capacity mechanism. **Two failure modes: accuracy creep, and circularity.** Test: could you delete the rationale and lose any information beyond H1's statement?
*Prediction:* AUROC(1B) < AUROC(4B) < AUROC(12B), total gap `AUROC(12B) − AUROC(1B)` ≥ 0.1 confirming. *Band:* 0.05–0.1 suggestive. *Falsifier:* non-monotonic ordering, or total gap < 0.05.

**H2a (confirmatory, main effect).** Within each model, AUROC decreases monotonically as precision drops. Three separate per-model checks, not one interleaved chain.
*Rationale:* the confidence signal lives in fine-grained logit differences; quantization noise corrupts those before it touches the argmax.
*Prediction:* stated orderings, each step independently ≥ 2 × pilot noise floor, across all five comparisons.
*Falsifier:* any ordering other than predicted, or **any per-step gap** below the magnitude threshold. (Corrected 2026-08-26 — previously said "the change (Δ)", which misused Δ.)

**H2b (confirmatory, interaction — the most original claim).** Δ(1B) > Δ(12B).
*Rationale:* larger models have enough weights to absorb compression; smaller models have no slack.
*Precondition:* evaluated only if Δ(1B) > 0.
*Prediction:* spread ≥ 2 × the pilot-measured floor **for the spread** — a different number from H2a's.

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

*Verified against commit `23e58ee` for §6. §1–5 and §7–13 checked against the 2026-08-27 morning upload; re-verify next session.*

| § | Status | What's left |
|---|---|---|
| Header | ⚠️ stale | "Study:" line still uses the old Kadavath framing. `Drafted: [7-15-2026]` is a filled value inside brackets — a pre-freeze bracket scan will false-positive on it. |
| 1. Research question | ✅ done | Written, names AUROC, scoped to gemma3 + consumer hardware. |
| 2. Background | ❌ unwritten | 3–5 sentences. Kadavath on base models, Tian 2023 on verbalized confidence, why small/quantized/instruct-tuned might differ, the community motivation. The stray 3×3-cell note belongs in §8 or §11. |
| 3. Hypotheses | ✅ COMPLETE | Locked 2026-08-02. H2a falsifier and H1 total-gap fixed 2026-08-26. **E1 missing entirely.** |
| 4. Models | ✅ COMPLETE | Locked 2026-08-08. |
| 5. Datasets | 🟡 **one stale paragraph** | **Runtime paragraph still says ~166 / ~36 tok/s, 4-6+ hours, and "spills into system RAM." All three superseded.** Three brackets outstanding (`p_weak`, `p_strong`, `N`) — pilot fills them. |
| 6. Procedure | ✅ **COMPLETE** | Content, structure, consistency. Committed `23e58ee`. |
| 7. Metrics | 🟡 partial | No throughput or memory-footprint metric, so nothing feeds E1. |
| 8. Analysis plan | 🟡 partial | Needs the per-hypothesis walkthrough **and the noise-floor measurement procedure**. |
| 9. Exclusion rules | 🟡 near-done | Timeout filled at 90s. `no_valid_response` still carries a leftover "within N seconds" clause duplicating the timeout rule — should be `done: false` only. **Exclusion table has no `no_valid_response` column.** Consider adding mean-retained-mass and truncation-rate columns; it's the only per-cell reporting structure in the document. |
| 10. Confounds | 🟡 partial | Stale qwen3/MMLU bullets. `[others]` unfilled. Extrapolation entry needs rewriting around the driver finding. ECE-declined entry needed. |
| 11. Null result | ❌ **placeholder** | Records the ECE decision but not the rule. Needs full redesign — three hypotheses can null independently, and H2b can come back *not evaluable*. Option-four interpretation rule lands here. |
| 12. Deviations | ✅ ready | Empty by design until freeze. |
| 13. Freeze | ⏳ blocked | Two threshold numbers bracketed until the pilot. `items.jsonl` not yet committed. |

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

## 5c. DECIDED BUT NOT YET WRITTEN

*Items leave this list only by landing on the page. Nothing else.*

1. **§5 runtime paragraph** — recompute from the current table. Three sessions overdue.
2. **§10: extrapolation limit, rewritten** — on a 16 GB card driving four 1440p displays, the largest cell fits with under 1 GB of margin, and a driver update moved it from spilling to resident. Peak 15474 MB against 16304 MB available, 2256 MB desktop baseline.
3. **§10: ECE co-primary considered and declined**, with the reason.
4. **§10: delete qwen3/MMLU bullets**, fill `[others]` from §5d.
5. **§11: the option-four interpretation rule** — currently a placeholder. Must be written before the pilot or it's post-hoc.
6. **§3: E1**, and **§7: throughput + memory footprint metrics** to feed it.
7. **§9: delete the "within N seconds" clause** from `no_valid_response`; add its column to the exclusion table.
8. **§8: noise-floor measurement procedure.** Two floors.
9. **`items.jsonl` committed** — §5 promises it.
10. **Lab log placement decided** — currently untracked in the repo. §10's rule says vault, but the prereg now cites it by name and a frozen published document can't cite a vault note. Commit or `.gitignore`, don't leave untracked.
11. **Re-enable AMD driver auto-update and Ollama auto-update post-study.** Disabled 2026-08-26.
12. *Optional:* `eval_count` on a compliant Template C response, to settle whether gemma3 splits digits. Two minutes.
13. *Optional:* re-run the three 1b cells at higher `num_predict` for a longer timing window, so every row in the throughput table means something.

---

## 5d. §10 accumulated list

benchmark contamination (gemma3 has likely seen TriviaQA) · quantization confounded with scale · **H1's primary rung is q4_K_M, so the headline size effect is measured on compressed models throughout** · vision asymmetry (1b text-only; 4b/12b multimodal) · context asymmetry (32K vs 128K) · differential exclusion across cells threatening H1/H2b · thin positive class on the weakest cells · **floor compression: if the 1b's AUROC at q8_0 is near 0.5 it has little room to fall, squeezing Δ(1B) and biasing against H2b** · **saturation: the 12b pinning near 1.0 risks ties in P(True); ties push AUROC toward 0.5, biasing against H1 for reasons unrelated to the capacity mechanism — the mirror of floor compression, different mechanism, different hypothesis** · **the k × noise-floor rule is a heuristic; bootstrapped CIs are the clean version, and if not implemented that must be stated** · QAT arm not bit-matched · **extrapolation limit, driver-aware version** (see §5c item 2) · H1's "bluffs less" contested in literature · **cold-load logprob variance observed once (n=1)** · **the AUROC noise floor is estimated via Hanley–McNeil pre-pilot; the pilot's measured floor governs** · **`unfiltered` avoids compounding contamination but does not remove it** · **degenerate generation at 1b: some "incorrect" answers are non-answers rather than wrong facts** · **forced response puts lucky guesses in the correct class; uniform across cells** · **TriviaQA used off-label** — built as a reading-comprehension benchmark, so its Wikipedia-harvested aliases are deliberately permissive; closed-book generation makes that permissiveness a false-positive hazard · **the `value` field carries scraping artifacts** (`"A: Basketball"` on tc_543) — `normalized_value` is canonical · **throughput numbers are only valid on an otherwise-idle GPU with the previous model unloaded** · **low retained mass produces a renormalized value computed from tail probabilities, less stable than the same value from dominant ones; a minimum-mass threshold was considered and rejected as an unjustifiable free parameter** · **ECE co-primary considered and declined against the timeline** · **throughput measured on one driver version; a driver update moved the largest cell from spilling to resident**

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

- **Slice 0** — pre-registration. ← *here. §3, §4, §6, §7 done. Blockers: §5 runtime, §8 noise floor, §11 redesign, §10 transcription.*
- **Slice 1** — dataset loader. TriviaQA validation → local JSONL.
- **Slice 2** — runner (one model, one method) + grader. Append-only JSONL.
- **Slice 3** — second elicitation method; loop the roster.
- **Slice 4** — analysis: reliability diagrams, ECE, Brier, AUROC, accuracy, exclusion table, throughput. Plus the noise-floor computation.

**Pilot is mandatory, runs before freeze, data discarded.** 50 items each on `gemma3:1b-it-q4_K_M` and `gemma3:12b-it-q8_0` — both extremes, because N's constraint is two-sided. **Different seed**, and **pilot items excluded from the main draw pool**.

Determines **four** numbers: p_weak, p_strong, the AUROC noise floor, and the spread noise floor. **A materially wider measured floor is a §12 disclosure**, stated in advance.

**Freeze mechanics:** `git tag -a prereg-frozen -m "Slice 0 frozen"`. Record the hash in the header. **Before tagging, hash the file you edited and confirm it matches the commit** — a stale handoff costs a session; a stale freeze costs the claim.

**Scope risk worth naming:** the document is nearly done; the harness doesn't exist. Slices 1–4 are where beginners lose months. If something must be cut for time, cut there — drop the QAT arm, or run at smaller N and disclose — not from the parts that make the study interpretable.

---

## 9. Working process

**Division of labor.** Laz writes the research content — hypotheses, rationales, thresholds, predictions, falsifiers. Claude's job is adversarial review: unfalsifiable phrasing, circular rationales, data-dependent exclusions, metrics that don't answer the stated question, contradictions between sections. Claude **declined** to draft the hypotheses; that's load-bearing, because the pre-registration *is* the research identity.

**Explanation protocol.** Name the term, state the problem it exists to solve, show the concrete failure it prevents — then apply it to the file. Don't slow down; decompress. Worked examples with actual numbers land far better than definitions.

**Concepts explained and confirmed landed** (don't re-explain from scratch; do check they haven't regressed): threshold = k × floor is multiplicative · bootstrapping is resampling *with replacement* · more resamples don't reduce uncertainty, only N does · *not evaluable* vs *not supported* · `num_ctx` vs `num_predict` · raw vs renormalized mass · **digest = cryptographic hash, same thing as a git commit hash** · **a priori vs a posteriori** · **AUROC = P(random correct ranks above random incorrect), ties count 0.5, which is why saturation degrades it**.

**Manual mile.** ARIA is ~5% Laz / 95% Claude by his own assessment. `calibration_lab` is the corrective — small enough to write alone, the artifact he can put his name on without an asterisk. The bar: rebuild the harness solo from a blank editor by OSU arrival.

**Progress note, 2026-08-26.** Longest session yet. Four things worth recording as evidence. (1) **He caught the stale handoff himself** at the top of the session — noticed the date was wrong and stopped the session rather than working from it. That prevented hours of work built on false premises. (2) **The P(True) probe reopened a decision he'd already made**, and he took the reversal on evidence rather than defending the earlier call. (3) **He questioned whether the driver mattered**, which surfaced that the throughput table predated it — and chose re-measurement over disclosure, which turned out to invalidate a mechanism he'd have otherwise frozen into the document. (4) He asked "should we hold the number accountable to both value and format?" on leading zeros — the right frame, and he reached the correct answer via his own precedent rather than by being told.

**The recurring correction pattern — his stated achilles heel.** Drafts contain the *evidence* for a claim without the claim itself. Diagnosis: curse of knowledge, not a comprehension gap. Rereading won't fix it because his brain supplies the missing inference. **The mechanical check: after writing a justification, ask whether a reader who doesn't know the answer could reconstruct it from the page — and run it on the last sentence of each block specifically**, since the conclusion is what gets dropped. Note the variation observed 2026-08-26: he began keeping the conclusion and dropping the *provenance* instead (the quantity without the observation that produced it). Same root, different half.

**Register.** Trend is real and improving: the throughput block took three passes, P(True) took five, `num_predict` took three, and he caught more himself each time. Two months from precalculus to a pre-registered study with locked hypotheses and empirically-grounded parameters.

**Tone that works:** direct pushback with reasoning; flagging the crack rather than smoothing it; handing back the rows that must be his. He asks to be graded honestly and uses it well. He'll say "unpack that" when vocabulary outruns him — and does, reliably.

---

## 10. Living-doc gap — the reason this file exists

`calibration_lab` had **no home** in the doc system, so it fell through the gap and evaporated from awareness during midterms.

**The leak is real and measured.** Six settled decisions had to be re-derived from scratch — the Δ rung pair (three times), the definitions block, Δ(4B)'s role, the threshold rule, H2a's verdict rule, the endpoints choice. All were transfer failures between conversation and disk.

**Second failure mode, identified 2026-08-26:** the handoff recorded decisions as *landed* when they were only *decided*. Fixed by §0b's protocol and §5c's list.

**Companions:**
- ✅ **Lab log** — `lab_log.md`, created 2026-08-26. Placement decision outstanding (see §5c item 10).
- ⬜ **Decisions log** — what was chosen and why. §2 here is doing this job informally.

Repo holds the pre-registration and data. Vault holds interpretation. **Canonical prereg copy in the repo only** — a frozen artifact in a mutable store isn't frozen.

---

## 11. Git state

```
23e58ee  2026-08-27  S6: reorder + throughput re-measurement on driver 26.8.1
a37c996  2026-08-27  S6: parsing rules, throughput, logging, grader-rule declaration, verification requirements
8438601  2026-08-09  section 5 completed in prereg
f8a12b4  2026-08-01  Section 3 completed
3496554  2026-06-24  pre-registration template WIP
```

`lab_log.md` untracked. `core.autocrlf` set to false to stop LF→CRLF conversion, so the bytes on disk match the bytes in the commit — relevant because the freeze mechanic is "the hash is my witness."
