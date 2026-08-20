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
            add_ticket(ticket_id, queue=success)
        except TypeError as e:
            failures.append((ticket_id, f"{e}"))
    
    print(success)
    print(failures)

    return success, failures

print(process_tickets([1, "abc", 2.5, "TCK-99", []]))

# 5. Explain-it-back (2-3 sentences, written, no lookup): what's the difference between the TypeError you raise for a bad input type and the TicketQueueFull you just added — i.e. why would a caller want to catch these differently?
# TypeError signals a permanently bad input — the ticket itself is the wrong type and retrying won't help, so a caller should just discard it. TicketQueueFull signals a temporary state problem — the ticket is valid, but the queue has no room right now, so a caller might want to retry later instead of throwing the ticket away. Catching them separately lets a caller respond correctly to each: discard vs. retry.