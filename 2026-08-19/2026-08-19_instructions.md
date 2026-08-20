# Day 3 — 2026-08-19 (regenerated — ABOUTME.md goals updated same day, use this version, disregard any earlier Day 3 you may have seen)

**Stage:** 1 of 5 — Python scripting confidence (hands-on track)
**Sequence:** Python scripting → CLI/Git → Spark internals → cloud fundamentals → K8s/containers → CI/CD → building with LLM APIs. (Conceptual AI track — tokens, context, RAG, agents, MCP — runs in parallel, no prerequisites; that starts separately, not folded into today.)

Note on the goals update: the target isn't "become a software engineer" — it's a script that works, that you wrote, that you understand, so you can automate your own work without waiting on someone else. That's why today is still logging/exceptions/entrypoint hygiene and not classes or type hints — those stay low priority. This is about making `ticket_queue_v2.py` into something you'd trust to run unattended against real tickets, not about architecture.

## Quiz on Day 2 (answer from memory first, then check yourself against `ticket_queue_v2.py`)

1. In your own words: what is actually happening at the `try/except TypeError` boundary inside `process_tickets` that lets one bad ticket (`2.5`, `[]`) get logged as a failure instead of crashing the whole batch?
2. You gave `add_ticket` a `max_size` parameter and raise `TicketQueueFull` when it's hit. Where in your actual support work have you seen a system need to say "no more room, back off" rather than just rejecting bad input outright? Name a real one.
3. Your Day 2 explain-it-back said `TypeError` is discard, `TicketQueueFull` is retry. Say it again from memory, more precisely this time: what specifically about each exception tells the caller which response is correct?
4. What was your Day 2 commit message? (From memory — not from re-reading the file.)

## Mental model (read once, then go)

`print()` is fine for a script you run once and read the output of yourself. It stops being fine the moment the script is something you'd trust to run unattended, or hand to a teammate, or point at real tickets — you need to be able to turn the noise up or down without editing code, and you need a record of what happened after the terminal's scrolled away. That's what `logging` gives you over `print`: levels (`INFO`, `WARNING`, `ERROR`) a caller can filter, and output that can go to a file instead of just stdout.

Second gap: right now `TicketQueueFull`'s message is a string a caller would have to parse to get the limit back out. An exception can carry real data — store `max_size` as an attribute on the exception object itself, so calling code can do `except TicketQueueFull as e: e.max_size` instead of regex-ing a sentence. Small thing, but it's the difference between an exception that just complains and one that hands the caller something to act on — which matters a lot when "the caller" is a support automation script deciding whether to retry.

Third: your Day 2 file runs its example calls at module level — the moment someone does `import ticket_queue_v2`, all of that fires. `if __name__ == "__main__":` is the guard that says "only run this when the file is executed directly." Wrap today's version in a `main()` function and this guard so tomorrow, when you want to reuse `add_ticket` from a different script, importing it doesn't spam your terminal.

## Assignment (45-60 min)

1. Copy `ticket_queue_v2.py` to a new file `ticket_queue_v3.py`.
2. `import logging` and add one `logging.basicConfig(level=logging.INFO)` call. Inside `process_tickets`, replace the two `print(success)` / `print(failures)` calls with `logging.info(...)` for the successful queue and `logging.warning(...)` for each failure (log each failed `(ticket_id, error_message)` as its own warning, not one dump).
3. Rewrite `TicketQueueFull` to actually store `max_size`: give it an `__init__(self, message, max_size)` that calls `super().__init__(message)` then sets `self.max_size = max_size`. Update the `raise TicketQueueFull(...)` call to pass both. Write one line that catches it and prints `e.max_size` directly — not the message string.
4. Move all your top-level script calls (the `add_ticket`/`process_tickets` example calls currently running at import time) inside a `def main():` function, then add `if __name__ == "__main__": main()` at the bottom. Run the file directly to confirm it still works.
5. Explain-it-back (2-3 sentences, no lookup): why does storing `max_size` as a real attribute on `TicketQueueFull` matter more once you imagine this exception being caught by code you didn't write yourself — say, a support automation script deciding whether to retry?

## Git/GitHub step

- `git checkout -b 2026-08-19`
- Add `ticket_queue_v3.py` inside a new `2026-08-19/` folder.
- Write a real commit message describing what changed, e.g. `add logging, structured TicketQueueFull, and main() entrypoint guard`.
- `git add 2026-08-19/ticket_queue_v3.py && git commit -m "<your message>"`
- `git push origin 2026-08-19`
- Open a PR against `main`, same as Day 1 and Day 2.

Tomorrow's quiz will include: what `logging.INFO` vs `logging.WARNING` bought you, how you access `e.max_size` on a caught exception, why the `main()` guard matters, and your commit message — from memory.
