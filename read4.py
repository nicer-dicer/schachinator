import chess

def start_read(task_queue):
    while True:
        x = input("X")
        x = int(x)
        y = input("Y")
        y = int(y)
        coords = [x, y]
        task_queue.put(coords + [False, 'W'])

if __name__ == "__main__":
    task_queue = []
    start_read(task_queue)
