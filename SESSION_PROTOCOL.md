# `calibration_lab` — Session Protocol

*Adopted 2026-08-29. Supersedes the working-protocol block in the handoff.*

The rule behind every item below: **nothing depends on either party remembering.**
If a check can only be performed by recalling what a file used to say, it is not a
check. Replace it with something the repo can answer.

---

## A. Closing a session (Laz, in order)

1. **Consistency sweep** on anything edited. Every measured number has one home;
   everywhere else cites the section. If a figure appears twice, one of them is
   already stale and neither of you knows which.
2. **Write the `lab_log.md` entry.** Dated, newest first. Raw measurements and what
   happened — not conclusions only. A conclusion whose data was discarded is
   unreconstructable, and that has already cost this project two figures.
3. **Rewrite the handoff against the file, not against the conversation.** Open the
   prereg and read the actual paragraph before claiming its state. Every mismatch
   found so far came from composing the handoff from memory of the discussion.
4. **Update the handoff header** with the commit it was synthesized against.
5. **Commit.** The upload is then the committed file by construction.
6. **Generate the opening block** (§B) and keep it with the files.

Steps 5 and 6 are not optional and not reorderable. Uploading before committing is
what produced the 2026-08-28 desync: a stale handoff shipped alongside a prereg that
had already moved past it.

---

## B. Opening block (paste into chat alongside the uploads)

```
cd C:\Users\legen\projects\calibration_lab
git log -1 --format="%h %ad %s"
git status --short
git diff --stat <last-verified-hash> HEAD
```

`<last-verified-hash>` is the hash recorded in the previous session's handoff header.

Upload: the prereg **and** the handoff, both current, both committed.

---

## C. Opening a session (Claude, before any work)

1. **Header hash + exactly one handoff-only commit vs `HEAD`.** Mismatch means the handoff describes a version that no
   longer exists. Stop and reconcile before touching anything.
2. **`git status` clean?** Anything uncommitted means the uploaded file is not the
   committed file, and no claim about repo state can be trusted.
3. **Read the diff, not the document.** `--stat` says which files moved. If the prereg
   moved during a harness session, that is a flag (see §D). Pull the full diff on
   anything unexpected.
4. **Verify the handoff's claims against the file.** Report every claim that does not
   check out — in both directions. Work logged as pending but already landed is the
   same defect as work logged as landed but never done.
5. **Only then**, the session's work.

---

## D. Harness phase — prereg drift

Once harness construction begins, the prereg is a **reference**, not a workspace.

Every commit that touches the prereg during a harness session falls into exactly one
of two categories:

- **Intentional pre-freeze amendment.** Recorded in `lab_log.md` with the reasoning,
  same session. Permitted — the document is not frozen yet.
- **Accident.** Reverted.

There is no third category. If a prereg change appears in `git diff --stat` and you
cannot immediately say which of the two it is, treat it as the second one and look at
the full diff.

**After freeze:** record the freeze hash in §13. From that point,
`git diff <freeze-hash> -- calibration_lab_prereg_TEMPLATE.md` must return empty.
If it does not, the diff is not a correction — it is a §12 deviation entry, and it
gets written as one.

---

## E. Standing rules (carried forward, unchanged)

- One session = lab log + commit, daily. Handoff = per chat. 
- Explained: The session is the work day. Every work day gets a lab log entry written from the file and a commit. A chat window no longer dictates a work session. 
- Reasoning: Even if one chat stays open for several days, a log and commit must happen every work session to prevent what's on disk falling behind what's in chat, and at the end of a long chat, the log gets written from the conversation instead of from the page - the 2026-08-26 failure in different clothing. I'm adopting this after my three day session with no daily log or commit, only after (see lab log ## 2026-09-06 - 2026-09-09). 
- A work day only counts as a session when it produces a commit.
- The 12-19 session harness estimate remains, and I consider the 3 day lot of time as 3 sessions. The session is no longer based on the chat window, but the work schedule itself remains unaltered. The unit changed name, not duration.
- **The prereg governs** where prereg and handoff disagree.
- **The handoff stays descriptive.** Reasoning that belongs in the prereg gets written
  by Laz, into the prereg, in his words.
- **Open-but-undecided items live in §5c** and leave it only by being decided —
  including "considered and declined."

---

## F. Why this exists

Two failures, both mechanical, neither a reasoning error:

- A handoff composed from conversation rather than from the page caused a session to
  open on false premises and produced three incorrect corrections (2026-08-26).
- A handoff uploaded from a prior commit desynced from a prereg that had moved past
  it (2026-08-28), so pending work appeared undone and completed work appeared
  pending.

Both are invisible to a careful reader and instantly visible to `git`. That is the
whole design principle: push every consistency check down to something automatic, and
spend the attention on the research instead.
