# Day 2 — 2026-08-18

**Stage:** 1 of 5 — Python as software engineering
**Sequence:** Python-as-engineering → CLI/Git fluency → Spark internals → cloud basics → LLM engineering

## Quiz on Day 1 (answer from memory first, then check yourself against `ticket_queue.py`)

1. In your own words: why did the buggy `add_ticket(ticket_id, queue=[])` share state across calls that never passed `queue`?
2. Why does `queue=None` + `if queue is None: queue = []` fix it, instead of just being a stylistic preference?
3. Your Day 1 script ends with `print(add_ticket([]))` — a list is neither `str` nor `int`, so your own `TypeError` check fires on it. That line isn't wrapped in `try/except`, so running the script as-is crashes on the last line with an unhandled traceback. Did you notice that when you ran it? What would you need to add to make that call fail gracefully instead of crashing the whole script?
4. What was your Day 1 commit message? (From memory — not from re-reading the file.)

## Mental model (read once, then go)

Day 1 gave you a function that can *detect* a bad input and raise. Detecting isn't the same as handling. A real script needs a boundary — usually near where the program actually runs (a `main()`, a CLI entry point, an API handler) — where exceptions from deeper functions get caught, logged or reported clearly, and dealt with, instead of leaking out as a raw traceback the caller has to decode. Today's gap: you can raise, but you haven't yet practiced deciding *where* to catch, and how much information to surface when you do.

## Assignment (45-60 min)

1. Start a new file `ticket_queue_v2.py` and copy in your corrected `add_ticket` from Day 1 (the `None`-default version).
2. Write a second function `process_tickets(ticket_ids, queue=None)` that loops over a list of `ticket_ids` and calls `add_ticket` on each one, catching `TypeError` per item instead of letting one bad item kill the whole batch. For each failure, keep a running list of `(ticket_id, error_message)` and continue processing the rest. Return `(queue, failures)`.
3. Call `process_tickets([1, "abc", 2.5, "TCK-99", []])` and print both the resulting queue and the failures list. Confirm: 2.5 and `[]` should land in failures, the rest should land in the queue.
4. Add one custom exception: `class TicketQueueFull(Exception)`. Give `add_ticket` an optional `max_size` parameter (default `None`, meaning unlimited); if provided and the queue is already at `max_size` before appending, raise `TicketQueueFull` with a message stating the limit. Write one call that triggers it.
5. Explain-it-back (2-3 sentences, written, no lookup): what's the difference between the `TypeError` you raise for a bad input type and the `TicketQueueFull` you just added — i.e. why would a caller want to catch these differently?

## Git/GitHub step

- `git checkout -b study_2026-08-18` if you haven't already (you appear to have created this branch already — reuse it).
- Add `ticket_queue_v2.py` inside a new `2026-08-18/` folder.
- Write a real commit message describing what changed, e.g. `add batch processing with per-item error handling and TicketQueueFull`.
- `git add 2026-08-18/ticket_queue_v2.py && git commit -m "<your message>"`
- `git push origin study_2026-08-18`

Tomorrow's quiz will include: the difference between the two exception types, what `process_tickets` returned for the bad inputs, and your commit message — from memory.
