# calibration_lab — Lab Log

*Append-only. Newest first. Raw measurements and what happened, dated.*

## 2026-10-12 Both-must-hold decided; section 3 amended; 10-11 public release logged

Open checks (SESSION_PROTOCOL section C) passed: git log from 94430cf to HEAD returned only 032ba89 (the handoff rewrite), the tree was clean, and the prereg was unchanged since the last verified hash. Three handoff claims did not check out: the KV-cache item cited prereg line numbers that were off by a few lines; the handoff contradicted itself on sessions spent, "roughly nine" in one bullet and "roughly seven" in the next; and it filed the elicitation-method question under "decided but not yet written" when it was an open decision. Process note: the handoff's numbered item lists mean nothing on my side, so from here on things are referenced by content, not by item number.

Public release, 10-11, previously recorded only in the handoff (the decision to publish was logged on 10-08; the act was not). The remote was added (origin, github.com/Lxzxrus/calibration_lab), the full history pushed, and the repo made public. Commit count checked against git rather than the handoff: origin/master was updated by two pushes, the first at 94430cf (43 commits) and the second the handoff rewrite, 032ba89 (44). The handoff's "43 commits at push" is right for the first push, and origin now holds 44.

Decision: both-must-hold. The gap, logged 10-08 and decided today: the AUROC line in section 7 says "primary metric for H1, H2a, H2b" without naming a method, and section 3 never named one either, so as written a verdict could be read off whichever method supported it. Averaging the two is ruled out by the section 9 precedent that ranges are not averaged, because averaging constructs a value the model never expressed. The rule: AUROC is computed separately for P(True) and for verbalized confidence; each must clear the hypothesis's bar against its own noise floor; the overall verdict is the weaker of the two per-method verdicts; per-method verdicts are always reported. Consequences: Template B is in the pilot of record, which settles the open question from 10-08; B's grader-side parser (the runner has collected B since 09-20) moves onto the critical path before the pilot; and the pilot produces six outputs, not four.

Accepted in advance, before any data exist: if verbalized confidence saturates on the 12b (the saturation flag from probe 2, already in this log, is the reason to expect it can), H1 can come out falsified on that method. A tie rate may be reported, descriptively only; it never changes a verdict. Caution for the eventual write-up: both AUROCs come from the same items and the same answers, so the two methods are correlated. Passing both is stricter than passing one, but it is not two independent confirmations.

Prereg amendments, all intentional, same session (SESSION_PROTOCOL section D):
- Section 3, Definitions: added the both-must-hold definition (AUROC computed separately per method; both per-method results must clear the bar) and the per-method noise-floor clause. Reason: the decision above; with two methods, one shared floor would let one method's noise set the other's bar.
- Section 3, H2a Verdict: "H2a is not supported" became "H2a is falsified", and "supported or not" became "supported or falsified". Reason: the new table needs one label per outcome, and the Falsifier already said "falsifies".
- Section 3, H2b Precondition: "rather than confirmed or falsified" became "rather than supported or falsified". Reason: H2b's success label is "supported" everywhere else, the table included.
- Section 3, new Split verdicts block after H2b: the opt-for-weaker rule with its three orderings (confirmed > suggestive > falsified for H1; supported > falsified for H2a; supported > not evaluable > falsified for H2b), a 15-row table of overall verdicts, and a closing line that per-method verdicts are always reported. Reason: the table is checkable against a stated ordering instead of fifteen cells that happen to agree.
- Section 5, pilot outputs: "four outputs" became "six". Reason: one AUROC noise floor and one spread noise floor per method, plus p_weak and p_strong.
- Section 6, verbalized-confidence parsing rule: corrected the stated reason for dividing by 100. The old text said AUROC needs the two methods on the same scale, which is false, since AUROC uses rank order only. The real reason is that ECE, Brier score, and the reliability diagrams compare confidence against accuracy, which is a proportion. The rule itself is unchanged.
- Section 8, noise-floor collision sentence: now "either method's" floor. Reason: with per-method floors, one method's floor can collide with H1's fixed threshold while the other's does not, and the single-floor wording left that case undefined.

Settled this session, because they ground the decision. AUROC is computed within a single cell and uses rank order only; ties count 0.5; rescaling the scores cannot change it. Saturation, confidence piling up at the top of the scale whether the answer is right or wrong, pulls AUROC toward 0.5. It is not always an artifact (it can be genuine overconfidence), and verbalized output alone cannot tell the two apart. AUROC is undefined only when a cell has zero correct or zero incorrect items; N is sized two-sided to guard against that.

Provenance commitment: the 300 harness-validation rows in pilot_runner_log.jsonl were not opened for this decision. They hold the same 50 pilot items on the same two models, which makes them pilot data in everything but name, so opening them for any pre-pilot rule would make that rule post-hoc. The refusal pattern list, the tie-rate statement, and the section 8 noise-floor procedure are all still unwritten. The boundary is therefore not "until the section 3 text is committed" but this: the rows are not opened for any pre-pilot rule, and are deleted without further inspection before the pilot of record. (They were examined on 09-20 for harness validation only: counts, duplicates, provenance, schema. No grading or AUROC has been computed on them, and the grader does not exist yet.) The deletion is required regardless, because the keep-first hard stop requires it.

Pre-pilot gaps surfaced, not fixed:
- Section 9's refusal rule has no pattern list. The grader cannot implement it, and a list written after seeing pilot refusals would be a new rule, not a code fix.
- Section 8's noise-floor measurement procedure is still unwritten (the 09-20 entry already noted this). When it is written it has to address three things: scaling the 50-item pilot floor to the main-study N; whether the floor is for a single AUROC or for a difference of AUROCs; and that the pilot runs two cells while H2b's spread needs four.
- Section 10's saturation entry covers P(True) only and needs to cover verbalized confidence too.
- The tie-rate statistic has to be stated as descriptive-only, in section 7 or in the exclusion table.
- Section 6's resume clause for a terminal Template A failure (under Harness Requirements) names only the C call; B runs too.
- Section 6's verbalized-confidence parsing rule states the leading-zero rule twice. Noted for the consistency review.

OSF: nothing is registered yet. Plan: register the prereg on OSF at freeze and post results to the OSF project at completion. Section 13's freeze mechanics mention only the git tag, so the OSF step needs adding there before freeze.

Pace: two sessions last week; the goal is three per week, November included; the worst case is one per week. Opus's estimates, labeled as estimates: 12-20 sessions to freeze, 8-15 more from freeze to posted results, roughly 45-55% of the way to posted results. Freeze date not set, pending the REU deadline research.

Deadlines: "mid-December" was never a verified REU deadline. It was a placeholder from July that got repeated as fact, the handoff included. REU sites each set their own dates, many of them January to April. I am checking the shortlist, DREU first. The recommenders are for PNNL CCI (early January 2027), which is a separate program from the REU.

## 2026-10-08 - 2026-10-10 README, LICENSE, CITATION; publish decisions; two pre-pilot findings

10-08, discussion only, no commit. Open checks passed at da50cea - the runner itself was already complete, so "finish the runner" meant the still-open handoff close-out items (28-31, 33-35) and not more runner code. New pre-pilot gap found: no hypothesis names which elicitation method its AUROC comes from - line 314 says "primary metric for H1, H2a, H2b," and section 3 never names P(True) or verbalized confidence anywhere. Averaging both into one number is ruled out by the line-348 precedent (constructs a value the model never expressed). Undecided between primary-plus-secondary and both-must-hold; item 29 (whether B enters the pilot of record) depends on this. Separately - to be added to handoff section 5c as item 36, not yet written there - the line-247 commit-hash hard stop collides with SESSION_PROTOCOL section E's daily-commit rule: any interrupted run becomes un-resumable once the repo changes before resume, whether by a commit (line 247) or an uncommitted edit (line 259's dirty-tree check). The main sweep (2-5 hours) is exposed; the pilot (~4 minutes) effectively isn't. Two decisions made: keep the handoff in the public repo (removing it would read as hiding), and publish with full history after an audit - only my name and email appear across every commit, the runner log was never committed, no tokens. Also on 10-08: three handoff items checked against the files. Two had already landed - the Template B reversal reasoning and the step-6 authorship statement, both in the 09-20 entry. One was half-landed: the cut-line decision (runner completion as the hard deadline, grader deferred as fragment-tolerant work, decided 09-18) is recorded in the handoff but never made it into the 09-18 lab log entry itself, despite the handoff asking for exactly that. Separately: the handoff's freeze-mid-October plan is overtaken by events; a new freeze date still needs setting.

10-10. Added README.md, LICENSE (MIT, code) and CITATION.cff. Documents and measurements are CC BY 4.0; TriviaQA's included records are included for reproducibility but excluded from both licenses (TriviaQA's own is listed as unknown); regenerable exactly via draw_pilot.py. Switched to GitHub's noreply email for future commits - past commits keep the Gmail address, unchanged. Prereg amendments, both intentional, same session: line 4's author changed from "Laz" to "Nathaniel Campbell", matching the public name in README and CITATION.cff; and the probe-pointer at line 368 corrected, since probe 4 is a .py file and probe_out/ also holds its two warm-run JSON files, not just raw CSVs. Handoff placeholders filled in.

Two findings while writing the README's Reproducing section. First: run_pilot.py crashes outside a git checkout - line 31's git rev-parse HEAD has no fallback, so a ZIP download can't run it at all. Documented in the README as a requirement (clone with git) rather than fixed in the harness. Second: rerunning draw_pilot.py always dirties the tree even at the identical seed - not because the draw changes (items_pilot.jsonl rewrites byte-for-byte identical at a fixed seed, verified across three runs in the 09-05 entry, and git compares content, not write times) but because items_manifest.json records a fresh timestamp on every run regardless. Same script, same files as the hazard the 09-05 entry already logged ("draw_pilot.py opens in 'w' mode, so re-running it overwrites both committed artifacts") - this is that hazard actually firing, not a new one. Not permanently dirty either: git checkout -- items_manifest.json restores it, and the README now documents the step.

Prior work found, not yet read: Proskurina et al. 2024, "When Quantization Affects Confidence of Large Language Models?" (NAACL Findings). Belongs in prereg section 2 once reviewed.

Carry-forward: once this commits, pilot_runner_log.jsonl (the 300-row harness-validation run from the 20th) will trip the keep-first hard stop the next time run_pilot.py starts with it present - a fresh run included, not just a resume attempt. Move or delete it before the pilot of record runs, not after.


## 2026-09-20 Steps 5-7 done: run_pilot.py hardened, resumed, and verified clean

Claude's review of the step-5 smoke test found six real gaps - no timeout, reading the response before checking done, C running regardless of A's outcome, options typed twice, no retry, unhandled HTTP errors - all fixed. Step 6 refactored the whole thing into one run_call function (retry, row-build, write) shared by all three templates, added resume (triple-based skip, plus a stored-answer lookup so B/C can still build prompts after a resumed A), warm-up and unload per model, and included Template B tonight rather than deferring it. Step 7 added the two remaining startup hard stops: working-tree-clean, and keep-first agreement on commit hash and Ollama version across existing rows.

False-provenance finding: the first strip-fixed, zero-duplicate 300-row set carried a false commit hash - written while step 6 was uncommitted, every row claimed Friday's step-5 commit as its origin. Line 259's exact hazard, caught as a measured event an hour before the dirty-tree check that would have prevented it existed. Deleted.

Four tests, all passed:

Forced timeout - one A row, timed_out true, attempt_count 2, no B/C row, run continues. Confirmed twice: pre-hardening and again against the final committed code.
Dirty-tree trigger - edited a tracked file, confirmed the stop; reverted, confirmed it proceeded.
Keep-first trigger - ran post-commit against the false-provenance rows, confirmed the stop on hash mismatch. Fired a second time, incidentally, when the stale file was still present for test 1's retry.
Full clean run - 300 rows, 300 unique triples, zero duplicates, 100/100/100 across methods, 150/150 across models, all done, zero timeouts, correct provenance. First run to genuinely exercise unload() and the /api/ps poll on real model swaps, since nothing was skipped by resume.
Roadblocks: the dirty-tree check blocked the timeout test itself, since testing it requires an edit - resolved by committing the test value, testing, then committing the revert, rather than bypassing the check. The keep-first check then blocked the same retry because the stale 300-row file was still sitting there - resolved by deleting it first. An earlier 303-row run showed one triple duplicated 4x; traced to pre-resume-era test attempts that predated run_call and were never cleaned up between them, confirmed by timestamp and commit hash, not a resume bug.

Open, not fixed tonight: a resumed row that's valid JSON but missing a key crashes instead of being skipped. A whitespace-only answer isn't distinguished from a real one.

Tonight's clean run is harness validation, not the pilot of record - section 8's procedure and section 11's rule aren't written yet. Not to be treated as study data by a future session.

Template B's reversal, and why: on 09-10 I set a bar for myself - complete through the start of step 7 in that session, or drop Template B from pre-21st scope - missed it, and deferred B to October. Tonight it went back into the runner. Reasoning: pushing to meet my own deadline, the runner's full completion before fall quarter classes begin on the 21st. I originally deferred B, but with how fast Sonnet and I were moving together tonight, I decided we could tackle it now instead of in fragmented time later.

Who wrote step 6, stated plainly since it bears on this project's no-edits rule: I wrote it. Every line, every character in run_pilot.py is mine, typed in myself. Sonnet explained the solution and guided me through each piece whenever I got stuck, drafted proposed text for me to type, and verified what landed against the live file afterward - but never touched the file directly. Same rule that's held for the prereg and this log since the start of the project, unchanged for code.

## 2026-09-18 Step 5: run_pilot.py writes and logs a verified row per call (Step 5 done except the forced-timeout test)

Step 5 mostly done and verified on sfq_1586: run_pilot.py now writes one JSON row per call to pilot_runner_log.jsonl (gitignored), built from a per_run_fields dict (the nine section 6 "per run" fields) plus per-call Identity/Response/Timing fields, using observed values (Ollama version, model digest) rather than the frozen constants they're checked against. Built alongside: a 90s timeout, retry-once on both timeout and done: false per section 9, C gated on A's outcome, the options dict deduplicated into base_options, and a deliberate decision to crash loudly on an Ollama/model-error response rather than retry it.

Raw measurements, sfq_1586, harness commit 6779746: A - raw response "A low, upholstered seat.", load_duration 3,516,066,500 ns (~3.52s, cold), eval_count 7, prompt_eval_count 46, attempt_count 1. C - raw response "10\n" (trailing newline preserved), load_duration 229,959,000 ns (~0.23s, warm), eval_count 4, prompt_eval_count 82, attempt_count 1. The cold/warm gap in load_duration is the measured reason step 6 needs its warm-up call.

One real fix mid-build: the row was gating done_reason, the timing fields, and the raw response entirely behind done: true, on the assumption done: false meant none of them existed. Line 298 only promises that on a timeout, not on done: false. Fixed to check each response field's presence individually and log whichever ones actually came back, so a done: false row still gives the grader something to apply the no_valid_response rule against.

Open going into next session: the forced-timeout failure path is untested - set a tiny timeout, confirm a timed_out row appears and C is skipped. Two minutes, blocks nothing, first item tomorrow. pilot_runner_log.jsonl held tonight's test rows and has been deleted ahead of the real pilot run - the keep-first/commit-hash hard stop would have caught stale rows post-commit anyway, but deletion doesn't rely on that.

## 2026-09-18 Prereg review finishing touches and fixes: Six blockers cleared, two review passes, Step 5 unblocked

Session framing. Opened by refreshing context against the live repo rather than the prior conversation: confirmed the last session's ~20 amendments were committed (e4f28e4), found HANDOFF had already been updated separately (eb83167) to state Step 5 was blocked on four specific section D amendments not yet landed. Verified all four against the live prereg before starting — every citation held.

E, A, B, C, D, F - worked in Opus's suggested order, one at a time, each verified against the live file before drafting.

E (runner/grader field split). Section 6's Logging block never actually separated what the runner writes from what the grader writes, despite that split being decided back on 09-12 - line 289 even said grading fields were "specified above in the Grader Spec" as if runner and grader output were one row, not two files. Rebuilt into two explicit lists. Sorted every existing field by who can produce it without parsing: raw response, raw logprobs, and the top-10 candidate list moved to the runner; matched/alias/negation/compliance/truncation/exclusion-reason and both templates' derived values (renormalized P(True), retained mass, parsed integer, mapped confidence) stayed grader-side.
A (elicitation_method's undefined values). The field existed, the resume triple depended on it, and nothing defined what it could hold - worse than assumed, since B and C had no values either, not just A. Landed as 'answer' / 'p_true' / 'verbalized' for Templates A/B/C, following "name the act," both terms already matching vocabulary the document uses elsewhere (P(True), verbalized confidence). Worth remembering: the document's own line 110 counts only two "elicitation methods" methodologically (P(True) and verbalized confidence) - the field still needs three values since Template A gets logged too, which isn't a contradiction, just easy to misread.
B (model tag/digest/quantization scope). Three lines disagreed: digest logged "per row" in one place, filed under "per run" in another, model tag required on every row by the resume triple but absent from the actual per-row field list. Root cause: the pilot runs two models in one process, so "per run" was simply false for these three fields. Moved tag, digest, and quantization into Identity; fixed the parenthetical to "constant for the process," which is now actually true of everything left there.
C (harness commit hash + run_id). Neither existed anywhere. This was a real decision, not just a gap - resolved in favor of everything living per-row (no separate run-record) rather than a run_id pointing back to one, because that's the same choice this project already made once, for the same reason, when provenance went on every row instead of a sidecar manifest. run_id declined explicitly, using the same uniqueness test that retired the draw index: it would only be a second, weaker version of a guarantee the row already carries.
D (dirty-tree hard stop). Nothing existed to catch git rev-parse HEAD reporting committed state while uncommitted edits actually ran. Verified against SESSION_PROTOCOL.md before accepting "whole tree, costs nothing" - confirmed true, since the protocol already requires a clean tree at both session close and open. Added as a third clause alongside the existing digest/version hard stops, same shape, same paragraph.
F (resume after a terminal Template A failure). The 09-12 decision that a terminal A failure writes no C row collided with resume's only two states (row present = skip, row missing = run) - a missing C row would get misread as "interrupted, run it" when really C's input never existed. Added a third resume state: an A row present and terminal (done: false or timed out) means C is already accounted for, not pending.
G stayed parked exactly as scoped - whether a terminal A failure needs its own section 9 reason code is grader-session work, noted for the log, not touched today.
First Opus review of the six: seven of eight items clean, one real gap. Three "real holes" surfaced - places the code would have actually broken, not just wording:

Keep-first had no precondition. As written, a runner bug fix and resume would let the old buggy rows keep winning, since keep-first never re-examined them - the commit hash on each row existed for exactly this and nothing used it. Added: compare existing rows' commit hash and Ollama version to the current process at startup, hard stop on mismatch.
The dirty-tree check would have blocked every resume, full stop - the runner's own output file, if tracked, dirties the tree the moment a row gets written. Fixed by stating output files are gitignored, distinct from items.jsonl's frozen/committed status.
A timeout had nowhere to be recorded - on a genuine timeout there's no API response at all, so done/done_reason don't exist to read, leaving both resume and the grader's §9 timeout rule with nothing to check. Added a timed_out field to Response.
Five smaller fixes landed alongside: raw logprobs of both matched tokens was flagged as grader work sitting in the runner list, and wrong on its own terms (the P(True) rule sums every matching candidate, not just two) - first pass moved a corrected version to the grader side but didn't remove the stale original from the runner side, caught and fixed in the next pass. Per-run fields were declared "constant for the process" but never explicitly said to be written on every row, which the run_id-decline reasoning depended on - said explicitly. Grader rows had no join key back to the runner row they graded - added the triple. Grader Spec's field list was being both pointed at and re-copied in parentheses at Logging - the eighth instance of the exact duplication pattern from last session's review, caught immediately by pattern-matching rather than needing to be re-discovered. And a wording fix: resume's language said the runner "excludes" a failed item, when the runner/grader split says exclusion is strictly a grader decision - changed to "accounted for."

Second small round. A stray in-document line citation ("line 239") got caught the same morning it was written - swapped for a durable name ("the runner/grader split rule above"), consistent with the citation discipline adopted last session. "Collect completed triples" turned out ambiguous in a way that reopens a real hole: read as "succeeded," a twice-failed C call would get re-run on every resume, which is exactly the re-rolling keep-first exists to prevent. Reworded to "any well-formed row - success or failure." One optional precision take: on a timeout, more than done/done_reason go missing (Timing and Raw response do too) - applied with a small adjustment, naming the specific categories rather than the looser "all response fields," since timed_out itself is very much present on a timeout and shouldn't read as excluded by that phrase.

Status. All eight items from the follow-up review confirmed landed via direct diff inspection before writing this entry. Step 5's blockers are cleared - next up is run_pilot.py itself, writing one row.

## 2026-09-17 - 2026-09-18 Full prereg review with Opus, sixteen findings, ~20 fixes landed

Session shape: Opus ran a fresh, full review of the revised prereg, surfacing sixteen findings made up of reasoning issues, contradictions, and prereg-vs-code checks.

Degenerate-generation number - resolved. The same measured boundary (num_predict ≥ 32 on gemma3:1b-it-q8_0) was stated twice: once with its digest in section 6's Findings block, once restated in the Parameters block justifying why all three templates' num_predict values sit below 32. Findings keeps the number; Parameters now points to it instead of restating it - and the first draft of that fix still leaked the literal "32" before the test caught it, which is the sharpest confirmation yet that the test has to be applied to my own drafts, not just the original text.

The no_valid_response retry rule - resolved. Section 6 and section 9 both stated the same retry-then-exclude rule for done: false and already drifting in wording ("same call with no change" vs "identical call"). Section 6 now delegates to section 9 by name instead of restating trigger/action/outcome. Checking whether this pattern recurred elsewhere found that Timeout has the identical retry-then-exclude bundling with no runner/grader split stated anywhere so the fix became a general statement in section 6 ("for every section 9 rule that both retries and excludes, retry is a runner action... exclusion is a grader decision...") rather than a patch scoped to one rule, closing a second, previously unflagged gap for free.

A seventh duplication, same policy: the Truncation detector. Template C's parsing-rule paragraph restated the Grader Spec's Truncation detector rule (trigger, action, outcome) instead of citing it. Fixed the same way as the others: restate the action ("follow the Grader Spec's Truncation detector"), not the condition or outcome.

Section 10 mostly repaired: the four scaffold bullets were rewritten, one duplication remains. Once the stale-finding confusion cleared, walked through all four real gaps left by deleting the old scaffold bullets: the differential-exclusion orphan fragment (now a real entry citing section 8's mechanism and bias direction), the contamination bullet (full rewrite. concedes contamination scales with model size, follows it into AUROC, threatens H1 specifically, spares H2a/H2b on the shared-baseline argument), quantization-confounded-with-scale (new, cites H1's q4_k_m-only rung), the instruct-tuning limitation (reframed from a false within-roster claim to the real cross-study one against Kadavath), and the extrapolation-limit block (the biggest rewrite in the document - scope/split, measured evidence, guidance for replicators).

draw_seed - named, and a real integrity rule added, value still open. Section 5 used bare "seed" for both the dataset draw and section 6's generation seed=42 without distinguishing them; HANDOFF already had the fix (draw_seed) but it never reached the prereg - renamed at all three draw-context mentions. A new rule was also added: draw_seed must be fixed before draw_main.py is ever executed, and the draw itself is not repeated, the first draw at that seed is the draw, recorded in items_manifest.json. That forecloses re-rolling the main draw if a first result looks unfavorable, not a scheduling note. The actual numeric value still doesn't exist anywhere, confirmed even HANDOFF says "Value not yet chosen", but it isn't blocking, since draw_main.py itself can't be written until the pilot reports p_weak/p_strong.

top_logprobs - load-bearing and previously unpinned. P(True)'s position-0 candidate-distribution read and the "full top-10 candidate list" logging requirement both depended on a parameter that appeared nowhere in Parameters or per-run logging: only in a passing Findings observation. Added as its own Parameters bullet (Template B only, mirroring num_predict's per-template treatment) and to per-row Identity logging, for the same self-contained-auditability reason num_predict and digest are already logged per row.

Header sentence, one of two defects fixed. "Survive instruct-tuning, quantization, and small scale" listed instruct-tuning as a tested axis when nothing tests it. every roster model is instruct-tuned, held constant by H1/H2a/H2b design. Removed from the list; the "frontier-scale" half of the same sentence (already tracked, HANDOFF item 1) stays untouched for its own dedicated session, since reframing it properly is entangled with the overlap-not-absence rework.

H1 versus the pilot-measured noise floor - a real collision, now disclosed. C=200 was sized so a predicted floor (~0.03) keeps H2a/H2b's threshold safely under H1's fixed 0.1 but H2a/H2b actually use the measured floor, and nothing said what happens if that measured floor comes in high enough to invert the relationship. Resolved as a disclosure rule in section 8, not a threshold change - H1 keeps its deliberately-fixed value (that's an intentional design choice, not an oversight), but a collision now gets reported explicitly rather than silently absorbed.

Contradictions. 1: Section 6's contamination-sources note said none of the three sources show up in load_duration; a separate harness-requirement line said load_duration detects mid-run reloads - apparently contradictory until realizing "source 1" was mislabeled: the warm-up call already discards genuine cold-loads, so whatever's left (57.9 vs ~239 tok/s leading the loop) is a separate GPU/driver-state effect, not model loading. Relabeled "cold-load/first-in-loop" to "first-in-loop," left the load_duration detection claim untouched. 2: The pilot was stated as "never analyzed" / "never enters the analysis" in two places, directly beside the pilot's own stated four outputs (p_weak, p_strong, two noise floors) that set N and every H2a/H2b threshold. Both instances reworded to "never enters the study's results" - the intended, narrower claim.

Two more duplications, same policy as the others. Template A's word-count rule restated the Grader Spec's Compliance detector instead of citing it, fixed the same way as the Truncation detector. And the contamination/load_duration pair itself turned out to duplicate: the detailed Findings-block version (with real measured numbers) is the home; a second, shorter mention later in section 6 restated it in different words and was replaced with a pointer, keeping only its one genuinely unique point (the E1/throughput link).

Prereg-vs-code: tag casing resolved, digest truncation deferred. Section 4's table used mixed-case q4_K_M where run_pilot.py uses lowercase q4_k_m. Resolved in favor of the code, since Ollama's live /api/tags was already empirically confirmed this project to return lowercase (this exact miscasing caused a real false "model missing" bug earlier this session before being fixed). Section 4 and the pilot-spec prose both updated to match. The separate digest-truncation question (12-char prefix in section 4 vs full 64-char digest in code) - a proposed assert digest.startswith(...) safeguard in run_pilot.py - deferred to another session; nothing landed there, correctly, since it's genuinely optional hardening rather than a live bug.

Exclusion table, attempt count, and reason-code placement. The exclusion table has carried three reason-code columns against section 9's four codes since a much earlier session: confirmed still broken on this pass, now fixed with an excluded-no_valid_response column. attempt_count added to per-row Identity logging, directly following the 09-12 retry decision. Exclusion reason itself went through real back-and-forth: first instinct was to add it alongside attempt_count in Identity, but section 6 already states explicitly that grading fields belong in the Grader Spec, not Identity - and Opus sharpened the reasoning further, grounding it in the runner/grader-decision architecture rather than just the document's own stated organization. Landed in the Grader Spec's per-row list instead. That surfaced one more real gap, explicitly carried forward rather than fixed tonight: three of section 9's four codes are grader-derivable from stored output, but timeout isn't - a call with no response in 90 seconds has no body to parse, so only the runner can ever know it happened, and nothing currently gives the runner anywhere to record that. Not blocking (timeouts are Step 6/7 work; Step 5 only writes rows from successful calls), but real, and worth having in the log so it doesn't surface as a surprise at implementation.

Administrative. The stray post-study TODO (re-enable Ollama/driver auto-update) moved out of section 12 into a new POST_STUDY_TODO.md, to be committed. I also added a second item (revert KV cache to q8_0) as well.

Open going into next session: KV cache finding (first of the review): line 142 pins f16 with a methodological reason, line 285 lists it as a per-run logged field, and run_pilot.py has zero references to it. No check, no log, while the Ollama version and the digest each get a hard stop for a weaker version of the same drift risk. Line 144 already solves the analogous problem for flash attention by reading the server log.digest-prefix equality check in run_pilot.py (deferred) · draw_seed's actual value for the main draw (not blocking, needs choosing before draw_main.py exists) · the runner-side timeout-recording gap (carry, not fix) · the frontier-scale/overlap header rework (its own full session) · §6 line 289's "grading fields... in the Grader Spec" framing possibly being stale against the runner/grader-separate-file decision (flagged, not resolved).

## 2026-09-12 - 2026-09-14 Scope and Step 5 decisions, prereg defects, and Claude's errors (No code)

Scope decision. Pilot execution deferred past the 21st; the harness itself becomes the pre-21st target. Reasoning: the pilot run is largely autonomous once triggered - so it doesn't need a protected uninterrupted block the way finishing the runner and grader do. Consequence: section 11's rule and section 8's procedure, both previously scoped as pre-21st, become pre-pilot instead, which happens to land them exactly where the re-plan already wanted prose written. This dissolved a scheduling collision rather than correcting a reasoning error.

Row structure - one row per call, not per item. Grounds: every field named at line 286 and in the timing block is a property of a single call, not of an item. Line 238's resume triple only resolves usefully at call granularity. My first framing of this as a potential-vs-confirmed-issue distinction was revised under challenge: the duplication failures seen elsewhere in this project were prose failures - a human editing one place and forgetting another - which a JSONL file written in a single loop pass structurally can't reproduce. The misalignment I was worried about is positional matching; joining on question_id (verified unique across all 11,313 rows) is the fix for that, not an instance of it.

Retry. One row per call regardless of retry count: a retry is the same measurement attempted a second time (line 322: "same call with no change"), not a new measurement. Attempt count recorded as its own field. Stated cost of this design: the first attempt's timing metadata is lost when the retry's row overwrites it.

Failure rows. Every call that concludes gets exactly one row. Consequence: a missing row means interrupted, never means failed - "failed" is always represented by a written row with done: false, not by absence.

Terminal A failure writes no C row. My first instinct was to write a C row with done: false. Corrected: C was never runnable - it had no input - which is different from C running and failing. done: false already carries a measured meaning that line 322's retry rule keys off; using it here would produce a row instructing a retry of a call whose input doesn't exist. Second ground: section 9 excludes an item from a cell on a terminal A failure, so that's one exclusion: one row reports the rate directly; two rows would double-count a single event.

Resume reads row presence, not the triple set. A well-formed row means concluded: skip it. No row means interrupted: run it. Section 6 already tolerates and discards a malformed trailing line on resume, so the mechanism was already there. I had claimed triple-matching was broken and needed a new field; it wasn't broken, and that pushback was correct.

Division of labor: runner records, grader decides. The runner writes raw text only - no parsing, no derived values. Grounds: section 6 says the pilot exists precisely so a grader bug costs a re-read of stored output, not a re-run of 100 model calls. Corollary: since output is append-only, the grader has to write its own second file: meaning section 6's "parsed integer, mapped confidence" describes graded output, not runner output, and the two were previously conflated.

Prompt template ID dropped from line 286. Its only job was versioning prompt text, and the harness's own git commit hash already pins repo state; since the prereg lives in the same repo, the commit hash identifies which template text was in force at least as precisely as a dedicated field would. This is the same test that eliminated the draw index in section 5e. Confirmed line 286 is the field's only occurrence in either document, so removal is clean. Recording it here explicitly because a field silently disappearing from a spec reads as an accident to anyone diffing later, not a decision.

elicitation_method keeps its name and carries the exception. Principle agreed on: name the act, not its absence. The value itself was never in question — it gates whether the row gets written at all.

Prereg defects found this session:

Line 282 vs. line 250 — 282 lists model digest as a per-run field; 250 requires it logged per row so a replicator can confirm which weights produced each measurement. Opposite instructions in the same document.
Line 282's parenthetical "(Constant for the process or the cell)" never actually picks one. Model tag, digest, and quantization vary per cell; the other eight fields in that block are constant for the whole process. The pilot runs two models, so this ambiguity becomes load-bearing at step 6.
Line 324's exclusion table carries three reason-code columns where section 9 defines four: no_valid_response has no column. This is section 5c item 9, and it's now confirmed as a narrow, specific gap rather than a vague concern.
Section 6 has no run_id field and no harness commit-hash field anywhere.
No dirty-tree check exists anywhere in section 6. Line 250 is the shape a fix should follow.

Claude errors, for the record (As stated by Claude): 

Claimed §9 had no no_valid_response category when line 322 defines exactly that. Cause: read lines 304–320, where §9's fourth rule actually sits at 322, then asserted the gap two turns later without reopening the file.
Repeated the handoff's characterization of row structure as open design work when line 286 had already specified it — caught only because you asked how I'd concluded that.
Claimed resume logic had broken and needed a new field, when it hadn't.
Claimed the method field discriminates at the runner level, when the fields at line 265 are grader outputs, not runner outputs.
Common mechanism behind all four: reasoning from a summary of the file instead of the file itself.
Process change adopted. Any file review from here forward cites a line number plus verbatim text, or explicitly states the file hasn't been checked yet — no more claims from memory of what a section says.

Open going into next session: Template A's method value · digest scope (process vs. cell) · run_id + commit hash fields · dirty-tree stop · line 324's missing column  · whether A's cascade needs a fifth reason code · per-run vs. per-cell split for the sidecar.

Gate. Next session is the review of these decisions against the prereg text, not new work. This needs to carry into the handoff as next-action #1, not just live in this entry.

## 2026-09-09 - 2026-09-10 run_pilot.py steps 2-4 completed

Step 2 finished and tested. Both hard stops (Ollama version mismatch, model digest mismatch) verified live by deliberately breaking each value and confirming the crash fires with a correct, informative message; both restored afterward.

Step 3: Template A, one item, one call. Deliberately picked sfq_1586 over qw_402, which carries CSV quote artifacts in its raw text - avoided so a bad result couldn't be confused for a bug. Verified Template A's frozen wording against section 6's raw file line numbers (not rendered view). Full pipeline works: real question in, /api/chat call out, message content extracted into its own variable, and printed. Model's answer was wrong but coherently shaped: expected from a 1B model on an obscure fact, and sufficient to prove the code path. Model's answer: "A low, upholstered seat"

Cold-contamination incident: Built /api/generate vs /api/chat logprobs comparison to settle Step 3's endpoint choice with evidence. First run showed every logprob diverging between endpoints despite identical text output, and I wrote it up as a real finding with attached files. It wasn't. Caught by reading load_duration: 2.52s on the /generate call (cold-load range, matching Probe 3's 2.15s baseline) against 0.24s on /chat (matching the established ~215.5ms warm constant). The two calls weren't testing endpoint vs endpoint - they were testing cold vs warm, the exact issue section 6 already names as finding #3, just not caught before running. Re-ran warm-vs-warm (throwaway call first, discarded, then the real comparison): logprobs matched bit-identical at all 12 positions. Correct conclusion: /api/chat and /api/generate agree numerically on a warm model; the endpoint choice rests on the chat-templating argument, not on any numerical divergence. This is the third time cold-load has produced clean-looking-but-wrong numbers. Worth remembering as a pattern, not just three isolated incidents. Extracted into probe4_endpoint_logprob_diff.py, matching the existing probe* convention; output files renamed to *_warm.json after the first run's identical filenames silently destroyed the cold-run evidence via 'w'-mode overwrite: a live example of the exact risk this project has been vigilant about elsewhere.

Step 4: Template C. Used multi-line f-strings via triple-quoted strings, and repr() to verify exact string structure rather than print(), which renders newlines invisibly (same "raw view vs. rendered view" lesson as the line-number check, applied to a Python string instead of a markdown file). .strip() decision implemented as a separate variable rather than overwriting the raw response. raw Template A output is whitespace-stripped before entering C's [Answer] slot, because whitespace behavior correlates with model size and a whitespace-sensitive prompt would put a size effect inside the instrument on a size hypothesis. Written as a rule in section 6's template sub-block with reasoning attached. Second call sent, raw confidence ("10") printed unparsed. Sense-checked: low confidence paired with a wrong answer is a coherent result, not just a well-formed one.

Post-Step-4 full-file review (Claude). Found: model name hardcoded in three places (both request bodies plus the frozen constant) instead of reading from MODEL_1B_Q4['model_name'] - fixed, one home for the fact now. Minor style/consistency fixes (== False → not, scaffolding marked for deletion once Step 6 replaces it, a comment explaining why the 12b is digest-verified but not yet called). Also surfaced a real prereg defect: section 6's Template B/C indentation is entangled with markdown list-continuation formatting, so the frozen prompt text isn't unambiguously specified in the document as written. Fenced code blocks in section 6 is the fix - landed.

The Template B threshold: With the September 21st deadline approaching quickly, I set a bar for myself which determines whether Template B is incorporated in this build before the 21st, or ran with only Template C. The threshold: in today's session, if I could not complete everything up to having started step 7 - the final step - I would drop template B. I completed up to step 4 and deferred step 5 to the next work session. I simply and honestly did not meet that bar. Template B is dropped from pre-21st scope. The pilot runs Template C only. B lands in October. B's parser is the hard one (position 0, renormalization, retained mass, the empty-token edge case), and it now gets built in fragmented time. That's the price

## 2026-09-06 - 2026-09-09 run_pilot.py creation and work.

A forenote: I neglected this log for a couple days. I am making amends by combining three days of work into this entry - all work is done inside run_pilot.py

- Step 1:
draw_pilot.py is finished. it produced items_pilot.jsonl which I used here. Since run_pilot.py runs as its own separate program, none of draw_pilot.py's in-memory variables survive; the only thing that persisted across that script's exit was the file it wrote. So run_pilot.py opens items_pilot.jsonl in read mode, loops line by line, and uses json.loads() to turn each raw text line back into a real dictionary  Only question and question_id are kept per item - the answer fields (normalized_value/normalized_aliases/value) are deliberately dropped here, since the grader will re-open the frozen items_pilot.jsonl later and rejoin on question_id rather than carrying answer data through this pipeline. Asserts exactly 50 items came through.

- Step 2:
Ollama tags are mutable pointers, and the project had already been silently moved once before (Ollama 0.32.6 moved to 0.32.14),  so this step exists to refuse to generate any data if the environment has drifted, hard stopping rather than just warning. Used requests library (already a listed dependency, no fresh install needed) to make HTTP calls against Ollama's local server at 127.0.0.1:11434, not localhost. GET /api/version returns the running Ollama version; compared against a frozen OLLAMA_VERSION constant and hard-stops via sys.exit() with a message stating expected vs. received.
GET /api/tags returns metadata for every locally installed model as a list under a 'models' key. Built two frozen constants, MODEL_1B_Q4 and MODEL_12B_Q8 - the pilot's weak/strong model pair from the prereg's section 4 roster - each pairing an expected model name with its expected digest, combined into a MODELS list. Built a nested loop: outer loop over the two expected models, inner loop searching all installed models for a name match, then comparing digests on match (hard stop on mismatch). Used break to stop the inner search early once found, and a "found" flag (reset fresh per outer-loop pass) to catch the case where an expected model isn't installed at all. Found that ollama list's CLI digest column is truncated (12-character prefix, not the full SHA256). Retrieved the full digests and verified against full digests - machine accuracy, a human can tell the difference by reading the first few characters of the hash. Tested code thoroughly and did a full pass of comments - step 2 functionally complete and verified.

hand-edited .gitignore to add tempCodeRunnerFile.py (an artifact of my VScode extension "Code Runner") and found that data/ was structurally dead - git can't re-include a file inside an excluded directory - so I deleted both rules.

Some findings: 
- /api/tags casing investigation: a bug tripped me up here - 'model_name' 's value inside the two model constants at the top of run_pilot.py caused a "missing model" crash. Curious, I was certain I had the model. I printed the api tags and found that the name field was lowercase: "gemma3:1b-it-q4_k_m" and the quantization level field was uppercase: "q4_K_M"
- The digest length bug fired on a healthy model because I trusted the windows powershell command "ollama list" to give me the digest hash, but ollama truncated the full hash in that CLI environment. I pulled the full hashes from the tags and updated the constants. But it did prove that the hard stop works - the check refused to proceed on a mismatch.

An honest confusion: I was planning to write run_pilot.py inside of draw_pilot.py because I was confused on my next steps after having completed draw_pilot.py - Slice 2 had no step breakdown before starting the work like slice 1 did. A confusion caught before amending a finished draw_pilot.py, thankfully.

A good lesson from debugging: inspect a structure you didn't build before reaching into it. Both came from writing the reach before printing the shape.

## 2026-09-06

hand-edited .gitignore to add tempCodeRunnerFile.py, discovered the data/ exception was structurally dead, removed both data/ rules because the pipeline writes to root.

## 2026-09-05 - Harness Slice 1 finished and deferred lab log entry resolved.
To begin, I fixed the deferred lab log entry - see entry "2026-08-31 - Re-plan" for more.

I shuffled the questions out of the dataset from seed = 8, took 50 of them, and sorted through them with a for loop - pulling the 5 values needed from all 50 items, verifying there is actually 50 via assert function, then recording them to items_pilot.jsonl and also recording timestamp, dataset, config, split, draw, draw_seed, source_rows, skipped, and items_drawn into items_manifest.json. I did a once-over of the two generated files and found ASCII escaping standing in for UTF-8 characters. 

I ran the script three times and got odql_4374 as item 0 every time. That's the seed verified rather than assumed - supports my replication claims. A replicator using DRAW_SEED = 8 gets the exact same items I did.

\uXXXX escapes throughout the alias lists. Not corruption - json.dumps defaults to ensure_ascii=True, so non-ASCII gets escaped. \u0430\u043b\u044f\u0441\u043a\u0430 is аляска, Alaska in Cyrillic. Kept the default deliberately: pure-ASCII output can't be misread by anyone regardless of their editor's encoding.

qw_402 carries CSV escaping that was never stripped - the question is wrapped in quotes with "" doubled around The Gold Cup. One of 50. Reaches the model as prompt noise, uniform across cells, not fixed because a de-escaping rule is the unjustifiable-free-parameter knob again.

TriviaQA's construction artifacts now appear in three distinct fields: the answer wiring (qf_1637), the value field ('(a', "A: Basketball" on tc_543), and the question field (qw_402). Three independent instances is a dataset-quality limitation, not three coincidences. This needs to be a section 10 entry.

Slice 1 done in 2 sessions, 12-19 sessions estimate for completed harness is holding accurate. 

One hazard worth logging: draw_pilot.py opens in 'w' mode, so re-running it overwrites both committed artifacts. Harmless while the seed is fixed; a live risk if DRAW_SEED or PILOT_N ever changes.

I discovered that .select() returns a dataset while example[0:50] returns a column dictionary - I need rows, not columns, so I used .select()

 ## 2026-08-31 - Re-plan: prereg paused for harness. Environment built, Slice 1 steps 1–2.

*Entry written 2026-09-05. Deferred at session close on 08-31 (session ran late), then
deferred four days beyond the stated 09-01. Measurements recovered from the session
transcript, not from disk, the reason the deferral was a risk.*

 A few handoff claims failed the verification:
 - "~2.3s is gone from the document entirely" is false. section 5 line 122 carries "~2.3 seconds (prompt_eval, eval and server_slack summed across the nine cells)." Different quantity from the dead one (the 1b cold-load figure generalized to the roster), same digits. The 08-29 lab log entry states it wrong too — this entry corrects it.
 - Section 5c item 1 was mis-scoped. Section 1's research question has no "uncharted" claim. The only stale text is the header Study: line - "frontier-scale," when Kadavath topped out at 52B. One-line fix. The overlap framing belongs in Section 2, which is empty.
 - No [others] placeholder exists in section 10 (Section 5c item 5 says to delete it). Separately: section 10 line 331 reads "qwen3 has almost certainly seen MMLU and TriviaQA" but the roster is gemma3 and MMLU was dropped. Wrong on the page, not scaffolding.

The re-plan: the pilot requires a harness, and up to this point I had done nothing at all to build the harness. Section 5's p_weak, p_strong, and N blanks and H2a/H2b's noise floor thresholds all require pilot data. The harness is a hard roadblock to the freeze. I decided that September 21st was not a hard deadline, but more so a "capacity cliff" - my life gets considerably busy after Sep 21st and I will no longer have the hours to dedicate to this lab that it deserves. i.e: I should get as much done as possible before Sep 21st, and after the 21st I tidy things up and prepare for freeze. My rough new target is slices 1-3 and the pilot completed before the 21st, slice 4 and freeze in October. This re-plan mainly revolves around my personal life. I am logging it to show the change in direction of work and effort. 

Design Decisions: items.jsonl will have 5 fields: question_id, question, normalized_value, normalized_aliases, value. Dropped answer.type and a draw index. Sidecar manifest, not a JSONL header line. Pilot exclusion by subtraction. Pilot is one draw of 50 on both extremes. Two scripts, duplication hazard (Row shape lives in two seperate files, changing one and missing the other produces mismatched shapes that won't crash) accepted.

The Measurements: 
- Validation split: 11,313 rows - Train: 87,622 (from verifying the split argument).
- question_id is unique across all 11,313 so it is usable as a key.
- entity_pages and search_results fields are empty - this is the nocontext config verified.
- Alias set size (normalized_value and normalized_aliases): min 1, max 214, mean 11.7.
- I found exactly one row with an empty normalized_value.
- Pool math: N = 200 / min(p_weak, 1 - p_strong) +10%: p_weak 0.10 → ~2,200 · 0.05 → ~4,400 · 0.03 → ~7,330 · 0.02 → ~11,000. Pool after pilot withdrawal 11,262. Comfortable unless the 1b lands near 2% accuracy.

The two items I found:
- qf_1637: Question: "In the cartoon, what kind of bird is the roadrunner?" Answer entity: static libraries, .lib, .a, static linking, static compilation. value is the fragment '(a', which normalizes to nothing - that's why normalized_value is blank. The answer entity is internally coherent, just attached to the wrong question, which is why there's nothing to scan for. Dropped by id at draw time, before any model runs, so it's a source defect and not a section 9 exclusion. Open and unquantifiable: rows mis-wired without blanking a field are mechanically undetectable.
- sfq_9993: The 214 max. Question: "In computing, what started life at Stanford University as 'backrub'?" Answer is Google; aliases are every country code domain (google.ae, google.am, google.at, etc.) and scraped typos (gogole com, giigke cin). This is the remnants of a Wikipedia redirect table. I did not cap it though, I would have to invent an unjustifiable number - which I have already rejected doing twice before.

Pre-Pilot Exceptions: Section 11's interpretation rule and section 8's noise floor procedure must be written before the pilot or else they are post-hoc.

Environment Setup: Python 3.12.8, .venv, requirements.txt, .gitignore, execution policy. 3.12 was chosen over the newest Python because the scientific stack may not have wheels built for the newest version yet, and the study's own principle is that this repo pins its own environment rather than inheriting one.

Code: draw_pilot.py steps 1–2 of 5: loads split, prints count, filters qf_1637 by id, asserts len(kept) == len(dataset) - 1. Verified 11,313 → 11,312.

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