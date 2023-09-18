import threading
import queue


def create_workers(outbox, inbox):
    # create 25 workers
    for _ in range(25):
        t = threading.Thread(target=worker, args[outbox, inbox])
        t.daemon = True
        t.start()

    print("created 25 workers.")


def worker(outbox, inbox):
    while True:
        item = outbox.get()

        result = do_something(item)

        print("worker input was " + str(item) + ", result put in inbox was "
              + str(result))

        inbox.put(result)
        outbox.task_done()


def do_something(some_item):
    # put your task to do here
    return some_item + 1


# DRIVER CODE
# example just adds 1 to each number in this list
some_data = [0, 1, 2, 3, 4]
items = len(some_data)

q = queue.Queue(items + 1)
q_inbox = queue.Queue(items + 1)

print("doing " + str(items) + " requests...")

for num in some_data:
    q.put(num)

create_workers(q, q_inbox)
q.join()

for result in list(q_inbox.queue):
    # print the results
    print(result)

print("done.")
