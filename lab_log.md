# calibration_lab — Lab Log

*Append-only. Newest first. Raw measurements and what happened, dated.*

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