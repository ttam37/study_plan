# logging is like print(), but messages have a severity level (INFO, WARNING, etc.)
# level=INFO means: show INFO messages and anything more severe, hide anything less severe.
import logging
logging.basicConfig(level=logging.INFO)


# Custom exception raised when a queue has hit its max_size.
# Carries max_size as an attribute so callers can inspect the limit that was hit.
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
# Only catches TypeError (invalid ticket type) - a TicketQueueFull would not be caught here.
def process_tickets(ticket_ids: list, success=None, failures=None, max_size=None):
    if success is None:
        success = []

    if failures is None:
        failures = []

    for ticket_id in ticket_ids:
        try:
            add_ticket(ticket_id, queue=success)
        except TypeError as e:
            # Invalid ticket type - record it as a (ticket_id, error message) pair instead of raising.
            failures.append((ticket_id, f"{e}"))
            logging.warning("Ticket %s failed: %s", ticket_id, e)

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
        # print(f"Ticket queue greater than max size. Passed size is {e.max_size}.")
        print(e) # this will print TicketQueueFull exception in add_ticket
    # Mixed batch: valid (1, "abc", "TCK-99") vs invalid (2.5, []) ticket types.
    print(f"\n{'Results of Batch Ticket Add':-^50}")
    print(process_tickets([1, "abc", 2.5, "TCK-99", []]))

# __name__ is a special variable Python sets automatically:
# - if this file is run directly (e.g. `python ticket_queue_v3.py`), __name__ is "__main__"
# - if this file is imported by another file instead, __name__ is the module's name ("ticket_queue_v3")
# So this line means: only call main() when the file is run directly, not when it's imported.
if __name__ == "__main__":
    main()