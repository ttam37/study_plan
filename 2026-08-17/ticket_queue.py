# buggy code

# def add_ticket(ticket_id, queue=[]):
#     queue.append(ticket_id)
#     return queue

# print(add_ticket(1))
# print(add_ticket(2))
# print(add_ticket(3))

# correct code
def add_ticket(ticket_id: int, queue=None) -> list:
    if not isinstance(ticket_id, (str,int)):
        raise TypeError("Argument must be either str or int.")

    if queue is None:
        queue = []

    queue.append(ticket_id)

    return queue

try:
    print(add_ticket(1))
    print(add_ticket(2))
    print(add_ticket(3))
    print(add_ticket([]))
    
except TypeError as e:
    print(f"Skipped invalid ticket: {e}")

# The reason for the buggy code is because every subsequent call will skip the queue parameter and reuse the same list.
# Using None makes sense because it's an empty value. I created a condition if queue is None, it will create a new list. However if queue is not None, the function will just append the value to the list.


