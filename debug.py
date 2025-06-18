import multiprocessing as mp
import worker
import read4 as  read

def coordinates():
    x = input("X")
    x = int(x)
    y = input("Y")
    y = int(y)
    coords = [x, y]
    return coords

def main():
    coordinates = coordinates()
    task_queue = mp.Queue()

    worker_process = mp.Process(target=worker.worker_task, args=(task_queue,))

    read_process = mp.Process(target=read.start_read, args=(task_queue, coordinates,))



    worker_process.start()
    read_process.start()

        

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Main: KeyboardInterrupt received. Stopping threads...")

        # Wait for read_process to finish (e.g., after 10 tasks)
        read_process.join()
        
        # Send termination signal to worker
        task_queue.put(None)
        worker_process.join()
        

        print("Main: Worker process stopped. Exiting.")

if __name__ == "__main__":
    main()
