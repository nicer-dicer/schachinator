import chess

def start_read(task_queue, coords):
    task_queue.put(coords + [False, 'W'])

if __name__ == "__main__":
    task_queue = []
    start_read(task_queue)
