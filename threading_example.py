import threading
import queue


# https://docs.python.org/3/library/threading.html
def worker(outbox, inbox):
    while True:
        try:  # Remove and return an item from the queue.
            item = outbox.get_nowait()
        # if a thread finds the queue empty, the function returns and the
        # thread exits
        except queue.Empty:
            return

        task_result = do_something(item)

        # after putting the results in the inbox, the worker will go get another
        # item from the outbox to do work on
        inbox.put(task_result)
        outbox.task_done()


def do_something(some_item):
    # put your slow script here!
    return some_item + 1


# DRIVER CODE
some_data = [0, 1, 2, 3, 4]
items = len(some_data)

# Constructor for FIFO queues
q = queue.Queue(items)
q_inbox = queue.Queue(items)

print("{} items in the queue...".format(items))

# Put item into the queue.
for num in some_data:
    q.put(num)


# a dict to keep track of our threads for later
workers = 2
threads = {}

print("Starting {} workers...".format(workers))

for i in range(workers):
    # target is the callable object to be invoked by the run() method.
    threads[i] = threading.Thread(target=worker, args=[q, q_inbox])
    # A thread can be flagged as a “daemon thread”. The significance of
    # this flag is that the entire Python program exits when only daemon threads are left.
    # Checkout https://stackoverflow.com/questions/190010/daemon-threads-explanation
    # to determine if you want daemon threads enabled(probably NO)
    threads[i].daemon = False

    # Start the thread’s activity.
    threads[i].start()

# .join() Blocks until all items in the queue have been gotten and processed.
# The count of unfinished tasks goes up whenever an item is added to the queue.
# The count goes down whenever a consumer thread calls task_done() to indicate
# that the item was retrieved and all work on it is complete.
q.join()

# Wait until the thread terminates. This example does not need it, but this will
# ensure all your threads terminate, or help you find bugs
for val in threads.values():
    val.join()

# extract results of our multithreading app
for result in list(q_inbox.queue):
    print(result)

print("done.")
