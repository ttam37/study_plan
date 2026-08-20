import logging
logging.basicConfig(level=logging.INFO)

class TicketQueueFull(Exception):
    def __init__(self, message, max_size):
        super().__init__(message)   
        self.max_size = max_size


def add_ticket(ticket_id: int, queue=None, max_size=None) -> list:
    if not isinstance(ticket_id, (str,int)):
        raise TypeError("Argument must be either str or int.")

    if queue is None:
        queue = []

    if max_size is not None and len(queue) >= max_size:
        raise TicketQueueFull(f"Queue is full (max {max_size}).", max_size)

    queue.append(ticket_id)

    return queue

def process_tickets(ticket_ids: list, success=None, failures=None, max_size=None):
    if success is None:
        success = []

    if failures is None:
        failures = []

    for ticket_id in ticket_ids:
        try:
            add_ticket(ticket_id, queue=success)
        except TypeError as e:
            failures.append((ticket_id, f"{e}"))
            logging.warning("Ticket %s failed: %s", ticket_id, e)
    
    logging.info("done: %s shipped, %s failed", len(success), len(failures))

    return success, failures

def main():
    try:
        print(add_ticket(1, max_size=2))
        print(add_ticket(2, max_size=1))
        print(add_ticket(3, max_size=0))
        print(add_ticket([]))
    except TypeError as e:
        print(f"Skipped invalid ticket: {e}")
    except TicketQueueFull as e:
        print(f"Ticket queue greater than max size. Passed size is {e.max_size}.")

    print("-"*50)

    print(process_tickets([1, "abc", 2.5, "TCK-99", []]))

if __name__ == "__main__":
    main()