# `calibration_lab` — Handoff

*Operational snapshot. Drop this + the pre-registration into a fresh chat and say hello — that's enough to resume.*

**Last updated:** 2026-08-09 · **Status:** Slice 0 (pre-registration) in draft, not frozen

---

## 0. YOU ARE HERE

The pre-registration is **~80% drafted**. Complete and locked: **§3 (hypotheses)**, **§4 (roster + justification block)**, **§5 (datasets)**, §7 (metrics), §9 (exclusions).

Remaining: §1, §2, §6, §8 (partial), §10 (partial), §11.

**Next action: §6 (Procedure).** It is the heaviest remaining section and the only one that still blocks the pilot. It also has stale content — it still describes *three* elicitation methods including MC logprobs, which was dropped with MMLU. §1, §2, and §10 are transcription-grade and can be done at low energy; §11 needs a real redesign (see §5 status table).

**The empirical logprob check is DONE** (2026-08-08) — three findings, recorded in §6 Environment below. This unblocks P(True)'s design.

**No study data has been run.** No harness code exists except a synthetic ECE/reliability-diagram experiment (`ece_test.py`) written for learning purposes. The only Ollama calls made so far were the logprob and throughput probes, which are environment characterization, not study data.

---

## 1. What this project is

A standalone research study measuring **calibration** — whether a model's confidence matches its accuracy — on small, quantized, instruct-tuned models running on consumer hardware.

Conceptual replication of **Kadavath et al. 2022** (arXiv 2207.05221, *Language Models (Mostly) Know What They Know*), whose cleanest results were on large **base pretrained** models. This study asks whether that picture survives instruct-tuning, quantization, and small scale.

**Dual audience, deliberately:** an academic portfolio artifact (a professor sees someone learning to navigate research) *and* a community finding (a reader with 8GB of VRAM learns which model at which quantization is actually trustworthy). Neither is the afterthought. This framing drives most scope decisions below.

**Research identity it serves:** *"I study whether AI systems know what they know and how humans stay meaningfully in control when they don't."*

**Timeline:** first reliability diagrams by September 2026.

---

## 2. Frozen decisions — and why

*These are settled. The rationale is the part that doesn't survive a context reset, so it's recorded here.*

**Standalone repo, entirely separate from ARIA.** `C:\Users\legen\Projects\calibration_lab\`, own git repo, own venv. Reason: the August ARIA decision leans toward a *curated public research mirror* rather than full open-source. If `calibration_lab` lived inside ARIA, publishing it later would require history surgery on a repo containing a gitignored personal memory store. Starting separate means the public artifact is already the public artifact — zero extraction. Ollama is shared, but as a service on `localhost:11434`, not a code dependency. **The harness talks to Ollama directly, never through ARIA** — ARIA's vault injection could silently prepend material to a frozen prompt template.

**Own venv, and free to pin a different Python.** ARIA is on 3.14; the scientific stack (numpy, matplotlib, HuggingFace `datasets`) may not have 3.14 wheels. Check before committing; drop to 3.12/3.13 if needed. Separation is what makes that choice free.

**gemma3 family only.** All three hypotheses are within-family. Holding family and training recipe fixed is what makes the scale claim clean — cross-family comparison confounds size with everything else. Cross-family replication (qwen, deepseek, llama, phi) is deferred to a **follow-up study**, explicitly a post-September discussion.

**TriviaQA only; MMLU dropped.** Reason: free-form trivia is closer to how people actually use models. Nobody asks a local model multiple-choice questions. **Consequence — this is load-bearing:** MC logprobs requires lettered options, so dropping MMLU drops it. Two elicitation methods remain: **P(True)** and **verbalized confidence**.

**The MMLU and `nocontext` decisions are one principle applied twice: never hand the model material that lets it succeed without knowing the fact.** Context supplies the answer to read; multiple choice supplies the answer set to pick from. The MC-specific harm is **recognition vs. recall** — with distractors, partial knowledge can produce a correct answer by elimination, so a correct MC response is *ambiguous evidence* (knowledge or elimination, indistinguishable from the outcome). That matters more than the accuracy inflation: under MC, confidence can track distractor quality rather than the model's own knowledge, which is a different quantity than the one AUROC is supposed to read. Free-form has no guessing floor.

**Config: `unfiltered.nocontext`, validation split.** `rc` drops questions whose retrieved evidence documents don't contain the answer, which selects for facts with strong web documentation — plausibly correlated with training-data over-representation. That would sample preferentially from high-coverage facts where calibration likely looks best, biasing every cell in the same direction and invisibly. `unfiltered` does not *solve* contamination (gemma3 has almost certainly seen TriviaQA — that stays in §10); it avoids compounding it. Validation because test-set answers aren't publicly released. **Still to verify on HuggingFace before freeze:** the exact config string, and the alias field shape (`answer.aliases` / `answer.normalized_aliases`) — aliases are the raw material §6's grader rules run on.

**Identical item set across all nine cells.** Sample once with a recorded seed, freeze to `items.jsonl`, every cell reads that file in fixed order. Per-cell sampling would confound model differences with question-difficulty differences — a cell could draw an easier set and its AUROC would partly reflect the draw. **Seed and file do different jobs:** the seed is provenance (how the set was drawn, auditable); the file is the guarantee (a replicator gets the exact items regardless of `datasets` version or platform). `items.jsonl` is **committed to the repo**. Fixed order also makes per-item cross-cell comparison possible — item 47 means the same thing everywhere.

**C = 200, held regardless of the N it implies.** C = the minimum items required in the smaller class (correct *or* incorrect) in the worst cell. Chosen on statistical grounds: puts the AUROC noise floor around 0.02–0.03 (Hanley–McNeil approximation), keeping `2 × floor` around 0.04–0.06 — small enough that H2a's per-step gaps and H2b's spread can clear it without the threshold swallowing effects the size of H1's suggestive band. **The escape hatch was deliberately removed.** An earlier draft said "if runtime exceeds 8 hours I'll adjust" — but the only knob is C, and that clause triggers precisely when p_weak is lowest, i.e. when the small model's signal is thinnest and the items are most needed. Runtime is an inconvenience; C is whether the thresholds can detect the study's own effects. Any change to C post-freeze is a §12 deviation.

**N is two-sided: `N = 200 / min(p_weak, 1 − p_strong)`, +10% exclusion margin.** AUROC needs both classes populated. Sizing only on the weakest cell's *correct* count misses the mirror problem — the strongest cell's *incorrect* count is its thin class. A 12b at 90% accuracy on N=1000 has only 100 wrong answers, below C, and the binding constraint silently flips ends of the roster. Costs 50 extra pilot items to cover both directions.

**AUROC is the primary metric.** All three hypotheses rest on it. Chosen over ECE because the practitioner question is "can I *trust* this model's confidence" — i.e. does high confidence actually track correctness (discrimination) — rather than "does 70% mean 70%" (calibration). Convenient side effect: AUROC is bin-independent, so the binning debate can't touch the hypotheses.

**Accuracy measured per cell as a control.** Free (already grading every answer). It's the instrument that adjudicates the open mechanistic question — see §4 below.

**Published quants only; asymmetric ladders accepted.** Laz's reasoning, verbatim: *"What is available to me via an ollama shell command is also available to anyone reading my paper in the future."* Building custom quants with `llama-quantize` would make the study *less* reproducible for the target reader. This is a methodological principle, not a fallback.

**Δ for H2b is defined over q8_0 → q4_K_M**, not fp16 → q4_K_M. Reason: **`gemma3:12b` has no published fp16** (tops out at q8_0). Using fp16 as the top rung would mean the 12b's Δ spans 8→4.8 bits while the 1b/4b span 16→4.8 — the 12b would show a smaller Δ *because it was compressed less*, artifactually confirming H2b. The q8_0→q4_K_M rung exists at all three sizes. fp16 stays in the study as a third rung at 1b and 4b for H2a's within-model check. **This decision has been re-derived three separate times after evaporating between sessions — it is now written into the pre-registration's Definitions block, not just here.**

**Within-model vs. across-model rung rule.** The general principle underneath the above: **within-model comparisons (H2a) use every rung available at that size; across-model comparisons (H1, H2b) use only the rung pair or rung that exists at every size.** This is why H2a's ladders can be asymmetric and Δ's cannot.

**H1's primary quantization rung is q4_K_M.** Both q8_0 and q4_K_M exist at all three sizes, so "same quantization" left two admissible studies and a free post-hoc choice. q4_K_M chosen because it is what the target reader actually runs — consistent with every other decision on this project favoring the community half of the dual audience. **q8_0 is a declared robustness check**, reported alongside, explicitly not the primary test; agreement strengthens the finding, disagreement is reported as a limitation on generality. **Cost, must land in §10:** at q4_K_M every model is compressed, so the headline size effect is scale *and* compression entangled.

**H2b uses endpoints, not strict monotonicity.** `Δ(1B) > Δ(12B)`, not `Δ(1B) > Δ(4B) > Δ(12B)`. Reason: three points in the predicted order occur ~17% of the time under pure noise, and a difference-of-differences is three subtractions deep, so a noisy middle measurement could null the study's most original claim. Δ(4B) is still measured (H2a needs those cells anyway) and is **declared descriptive context, not part of the verdict** — written down so it can't be selectively mentioned only when flattering.

**H2b has a sign precondition.** Δ is signed, and ordering-by-value is not ordering-by-magnitude: all-negative Δs (compression *helped*) can satisfy `Δ(1B) > Δ(12B)` while contradicting the hypothesis's premise. So H2b is evaluated only if Δ(1B) > 0; otherwise it is reported **not evaluable**, not falsified. *Not evaluable* (test conditions didn't obtain) and *not supported* (test ran, prediction failed) are kept as distinct verdicts throughout §3.

**k = 2 for both H2a and H2b, committed blind 2026-08-01.** Magnitude thresholds are `k × the pilot-measured noise floor`. Rationale for the structure: multiplication, not subtraction — the noise floor is in AUROC units, k is a bare count of noise-widths, and multiplying makes the threshold scale automatically with the instrument's precision. Rationale for identical k: **the differing noise floors already account for the differing noise.** H2b's spread is three subtractions deep so its floor will be wider; adding a larger k on top would charge H2b twice for the same fact and could make a true hypothesis unreachable. Identical k = identical skepticism applied to two instruments of different precision.

**H1 keeps hardcoded thresholds; H2a/H2b use the formula.** Deliberate asymmetry, explained in a note inside §3. H1's gap is a quantity Laz has an informed opinion about (decision-relevance: "how much better before I'd tell someone to upgrade"). H2a's per-step gaps and H2b's spread are quantities never observed, with no basis for a guess — so they defer to measured noise. **Where you have judgment, use it; where you don't, defer to the instrument.**

**H2a's verdict rule: supported only if all three per-model checks hold**, with per-model verdicts reported individually regardless of the aggregate. The second half is load-bearing — a 2-of-3 outcome (quantization damage not uniform across scale) is a genuine finding and must not vanish under a bare "not supported," and the reporting obligation removes the freedom to foreground only the checks that worked.

**H2a's magnitude threshold is per-step, not total span.** Every adjacent gap must independently clear `2 × noise floor`, across all five comparisons (two at 1b, two at 4b, one at 12b). Per-step is the more faithful reading of "monotonic decline" — the claim is that each drop in precision costs something, not merely that the endpoints differ.

**QAT arm is exploratory, not confirmatory.** `gemma3:4b-it-qat` is **Q4_0**; the standard 4b is **Q4_K_M**. Those are different schemes (Q4_K_M is a k-quant, ~4.8 bpw with higher-precision outlier tensors; Q4_0 is legacy uniform 4-bit), so the comparison moves two variables — quantization-aware training *and* the quantization scheme. The arm carries **no falsifier and no direction**.

**The QAT/non-QAT scheme split is structural across the whole gemma3 family** — verified 2026-08-09 on both Ollama and HuggingFace. QAT is published at 1b, 4b, *and* 12b, and is **always Q4_0**; non-QAT is **never Q4_0** at any size. So no bit-matched control exists anywhere in the family, not just at 4b. This closes the obvious follow-up ("try a different size"). A full QAT ladder at 1b/4b/12b was therefore declined not only on scope but because it would be Q4_0 at every rung with no non-QAT Q4_0 to compare against — a separate study, not a repair. Ollama's quantizer also refuses Q4_0 (`supported types are F32, F16, Q4_K_S, Q4_K_M, Q8_0`), and hand-building via llama.cpp was ruled out against September. **If a non-QAT Q4_0 build is later discovered, that is a §12 deviation entry, not a quiet correction.**

**10 bins for ECE, dual scheme.** Equal-width is **primary** (comparable to published work), equal-mass is a robustness check against clumped confidence distributions. Declaring primacy in advance is required — otherwise reporting two ECEs is a fresh researcher degree of freedom. Bin count justified by Laz's own synthetic experiment: ECE stable at 5–10 bins (0.0535), inflating to 0.0921 at 500 and 0.1168 at 1000 on data with *fixed, known* miscalibration. The inflation is systematic, not random — `|gap|` can't go negative, so bin noise only ever adds.

**Thresholds (H1): ≥0.1 confirms · 0.05–0.1 suggestive · <0.05 refutes.** Three pre-committed buckets so no result lands in an unlabeled zone. Chosen by *decision relevance* — "how much better before I'd tell someone to upgrade" — not statistical convention. The middle band exists because the scholarly-interest threshold (~0.03–0.08) and the practitioner-recommendation threshold (~0.1) genuinely differ, and the dual-audience framing means neither should be silently discarded.

**Exclusion rules are mechanical, per-item decision procedures**, not interpretations. The "items where all models fail" rule was **deleted** — it's a data-dependent exclusion (defined by the outcome measured) and it would delete the hardest, most informative items. Refusals are excluded from calibration metrics *and reported as their own per-cell rate table*.

---

## 3. Hypotheses (§3 COMPLETE — locked 2026-08-02)

**Definitions block (sits above H1).** Δ(M) = AUROC(M, q8_0) − AUROC(M, q4_K_M). Uniform at all three sizes. fp16 rungs, where published (1b, 4b), serve only H2a's within-model check and never enter Δ.

**H1 (confirmatory).** As parameter count increases across gemma3 1B → 4B → 12B — same family, **all sizes at q4_K_M**, same prompts — AUROC increases monotonically.
*Rationale (rebuilt this session):* a larger model has capacity to store both the facts it was trained on and how reliably it holds each one; a smaller model's capacity goes to the facts themselves, leaving little for the reliability signal. So a larger model's confidence **varies** with how well it actually knows a given fact, while a smaller model's is comparatively flat — and that variation is what AUROC reads.
*Rationale history — do not let this regress:* drafts 1–2 were circular (restating the metric); draft 3 named the wrong cause (knowledge → **accuracy**, not discrimination); draft 4 added metacognition; draft 5 (current) cut the accuracy material entirely and replaced "knows more of what it doesn't know" — which was H1 restated in different words — with the capacity mechanism. **Two failure modes to watch: accuracy creep, and circularity.** Test: could you delete the rationale and lose any information beyond H1's statement? If not, it's circular again.
*Prediction:* AUROC(1B) < AUROC(4B) < AUROC(12B), total gap ≥ 0.1 confirming. *Band:* 0.05–0.1 suggestive. *Falsifier:* non-monotonic ordering, or total gap < 0.05.
*Robustness check:* same comparison at q8_0, reported alongside, explicitly not primary.

**H2a (confirmatory, main effect).** Within each model, AUROC decreases monotonically as precision drops. Three separate per-model checks, **not** one interleaved chain across sizes — an interleaved ordering would silently assume every size effect beats every quantization effect. Three rungs at 1b and 4b (fp16 > q8_0 > q4_K_M); two at 12b (q8_0 > q4_K_M), no fp16 published.
*Rationale:* the confidence signal lives in fine-grained logit differences; quantization noise corrupts those before it touches the argmax.
*Prediction:* the stated orderings, with the AUROC gap at **each step independently** ≥ 2 × pilot noise floor, across all five comparisons.
*Verdict:* supported only if all three per-model checks hold; per-model verdicts reported individually regardless.
*Falsifier:* any ordering other than the predicted one, or any step below the magnitude threshold.

**H2b (confirmatory, interaction — the most original claim).** Δ(1B) > Δ(12B).
*Rationale:* larger models have enough weights to absorb compression; smaller models have no slack — there isn't "enough of the model" to lose.
*Precondition:* evaluated only if Δ(1B) > 0; otherwise **not evaluable**.
*Prediction:* Δ(1B) > Δ(12B), with the spread Δ(1B) − Δ(12B) ≥ 2 × the pilot-measured noise floor **for the spread** (a different number from H2a's floor — the wobble of a difference of differences, not of a single gap). Δ(4B) measured and reported as descriptive context only.
*Falsifier:* Δ(1B) ≤ Δ(12B), or spread below threshold. Precondition failure → not evaluable, not falsified.

**E1 (exploratory, labeled).** Sweet-spot map: calibration and throughput against memory footprint, so a reader can pick a model for their constraint. No falsifier, no direction. Deliberately exploratory so post-hoc pattern-finding can't be laundered into a claim.

**Known tension to acknowledge in §10:** H1's "bigger models bluff less" is contestable. Some literature suggests scale and post-training make bluffing *more fluent*. Sources gathered — see §7.

---

## 4. The open mechanistic question

Does quantization degrade **the stored knowledge** or **the confidence signal that tracks it**?

Laz's honest answer is "both, somewhere in the gray" — which is likely correct and, importantly, *testable* rather than a hedge. The accuracy control reads out the mixture:

- AUROC drops **and** accuracy drops in lockstep → knowledge decay
- AUROC drops **but** accuracy barely moves → signal fragility
- both degrade at different rates → gray, and the ratio is measurable

This is why accuracy-per-cell went from nice-to-have to load-bearing.

---

## 5. Section status — pre-registration file

| § | Status | What's left |
|---|---|---|
| Header | ⚠️ stale | "Study:" line still uses the old Kadavath framing |
| 1. Research question | ❌ **stale** | Still the original Kadavath one-liner. **Must name AUROC**, not ECE — the hypotheses are all AUROC. Should scope to gemma3 + consumer hardware. |
| 2. Background | ❌ unwritten | 3–5 sentences. Kadavath on base models, Tian 2023 on verbalized confidence, why small/quantized/instruct-tuned might differ, and the community motivation (strongest material — already articulated, never written). The stray 3×3-cell note at the top belongs in §8 or §11, not here. |
| 3. Hypotheses | ✅ **COMPLETE** | Locked 2026-08-02. All four fields on all three hypotheses, plus definitions block and threshold-philosophy note. |
| 4. Models | ✅ **COMPLETE** | Locked 2026-08-08. Roster + IDs pinned, justification block written: family-fixed rationale, three-sizes-for-monotonicity, published-quants principle, q4_K_M as H1's primary rung, within-model/across-model rung rule, QAT/bit-matched-control block with verification note. |
| 5. Datasets | ✅ **COMPLETE** | Locked 2026-08-09. Four sub-blocks: dataset choice, config choice, split choice, selection rule, N. Three brackets outstanding (`p_weak`, `p_strong`, `N`) — pilot fills them. |
| 6. Procedure | ❌ mostly stale | **Heaviest remaining section, and the only one blocking the pilot.** Still says "three elicitation methods" incl. MC logprobs — now two. See below. |
| 7. Metrics | ✅ done | — |
| 8. Analysis plan | 🟡 partial | Has the differential-exclusion line. Needs the per-hypothesis walkthrough **and the noise-floor measurement procedure** (see New pending items). |
| 9. Exclusion rules | ✅ done | — |
| 10. Confounds | 🟡 partial | Stale bullets reference qwen3 and MMLU — both dropped. Consolidate the accumulated list (below), and add the q4_K_M entanglement consequence. |
| 11. Null result | ❌ **stale** | Still the original underpowered-trap text. Needs full redesign — three hypotheses can null *independently*, and H2b can now also come back *not evaluable*, which is a third outcome the section must handle. |
| 12. Deviations | ✅ ready | Empty by design until freeze. |
| 13. Freeze | ⏳ blocked | Two threshold numbers stay blank until the pilot reports. See freeze blockers. |

**§6 contains, specifically:**
- Two prompt templates, verbatim (frozen artifacts — prompt wording measurably moves calibration)
- Sampling params pinned identically across all cells: `temperature`, `top_k`, `top_p`, `seed`, `num_ctx`, `num_predict`. **Inherit nothing.** Gemma3 Modelfiles default to `temperature 1, top_k 64, top_p 0.95` — identical across all three sizes, but must still be set explicitly per call.
- **`num_ctx` ≤ 32768** — the 1b models cap at 32K while 4b/12b are 128K. Must be uniform across cells.
- **KV cache decision.** Currently `OLLAMA_KV_CACHE_TYPE=q8_0`, inherited from ARIA config, never chosen for this study. A quantized attention cache perturbs the exact probabilities being measured. Either set `f16` or declare q8_0 — but decide. Interacts with VRAM: `gemma3:12b-it-q8_0` is 13GB on a 16GB card, leaving ~3GB for cache, and f16 roughly doubles cache size. **Setting this requires a Windows environment variable + Ollama restart from the tray** — `set` in a cmd window will not reach the already-running server. Verify it applied.
- ~~**Empirical logprob check**~~ ✅ **DONE 2026-08-08** — findings in §6 Environment. Three consequences land in §6: the warm-up requirement, the parser's `bytes` edge case, and the P(True) surface-variant decision.
- **⚠ P(True) surface-variant decision — OPEN, and a real degree of freedom.** The returned distribution contains multiple surface forms of the same answer: on the probe, `True` (0.969), `TRUE` (0.0058), `T` (0.0022), `Yes` (0.0017), `true` (0.0012). Read **only the exact `"True"` token**, or **sum the mass** across variants? Both defensible. The gap is small on a 1b at q8_0 and may not be on a 1b at q4_K_M with a fuzzier distribution. Must be chosen and frozen — "we tried it the other way" is exactly what §6 exists to prevent.
- **⚠ Resumability — HARNESS REQUIREMENT, do not lose this.** JSONL keeps the log *valid* under interruption but does not make a run *continuable*; restarting re-runs from item 1 and appends duplicates. Fix: log the `(item ID, model tag, elicitation method)` triple per row; on startup read the log, collect completed triples, skip them. ~15 lines. **Warm-up call fires again on resume** — a resumed run cold-loads, and cold ≠ warm (see Environment). With this, a mid-sweep interruption is not a deviation: same items, same seed, deterministic warm.
- **Model-swap loop order:** hold one model, run all items, then swap. Nine loads at ~2.3s each is trivial that way and brutal the other way.
- **Answer-generation structure — OPEN.** Generate the answer once and run both elicitations against it (cheaper, holds the answer fixed across methods), or let each method generate its own (methods fully independent)? Determines whether an item costs 2 or 3 calls per cell.
- **Grader-rule development against pilot outputs — OPEN, needs an explicit pre-freeze declaration.** Writing normalization rules while looking at real outputs is where unconscious tuning-toward-generosity lives. Probably permissible (separate sample, discarded, same status as the noise floor and N) — but it needs the same explicit treatment those got, including a stated rule about what may and may not change after seeing pilot data.
- **Grader normalization rules.** Free-form TriviaQA means exact-match fails ("It was white, covered in rhinestones" vs. key "white"). TriviaQA ships answer aliases; still needs case/article/punctuation/substring rules. **This is the single biggest engineering task** — grading produces the correct/incorrect labels every metric is computed from.
- **Throughput logging:** `eval_count` / `eval_duration` → tokens/sec, plus model size on disk and whether it fit in VRAM. Free from Ollama's response. Catches VRAM spill, which produces *slow successes*, not timeouts — invisible to §9. Feeds E1: a cell with great AUROC at 2 tok/s is not a recommendation.

**§10 accumulated list:**
benchmark contamination (gemma3 has likely seen TriviaQA) · quantization confounded with scale · **H1's primary rung is q4_K_M, so the headline size effect is measured on compressed models throughout — scale and compression are entangled in that specific result** · vision asymmetry (1b is text-only; 4b/12b are multimodal) · context asymmetry (32K vs 128K) · differential exclusion across cells threatening H1/H2b · thin positive class on the weakest cells (no guessing floor in free-form) · **floor compression: if the 1b's AUROC at q8_0 is near 0.5 it has little room to fall, squeezing Δ(1B) and biasing against H2b — so an H2b null with a near-chance 1b cannot distinguish "small models are robust" from "the 1b had no signal to lose"** · **the k × noise-floor rule is a heuristic approximation; bootstrapped confidence intervals are the statistically clean version, and if they aren't implemented that must be stated** · QAT arm not bit-matched · single hardware/runtime · **extrapolation limit** — one machine (RX 9070 XT 16GB, 32GB DDR5-6000); can report footprint + measured throughput, cannot claim what happens on a reader's DDR4 8GB rig · H1's "bluffs less" contested in literature · **cold-load logprob variance observed once (n=1); mitigated by the warm-up requirement rather than characterized** · **the AUROC noise floor is estimated via Hanley–McNeil pre-pilot; the pilot's measured floor governs, and a materially wider one is disclosed** · **`unfiltered` avoids compounding contamination with rc's coverage filter but does not remove contamination itself**.

---

## 5b. New pending items (created by §3's completion)

**1. Noise-floor measurement procedure — §6 or §8, blocking.** Two magnitude thresholds now depend on a number, and nothing yet specifies how to produce it. Needs: what gets resampled (graded items, with replacement), how many resamples, and which statistic counts as "the floor" (standard deviation of the resampled AUROCs is the usual choice). **Two distinct floors are required** — H2a's is the wobble of a single AUROC gap; H2b's is the wobble of the spread, a difference of differences. Decide whether H2b's is measured directly or estimated from components.

**2. Bootstrapping decision.** Resample graded items *with replacement* (not scrambling — that's a permutation test, a different tool), recompute AUROC, repeat ~1000×, take percentiles. This is the principled answer to "is this spread real," and it would replace the k-heuristic with reported confidence intervals. **More resamples do not narrow the underlying uncertainty — only N does.** Cost: a Slice 4 task plus statistics Laz would need to defend. Genuine tradeoff against September; if declined, say so in §10.

**3. Freeze blockers for §13.** Both threshold numbers (H2a's per-step, H2b's spread) stay bracketed until the pilot reports. §13 cannot be signed with a bracket unfilled. The k values are already committed and dated; only the multiplicands are outstanding.

~~**4. §4's empty justification block**~~ ✅ done 2026-08-08.

**5. Open decisions now living in §6** (listed in full in the §6 contents block above): P(True) surface-variant rule · resumability · answer-generation structure (2 vs 3 calls per item) · grader-rule development against pilot data · KV cache · the two prompt templates.

**6. Pre-freeze verification, small but blocking:** confirm the exact TriviaQA config string on HuggingFace and inspect the alias field shape in the validation split. §6's grader normalization rules are speculative until this is done.

---

## 6. Environment

- **Hardware:** AMD RX 9070 XT, 16GB VRAM · 32GB DDR5-6000 · Windows · 4K
- **Ollama 0.32.6** — corrected 2026-08-08; the docs previously said 0.31.1. Version is a logged-per-run field, and a mid-study version change would be a §12 deviation. **Do not upgrade Ollama between the pilot and the sweep.**
- Flash attention **on**, KV cache **q8_0** — both inherited from ARIA, both still need an explicit §6 decision
- **PowerShell chains with `;`, not `&&`.** cmd has **no `#` comments** — a `# 5.0 GB` annotation on a command line breaks it. `curl` is aliased to `Invoke-WebRequest`; use `Invoke-RestMethod` or `curl.exe`.
- Roster on disk: 9 cells, all IDs pinned in §4 of the pre-reg.

### Logprob check — COMPLETE 2026-08-08

Run against `gemma3:1b-it-q8_0` via native `/api/chat`, `logprobs: true`, `top_logprobs: 10`.

**1. Logprobs are RAW, not temperature-scaled.** Same prompt/seed at `temperature 0` vs `temperature 2`: True −0.0310 vs −0.0324, False −4.3070 vs −4.3420. Scaling at temp 2 would have roughly halved the logit gap (False would sit near −2.2). It didn't move. **Temperature choice does not change the measured quantity.** Temperature *did* change generation (`eval_count` 3 → 2), which is exactly the separation wanted.

**2. `top_k` does NOT truncate the returned distribution.** `top_logprobs: 10` with `top_k: 5` returned 10 candidates. `top_k` governs the sampling pool; `top_logprobs` governs reporting. Independent knobs.

**3. Cold-load ≠ warm-load. THIS IS A PROCEDURE REQUIREMENT.** The first (cold, `load_duration` 2.52s) call differed from all subsequent warm calls at identical temp/seed: TRUE −5.1499 vs −4.9346, and the tail reordered. Three warm runs at *differing* temp and `top_k` were bit-identical to each other; a warm re-run of the cold run's exact config matched them to the last digit. **Every model gets a discarded warm-up call before measurement**, or the first item of every cell is measured on a different instrument than the rest. **Log `load_duration` per call** to verify no cell silently cold-started mid-run. Honest caveat for §10: n=1 on the cold side — it is known that cold differed once, not whether cold noise is deterministic-but-different or arbitrary. The warm-up requirement makes the question moot, which is why it's the fix rather than an investigation.

**4. Parser edge case.** In the second generated token's candidate list, one entry has an **empty token string and no `bytes` field at all**. Any parser doing `entry["bytes"]` unconditionally will crash. Present in both multi-token runs.

### Throughput — measured 2026-08-08

Warm, `num_predict: 64`, real trivia question. `gemma3:1b-it-q8_0` **~166 tok/s** (37 tok, 0.22s); `gemma3:12b-it-q8_0` **~35.9 tok/s** (51 tok, 1.42s). Four repeats each.

**The 12b is NOT spilling to system RAM** — an earlier reading of these numbers said it was. Generation is bandwidth-bound (every token streams the whole model), so the ceiling is ~640 GB/s ÷ 13GB ≈ 49 tok/s; 35.9 is ~73% of theoretical, a normal realized fraction. Spill would cost an order of magnitude (single digits), not 27%. The stability is the stronger tell — 35.9/35.9/35.8/35.9 across four runs, where spill is erratic. The ~4% variation that *does* appear is in the **1b**, because a 0.22s eval makes timer granularity a meaningful fraction of the measurement. Expect throughput logging to look jitterier on fast cells for reasons unrelated to the model.

Extrapolated full sweep (9 cells × 2 methods, ~60 generated tokens/item): **~7.5s per item across the full roster** → ~38 min at N=300, ~63 min at N=500, ~2.1 hrs at N=1000, ~6 hrs at N≈2750. **Runtime is not the binding constraint.** 4b and fp16 cells are extrapolated, not measured; the pilot logs real per-cell throughput.

**Prompt processing is compute-bound, not bandwidth-bound** (the whole prompt goes through in parallel), which is why `prompt_eval_duration` and `eval_duration` are reported separately.

---

## 7. Sources gathered

- **Kadavath et al. 2022** — arXiv 2207.05221. The paper being replicated. Read the reliability diagrams first.
- **Tian et al. 2023** — *Just Ask for Calibration*. Source of the verbalized-confidence-beats-logits finding.
- **Leng et al. 2025** — arXiv 2410.09724, *Taming Overconfidence in LLMs: Reward Calibration in RLHF* (ICLR 2025). The canonical counter-direction cite. **Scope carefully:** it's about *verbalized* confidence under RLHF, so it's a prediction about one elicitation method, not a head-on refutation of H1. Also the cite for why "more confident" ≠ "better calibrated" — relevant to H1's rationale, which must claim confidence *varies appropriately*, never that it is *higher*.
- **"Mind the Confidence Gap"** — OpenReview, Sept 2025. Most directly relevant to H1: large RLHF-tuned models show calibration strengths but can be *more* miscalibrated on easy queries; small models remain significantly miscalibrated. Implies the size effect may not be uniform across difficulty.
- **Dunning-Kruger paper** — arXiv 2603.09985 (2026, read critically). Argues models are well-calibrated in domains of strong pre-training coverage and overconfident outside them. **This is H1's rationale in different words** — chase the primary source.
- **arXiv 2311.13240** — *On the Calibration of LLMs and Alignment*. Finds *no* significant ECE degradation from RLHF applied atop instruction tuning. Cite alongside Leng to show the field disagrees with itself.

---

## 8. Slice roadmap

- **Slice 0** — pre-registration. ← *here. §3, §4, §5, §7, §9 done. §6 is the blocker.*
- **Slice 1** — dataset loader. TriviaQA validation → local JSONL.
- **Slice 2** — runner (one model, one method) + grader. Append-only JSONL, never overwrite raw data.
- **Slice 3** — second elicitation method; loop the roster.
- **Slice 4** — analysis: reliability diagrams, ECE, Brier, AUROC, accuracy, exclusion table, throughput. **Plus the noise-floor computation, and bootstrapping if adopted.**

**Pilot is mandatory, runs before freeze, and its data is discarded and never enters analysis.** Spec fixed 2026-08-09: **50 items each on `gemma3:1b-it-q4_K_M` and `gemma3:12b-it-q8_0`** — both extremes, because N's constraint is two-sided. Drawn with a **different seed** than the main sample, and **pilot items are excluded from the main draw pool** (otherwise a handful of items were seen during grader development).

It now determines **four** numbers: **p_weak** (1b accuracy), **p_strong** (12b accuracy), the **AUROC noise floor** (fills H2a's magnitude threshold), and the **spread noise floor** (fills H2b's — the wobble of a difference of differences, a different number). All logged as pre-freeze decisions, not peeks. The Hanley–McNeil estimate says the floor should land ~0.02–0.03 at C=200; **a materially wider measured floor is a §12 disclosure**, stated in advance so it reads as a caveat rather than a scramble.

**Freeze mechanics:** the pre-registration should be the **first commit** in the repo, so the history reads as prediction-then-test and can't be reordered. Then `git tag -a prereg-frozen -m "Slice 0 frozen"`. Record the hash in the header.

---

## 9. Working process

**Division of labor is deliberately different from ARIA.** Laz writes the research content — hypotheses, rationales, thresholds, predictions, falsifiers. Claude's job is adversarial review: hunt unfalsifiable phrasing, circular rationales, data-dependent exclusions, metrics that don't answer the stated question, and contradictions between sections. Claude **declined** to draft the hypotheses; that's load-bearing, because the pre-registration *is* the research identity and a borrowed rationale reads as borrowed. When Claude has supplied bullet-list scaffolding, Laz has correctly called it out as too close to drafting.

**Explanation protocol — added 2026-08-02, important.** Laz flagged mid-session that the guidance had outpaced him: not the research, the *vocabulary*. Terms like "magnitude threshold," "sign precondition," and "bootstrapping" were being used as labels for concepts he had, in several cases, already invented independently (H1's three-bucket threshold structure is a magnitude threshold, built from scratch before he knew the term). The fix that worked, and should continue: **name the term, state the problem it exists to solve, show the concrete failure it prevents — then apply it to the file.** Don't slow down; decompress. Laz will say "unpack that" when needed. Worked examples with actual numbers land far better than definitions.

**Confirmed misconceptions corrected this session** (worth not re-explaining from scratch, and worth checking haven't regressed): threshold = k × floor is *multiplicative* because k is a unitless count of noise-widths, not a quantity in AUROC units; bootstrapping is resampling *with replacement*, not scrambling (scrambling is a permutation test); more resamples measure uncertainty more precisely but do not reduce it — only N does; true negative vs. false negative; *not evaluable* vs. *not supported*.

**Manual mile.** ARIA is ~5% Laz / 95% Claude by his own honest assessment, which is why he won't claim it as engineering credit. `calibration_lab` is the corrective: small enough to write alone (a loader, a runner, a JSONL log, a matplotlib script), and the artifact he can put his name on without an asterisk. The bar: rebuild the harness solo from a blank editor by OSU arrival.

**Progress note.** Wrote a synthetic ECE + reliability-diagram script (with Gemini's help, typed not pasted), then passed a blank-editor retest of the ECE concept. Conceptual understanding is solid; Python fluency is early and improving. §3's completion is the strongest evidence so far — the endpoints decision, the k reasoning, the capacity mechanism, and the q4_K_M rung choice were all his calls.

**Progress note, 2026-08-09.** The review work has shifted register: less concept-explanation, more editing for precision, structure, and don't-lose-this. Two things worth recording as evidence rather than encouragement. (1) He proposed a run-until-threshold loop for sizing cells, then identified its flaw himself mid-explanation before the objection finished — the flaw being that stopping on a quantity computed from the outcome is his own §8 stopping rule inverted. (2) He caught the missing-bracket convention as soon as it was named, having already internalized why §3's thresholds were bracketed. Caveat against over-reading this: §4 and §5 are *specification* sections, where the work is precision rather than argument, and genuine concept explanation was still needed this session (JSONL, recognition-vs-recall, the C-is-chosen-not-measured knot, bandwidth-bound generation). The register shift is partly real skill and partly the kind of section.

**A recurring correction pattern worth naming.** Several times now his draft has contained the *evidence* for a claim without the claim itself — the QAT bullet listed the published-quant correlation but never named the two confounded variables; the rc bullet had the filter's effect but not its mechanism. Fix that generalizes: after writing a justification, check whether a reader who doesn't already know the answer could reconstruct it from what's on the page.

**Tone that works:** direct pushback with reasoning; flagging the crack rather than smoothing it; handing back the rows that must be his. He asks to be graded honestly and uses it well.

---

## 10. Living-doc gap — the reason this file exists

`calibration_lab` had **no home** in the doc system. ARIA has four living documents; this project had none, so it fell through the gap and evaporated from awareness during midterms.

**The leak is real and measured.** Across sessions, six settled decisions had to be re-derived from scratch — the Δ rung pair (three times), the definitions block, Δ(4B)'s role, the threshold rule, H2a's verdict rule, and the endpoints choice. None was a comprehension failure; all were transfer failures between conversation and disk.

**Two fixes, both adopted 2026-08-02:**
1. ✅ **DONE — the pre-registration is committed and Laz has been committing after every editing session since.** *This line previously read as a pending instruction, which caused at least one fresh session to open by telling him to do something he'd already done. Status, not instruction.* Freezing is a *tag*, not the first commit, so committing early cost nothing and the history still reads prediction-then-test. Each session now opens with a diff instead of a memory.
2. **Keep a running "decided but not yet written" list at the bottom of the section being worked on**, deleted from as items land.

Two companions still to stand up:
- **Lab log** — append-only, daily, prose. Vault.
- **Decisions log** — what was chosen and why. Vault.

Repo holds the pre-registration and data. Vault holds interpretation. The pre-reg is the one deliberate exception to that split: **canonical copy in the repo only** — a frozen artifact in a mutable store isn't frozen, and two copies means two versions and an argument about which was frozen. The vault gets a pointer note, not a copy.
