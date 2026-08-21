# 1. What did switching process_tickets's summary line from print to logging.info / a failure to logging.warning actually buy you, concretely — not "better practice," what can you do now that you couldn't before?
    # - You can now suppress or surface messages by severity without editing the code that generates them — flip one level= value and INFO-level noise disappears while WARNING/ERROR still show, or route different severities to different destinations (console vs. file vs. Slack).
# 2. You made TicketQueueFull store max_size as a real attribute. Write the exact line of code you'd use to catch it and pull that number back out.
    # - except TicketQueueFull as e: print(e.max_size)
# 3. main() plus if __name__ == "__main__": — if a teammate wrote import ticket_queue_v3 from another script, what would happen with this guard versus without it? Be specific about what runs and what doesn't.
    # - when running ticket_queue_v3 directly, it will be set to "__main__" and main() will execute. If running import ticket_queue_v3 from another script, __name__ will be set to that other script's name and main() will not execute.
# 4. What was your Day 3 commit message? (From memory.)
    # - "2026-08-19 ticket_queue_v3"
# 5. Open your own ticket_queue_v3.py and trace it by hand, don't run it yet: inside process_tickets, look at the exact call to add_ticket. Does it ever pass max_size? Walk through what that means for whether TicketQueueFull can ever actually fire during a batch run through process_tickets — as opposed to the direct add_ticket() calls in main().
    # - didn't have time to complete this question.

# logging is like print(), but messages carry a severity level (DEBUG < INFO < WARNING < ERROR < CRITICAL).
# level=INFO is a threshold: it shows INFO and anything more severe, and silently drops
# anything below it (here, just DEBUG). Raising the threshold (e.g. to WARNING) suppresses
# lower levels without touching the logging.info(...)/logging.warning(...) calls themselves.
# Where messages that pass the threshold actually go (console, file, Slack, etc.) is a
# separate concern, controlled by handlers - not by this level setting.
import logging
logging.basicConfig(level=logging.INFO)


# Custom exception raised when a queue has hit its max_size.
# Subclasses Exception and overrides __init__ to accept max_size in addition to the
# usual message. super().__init__(message) hands the message to Exception's own
# __init__, so str(e)/printing the exception still works normally. self.max_size then
# stores the limit as a real attribute on the instance, so a caller that does
# `except TicketQueueFull as e:` can read e.max_size directly - no need to parse it
# back out of the message string.
class TicketQueueFull(Exception):
    def __init__(self, message, max_size):
        super().__init__(message)
        self.max_size = max_size


# Adds a single ticket_id to a queue (list), creating a new list if none is given.
# Validates the ticket type and enforces max_size before appending.
# Returns the queue so calls can be chained/printed directly.
def add_ticket(ticket_id: int, queue=None, max_size=None) -> list:
    # Only str or int ticket_ids are allowed - anything else (list, float, etc.) is rejected.
    if not isinstance(ticket_id, (str,int)):
        raise TypeError("Argument must be either str or int.")

    # No queue passed in -> start a fresh empty one.
    # Note: because this creates a NEW list each call, passing max_size without
    # also passing a shared queue means the size check always starts from 0.
    if queue is None:
        queue = []

    # Reject the ticket if the queue is already at (or over) capacity.
    if max_size is not None and len(queue) >= max_size:
        raise TicketQueueFull(f"Queue is full (max {max_size}).", max_size)

    queue.append(ticket_id)

    return queue

# Adds a batch of ticket_ids one at a time, sorting them into "success" and "failures" lists.
def process_tickets(ticket_ids: list, success=None, failures=None, max_size=None):
    if success is None:
        success = []

    if failures is None:
        failures = []

    for ticket_id in ticket_ids:
        try:
            add_ticket(ticket_id, queue=success, max_size=max_size)
        except TypeError as e:
            # Invalid ticket type - record it as a (ticket_id, error message) pair instead of raising.
            failures.append((ticket_id, f"{e}"))
            logging.warning("Ticket %s failed: %s", ticket_id, e)
        except TicketQueueFull as e:
            logging.error("Ticket %s failed: queue full (max_size=%s)", ticket_id, e.max_size)
            break

    logging.info("done: %s shipped, %s failed", len(success), len(failures))

    return success, failures

# Demo entry point: exercises add_ticket's error handling, then process_tickets' batch handling.
def main():
    try:
        # Each of these calls omits `queue`, so every call starts a brand-new empty list -
        # max_size is compared against that call's own list (size 0), not a running total.
        print(f"\n{'Results of Individual Ticket Add':-^50}")
        print(add_ticket(1, max_size=2))
        print(add_ticket(2, max_size=1))
        print(add_ticket(3, max_size=0))
        print(add_ticket([]))  # list is not str/int -> raises TypeError, stops the try block here
    except TypeError as e:
        print(f"Skipped invalid ticket: {e}")
    except TicketQueueFull as e:
        print(f"Ticket queue greater than max size. Passed size is {e.max_size}.")
        # print(e) # this will print TicketQueueFull exception in add_ticket
    # Mixed batch: valid (1, "abc", "TCK-99") vs invalid (2.5, []) ticket types.
    print(f"\n{'Results of Batch Ticket Add':-^50}")
    print(process_tickets([1, "abc", 2.5, "TCK-99", [], "CS-123", {}], max_size=3))

# ---------Results of Individual Ticket Add---------
# [1]
# [2]
# Queue is full (max 0).

# -----------Results of Batch Ticket Add------------
# WARNING:root:Ticket 2.5 failed: Argument must be either str or int.
# WARNING:root:Ticket [] failed: Argument must be either str or int.
# ERROR:root:Ticket CS-123 failed: queue full (max_size=3)
# INFO:root:done: 3 shipped, 2 failed
# ([1, 'abc', 'TCK-99'], [(2.5, 'Argument must be either str or int.'), ([], 'Argument must be either str or int.')])
# thomastam@Thomass-MacBook-Pro 2026-08-20 % 


# __name__ is a special variable Python sets automatically:
# - if this file is run directly (e.g. `python ticket_queue_v3.py`), __name__ is "__main__"
# - if this file is imported by another file instead, __name__ is the module's name ("ticket_queue_v3")
# So this line means: only call main() when the file is run directly, not when it's imported.
if __name__ == "__main__":
    main()