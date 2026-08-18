# Day 1 — 2026-08-18

**Stage:** 1 of 5 — Python as software engineering
**Sequence:** Python-as-engineering → CLI/Git fluency → Spark internals → cloud basics → LLM engineering

## Mental model (read once, then go)

Analytical Python (pandas, notebooks) forgives you — cells run in any order, state is implicit, mistakes are visible immediately in output. Software-engineering Python doesn't forgive you — a script runs top to bottom in a fresh process, so structure, error handling, and function boundaries are the only thing between you and a crash. You already have the analytical instincts. Today's gap is authoring discipline: writing a script from a blank file that a stranger (or you, in six months) can run and understand without asking you anything.

The specific trap you missed in assessment — mutable default arguments — is today's anchor:

```python
def add_ticket(ticket_id, queue=[]):
    queue.append(ticket_id)
    return queue
```

That default `[]` is created **once**, at function definition time, not on every call. Every call that doesn't pass its own `queue` shares the *same* list. Don't take my word for it — prove it to yourself in the assignment.

## Assignment (30-45 min)

1. From a **blank file** (`ticket_queue.py`), write a function `add_ticket(ticket_id, queue=None)` that adds a ticket ID to a queue and returns it. Don't just fix the trap — first write it *with* the mutable-default bug, call it 3 times with no `queue` argument, and print the result after each call. Watch it accumulate across calls that should've been independent.
2. Now fix it properly (the idiomatic pattern, not a workaround) and rerun the same 3 calls to confirm each one now starts clean.
3. Add basic error handling: if `ticket_id` is not a string or int, raise a `TypeError` with a clear message. Write one call that triggers it and confirm the message is useful.
4. Explain-it-back: in your own words (written, no lookup), answer — *why does the buggy version share state across calls, and why does `None` as a default avoid it?* Keep it to 2-3 sentences. I'll check this against what you actually wrote, not just whether the code works.

## Git/GitHub step (today's habit-building)

If you don't already have a repo for this: create one on GitHub named **`study-log`** (public or private, your call), clone it locally. If `study-log` already exists, tell me next run and I'll stop assuming.

- `git init` (if not already a repo) → add `ticket_queue.py`
- Write a real commit message — not "update" or "wip". Something like: `fix mutable default argument bug in add_ticket`
- `git add ticket_queue.py && git commit -m "<your message>"`
- `git push` to `study-log` on `main`

Tomorrow's quiz will include: what the bug was, why `None` fixes it, and what your commit message said — from memory, not from re-reading the file.

---
*No quiz today — day 1. Tomorrow opens with one on this material.*
