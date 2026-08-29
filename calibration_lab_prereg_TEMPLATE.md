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

Prediction: AUROC(1B) < AUROC(4B) < AUROC(12B), with the total gap (AUROC(12B) − AUROC(1B)) >= 0.1 confirming. 

Reporting band: Monotonic gaps in 0.05–0.1 reported as suggestive, below the confirmation threshold. 

Falsifier: Non-monotonic ordering, or total gap < 0.05. 

- H2a (main effect): Within each model, AUROC decreases monotonically as precision drops: AUROC(fp16) > AUROC(q8_0) > AUROC(q4_K_M). Three separate monotonic checks, one per model, not one interleaved chain: Three-rung on 1b and 4b model sizes (fp16, q8_0, q4_k_M), fp16 does not exist at 12b, so 12b is a two-rung check at q8_0 and q4_K_M.

Verdict: supported only if all 3 per-model checks confirm AUROC score decreases monotonically as precision drops. A break at any size means H2a is not supported. Per-model verdicts will still be recorded and reported regardless of H2a itself being supported or not. 
    
H2a rationale: The confidence signal AUROC reads lives in fine-grained differences between logits. Quantization adds noise to those logits, and that noise corrupts the small differences carrying the discrimination signal before it touches the answer. So self discrimination degrades as precision drops. 

Prediction: At 1b and 4b: AUROC(fp16) > AUROC(q8_0) > AUROC(q4_K_M). At 12b: AUROC(q8_0) > AUROC(q4_K_M). The AUROC gap at each step must independently be ≥ 2 × the pilot-measured noise floor, across all five comparisons: 1b (fp16→q8_0, q8_0→q4_K_M), 4b (fp16→q8_0, q8_0→q4_K_M), 12b (q8_0→q4_K_M).

Falsifier: any ordering other than the predicted one falsifies, or any per-step gap falls below the magnitude threshold.

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
| `gemma3:1b-it-fp16` | `16d00907691b` | 999.89M | FP16 | 32768 | no | H2a (3rd rung) |
| `gemma3:4b` (= q4_K_M) | `a2af6cc3eb7f` | 4.3B | Q4_K_M | 131072 | yes | H1, H2a, H2b |
| `gemma3:4b-it-q8_0` | `2376388dec16` | 4.3B | Q8_0 | 131072 | yes | H1, H2a, H2b |
| `gemma3:4b-it-fp16` | `c4da438ae756` | 4.3B | FP16 | 131072 | yes | H2a (3rd rung) |
| `gemma3:12b` (= q4_K_M) | `f4031aab637d` | 12.2B | Q4_K_M | 131072 | yes | H1, H2a, H2b |
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

- Selection Rule: Using a recorded seed, I'll pull N questions from the dataset: uniform random sample without replacement, then I'll record the question text, answer aliases, and the source TriviaQA question ID to items.jsonl (sampled once, frozen, and read by every cell). I will apply those questions in fixed order, identical across all nine cells in section 4's roster.

- Reasoning: the seed offers provenance and the frozen file offers reproducibility to whoever wishes to carry out this experiment for themselves. As for the item set, per-cell sampling would confound model differences with question difficulty differences. If each cell drew its own sample, one cell might get an easier or harder draw, and its AUROC would partly reflect that rather than the model. Fixed items make the model the only thing varying.

- items.jsonl will be committed in the repo alongside the preregistration.

- Let C be the minimum number of items required in the smaller class, correct or incorrect, in the worst cell. I set the value to 200. C = 200 was chosen on statistical    grounds: it puts the noise floor around 0.02–0.03 (Hanley–McNeil approximation), which keeps 2x the floor around 0.04–0.06: small enough that H2a's per-step gaps and H2b's spread can clear it without the threshold swallowing effects the size of H1's suggestive band.

 At ~8.1s/item across all nine cells, N=900 takes 2.0 hours, N=1500 takes 3.4h, and N=2200 takes 5.0h.

 ~8.1s/item comes from the constant 5.82 seconds (27 calls per item * 215.5 ms) plus ~2.3 seconds (prompt_eval, eval and server_slack summed across the nine cells).

 The runtime probe (run 2026-08-28, complete) yielded that the load_duration was nearly identical between 12b-q8_0 and 1b-q4_K_M - 215.73 ms and 215.39 ms respectively. This accounts for ~72% of projected runtime and it is invariant across model size, quantization, template, prompt length, and logprobs, therefore it is a constant. The remaining ~28% is made up of prompt_eval, eval, and server_slack measurements. When accounted for, the 12b-q8_0 has a wall-clock time of 317.86 ms per call, and the 1b-q4_K_M 251.52 ms per call. Model load and unload across all nine cells is negligible against the sweep; per-model figures and total are in section 6's findings block.

 The pilot is specified below, not yet run. p_weak = the accuracy of the weakest cell, and p_strong is the accuracy of the strongest cell. The formula: N = 200 / min(p_weak, 1 - p_strong) plus 10% exclusion margin. The pilot spec: 50 items each on gemma3:1b-it-q4_K_M and gemma3:12b-it-q8_0, different seed, and pilot items excluded from the main draw pool and data discarded. 50 pilot items on both extremes to ensure no thin cells in the case of extreme high/low accuracy. So, the pilot has four outputs: p_weak, p_strong, the AUROC noise floor, and the spread noise floor.

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

Templates
- A: [Question] Answer with only the answer, no explanation, in 10 words or fewer. If unsure, give your single best guess.
- B: Question: [Question]

  Answer: [Answer]

  Is the Answer correct? Respond with only True or False.

* Note: Deviation from Kadavath et al. Each call is stateless, the model doesn't remember that the answer in question is its own. Self-referential framing would assert something false about the context.

- C: Question: [Question]

  Answer: [Answer]

  How confident are you that the answer is correct? Respond with any integer between 0 and 100 where 0 is not confident and 100 is certain that the answer is correct. Respond with only that integer and nothing else.

Template A word count → flag, reported, never excludes.
Template C unparseable confidence → §9 exclusion, logged with reason, appears in the exclusion table.

- P(True) - Why renormalize at all: raw True-mass conflates uncertainty about the answer with failure to follow the format. Format-following degrades at smaller model sizes, especially across this consumer-level order of magnitude - a 12b obeys "answer with True or False" more consistently than a 1b does. So raw mass would be systematically lower on small models for a reason unrelated to calibration, and H1 is a size hypothesis. Renormalizing removes that effect from the measurement; logging the retained mass keeps the format-following signal visible as a reported statistic instead of letting it slip away. Read the generated token position 0 only, fixed, no exceptions because scanning forward for a position that matches would rescue more items on the 1b than the 12b which is differential exclusion, and searching for the position where you find what you want is a degree of freedom. Normalize each candidate: strip whitespaces, make lowercase. The affirmative mass is the sum of the probabilities of all candidates whose normalized form is `true`, and likewise for `false` 'True' , 'TRUE' , 'true' , and [sp]True will all normalize to true after strip and lowercase. Strict format compliance; exact match against {true} / {false} only. The prompt names two tokens, so two tokens count; semantic enumeration has no natural stopping point. Anything else is non-compliant and remains outside the retained mass. P(True) = affirmative mass / (affirmative + negative mass); computed from raw logprobs at full precision because concentrated mass can round to a zero in the denominator - unacceptable. Zero retained mass will be recorded as unparseable and logged in section 9 as an exclusion (logged with the per-cell rate); 0.5 manufactures a number the model never expressed, and  0 treats the absence of 'true' as evidence for 'false'. No minimum mass floor; I considered but rejected it because any threshold I could come up with would just be an invented number with no basis. Retained mass is logged per row and per-cell mean is reported in the main body. Raw logprobs of both matched tokens will be logged per row too. And the parser will tolerate a candidate with an absent 'bytes' key and an empty token string.

- Verbalized confidence parsing rule: The entire response, after stripping whitespaces, stripping a trailing % (since 85% is the same as 85/100), and stripping any leading zeros, must parse as an integer. The integer is then divided by 100 to put it on a scale [0,1] so the two elicitation methods end up on the same scale, since AUROC needs them comparable. When a response returns done_reason: "length" flag, log, and report the per-cell rate but never exclude. Reasoning: A truncated response that is long enough to be cut off is almost certainly a response that failed the entire-response-is-an-integer rule so it's already excluded on those grounds. The only case that could survive to corrupt a value is a bare integer that was clipped midway through the digits, which needs a digits-only response longer than num_predict. The [0,100] scale makes that impossible. So the flag is simply a check that the hazard didn't show up. Anything else is unparseable → §9 exclusion, logged. Leading zeros are stripped. 085 parses as 85 - the transformation is unambiguous and adds no degree of freedom, and excluding it would put a formatting artifact in the same bucket as refusals and genuine non-answers, inflating a rate the exclusion table reports as a finding.

Parameters
- num_predict = Template A: 25 tokens; generous headroom well beyond a ten-words-or-fewer answer, including hedging. Template B: 5 tokens; one token for True/False plus a stop token, with margin. Template C: 10 tokens; worst case is three digit tokens for 100 plus a stop token, four total, plus headroom.
All three sit below 32. On gemma3:1b-it-q8_0, one TriviaQA item producing degenerate repeating output returned done: false with no metadata fields at num_predict ≥ 32, and returned normally with done_reason: "length" at ≤ 31 - confirmed on Ollama 0.32.6 and 0.32.14, same digest. Observed on a single item, so the boundary is stable rather than general. Staying below it means degenerate items return cleanly with usable metadata instead of malformed responses I cannot grade or log.
- num_ctx = 2048 tokens. num_ctx is an allocation, not a limit, so oversizing costs VRAM for nothing. 2048 is chosen as a round number well above the measured worst case.
- temperature = 0
- top_k = 64 (inert at temperature = 0)
- top_p = 0.95 (inert at temperature = 0)
- seed = 42

Throughput Measurements:

* Conditions - num_ctx = 2048, KV cache = f16, model warmed, previous model unloaded, nothing else consuming GPU resources. One item per cell: estimates runtime, not a benchmark. tok/s is calculated from eval_count / eval_duration, both server-side. Measured on Adrenalin 26.8.1 / driver 32.0.31041.1004.
* Table - 1b at Q4_K_M: 234.3 tok/s, 1b at Q8_0: 248.7 tok/s, 1b at fp16: 184.4 tok/s, 4b-it-qat at Q4_0: 134.4 tok/s, 4b at Q4_K_M: 132.5 tok/s, 4b at Q8_0: 110.6 tok/s, 4b at fp16: 67.8 tok/s, 12b at Q4_K_M: 66.0 tok/s, 12b at Q8_0: 43.9 tok/s.
* Readings - The two 1b cells are within run to run noise - two runs put the ordering in opposite directions, ~6% swing either way. A 22 token generation is too short of a window, so don't read the ordering between them. - QAT at 134.4 beside the standard 4b at 132.5 is near identical bit budgets, consistency check passes. 
- Re-measured after finding the original table predated the current driver. On the old driver, 12b-q8_0 spilled into system RAM and yielded 15.4 tok/s, ~31% of the 644 GB/s ceiling. On driver version 26.8.1 it is fully resident and yields 43.9 tok/s, ~89%. Old value in the lab log. 
- 12b q8_0 -> q4_K_M is 1.49x against a ~1.6x file size ratio: ordinary bandwidth scaling, no spill. Separately, that cell is the slowest in the roster and accounts for ~25% of sweep runtime.
* Contamination Sources - 1: cold-load/first-in-loop. the 1b read 57.9 tok/s when it led the loop, ~239 in isolation. 2: Keep-alive stacking: OLLAMA_KEEP_ALIVE defaults to 5m, so nine models called within five minutes all stay resident - stacking exhausts VRAM and the later cells spill; degradation scaling with model size is the tell. And 3: Other GPU consumers: a game running in the background cost 4b-q8_0 31.5 against 105.2. None of the three showed up in load_duration, so every contaminated run looked healthy with a report of ~0.23s. There's no automatic check, so the protection is procedural: warm models before run, unload models in between runs, and ensure GPU resources are free.

- Harness Requirements:

 Answer generated once per item per cell, reused as the [Answer] input in both Template B and C. Any difference between P(True) and verbalized confidence should be about the elicitation method and not about two different answers. Also reduces the amount of calls.

 Warm up call before the measurement, whose output is discarded. Done on every cold start and resume. Without this warm up, the first item of every cell is measured on a different instrument than the rest.

 Check 'done' before reading any other field. If 'done' is false, no valid response was obtained. Retry once, same call with no change. On a second failure, exclude and log in section 9's no_valid_response category. Ollama can return an incomplete response with no metadata at all, observed under degenerate generation. 

 Log the (item ID, model tag, elicitation method) triple on every row. On startup, read the existing log, collect completed triples, skip them. JSONL keeps the log valid under interruption but it won't make a run continuable. On resume, the log reader tolerates a malformed final line and discards it. An interrupted run can leave a partial JSON object at the end of the file. Because every completed row is a self contained line, only the incomplete line is lost. Re run that call.

 Log 'load_duration' per call. Lets me verify no cell silently cold started mid run. The warm value is a fixed per-call constant (section 5, runtime block); cold load is model-dependent (findings table above). A row whose load_duration sits near its own model's cold figure rather than near the constant means that cell reloaded mid-run.

 Parser tolerates an absent bytes field.

 Loop order: hold one model, run all items, unload model, then swap.  One load and one unload per cell is negligible against a multi-hour sweep; measured per-model figures and the total are in the findings block above. Swapping on every item would pay that cost once per item instead of once per cell.

 All Ollama calls use http://127.0.0.1:11434, never localhost. On Windows, localhost resolves to the IPv6 loopback first; Ollama binds IPv4, so every call pays a connection-failure fallback. Measured: 5 calls took 5,855 ms via localhost versus 1,338 ms via 127.0.0.1 , roughly 900 ms per call. At 27 calls per item this would add ~24 s per item to wall-clock runtime. Server-side eval_duration is unaffected, so the throughput table is unchanged by this.

 keep_alive generous within a cell, keep_alive: 0 on the final call to each model, replacing the ollama stop subprocess. ollama ps as verification.

 Verify the model digest at the point of load, once per model, against the digests frozen in section 4. On mismatch, hard stop - the weights have changed, and a cell computed across two different sets of weights is uninterpretable. Log the digest per row so a replicator can confirm which weights produced each measurement. Same rule for the runtime: read the Ollama version at process start and hard stop if it differs from the frozen value. Tags and installs both drift without intervention - this was observed once already, when Ollama auto-updated from 0.32.6 to 0.32.14 between sessions.

 The sweep runs with no other GPU consumers and with the previous model unloaded before the next loads; contamination doesn't affect the probabilities, but it does corrupt the throughput measurements E1 depends on, and none of the three contamination sources is detectable from load_duration.

- Negation Marker List: not, no, never, isn t, won t, wasn t, doesn t, aren t, couldn t, can t, wouldn t, shouldn t, cannot, don t, didn t, hasn t, haven t

 4 word marker window: 4 words because something like "couldn t ever be vancouver" is a realistic answer and is 4 words back from "vancouver" after normalization. 

 What happens when the negation marker flags? Set a boolean on the row. It never changes the score. It is for recording only. If the rate comes back high on any cell, I'll know that the substring matching is producing false positives and I can report that.

Grader Spec:
- Normalize: lowercase, punctuation -> space, collapse whitespace. Applied identically to the response and to TriviaQA's strings.
- Match: normalized_value plus all of normalized_aliases , checked as complete words/phrases (word boundary regex) against the normalized response.
- Any match = correct. No match = incorrect.
- No article stripping, no prefix stripping. Boundary matching absorbs leading scaffolding.
- Per-row logging: raw response, matched (bool), which alias matched, negation flag (bool), compliance flag (bool), truncation flag (bool).
- Compliance detector: raw word count ≤ 10, measured on the raw response rather than the normalized one — normalization only ever splits words apart, so raw is what the model actually emitted. Purely observational, never changes the score, per-cell rate reported.
- Truncation detector: set when done_reason is "length". Purely observational, never changes the score, per-cell rate reported.
- Negation detector: marker list frozen, 4-word window preceding the matched alias, purely observational — never changes the score.

Grader Rule Declaration:
- What may change? Code that fails to implement a written rule.

- What may not change? The rules themselves. Changing the rules after seeing data means I cannot prove that the change wasn't chosen for its effect on the results.

- How to decide where your case falls? Does the fix make the code do what section 6 already says, or does it change what section 6 says? If the former, permitted. If the latter, not permitted.

- What if a rule genuinely needs changing? If pre-freeze: amend and record the reasoning. If post-freeze: record in section 12 as a deviation.

- The pilot: the pilot is run pre-freeze - fixing grader bugs post-freeze means fixing them against real study data which is worse than fixing against pilot data. The pre-freeze pilot should eliminate any post-freeze grader changes. the pilot is genuinely safe to look at because it is run with a separate seed, excluded from the draw pool, discarded, and never analyzed. Any fix made against the pilot's outputs is recorded pre-freeze.

Logging:
- Per run (Constant for the process or the cell): model tag, model digest, quantization, Ollama version, KV cache type, temperature, seed, num_ctx, top_k, top_p, and timestamp.

- Per row (varies per call) - grading fields and flags are specified above in the Grader Spec.

 Identity: item ID, elicitation method, prompt template ID, num_predict
 Response: done, done_reason
 Timing: load_duration, eval_count, eval_duration, prompt_eval_count, prompt_eval_duration
 P(True) rows: renormalized P(True), retained mass, raw logprobs of both matched tokens, full top-10 candidate list (recompute insurance if the parsing rule needs re-deriving)
 Template C rows: parsed integer, mapped confidence

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

Unparseable → IF no confidence value can be extracted per the method's parsing rule, THEN exclude that item from that cell; log reason='unparseable'.

Refusal → IF the response matches refusal patterns and contains no answer, THEN exclude from calibration metrics; log reason='refusal'.

Timeout → IF no response within 90 seconds (well above worst measured call so a timeout indicates a genuine fault rather than a slow cell), retry once; if it fails again, exclude; log reason='timeout'.

No valid response → IF a response is returned with done: false (incomplete, no metadata), THEN retry once with the identical call; if it fails again, exclude that item from that cell and log reason='no_valid_response'

Required output. An exclusion table reported in the results, one row per cell (model × quantization × elicitation method), with columns: total items attempted, excluded-unparseable, excluded-refusal, excluded-timeout, N retained, and exclusion rate. Reported in the main body, not an appendix. Per-cell exclusion rates are treated as a reported finding, not bookkeeping - differential exclusion across model sizes is a known threat to H1 and H2b and must be visible. One column for mean retained mass (P(True) cells). One column for truncation flag rate.

- Template C's unparseable cases: 

 Multiple integers

 Ranges (80-90) — not averaged, because averaging constructs a value the model never expressed. Same objection that killed 0.5 for zero retained mass, and worth naming as the same principle rather than restating it fresh

 Spelled-out numbers (eighty-five)

 Out of range — the prompt bounds the answer to [0, 100], so anything outside it isn't a confidence value

 Any response that isn't wholly an integer (preamble, trailing prose, units)

## 10. Known confounds and limitations

*State them now, not after a reviewer finds them. Honesty declared in advance reads as rigor; the same admission afterward reads as damage control.*

differential exclusion named as a limitation.

- **Benchmark contamination.** qwen3 has almost certainly seen MMLU and TriviaQA in training. What does this do to your claims, and what can you still say despite it?
- **Quantization as confound.** Your q4 weights are not the full-precision model. You cannot cleanly separate "small" from "quantized" — say so.
- **Instruct-tuning is not RLHF.** Your models' post-training recipes differ from each other and from Kadavath's. Family effects and tuning effects are entangled.
- **Single hardware/runtime.** One GPU, one Ollama version.

- degenerate output means some of the 1b's incorrect answers may be non-answers rather than wrong facts, which affects how the accuracy control reads.

- low retained mass produces a renormalized value that was computed from tail probabilities. This is less stable than the same value computed from dominant ones. A minimum mass threshold was considered here, but I rejected the idea because I'd have to invent a number I could not defend; it would be an unjustifiable free parameter. Per-cell mean retained mass is reported so that the reader can weigh any cell's AUROC accordingly.

- saturation: the 12b pinning near 1.0 risks ties in P(True); ties push AUROC toward 0.5; that biases against H1 for reasons unrelated to the capacity mechanism.

- The QAT exploratory arm clause -"All nine models share the same gemma3 instruct recipe, but 4b-qat has a caveat: it confounds quantization-aware training with quantization scheme and has no bit-matched control, so it can neither confirm nor disconfirm H2a. See section 4."

- The asymmetry in the model roster in section 4 (the lack of 12b-fp16) causes asymmetry in section 3's H2a within-model check: 2 rungs for the 1b, 2 rungs for the 4b (excluding the exploratory 4b-qat), but just 1 rung for the 12b. This means the shape across the two steps on the 1b and across the two steps on the 4b are observable, but the 12b is only a directional test between two quants.

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


* Post-Study note: re-enable Ollama auto-update and AMD Adrenalin driver auto-update.
---

## 13. Freeze declaration

> I commit to the above before observing any results. Deviations after this point are logged in §12 and disclosed in the report.

**Signed:** [ ] **Date:** [ ] **Commit:** [ ]

*Freeze mechanics: commit this file, then tag it — `git tag -a prereg-frozen -m "Slice 0 frozen"`. The tag is the timestamp you can point at. Version control is your witness; that's what makes "I predicted this beforehand" a checkable claim rather than a story you tell.*
