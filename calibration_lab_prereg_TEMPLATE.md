# Pre-Registration — `calibration_lab` (Slice 0)

**Study:** Does frontier-scale calibration behavior survive instruct-tuning, quantization, and small scale?
**Author:** Laz
**Drafted:** [7-15-2026]
**FROZEN:** [date] · commit `[hash]`
**Status:** DRAFT — not frozen

> *Fill every section. Where you see* ⚠ *, that's a researcher-degree-of-freedom: a knob you could unconsciously turn after seeing results to make the story better. Nailing it down now is the entire point of this document.*
>
> *A pre-registration is not a promise to be right. It's a dated record of what you predicted before you knew. Being wrong is a finding — an unsurprising study is a study that taught you nothing.*

---

## 1. Research question

*One sentence. Interrogative. Specific enough that a result could answer it.*

Within the gemma3 family, how do parameter count and weight quantization affect a model's ability to distinguish its own correct answers from its incorrect ones (AUROC), at sizes and precisions that run on consumer hardware?

## 2. Background

*Three to five sentences, not an essay. What Kadavath et al. (arXiv 2207.05221) found, on what kind of models. What Tian et al. 2023 added. Why the answer might differ for small, quantized, instruct-tuned local models — and why anyone should care (privacy-preserving agents, edge deployment, ARIA itself).*

- making a note here, because I am unsure of how to divide up the info: making a 3x3 cell with the findings of how size and quantization affect auroc score (1b, 4b, and 12b) on gemma3 family. Also worth recording: is it the confidence signal getting noisy, or the knowledge amount getting smaller? 

[ ]

## 3. Hypotheses

- Definitions: Δ = the within-model AUROC gap across the q8_0 → q4_K_M rung pair: Δ(M) = AUROC(M, q8_0) − AUROC(M, q4_K_M). Used uniformly at all three sizes. fp16 rungs, where published (1b, 4b), are used only for H2a's within-model monotonicity check and never enter Δ.

- H1: As parameter count increases across gemma3 1B → 4B → 12B (same family, all sizes at q4_K_M, same prompts), the model's ability to distinguish its own correct from incorrect answers improves: AUROC increases monotonically. 

Rationale: A larger model has the capacity to store both the facts it was trained on and how reliably it holds each one. A smaller model does not, its capacity goes to the facts themselves, leaving little for the reliability signal. Therefore a larger model's confidence varies with how well it actually knows a given fact, while a smaller model's confidence is comparatively flat. That variation is what AUROC reads.  

Robustness check: The same comparison at q8_0 is reported alongside. It is not the primary test of H1; agreement between rungs strengthens the finding, disagreement is reported as a limitation on generality.

Prediction: AUROC(1B) < AUROC(4B) < AUROC(12B), with the total gap >= 0.1 confirming. 

Reporting band: Monotonic gaps in 0.05–0.1 reported as suggestive, below the confirmation threshold. 

Falsifier: Non-monotonic ordering, or total gap < 0.05. 

- H2a (main effect): Within each model, AUROC decreases monotonically as precision drops: AUROC(fp16) > AUROC(q8_0) > AUROC(q4_K_M). Three separate monotonic checks, one per model, not one interleaved chain: Three-rung on 1b and 4b model sizes (fp16, q8_0, q4_k_M), fp16 does not exist at 12b, so 12b is a two-rung check at q8_0 and q4_K_M.

Verdict: supported only if all 3 per-model checks confirm AUROC score decreases monotonically as precision drops. A break at any size means H2a is not supported. Per-model verdicts will still be recorded and reported regardless of H2a itself being supported or not. 
    
H2a rationale: The confidence signal AUROC reads lives in fine-grained differences between logits. Quantization adds noise to those logits, and that noise corrupts the small differences carrying the discrimination signal before it touches the answer. So self discrimination degrades as precision drops. 

Prediction: At 1b and 4b: AUROC(fp16) > AUROC(q8_0) > AUROC(q4_K_M). At 12b: AUROC(q8_0) > AUROC(q4_K_M). The AUROC gap at each step must independently be ≥ 2 × the pilot-measured noise floor, across all five comparisons: 1b (fp16→q8_0, q8_0→q4_K_M), 4b (fp16→q8_0, q8_0→q4_K_M), 12b (q8_0→q4_K_M).

Falsifier: any ordering other than the predicted one falsifies, or the change (Δ) falls below the magnitude threshold.

- H2b (interaction): The size of that drop (q8_0 → q4_K_M) is larger for smaller models. Formally: Δ(1B) > Δ(12B). 

Precondition: H2b is evaluated only if Δ(1B) > 0. If Δ(1B) ≤ 0, the 1b model did not degrade under compression, H2b's premise does not obtain, and H2b is reported as not evaluable rather than confirmed or falsified.

H2b rationale: Larger models have enough weights that quantization's compression has little effect on the model's self-assessment capability, where a smaller model does not have enough weights to support that same compression without more noticeable adverse effects to self-assessment capability. There simply is not "enough" of the model at smaller parameter sizes to handle quantization without capability deterioration.

Prediction: Δ(1B) > Δ(12B), where Δ is the AUROC gap from q8_0 → q4_K_M at both sizes. The spread Δ(1B) − Δ(12B) must be ≥ 2 × the pilot-measured noise floor for the spread. Δ(4B) is measured and reported as descriptive context but it does not enter the H2b verdict. k = 2 committed 08-01-2026.

Falsifier: Δ(1B) ≤ Δ(12B): the small model's drop is not greater than the large model's, or the spread Δ(1B) − Δ(12B) falls below the magnitude threshold. Cases where the precondition fails (Δ(1B) ≤ 0) are reported as not evaluable, not falsified.

- Note on thresholds. H1's numbers are hardcoded while H2a's and H2b's are a formula (2 × the pilot-measured noise floor). This is intentional. H1's gap is a quantity I have an informed opinion about: "≥0.1 confirming" comes from asking how big a difference would have to be before I'd actually tell someone about it. H2a's per-step gaps and H2b's spread are quantities I have never observed and have no basis for guessing, so the threshold defers to the instrument: the noise floor sets the scale, and k = 2 sets how far above that noise an effect must sit before I'll claim it.

## 4. Models

⚠ Frozen roster. No additions after freeze without a deviation entry.

| Ollama tag | ID | Params | Quant | Ctx | Vision | Role |
|---|---|---|---|---|---|---|
| `gemma3:1b-it-q4_K_M` | `8648f39daa8f` | 999.89M | Q4_K_M | 32768 | no | H1, H2a, H2b |
| `gemma3:1b-it-q8_0` | `0fdb9c7fefee` | 999.89M | Q8_0 | 32768 | no | H1, H2a, H2b |
| `gemma3:1b-it-fp16` | `16d00907691b` | 999.89M | F16 | 32768 | no | H2a (3rd rung) |
| `gemma3:4b` (= q4_K_M) | `a2af6cc3eb7f` | 4.3B | Q4_K_M | 131072 | yes | H1, H2a, H2b |
| `gemma3:4b-it-q8_0` | `2376388dec16` | 4.3B | Q8_0 | 131072 | yes | H1, H2a, H2b |
| `gemma3:4b-it-fp16` | `c4da438ae756` | 4.3B | F16 | 131072 | yes | H2a (3rd rung) |
| `gemma3:12b` (= q4_K_M) | `f4031aab637d` | 12.2B | Q4_K_M | 131072 | yes | H1, H2a, H2b |
| `gemma3:12b-it-q8_0` | `997a7c2c0975` | 12.2B | Q8_0 | 131072 | yes | H1, H2a, H2b |
| `gemma3:4b-it-qat` | `d01ad0579247` | 4.3B | Q4_0 (QAT) | 131072 | yes | exploratory |

**Decisions to make and justify here:**


## 5. Datasets

- **MMLU subset:** which subjects, why those, how many items. [ ]
- **TriviaQA:** which split, how many items. [ ]
- ⚠ **Selection rule + RNG seed.** How items get sampled, with the seed written down. Otherwise "we reran with a different sample" becomes available to you later.
- **Sample size justification:** target ≥50 items per confidence bin — state the arithmetic that gets you there.

## 6. Procedure

- asymetrical quant ladders is fine: reproducible. My reasoning exactly, "What is available to me via an ollama shell command is also available to anyone reading my paper in the future. This research project doubles as an academic portfolio project and a community finding: a college professor could read my paper and find that Im learning to navigate researching, and a community member could read my paper and discover that x model at y quant is measured to be better calibrated for a z memory constraint."

For each of the three elicitation methods — **MC logprobs**, **P(True)**, **verbalized confidence** — specify:

- The exact prompt template, verbatim. ⚠ Prompt format measurably moves calibration; the paper demonstrates this itself. Templates are frozen here and reproduced in the appendix of the report.
- Generation settings: temperature, seed, `num_ctx`, `num_predict`.
- What gets read from the response, and how it's parsed.
- ⚠ **Verify empirically whether Ollama's returned logprobs are temperature-scaled or raw.** Don't assume. If they're scaled, your temperature choice silently changes your measured quantity. Confirm before freezing and record the finding here.

**Logged per run, always:** model tag, quantization, temperature, seed, prompt template ID, Ollama version, timestamp.

## 7. Metrics

ECE — 10 bins. Reported under two schemes: equal-width (primary, comparable to published work) and equal-mass (robustness check against clumped confidence distributions). Bin populations reported alongside both. Bin count fixed at 10 based on a synthetic-data experiment in which ECE was stable at 5–10 bins and inflated to 0.1168 at 1000 bins on data with known, fixed miscalibration.

Reliability diagrams — one per cell, under both binning schemes.

AUROC — primary metric for H1, H2a, H2b. Bin-independent.

Brier score — proper scoring rule, bin-independent.

Accuracy — per cell, bin-independent. Control distinguishing knowledge decay from confidence-signal degradation under quantization.

## 8. Analysis plan

*Written so a stranger could execute it without asking you anything.* For each hypothesis: which metric, which comparison, what pattern counts as support, what counts as against.

if exclusion rates differ substantially across cells, H1 and H2b results are interpreted in light of that, since selective removal of a small model's worst outputs inflates its apparent AUROC.

⚠ **Stopping rule.** The full sweep runs to completion. No looking at partial results and deciding you have enough.

⚠ **Pilot exemption.** A 50-item end-to-end pilot is mandatory (graders always have bugs) — state explicitly that **pilot data is discarded and never enters the analysis.** The pilot tests the harness, not the hypotheses.

## 9. Exclusion rules

⚠ Write these before you have any data, because afterward you will be able to construct a sincere-sounding reason to drop exactly the runs that hurt.

Unparseable → IF no confidence value can be extracted per the method's parsing rule, THEN exclude that item from that cell; log reason='unparseable'.

Refusal → IF the response matches refusal patterns and contains no answer, THEN exclude from calibration metrics; log reason='refusal'.

Timeout → IF no response within N seconds, retry once; if it fails again, exclude; log reason='timeout'.

Required output. An exclusion table reported in the results, one row per cell (model × quantization × elicitation method), with columns: total items attempted, excluded-unparseable, excluded-refusal, excluded-timeout, N retained, and exclusion rate. Reported in the main body, not an appendix. Per-cell exclusion rates are treated as a reported finding, not bookkeeping — differential exclusion across model sizes is a known threat to H1 and H2b and must be visible.

## 10. Known confounds and limitations

*State them now, not after a reviewer finds them. Honesty declared in advance reads as rigor; the same admission afterward reads as damage control.*

differential exclusion named as a limitation.

- **Benchmark contamination.** qwen3 has almost certainly seen MMLU and TriviaQA in training. What does this do to your claims, and what can you still say despite it?
- **Quantization as confound.** Your q4 weights are not the full-precision model. You cannot cleanly separate "small" from "quantized" — say so.
- **Instruct-tuning is not RLHF.** Your models' post-training recipes differ from each other and from Kadavath's. Family effects and tuning effects are entangled.
- **Single hardware/runtime.** One GPU, one Ollama version.
- [others]

## 11. What a null result looks like

*If every hypothesis fails and calibration looks basically like Kadavath's picture, what have you learned, and is it still worth writing up?*

If every hypothesis fails and calibration is not noticably different, I've learned that model size and quantization do not reasonably affect model calibration (AUROC). This means that, for consumer models, size and quantization should aid you in choosing what fits into your system resources. i.e, in regards of calibration, simply picking the biggest model that comfortably fits into your system resources (system RAM, VRAM) 

---

## 12. Deviations log

*Append-only. Post-freeze. A pre-registration is not a prison — plans change for good reasons. The rule is that changes are **logged and disclosed**, never silently absorbed. An undisclosed deviation is the thing that makes the whole document worthless.*

| Date | What changed | Why | Effect on hypotheses |
|---|---|---|---|
| | | | |

---

## 13. Freeze declaration

> I commit to the above before observing any results. Deviations after this point are logged in §12 and disclosed in the report.

**Signed:** [ ] **Date:** [ ] **Commit:** [ ]

*Freeze mechanics: commit this file, then tag it — `git tag -a prereg-frozen -m "Slice 0 frozen"`. The tag is the timestamp you can point at. Version control is your witness; that's what makes "I predicted this beforehand" a checkable claim rather than a story you tell.*
