# Quiz on Day 1 (answer from memory first, then check yourself against ticket_queue.py)

# In your own words: why did the buggy add_ticket(ticket_id, queue=[]) share state across calls that never passed queue?
# The queue list is only instantiated once in the function. Calling the function consecutive times will append ticket_id to queue.
# Additionally, I learned that queue is locally scoped to the function and is not a global variable. When doing print(queue), it won't work.


# Why does queue=None + if queue is None: queue = [] fix it, instead of just being a stylistic preference?
# Using "if queue is None, queue = []" will create a new list if queue is None. This will allow each ticket_id to be in it's own list.


# Your Day 1 script ends with print(add_ticket([])) — a list is neither str nor int, so your own TypeError check fires on it. That line isn't wrapped in try/except, so running the script as-is crashes on the last line with an unhandled traceback. Did you notice that when you ran it? What would you need to add to make that call fail gracefully instead of crashing the whole script?
# Is the answer to do:
# def add_ticket(ticket_id: int, queue=None) -> list:
#     if not isinstance(ticket_id, (str,int)):
#         raise TypeError("Argument must be either str or int.")

#     if queue is None:
#         queue = []

#     queue.append(ticket_id)

#     return queue

# try:
#     print(add_ticket([]))
# except TypeError as e:
#     print(f"Skipped invalid ticket: {e}")

# What was your Day 1 commit message? (From memory — not from re-reading the file.)
# I think I just added the date as the commit message.

class TicketQueueFull(Exception):
    pass


def add_ticket(ticket_id: int, queue=None, max_size=None) -> list:
    if not isinstance(ticket_id, (str,int)):
        raise TypeError("Argument must be either str or int.")

    if queue is None:
        queue = []

    if max_size is not None and len(queue) >= max_size:
        raise TicketQueueFull(f"Queue is full (max {max_size}).")

    queue.append(ticket_id)

    return queue

try:
    print(add_ticket(1, max_size=2))
    print(add_ticket(2, max_size=1))
    print(add_ticket(3, max_size=0))
    print(add_ticket([]))
except TypeError as e:
    print(f"Skipped invalid ticket: {e}")
except TicketQueueFull as e:
    print("Ticket queue greater than max size.")


def process_tickets(ticket_ids: list, success=None, failures=None):
    if success is None:
        success = []

    if failures is None:
        failures = []
        

    for ticket_id in ticket_ids:
        try:
            add_ticket(ticket_id, success)
        except TypeError as e:
            failures.append((ticket_id, f"{e}"))
    
    print(success)
    print(failures)

    return success, failures

print(process_tickets([1, "abc", 2.5, "TCK-99", []]))

# 5. Explain-it-back (2-3 sentences, written, no lookup): what's the difference between the TypeError you raise for a bad input type and the TicketQueueFull you just added — i.e. why would a caller want to catch these differently?
# TypeError signals a permanently bad input — the ticket itself is the wrong type and retrying won't help, so a caller should just discard it. TicketQueueFull signals a temporary state problem — the ticket is valid, but the queue has no room right now, so a caller might want to retry later instead of throwing the ticket away. Catching them separately lets a caller respond correctly to each: discard vs. retry.