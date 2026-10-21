# Pre-Registration — `calibration_lab` (Slice 0)

**Study:** Does frontier-scale calibration behavior survive quantization and small scale?
**Author:** Nathaniel Campbell
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

- Definitions: Δ = the within-model AUROC gap across the q8_0 → q4_K_M rung pair: Δ(M) = AUROC(M, q8_0) − AUROC(M, q4_K_M). Used uniformly at all three sizes. fp16 rungs, where published (1b, 4b), are used only for H2a's within-model monotonicity check and never enter Δ. Both-must-hold: AUROC is computed separately for each elicitation method - P(True) logprobs and verbalized confidence. A hypothesis's overall verdict requires both per-method results to clear its bar; one method passing alone does not produce that verdict. Where a threshold is derived from the pilot noise floor, each method is held to the floor measured for that method - P(True) and verbalized confidence do not share one floor.


- H1: As parameter count increases across gemma3 1B → 4B → 12B (same family, all sizes at q4_K_M, same prompts), the model's ability to distinguish its own correct from incorrect answers improves: AUROC increases monotonically. 

Rationale: A larger model has the capacity to store both the facts it was trained on and how reliably it holds each one. A smaller model does not, its capacity goes to the facts themselves, leaving little for the reliability signal. Therefore a larger model's confidence varies with how well it actually knows a given fact, while a smaller model's confidence is comparatively flat. That variation is what AUROC reads.  

Robustness check: The same comparison at q8_0 is reported alongside. It is not the primary test of H1; agreement between rungs strengthens the finding, disagreement is reported as a limitation on generality.

Prediction: AUROC(1B) < AUROC(4B) < AUROC(12B), with the total gap (AUROC(12B) − AUROC(1B)) >= 0.1 confirming. 

Reporting band: Monotonic gaps in 0.05–0.1 reported as suggestive, below the confirmation threshold. 

Falsifier: Non-monotonic ordering, or total gap < 0.05. 

- H2a (main effect): Within each model, AUROC decreases monotonically as precision drops: AUROC(fp16) > AUROC(q8_0) > AUROC(q4_K_M). Three separate monotonic checks, one per model, not one interleaved chain: Three-rung on 1b and 4b model sizes (fp16, q8_0, q4_k_M), fp16 does not exist at 12b, so 12b is a two-rung check at q8_0 and q4_K_M.

Verdict: supported only if all 3 per-model checks confirm AUROC score decreases monotonically as precision drops. A break at any size means H2a is falsified. Per-model verdicts will still be recorded and reported regardless of H2a itself being supported or falsified. 
    
H2a rationale: The confidence signal AUROC reads lives in fine-grained differences between logits. Quantization adds noise to those logits, and that noise corrupts the small differences carrying the discrimination signal before it touches the answer. So self discrimination degrades as precision drops. 

Prediction: At 1b and 4b: AUROC(fp16) > AUROC(q8_0) > AUROC(q4_K_M). At 12b: AUROC(q8_0) > AUROC(q4_K_M). The AUROC gap at each step must independently be ≥ 2 × the pilot-measured noise floor, across all five comparisons: 1b (fp16→q8_0, q8_0→q4_K_M), 4b (fp16→q8_0, q8_0→q4_K_M), 12b (q8_0→q4_K_M).

Falsifier: any ordering other than the predicted one falsifies, or any per-step gap falls below the magnitude threshold.

- H2b (interaction): The size of that drop (q8_0 → q4_K_M) is larger for smaller models. Formally: Δ(1B) > Δ(12B). 

Precondition: H2b is evaluated only if Δ(1B) > 0. If Δ(1B) ≤ 0, the 1b model did not degrade under compression, H2b's premise does not obtain, and H2b is reported as not evaluable rather than supported or falsified.

H2b rationale: Larger models have enough weights that quantization's compression has little effect on the model's self-assessment capability, where a smaller model does not have enough weights to support that same compression without more noticeable adverse effects to self-assessment capability. There simply is not "enough" of the model at smaller parameter sizes to handle quantization without capability deterioration.

Prediction: Δ(1B) > Δ(12B), where Δ is the AUROC gap from q8_0 → q4_K_M at both sizes. The spread Δ(1B) − Δ(12B) must be ≥ 2 × the pilot-measured noise floor for the spread. Δ(4B) is measured and reported as descriptive context but it does not enter the H2b verdict. k = 2 committed 08-01-2026.

Falsifier: Δ(1B) ≤ Δ(12B): the small model's drop is not greater than the large model's, or the spread Δ(1B) − Δ(12B) falls below the magnitude threshold. Cases where the precondition fails (Δ(1B) ≤ 0) are reported as not evaluable, not falsified.

**Split verdicts.** Under the both-must-hold clause, the overall verdict for each hypothesis is the weaker of its two per-method verdicts - ordered confirmed > suggestive > falsified for H1, supported > falsified for H2a, and supported > not evaluable > falsified for H2b - giving the overall verdict for every pair of per-method outcomes below.

| Hypothesis | One method | Other method | Overall verdict |
|---|---|---|---|
| H1 | confirmed | confirmed | confirmed |
| H1 | confirmed | suggestive | suggestive |
| H1 | confirmed | falsified | falsified |
| H1 | suggestive | suggestive | suggestive |
| H1 | suggestive | falsified | falsified |
| H1 | falsified | falsified | falsified |
| H2a | supported | supported | supported |
| H2a | supported | falsified | falsified |
| H2a | falsified | falsified | falsified |
| H2b | supported | supported | supported |
| H2b | supported | not evaluable | not evaluable |
| H2b | supported | falsified | falsified |
| H2b | not evaluable | not evaluable | not evaluable |
| H2b | not evaluable | falsified | falsified |
| H2b | falsified | falsified | falsified |

Per-method verdicts are reported regardless of the overall verdict, the same precedent already set for H2a's per-model verdicts above.

- Note on thresholds. H1's numbers are hardcoded while H2a's and H2b's are a formula (2 × the pilot-measured noise floor). This is intentional. H1's gap is a quantity I have an informed opinion about: "≥0.1 confirming" comes from asking how big a difference would have to be before I'd actually tell someone about it. H2a's per-step gaps and H2b's spread are quantities I have never observed and have no basis for guessing, so the threshold defers to the instrument: the noise floor sets the scale, and k = 2 sets how far above that noise an effect must sit before I'll claim it.

## 4. Models

⚠ Frozen roster. No additions after freeze without a deviation entry.

| Ollama tag | ID | Params | Quant | Ctx | Vision | Role |
|---|---|---|---|---|---|---|
| `gemma3:1b-it-q4_k_m` | `8648f39daa8f` | 999.89M | Q4_K_M | 32768 | no | H1, H2a, H2b |
| `gemma3:1b-it-q8_0` | `0fdb9c7fefee` | 999.89M | Q8_0 | 32768 | no | H1, H2a, H2b |
| `gemma3:1b-it-fp16` | `16d00907691b` | 999.89M | FP16 | 32768 | no | H2a (3rd rung) |
| `gemma3:4b` (= q4_k_m) | `a2af6cc3eb7f` | 4.3B | Q4_K_M | 131072 | yes | H1, H2a, H2b |
| `gemma3:4b-it-q8_0` | `2376388dec16` | 4.3B | Q8_0 | 131072 | yes | H1, H2a, H2b |
| `gemma3:4b-it-fp16` | `c4da438ae756` | 4.3B | FP16 | 131072 | yes | H2a (3rd rung) |
| `gemma3:12b` (= q4_k_m) | `f4031aab637d` | 12.2B | Q4_K_M | 131072 | yes | H1, H2a, H2b |
| `gemma3:12b-it-q8_0` | `997a7c2c0975` | 12.2B | Q8_0 | 131072 | yes | H1, H2a, H2b |
| `gemma3:4b-it-qat` | `d01ad0579247` | 4.3B | Q4_0 (QAT) | 131072 | yes | exploratory |

**Decisions to make and justify here:**
- Why only one family? It holds the training recipe fixed across all nine, with QAT carrying an additional training stage (which is why it's exploratory), so the claim is clean.

- Why 1b, 4b, and 12b models? They fit on most consumer-level hardware, with 12b being for those with enthusiast level hardware (like me.) Also: three sizes is the minimum for a monotonicity claim. Two points can't be non-monotonic, so H1 would be untestable. Three sizes spanning roughly one order of magnitude is the smallest ladder that can carry the hypothesis.

- Why published quants only? I wanted the models to be ones that any consumer could easily install, with no difference between the one they get via ollama pull or hugging face or other methods, and mine. What I run, is what you can run, provided you've got the hardware. Additionally, gemma3:12b @ fp16 would consume 24gb of VRAM - more than my 16gb and definitely more than most consumers. This is why I opted to leave 12b @ fp16 out, instead of building it myself.

- Why is H1's primary rung q4_K_M instead of q8_0? If a consumer is downloading these models via ollama, like I am, they'd use the command ollama pull gemma3:4b, which is q4_K_M; the bare tag resolves to it.

- Within-model comparisons (H2a) use every rung published at that size. Across-model comparisons (H1, H2b) use only the rung, or rung pair, that exists at every size.

- asymetrical quant ladders is fine: reproducible. My reasoning exactly, "What is available to me via an ollama shell command is also available to anyone reading my paper in the future. This research project doubles as an academic portfolio project and a community finding: a college professor could read my paper and find that Im learning to navigate researching, and a community member could read my paper and discover that x model at y quant is measured to be better calibrated for a z memory constraint."

- Why is the QAT arm exploratory only? the 4b QAT model is Q4_0, different than the Q4_K_M I'm using. Using the QAT version of the model raises the question if H2a's damage is inevitable at 4 bits or an artifact of careless quantization. I still decided to incorporate it because normal quant is post-training; QAT simulates that rounding during training. It settles into weight values that survive being rounded. Normal quant: the model didn't know it was coming, so wherever the weight's exact values mattered, the precision is just gone. QAT: the model anticipates and accommodates this. It's genuinely interesting.

- Why not test QAT across the board?: Because the QAT arm moves two variables at once: Quantization-Aware Training and the quantization scheme (Q4_0 vs. Q4_K_M are different algorithms with different effects on the probabilities I'm measuring.) To isolate it, you would need a bit-matched control to separate them: the same exact architecture, at the same scheme and bit-budget, differing only in QAT. The gemma3 family's 1b, 4b, and 12b all shipped with QAT versions, but every QAT model is quantized at q4_0, and their non-QAT counterparts are not quantized at q4_0. I could run a full QAT ladder at 1b, 4b, and 12b, but it would be QAT Q4_0 at every rung, with no non-QAT q4_0 to compare against. So, the QAT arm is exploratory: no falsifier, no direction.

*Note* I checked ollama and hugging face and confirmed the QAT vs quant situation. If Google has published QAT versions at other quants for gemma3 1b, 4b, and/or 12b, I am not aware of it, and if i discover their existence later, it will be logged as a deviation entry.

## 5. Datasets

- Dataset Choice: TriviaQA over MMLU. free-form trivia matches how people would actually query a local model.  Additionally, multiple choice questions from MMLU would introduce recognition vs. recall: a model queried with a multiple choice question could still determine the answer even if it has weak or partial knowledge simply by elimination of the distractors. This overstates what the model knows and lets confidence reflect narrowing rather than knowledge. Free-form has no guessing floor, so a correct answer means the model produced the fact.

- Config Choice: unfiltered.nocontext: I decided to use the TriviaQA's nocontext variant and not use MMLU because the normal TriviaQA variant includes evidence documents that contain the answers, and MMLU gives the answer set to the model, so the model just has to determine which of the candidates it is. So, by using TriviaQA's nocontext variant only, I ensure the dataset will yield a result that is a measure of knowledge, not reading comprehension. Two config strings for nocontext: unfiltered and rc (reading comprehension). I chose unfiltered because rc drops questions whose retrieved evidence documents don't contain the answer, which selects for facts with strong web documentation. Heavily-documented facts are plausibly over-represented in any web training. rc would sample preferentially from high coverage facts, where calibration plausibly looks best, biasing every cell in the same direction and invisibly. unfiltered keeps the original question without the filter, which doesn't solve the contamination, but it does stop the contamination from compounding. 

- Split Choice: Validation: the test-set answers aren't publicly released, so validation is the only split that allows me to grade.

- Consequence: dropping MMLU dropped MC logprobs, which leaves just two elicitation methods: P(True) and verbalized confidence.

- Pool Rule: qf_1637 is dropped from the pool by id before any draw, pilot or main, as a source defect: its question (the cartoon roadrunner) and its answer entity (static libraries) do not correspond, its value is the fragment '(a', and its normalized_value is blank. No model ever sees it, so it is not a section 9 exclusion and is not counted in the exclusion table.

- Selection Rule: Using a recorded draw_seed, I'll pull N questions from the dataset: uniform random sample without replacement, then I'll record the question text, answer aliases, and the source TriviaQA question ID to items.jsonl (sampled once, frozen, and read by every cell). I will apply those questions in fixed order, identical across all nine cells in section 4's roster.

- Reasoning: the draw_seed offers provenance and the frozen file offers reproducibility to whoever wishes to carry out this experiment for themselves. As for the item set, per-cell sampling would confound model differences with question difficulty differences. If each cell drew its own sample, one cell might get an easier or harder draw, and its AUROC would partly reflect that rather than the model. Fixed items make the model the only thing varying.

- items.jsonl will be committed in the repo alongside the preregistration.

- A verification re-run of draw_pilot.py at the same seed is not a second draw: it reproduces the same items in items_pilot.jsonl but rewrites items_manifest.json with a fresh timestamp, which dirties the tree and would stop the runner at its next start under section 6's clean-tree check. The re-run's output is restored from git and never committed, so the committed items_pilot.jsonl and items_manifest.json stay the draw of record; the README's Reproducing section has the steps.

- Let C be the minimum number of items required in the smaller class, correct or incorrect, in the worst cell. I set the value to 200. C = 200 was chosen on statistical    grounds: it puts the noise floor around 0.02–0.03 (Hanley–McNeil approximation), which keeps 2x the floor around 0.04–0.06: small enough that H2a's per-step gaps and H2b's spread can clear it without the threshold swallowing effects the size of H1's suggestive band.

 At ~8.1s/item across all nine cells, N=900 takes 2.0 hours, N=1500 takes 3.4h, and N=2200 takes 5.0h.

 ~8.1s/item comes from the constant 5.82 seconds (27 calls per item * 215.5 ms) plus ~2.3 seconds (prompt_eval, eval and server_slack summed across the nine cells).

 The runtime probe (run 2026-08-28, complete) yielded that the load_duration was nearly identical between 12b-q8_0 and 1b-q4_K_M - 215.73 ms and 215.39 ms respectively. This accounts for ~72% of projected runtime and it is invariant across model size, quantization, template, prompt length, and logprobs, therefore it is a constant. The remaining ~28% is made up of prompt_eval, eval, and server_slack measurements. When accounted for, the 12b-q8_0 has a wall-clock time of 317.86 ms per call, and the 1b-q4_K_M 251.52 ms per call. Model load and unload across all nine cells is negligible against the sweep; per-model figures and total are in section 6's findings block.

 The pilot is specified below, not yet run. p_weak = the accuracy of the weakest cell, and p_strong is the accuracy of the strongest cell. The formula: N = 200 / min(p_weak, 1 - p_strong) plus 10% exclusion margin. The pilot spec: 50 items each on gemma3:1b-it-q4_k_m and gemma3:12b-it-q8_0, different draw_seed, and pilot items excluded from the main draw pool and data discarded. 50 pilot items on both extremes to ensure no thin cells in the case of extreme high/low accuracy. So, the pilot has six outputs: p_weak, p_strong, the AUROC noise floor for each elicitation method, and the spread noise floor for each elicitation method.


 - draw_seed is fixed before draw_main.py is first executed, recorded in items_manifest.json, and the draw is not repeated - the first draw at that seed is the draw.

- p_weak = [ ] , p_strong = [ ] , N = [ ]

- Note: C = 200 is held regardless of the N it implies.

## 6. Procedure

- Environment: 

 Hardware spec: AMD Ryzen 7 9850X3D (8C/16T, 4.70 GHz) · 32 GB (2×16 GB) G.Skill F5-6000J3636F16G DDR5-6000, EXPO enabled, verified at 3003.4 MHz, CL36 · XFX Swift Radeon RX 9070 XT, 16 GB GDDR6, reference clocks (2400 MHz game clock), 644 GB/s memory bandwidth, PCIe 5.0 x16 · Windows 10 22H2 · AMD Adrenalin 26.8.1, driver 32.0.31041.1004. Reported so the throughput measurements are interpretable and so §10's extrapolation limit is concrete.

 Display configuration: 4 × 1440p (2 at 60 Hz, 1 at 75 Hz, 1 at 180 Hz), all driven by the 9070 XT. Reported because framebuffer allocation reduces VRAM available to the model, and the largest cell fits with under 1 GB of margin.

 Ollama version is 0.32.14 *Note: the version changed between drafting and freeze, observed rather than intended. Originally ollama version 0.32.6 - I have since disabled auto update for Ollama.

 KV cache is set to f16. The reason is methodological: quantizing the cache adds a second noise source on top of the weight quantization H2a is about, and the probabilities are the dependent variable. Measured afterward, f16 was also faster than q8_0 - 12b 20 vs 19, 4b 91 vs 78, 1b 200 vs 162 tok/s * measured on the previous driver, comparison between cache types rather than absolute throughput, not re-checked on 26.8.1. That inverts the usual result, because KV quantization pays off at 32K–128K context where the cache is large; at num_ctx = 2048 the cache is small enough that per-token dequantization overhead outweighs any bandwidth savings. So the choice is overdetermined — cleaner and faster — rather than a tradeoff.

 Flash Attention: enabled. Verified from the Ollama server log at model load rather than assumed from the environment variable, since Ollama falls back silently if the model or hardware doesn't support it. Mathematically equivalent to standard attention but not bit-identical.

- Findings: 

 position 0 carries the answer at both extremes (True 0.948 on 1b-q4_K_M, saturated on 12b), retained mass 0.995 and ~1.0, observed variants True/TRUE/true/[sp]True/Yes, Correct in the tail as a non-compliant semantic affirmative, empty-token candidates with absent bytes at position 0 on the 12b. Hand-written question, not a TriviaQA item, so no draw-pool contamination.

 Logprobs are raw, not temperature-scaled. Temp 0 vs temp 2, same prompt and seed: True −0.0310 vs −0.0324, False −4.3070 vs −4.3420. Scaling would have roughly halved the gap. Consequence: temperature choice doesn't change the measured quantity.

 top_k does not truncate the returned distribution. top_logprobs: 10 with top_k: 5 returned 10 candidates. Independent knobs — top_k governs sampling, top_logprobs governs reporting.

 Cold ≠ warm. First call after load differed from every warm call at identical temp and seed (TRUE −5.1499 vs −4.9346, tail reordered). Three warm calls at differing temp and top_k were bit-identical to each other. Consequence: the warm-up requirement. Caveat: n=1 on the cold side.

 Degenerate generation. On gemma3:1b-it-q8_0 (digest 0fdb9c7fefee), one TriviaQA item produced degenerate repeating output. With num_predict ≥ 32 the response returned done: false with no metadata fields; at ≤ 31 it returned normally with done_reason: "length". Confirmed on Ollama 0.32.6 and 0.32.14, same digest, identical boundary. Observed on a single item - two versions makes the boundary stable, not general.

 Pinning num_ctx from 131072 to 2048 cost throughput on the 12b (35.9 → ~20 tok/s), which is counterintuitive and unexplained. Uniform across cells, so it threatens nothing, but recorded as a measured fact. * measured on the previous driver, not re-checked on 26.8.1

 Model load/unload timing data table:

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

 The table above shows cold load ranges 2.15-11.93 s and scales with model size, unload scales with resident VRAM, and nine loads plus nine unloads total ~51 s. unload_polls was 0 on every row, so each unload figure is the latency of a single blocking /api/ps call rather than a polled interval - probably teardown given the clean scaling on VRAM but not proven, and doesn't affect the conclusion that model loading is negligible against the multi-hour sweep.

Templates:

Template A:
```
[Question] Answer with only the answer, no explanation, in 10 words or fewer. If unsure, give your single best guess.
```
Template B:
```
Question: [Question]

Answer: [Answer]

Is the Answer correct? Respond with only True or False.
```

* Note: Deviation from Kadavath et al. Each call is stateless, the model doesn't remember that the answer in question is its own. Self-referential framing would assert something false about the context.

Template C:
```
Question: [Question]

Answer: [Answer]

How confident are you that the answer is correct? Respond with any integer between 0 and 100 where 0 is not confident and 100 is certain that the answer is correct. Respond with only that integer and nothing else.
```

Template A word count → follows the Grader Spec's Compliance detector.
Template C unparseable confidence → §9 exclusion, logged with reason, appears in the exclusion table.

The Whitespace strip rule: raw Template A output is stripped of leading and trailing whitespaces only - no punctuation removal, case folding, or article stripping - before entering the [Answer] slot in Templates B and C.
Reasoning: Whitespace behavior correlates with model size. A whitespace sensitive prompt would put a size effect inside an instrument on a size hypothesis. .strip() is total and unambiguous - no threshold to pick and no stopping-point problem. A response that is empty after the strip is scored incorrect and not excluded, although it enters B and C as a non-answer by the same mechanism section 9 excludes refusals for; no code describes it and none is invented for a case not yet observed.

- P(True) - Why renormalize at all: raw True-mass conflates uncertainty about the answer with failure to follow the format. Format-following degrades at smaller model sizes, especially across this consumer-level order of magnitude - a 12b obeys "answer with True or False" more consistently than a 1b does. So raw mass would be systematically lower on small models for a reason unrelated to calibration, and H1 is a size hypothesis. Renormalizing removes that effect from the measurement; logging the retained mass keeps the format-following signal visible as a reported statistic instead of letting it slip away. Read the generated token position 0 only, fixed, no exceptions because scanning forward for a position that matches would rescue more items on the 1b than the 12b which is differential exclusion, and searching for the position where you find what you want is a degree of freedom. Normalize each candidate: strip whitespaces, make lowercase. The affirmative mass is the sum of the probabilities of all candidates whose normalized form is `true`, and likewise for `false` 'True' , 'TRUE' , 'true' , and [sp]True will all normalize to true after strip and lowercase. Strict format compliance; exact match against {true} / {false} only. The prompt names two tokens, so two tokens count; semantic enumeration has no natural stopping point. Anything else is non-compliant and remains outside the retained mass. P(True) = affirmative mass / (affirmative + negative mass); computed from raw logprobs at full precision because concentrated mass can round to a zero in the denominator - unacceptable. Zero retained mass will be recorded as unparseable and logged in section 9 as an exclusion (logged with the per-cell rate); 0.5 manufactures a number the model never expressed, and  0 treats the absence of 'true' as evidence for 'false'. No minimum mass floor; I considered but rejected it because any threshold I could come up with would just be an invented number with no basis. Retained mass is logged per row and per-cell mean is reported in the main body. Raw logprobs of both matched tokens will be logged per row too. And the parser will tolerate a candidate with an absent 'bytes' key and an empty token string.

- Verbalized confidence parsing rule: The entire response, after stripping whitespace and then a trailing % (since 85% is the same as 85/100), must parse as an integer with int(), which accepts leading zeros: 085 parses as 85, and 0 or 00 parse as 0. The integer is then divided by 100 to put it on [0,1], since ECE, Brier score, and the reliability diagrams compare confidence against accuracy, which is a proportion. When a response returns done_reason: "length", follow the Grader Spec's Truncation detector. Reasoning: A truncated response that is long enough to be cut off is almost certainly a response that failed the entire-response-is-an-integer rule so it's already excluded on those grounds. The only case that could survive to corrupt a value is a bare integer that was clipped midway through the digits, which needs a digits-only response longer than num_predict. The [0,100] scale makes that impossible. So the flag is simply a check that the hazard didn't show up. Anything else is unparseable → §9 exclusion, logged. Accepting leading zeros is unambiguous and adds no degree of freedom, and excluding such a response would put a formatting artifact in the same bucket as refusals and genuine non-answers, inflating a rate the exclusion table reports as a finding.

Parameters
- num_predict = Template A: 25 tokens; generous headroom well beyond a ten-words-or-fewer answer, including hedging. Template B: 5 tokens; one token for True/False plus a stop token, with margin. Template C: 10 tokens; worst case is three digit tokens for 100 plus a stop token, four total, plus headroom.
All three sit below the degenerate-generation boundary measured in this section's Findings block above. Staying below it means degenerate items return cleanly with usable metadata instead of malformed responses I cannot grade or log.
- num_ctx = 2048 tokens. num_ctx is an allocation, not a limit, so oversizing costs VRAM for nothing. 2048 is chosen as a round number well above the measured worst case.
- temperature = 0
- top_k = 64 (inert at temperature = 0)
- top_p = 0.95 (inert at temperature = 0)
- seed = 42
- top_logprobs = 10, Template B only: the candidate distribution P(True) reads at position 0 requires it; unset on Templates A and C.

Throughput Measurements:

* Conditions - num_ctx = 2048, KV cache = f16, model warmed, previous model unloaded, nothing else consuming GPU resources. One item per cell: estimates runtime, not a benchmark. tok/s is calculated from eval_count / eval_duration, both server-side. Measured on Adrenalin 26.8.1 / driver 32.0.31041.1004.
* Table - 1b at Q4_K_M: 234.3 tok/s, 1b at Q8_0: 248.7 tok/s, 1b at fp16: 184.4 tok/s, 4b-it-qat at Q4_0: 134.4 tok/s, 4b at Q4_K_M: 132.5 tok/s, 4b at Q8_0: 110.6 tok/s, 4b at fp16: 67.8 tok/s, 12b at Q4_K_M: 66.0 tok/s, 12b at Q8_0: 43.9 tok/s.
* Readings - The two 1b cells are within run to run noise - two runs put the ordering in opposite directions, ~6% swing either way. A 22 token generation is too short of a window, so don't read the ordering between them. - QAT at 134.4 beside the standard 4b at 132.5 is near identical bit budgets, consistency check passes. 
- Re-measured after finding the original table predated the current driver. On the old driver, 12b-q8_0 spilled into system RAM and yielded 15.4 tok/s, ~31% of the 644 GB/s ceiling. On driver version 26.8.1 it is fully resident and yields 43.9 tok/s, ~89%. Old value in the lab log. 
- 12b q8_0 -> q4_K_M is 1.49x against a ~1.6x file size ratio: ordinary bandwidth scaling, no spill. Separately, that cell is the slowest in the roster and accounts for ~25% of sweep runtime.
* Contamination Sources - 1: first-in-loop (not model cold-load - the warm-up call already discards that; this is a separate GPU/driver-state effect load_duration doesn't measure) the 1b read 57.9 tok/s when it led the loop, ~239 in isolation. 2: Keep-alive stacking: OLLAMA_KEEP_ALIVE defaults to 5m, so nine models called within five minutes all stay resident - stacking exhausts VRAM and the later cells spill; degradation scaling with model size is the tell. And 3: Other GPU consumers: a game running in the background cost 4b-q8_0 31.5 against 105.2. None of the three showed up in load_duration, so every contaminated run looked healthy with a report of ~0.23s. There's no automatic check, so the protection is procedural: warm models before run, unload models in between runs, and ensure GPU resources are free.

- Harness Requirements:

 Answer generated once per item per cell, reused as the [Answer] input in both Template B and C. Any difference between P(True) and verbalized confidence should be about the elicitation method and not about two different answers. Also reduces the amount of calls.

 Warm up call before the measurement, whose output is discarded. Done on every cold start and resume. Without this warm up, the first item of every cell is measured on a different instrument than the rest.

Runner and grader split: for every section 9 rule that both retries and excludes, retry is a runner action, made before any row is written; exclusion is a grader decision, made afterward from stored output.

 Check 'done' before reading any other field. If false, apply section 9's no_valid_response rule. The check exists because of the degenerate-generation finding above (section 6 Findings).

 Log the (item ID, model tag, elicitation method) triple on every row. On startup, read the existing log, collect the triples from every well-formed row - success or failure - and skip them. JSONL keeps the log valid under interruption but it won't make a run continuable. On resume, the log reader tolerates a malformed final line and discards it. An interrupted run can leave a partial JSON object at the end of the file. Because every completed row is a self contained line, only the incomplete line is lost. Re run that call.

 A terminal Template A failure ends resume for that item's B and C calls too: if the A row is present and shows done: false or timed_out: true, it's terminal by construction (the runner/grader split rule above: retries happen before any row is written, so every A row that exists is already the final outcome) - the item's B and C triples are treated as already accounted for, not as interrupted-and-needing-a-run, since their [Answer] input doesn't exist and there's nothing valid to retry. Row presence at resume therefore isn't just "missing → run it": it's "missing, and not already accounted for by an upstream terminal A failure → run it."

 Keep-first dedup, no run_id: the (item ID, model tag, elicitation method) triple is the whole key. The first well-formed row for a given triple is authoritative; resume's skip-on-presence check is what enforces this. A run_id was considered and declined - its only proposed job was tying a row back to a separate per-run record, and every field that record would have held (harness commit hash, Ollama version, and the rest of Per run) is already written on the row itself. Same reasoning that retired the draw index: a field isn't needed when it would only be a second, weaker version of a guarantee the row already carries. On startup, if the output file already has rows, compare their commit hash and Ollama version to the current process's values. On a mismatch, hard stop - otherwise keep-first would let rows from an already-fixed runner bug stand simply because they were written first.

 Log 'load_duration' per call. Lets me verify no cell silently cold started mid run. The warm value is a fixed per-call constant (section 5, runtime block); cold load is model-dependent (findings table above). A row whose load_duration sits near its own model's cold figure rather than near the constant means that cell reloaded mid-run.

 Parser tolerates an absent bytes field.

 Loop order: hold one model, run all items, unload model, then swap.  One load and one unload per cell is negligible against a multi-hour sweep; measured per-model figures and the total are in the findings block above. Swapping on every item would pay that cost once per item instead of once per cell.

 All Ollama calls use http://127.0.0.1:11434, never localhost. On Windows, localhost resolves to the IPv6 loopback first; Ollama binds IPv4, so every call pays a connection-failure fallback. Measured: 5 calls took 5,855 ms via localhost versus 1,338 ms via 127.0.0.1 , roughly 900 ms per call. At 27 calls per item this would add ~24 s per item to wall-clock runtime. Server-side eval_duration is unaffected, so the throughput table is unchanged by this.

 keep_alive generous within a cell, keep_alive: 0 on the final call to each model, replacing the ollama stop subprocess. ollama ps as verification.

Verify the model digest at the point of load, once per model, against the digests frozen in section 4. On mismatch, hard stop - the weights have changed, and a cell computed across two different sets of weights is uninterpretable. Log the digest per row so a replicator can confirm which weights produced each measurement. Same rule for the runtime: read the Ollama version at process start and hard stop if it differs from the frozen value. Tags and installs both drift without intervention - this was observed once already, when Ollama auto-updated from 0.32.6 to 0.32.14 between sessions. Same rule for the working tree: check the whole tree is clean via git status at process start and hard stop if it is not. git rev-parse HEAD reports what's committed, not what's running - uncommitted edits to the harness would execute under a commit hash that doesn't describe them, the same mutable-identity hazard as a model tag one level up. Checked once, at start; editing lab_log.md or anything else afterward doesn't retrigger it. Output files: the runner's and grader's per-row JSONL logs are gitignored, unlike items.jsonl (see section 5), which is a frozen input committed to the repo. A live, growing output file would otherwise dirty the tree on every row written, permanently blocking this check on every resume.

The three contamination sources and procedural protections above apply equally here: contamination doesn't affect the probabilities, but it does corrupt the throughput measurements E1 depends on.

- Negation Marker List: not, no, never, isn t, won t, wasn t, doesn t, aren t, couldn t, can t, wouldn t, shouldn t, cannot, don t, didn t, hasn t, haven t

 4 word marker window: 4 words because something like "couldn t ever be vancouver" is a realistic answer and is 4 words back from "vancouver" after normalization. 

 What happens when the negation marker flags? Set a boolean on the row. It never changes the score. It is for recording only. If the rate comes back high on any cell, I'll know that the alias matching is producing false positives and I can report that.

Grader Spec:
- Normalize: TriviaQA's own normalize_answer function (evaluation/triviaqa_evaluation.py in mandarjoshi90/triviaqa, commit 51b5359), copied verbatim into the grader and cited there: underscores to spaces, lowercase, punctuation to spaces, standalone a, an and the removed, whitespace collapsed. Punctuation means ASCII punctuation plus the curly single quotes and the acute accent; other characters, such as curly double quotes and en and em dashes, are left as they are. Applied to the response. TriviaQA's normalized_value and normalized_aliases are already its output, apart from empty strings the dataset drops (checked on every validation item, lab log 10-19), so both sides go through one function.
- Match: normalized_value plus all of normalized_aliases , checked as complete words/phrases (whitespace-delimited: the key must be preceded and followed by a space or an end of the text; regex \b is not used, because it cannot match a key that begins or ends with a non-word character) against the normalized response. Every distinct hit is logged, normalized_value first, then normalized_aliases in stored order. An empty alias never matches.
- Any match = correct. No match = incorrect.
- No prefix stripping. Boundary matching absorbs leading scaffolding. Article removal is not a grader choice but part of the dataset's own normalization: a normalizer without it could never match a correct answer that contains an internal article (measured, lab log 10-19).
- Per-row logging: matched (bool), matched aliases (list), negation flag (bool), raw word count (int), compliance flag (bool), truncation flag (bool), multi-candidate flag (bool), exclusion reason (one of section 9's codes, or blank if not excluded).
- Compliance detector: true when raw word count ≤ 10, counted as len(raw.split()) on the raw response rather than the normalized one — normalization splits words apart and drops articles, so raw is what the model actually emitted. Purely observational, never changes the score, per-cell rate reported.
- Truncation detector: set when done_reason is "length". Purely observational, never changes the score, per-cell rate reported.
- Negation detector: marker list frozen, set when a marker lies wholly within the 4-word window preceding the earliest match in the normalized response (false when nothing matched), purely observational — never changes the score, per-cell rate reported. Markers match as whole words and phrases, by the same boundary rule as the Match bullet.
- Multi-candidate detector: set when "or" appears as a whitespace-delimited word in the normalized response. Purely observational, never changes the score, per-cell rate reported. Crude by design: it misses candidate lists written with commas or ranges, and it fires on single answers that themselves contain "or".

Grader Rule Declaration:
- What may change? Code that fails to implement a written rule.

- What may not change? The rules themselves. Changing the rules after seeing data means I cannot prove that the change wasn't chosen for its effect on the results.

- How to decide where your case falls? Does the fix make the code do what section 6 already says, or does it change what section 6 says? If the former, permitted. If the latter, not permitted.

- What if a rule genuinely needs changing? If pre-freeze: amend and record the reasoning. If post-freeze: record in section 12 as a deviation.

- The pilot: the pilot is run pre-freeze - fixing grader bugs post-freeze means fixing them against real study data which is worse than fixing against pilot data. The pre-freeze pilot should eliminate any post-freeze grader changes. the pilot is genuinely safe to look at because it is run with a separate seed, excluded from the draw pool, discarded, and never enters the study's results. Any fix made against the pilot's outputs is recorded pre-freeze.

- Logging: two files, not one - the runner writes raw text and raw numbers live, one row per call; the grader writes derived values afterward, reading the runner's file rather than the live model. Every field below belongs to exactly one of the two.

Runner file (written live, one row per call):

Per run (constant for the process, written on every row): Ollama version, KV cache type, temperature, seed, num_ctx, top_k, top_p, timestamp, and harness commit hash.

Identity: item ID, model tag, model digest, quantization, elicitation method (one of 'answer', 'p_true', 'verbalized' - Template A, B, C respectively), num_predict, top_logprobs, attempt_count

Response: done, done_reason, timed_out (true if no response was returned within 90 seconds; done, done_reason, Timing, and Raw response are then all absent).
Timing: load_duration, eval_count, eval_duration, prompt_eval_count, prompt_eval_duration
Raw response: the unparsed text returned for that call.
P(True) calls only: full top-10 candidate list (recompute insurance if the parsing rule needs re-deriving).

Grader file (written afterward, reading the runner's file, never the live model):
Per row - the (item ID, model tag, elicitation method) triple, plus the fields specified in the Grader Spec above. The grader writes one row per item and method, including the B and C cells of a terminal A failure, which have no runner row; if A succeeded and its B or C row is missing, the grader stops.
P(True) rows: renormalized P(True), retained mass, logprobs of all matched tokens.
Template C rows: parsed integer, mapped confidence.

## 7. Metrics

ECE — 10 bins. Reported under two schemes: equal-width (primary, comparable to published work) and equal-mass (robustness check against clumped confidence distributions). Bin populations reported alongside both. Bin count fixed at 10 based on a synthetic-data experiment in which ECE was stable at 5–10 bins and inflated to 0.1168 at 1000 bins on data with known, fixed miscalibration.

Reliability diagrams — one per cell, under both binning schemes.

AUROC — primary metric for H1, H2a, H2b. Bin-independent.

Tie rate — the fraction of correct-incorrect item pairs in a cell with identical confidence, the pairs AUROC scores as 0.5. Reported per cell for P(True) and for verbalized confidence, descriptively. A tie rate never changes a verdict.

Brier score — proper scoring rule, bin-independent.

Accuracy — per cell, bin-independent. Control distinguishing knowledge decay from confidence-signal degradation under quantization. Computed over the cell's retained items (section 9), so accuracy and AUROC share one item set.

## 8. Analysis plan

*Written so a stranger could execute it without asking you anything.* For each hypothesis: which metric, which comparison, what pattern counts as support, what counts as against.

if exclusion rates differ substantially across cells, H1 and H2b results are interpreted in light of that, since selective removal of a small model's worst outputs inflates its apparent AUROC.

If either method's pilot-measured noise floor is high enough that 2x that floor meets or exceeds H1's threshold, H1's verdict is still read against that fixed value (section 3), but reported alongside a note that the same gap would not clear H2a/H2b's own evidentiary bar for that method: the two verdicts would not share a comparable standard of evidence in that case.

⚠ **Stopping rule.** The full sweep runs to completion. No looking at partial results and deciding you have enough.

⚠ **Pilot exemption.** A 50-item end-to-end pilot is mandatory (graders always have bugs) — state explicitly that **pilot data is discarded and never enters the study's results.** The pilot tests the harness, not the hypotheses.

## 9. Exclusion rules

Unparseable → IF no confidence value can be extracted per the method's parsing rule, THEN exclude that item from that cell; log reason='unparseable'.

Refusal → IF the normalized Template A response contains any entry of the refusal pattern list as a complete phrase (whitespace-delimited match, same normalizer as the Grader Spec) AND the Grader Spec finds no alias match, THEN exclude that item from both of that model's calibration cells (p_true and verbalized); log reason='refusal' on the A row and in both cells. An alias match is scored correct regardless of refusal patterns — the match rule governs, so refusal exclusion only ever removes items from the incorrect class.

Refusal pattern list, closed at freeze, in normalized form: i don t know · i do not know · cannot know · can t know · no way to know · impossible to know · cannot determine · can t determine · not enough information · insufficient information · cannot answer · can t answer · unable to answer.

Provenance: the list is canonical English, declared blind, with one admission criterion — a phrase is included only if it commits to not answering; a phrase that qualifies an answer (not sure, possibly, probably) is excluded, since Template A invites a hedged guess and a hedge is compliant, and a phrase that only discloses what the speaker is (as an AI) is excluded for the same reason. Probe 5 (2026-10-16, ten hand-written non-pool questions on gemma3:1b-it-q4_k_m and gemma3:12b-it-q8_0, 20 calls, probe5_refusal_phrasing.py, outputs in probe_out/) produced zero refusals — every call returned a committed answer — so the list could not be derived from observation and the rule is expected to fire rarely. Two consequences, stated now: a wrong answer that also contains a list phrase ("I cannot know, but probably 1915") is excluded as a refusal rather than scored incorrect, because separating a hedged guess from a refusal would need a word cap this document refuses to invent, and the per-cell refusal count includes such cases; and a refusal the list misses is scored incorrect, which concentrates in whichever cells refuse most and enters the B and C cells by the mechanism below. The per-cell refusal exclusion rate in the exclusion table includes the first case; it cannot count the second, since a refusal the list misses is never excluded.

Why exclusion rather than an observational flag, when negation, compliance, truncation and multi-candidate answers are all counted and never excluded: those four never change what Templates B and C are asked about. A refusal does — the Template A output becomes the [Answer] in B and C, and the confidence calls are then about a non-answer labeled incorrect, a row whose confidence signal is not about knowledge.

Timeout → IF no response within 90 seconds (well above worst measured call so a timeout indicates a genuine fault rather than a slow cell), retry once; if it fails again, exclude; log reason='timeout'.

No valid response → IF a response is returned with done: false (incomplete, no metadata), THEN retry once with the identical call; if it fails again, exclude that item from that cell and log reason='no_valid_response'.

A terminal Template A failure — done: false or timed_out: true after the retry — likewise removes the item from both of that model's calibration cells, logged under the A row's own code (no_valid_response or timeout) in both. No separate code: the four codes already name the cause, and the cascade is the same one refusal uses.

Required output. An exclusion table reported in the results, one row per cell (model × quantization × elicitation method), with columns: total items attempted, excluded-unparseable, excluded-refusal, excluded-timeout, excluded-no_valid_response, N retained, and exclusion rate. Reported in the main body, not an appendix. Per-cell exclusion rates are treated as a reported finding, not bookkeeping - differential exclusion across model sizes is a known threat to H1 and H2b and must be visible. One column for mean retained mass (P(True) cells). One column for truncation flag rate. One column each for compliance, negation, and multi-candidate flag rates.

- Template C's unparseable cases: 

 Multiple integers

 Ranges (80-90) — not averaged, because averaging constructs a value the model never expressed. Same objection that killed 0.5 for zero retained mass.

 Spelled-out numbers (eighty-five)

 Out of range — the prompt bounds the answer to [0, 100], so anything outside it isn't a confidence value

 Any response that isn't wholly an integer (preamble, trailing prose, units)

## 10. Known confounds and limitations

*State them now, not after a reviewer finds them. Honesty declared in advance reads as rigor; the same admission afterward reads as damage control.*

Differential exclusion across cells is a limitation - section 8 covers the mechanism and interpretation; the bias runs toward the null, against H1.

Forced response. Template A instructs the model to guess rather than decline. The cost is that a guess can be correct without the fact being known and lands in the correct class. Free-form generation has no guessing floor — the answer space is unbounded, so a blind guess is almost never right — which should keep the pollution small, but its rate is not measured and nothing here claims it is equal across cells. The alternative, permitting "I don't know," would have fed refusals into section 9's exclusion rule at rates that may differ by size.

Refusal exclusion removes items from the incorrect class only, since an alias match is scored correct regardless (section 9). The rate may differ by size and is reported per cell in the exclusion table; probe 5 observed no refusals under Template A at either extreme (section 9).

- Benchmark contamination. Gemma3 has almost certainly seen TriviaQA in training. Contamination magnitude plausibly scales with model size: larger models memorize more of what they were trained on. A memorized item is answered correctly and confidently, which is exactly a correctly-discriminated item, so memorization plausibly inflates AUROC more in larger models than smaller ones. That threatens H1 specifically: an AUROC increase with size could arrive from memorization rather than from the capacity-for-reliability mechanism H1 is actually about. H2a and H2b compare quantizations within a fixed size, sharing the same memorization baseline, so this particular confound largely cancels there. The unfiltered config (section 5) avoids compounding the problem by not selecting for well-documented facts, though it does not remove the underlying contamination.

Quantization confounded with scale. H1's headline comparison (AUROC across 1B → 4B → 12B) is measured entirely at q4_K_M - there is no full-precision size comparison in this study. A pure scale effect and a scale-by-quantization interaction cannot be fully separated from H1 alone; H2a and H2b's within-size quantization checks are what bound how large that interaction plausibly is.

Instruct-tuning is a cross-study limitation, not a within-roster one. Every model in the roster shares the same gemma3 instruct recipe, so H1, H2a, and H2b all hold it constant. Relative to Kadavath, four things change at once: instruct-tuning, quantization, scale, and model lineage, so a difference between this study's findings and Kadavath's cannot be cleanly attributed to any one of them.

Extrapolation limit. Every throughput and memory-footprint figure in this document is bound to this exact hardware, driver, and context configuration and does not transfer to other setups - this limits E1 (the throughput-vs-memory-footprint sweet-spot map) directly, since E1 is built from those figures. The calibration results (H1, H2a, H2b) do transfer: AUROC is computed from the model's output probabilities, and a model that spills out of VRAM runs slower, not differently confident. Evidence this is a regime change and not incremental noise: a single AMD driver update alone moved the largest cell's throughput from 15.4 to 43.9 tok/s, crossing from VRAM-spilling to resident: no fixed scaling factor recovers this study's throughput table on different hardware, since different hardware or drivers can land on either side of that same threshold. Silicon-lottery variation between individual GPU units is real but secondary next to that. For replicators: re-measure your own throughput and memory constants rather than reusing this study's numbers; the measurement scripts are committed (probe*.ps1 and probe4_endpoint_logprob_diff.py at the repo root; raw CSVs and probe 4's two warm-run JSON files in probe_out/). Two caveats for that re-measurement: section 6 documents Flash Attention as not bit-identical to standard attention, so claiming the same output distribution on different hardware overclaims by one clause; and the only run-to-run spread actually measured in this study is the ~6% swing on the 1b cells (section 6, Throughput Measurements) - treat that as a lower bound on expected variance, not a general figure. VRAM context: peak usage of 15,474 MB against 16,304 MB available, a 2,256 MB desktop baseline from four 1440p displays, under 1 GB of margin on the largest cell.

- degenerate output means some of the 1b's incorrect answers may be non-answers rather than wrong facts, which affects how the accuracy control reads.

- low retained mass produces a renormalized value that was computed from tail probabilities. This is less stable than the same value computed from dominant ones. A minimum mass threshold was considered here, but I rejected the idea because I'd have to invent a number I could not defend; it would be an unjustifiable free parameter. Per-cell mean retained mass is reported so that the reader can weigh any cell's AUROC accordingly.

- saturation: the 12b pinning near 1.0 risks ties in P(True), and in verbalized confidence, where the integer scale makes ties the larger risk and, because section 3 takes the weaker of the two per-method verdicts, either method's ties can set the verdict; ties push AUROC toward 0.5; that biases against H1 for reasons unrelated to the capacity mechanism.

- 4b-qat confounds quantization-aware training with quantization scheme and has no bit-matched control, so it can neither confirm nor disconfirm H2a. See section 4.

- The asymmetry in the model roster in section 4 (the lack of 12b-fp16) causes asymmetry in section 3's H2a within-model check: 2 rungs for the 1b, 2 rungs for the 4b (excluding the exploratory 4b-qat), but just 1 rung for the 12b. This means the shape across the two steps on the 1b and across the two steps on the 4b are observable, but the 12b is only a directional test between two quants.

- Multi-candidate answers. Under "any match = correct," a response naming several candidates is scored correct if any one is an alias, and ten words can name several. Observed in probe 5 on both extremes ("Possibly a terrier or chihuahua."; "13mm - 15mm, likely 13mm."). A recognition-shaped hazard inside a free-form design. Never corrected; section 6's multi-candidate detector flags only responses that use "or" (the first example, not the second), per-cell rate reported.

- Characters the normalizer leaves alone. TriviaQA's normalizer turns ASCII punctuation into spaces but leaves en dashes, em dashes, curly double quotes and the ellipsis as they are, so a correct answer typed with a different dash or quote than the key is scored incorrect, in either direction: an answer typed with a hyphen misses a key that holds an en dash, and an answer typed with an en or em dash misses a key that holds a space where the gold value has a hyphen. A correct answer with one of those characters attached to it (for example in curly double quotes, or joined to the next word by an em dash) is also missed, because matching is whitespace-delimited. Counts are in lab log 10-20. How often models type those characters is not measured; the pilot counts them in the runner file. Never corrected.

## 11. What a null result looks like

- ECE was considered as a co-primary metric and declined against the timeline. The case where AUROC remains unchanged while calibration degrades will be handled here instead of a hypothesis.

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
