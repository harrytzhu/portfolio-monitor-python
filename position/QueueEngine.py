import queue

q = queue.Queue(maxsize=1)


def put(item):
    if not q.empty():
        q.get()
    q.put(item)


def get():
    return q.get()
