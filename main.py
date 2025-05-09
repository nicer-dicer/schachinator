import threading
import queue
import worker
import read

def main():
    task_queue = queue.Queue()

    worker_thread = threading.Thread(target=worker.worker_task, args=(task_queue,))
    read_thread = threading.Thread(target=read.read_loop, args=(task_queue,))

    worker_thread.start()
    read_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Main: KeyboardInterrupt received. Stopping threads...")

        task_queue.put("STOP")
        worker_thread.join(timeout=5)

        print("Main: Worker thread stopped. Exiting.")

if __name__ == "__main__":
    main()
