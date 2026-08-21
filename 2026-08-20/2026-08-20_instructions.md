# Day 4 — 2026-08-20

**Stage:** 1 of 5 — Python scripting confidence (hands-on track)
**Sequence:** Python scripting → CLI/Git → Spark internals → cloud fundamentals → K8s/containers → CI/CD → building with LLM APIs. (Conceptual AI track runs in parallel, no prerequisites — not folded into today.)

## Quiz on Day 3 (answer from memory first, then check yourself against `ticket_queue_v3.py`)

1. What did switching `process_tickets`'s summary line from `print` to `logging.info` / a failure to `logging.warning` actually buy you, concretely — not "better practice," what can you *do* now that you couldn't before?
2. You made `TicketQueueFull` store `max_size` as a real attribute. Write the exact line of code you'd use to catch it and pull that number back out.
3. `main()` plus `if __name__ == "__main__":` — if a teammate wrote `import ticket_queue_v3` from another script, what would happen with this guard versus without it? Be specific about what runs and what doesn't.
4. What was your Day 3 commit message? (From memory.)
5. Open your own `ticket_queue_v3.py` and trace it by hand, don't run it yet: inside `process_tickets`, look at the exact call to `add_ticket`. Does it ever pass `max_size`? Walk through what that means for whether `TicketQueueFull` can ever actually fire during a batch run through `process_tickets` — as opposed to the direct `add_ticket()` calls in `main()`.

Question 5 isn't a trick — trace it before you read further. It's where today's work starts.

## Mental model (read once, then go)

You've now got two exception types living in the same territory — `TypeError` for a bad individual ticket, `TicketQueueFull` for a queue that's out of room. Day 2's explain-it-back called this discard-vs-retry, and that's right, but today's the day you actually have to *build* the fork instead of just naming it.

They're not the same kind of failure. A bad `ticket_id` is a per-item problem — one ticket is malformed, the other 99 in the batch are fine, so you log it, discard it, and keep going. A full queue is not a per-item problem — it's a statement about the whole batch's capacity. If ticket #4 out of 20 hits `TicketQueueFull`, tickets #5 through #20 aren't going to fare any better against the same limit. Catching it the same way you catch `TypeError` — log and continue looping — means you'll just raise the same exception 16 more times for no reason. The correct response to a per-item failure is "skip and continue." The correct response to a capacity failure is "stop the batch and report how far you got."

That distinction — which exceptions let the loop continue and which ones should stop it — is a real production judgment call, and it's exactly the kind of thing a support automation script needs to get right: you don't want it silently discarding tickets it should have backed off on, and you don't want a full queue to look identical in the logs to one bad ticket ID.

## Assignment (45-60 min)

1. Copy `ticket_queue_v3.py` to a new file `ticket_queue_v4.py`.
2. Give `process_tickets` a `max_size=None` parameter, and pass it through to the `add_ticket` call inside the loop (this closes the gap from quiz question 5 — right now `max_size` never reaches `add_ticket` during a batch run).
3. Add a second `except TicketQueueFull as e:` clause to the loop's try/except (alongside the existing `TypeError` one). On `TicketQueueFull`: log it with `logging.error(...)` including `e.max_size`, then **stop the loop** — don't just discard-and-continue like you do for `TypeError`. Have `process_tickets` still return `(success, failures)` reflecting how far it actually got.
4. In `main()`, call `process_tickets` with a longer ticket list (6-8 items, mix of valid and invalid) and a small `max_size` (e.g. `3`) so `TicketQueueFull` actually fires partway through the batch. Confirm: does the loop stop where you expect, and do the logs make it obvious *why* it stopped versus just showing another failure?
5. Explain-it-back (2-3 sentences, no lookup): why would "log and continue" be the wrong response to `TicketQueueFull` inside `process_tickets`, even though it's the right response to `TypeError` in the exact same loop?

## Git/GitHub step

- `git checkout -b 2026-08-20`
- Add `ticket_queue_v4.py` inside a new `2026-08-20/` folder.
- Write a real commit message describing what changed, e.g. `wire max_size through process_tickets and stop the batch on TicketQueueFull`.
- `git add 2026-08-20/ticket_queue_v4.py && git commit -m "<your message>"`
- `git push origin 2026-08-20`
- Open a PR against `main`, same as Days 1-3.

Tomorrow's quiz will include: why `TicketQueueFull` stops the loop but `TypeError` doesn't, what your `max_size=3` test actually printed/logged, and your commit message — from memory.
