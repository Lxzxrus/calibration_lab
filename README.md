# Calibration Lab

**Do small, quantized language models know what they know?**

A conceptual replication of *Language Models (Mostly) Know What They Know* ([Kadavath et al., 2022](https://arxiv.org/abs/2207.05221)). It asks whether small-scale, quantized models "know what they know" by measuring whether their confidence separates their right answers from their wrong ones (AUROC), using the Gemma 3 family at sizes and precisions that run on consumer hardware.

By Nathaniel (Nate) Campbell

> [!NOTE]
> **Status:** Pre-registration draft in progress, not frozen. Harness in progress: runner built, grader not yet started, pilot not yet run. **No study data in this repository.**

## Why this study

To test how calibration holds up under the two constraints in play in models run on consumer hardware: parameter size and quantization. Do small, quantized models "know what they know"? This study aims to answer that question for two groups of people: researchers and the local AI community. A community member could use the results to pick the best-calibrated model and quantization for their memory budget.

## Design at a glance

| | |
|---|---|
| **Models** | Gemma 3 at 1B, 4B and 12B; fp16, q8_0 and q4_K_M wherever published (nine cells, including one exploratory QAT model) |
| **Dataset** | TriviaQA, free-form, no context documents |
| **Confidence measures** | P(True) and verbalized confidence (0–100) |
| **Primary metric** | AUROC |
| **Also reported** | ECE, Brier score, accuracy |
| **Runtime** | Ollama 0.32.14, fully local |

**Hypotheses** (full statements, thresholds and falsifiers in prereg §3):

- **H1:** AUROC rises with model size (1B → 4B → 12B, at q4_K_M).
- **H2a:** Within each size, AUROC falls as precision drops.
- **H2b:** That drop (q8_0 → q4_K_M) is larger for the 1B than for the 12B.

## Repository map

| Group | File | What it is |
|---|---|---|
| Study design | `calibration_lab_prereg_TEMPLATE.md` | The pre-registration draft. **Start here.** (The filename predates the draft; other documents cite it by name, so it stays.) |
| Code | `draw_pilot.py` | Draws the 50 pilot items from TriviaQA with a fixed, recorded seed |
| Code | `run_pilot.py` | The runner: sends each item to each model and logs one raw row per call |
| Frozen inputs | `items_pilot.jsonl` | The 50 pilot questions and their answer aliases |
| Frozen inputs | `items_manifest.json` | Provenance for the draw: dataset, split, seed, timestamp, excluded rows |
| Measurement scripts | `probe1_per_call_overhead.ps1`, `probe2_prompt_eval.ps1`, `probe3_load_unload.ps1`, `probe4_endpoint_logprob_diff.py` | Runtime and endpoint measurements behind prereg §5–6 |
| Measurement outputs | `probe_out/` | Raw CSV and JSON output from the probes |
| Process record | `lab_log.md` | My dated, append-only log of every work session, including errors and reversals |
| Process record | `calibration_lab_HANDOFF.md` | A running context file for Claude, written primarily by Claude (see [How this was built](#how-this-was-built)) |
| Process record | `SESSION_PROTOCOL.md` | How each session opens and closes, so every change is verified, committed and tracked |
| Process record | `POST_STUDY_TODO.md` | Settings frozen for the study, to be restored after it ends |

## How this was built

I worked closely with Claude (Anthropic) on this project: Claude explained concepts and code, reviewed my work for errors, and proposed text and code. I typed every line of the prereg, the lab log and the Python code, and I accepted, rewrote, or rejected every proposal, with two exceptions: `measure_normalizer.py` and `measure_boundary.py` were written by Claude and copied into the repository by me, and the function in `triviaqa_normalize.py` is TriviaQA's, copied from their repository without changes to its text. Claude also wrote the three PowerShell probes (`probe1_per_call_overhead.ps1`, `probe2_prompt_eval.ps1`, `probe3_load_unload.ps1`) and `CITATION.cff`, and generated the `LICENSE` text. The handoff, `SESSION_PROTOCOL.md` and this README are written primarily by Claude.

"Laz" in the process documents is me.

## Reproducing

1. **Clone with git**, not a ZIP download. `run_pilot.py` reads the commit hash and checks for uncommitted changes, so it needs a git checkout.

   ```
   git clone https://github.com/Lxzxrus/calibration_lab.git
   ```

2. **Python 3.12.8**, then inside a venv:

   ```
   pip install -r requirements.txt
   ```

3. **Ollama 0.32.14**, serving on `127.0.0.1:11434`, with the server settings in prereg §6 (KV cache f16, Flash Attention enabled). Pull the roster (prereg §4 lists every tag and digest):

   ```
   ollama pull gemma3:1b-it-q4_k_m
   ollama pull gemma3:1b-it-q8_0
   ollama pull gemma3:1b-it-fp16
   ollama pull gemma3:4b
   ollama pull gemma3:4b-it-q8_0
   ollama pull gemma3:4b-it-fp16
   ollama pull gemma3:4b-it-qat
   ollama pull gemma3:12b
   ollama pull gemma3:12b-it-q8_0
   ```

   The pilot uses only `gemma3:1b-it-q4_k_m` and `gemma3:12b-it-q8_0`.

4. **Optional: verify the draw.** `python draw_pilot.py` regenerates `items_pilot.jsonl` exactly (`DRAW_SEED = 8`; pilot draw only, the main draw's seed is not yet chosen). It also rewrites `items_manifest.json` with a new timestamp, so restore both before the next step:

   ```
   git checkout -- items_pilot.jsonl items_manifest.json
   ```

5. **Run the pilot:** `python run_pilot.py`

> [!IMPORTANT]
> **Deliberate hard stops:** `run_pilot.py` refuses to run on a different Ollama version, a model digest mismatch, or uncommitted changes. These are integrity checks, not bugs (prereg §6).

Throughput figures are tied to the author's hardware (prereg §6); calibration results are not. See prereg §10 for guidance on re-measuring.

## Data

This study uses TriviaQA (Joshi, Choi, Weld & Zettlemoyer, *TriviaQA: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension*, ACL 2017). `items_pilot.jsonl` holds 50 records from its validation split (`unfiltered.nocontext`). TriviaQA's license is listed as unknown, and its authors note that the University of Washington does not own the copyright of the questions. These records are included only for reproducibility, are not covered by this repository's licenses, and can be regenerated exactly with `draw_pilot.py`. One source-defective row (`qf_1637`) is excluded; see prereg §5.

## License

Code is released under the [MIT License](LICENSE). Documents and measurements (`*.md`, `probe_out/`) are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). TriviaQA records are excluded; see [Data](#data).

`triviaqa_normalize.py` is a verbatim copy of one function from [mandarjoshi90/triviaqa](https://github.com/mandarjoshi90/triviaqa). It is under that repository's [Apache License 2.0](third_party/triviaqa/LICENSE), not this repository's MIT License.

## Contact

Questions and critique are welcome: please [open an issue](https://github.com/Lxzxrus/calibration_lab/issues).
