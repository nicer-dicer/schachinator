
target_field = [0,0]

   

def read_loop(task_queue):
    for i in range(10):
        #move 1 field diagonal
        task_queue.put(target_field)
        print(target_field)
        target_field[0] += 1
        target_field[1] += 1