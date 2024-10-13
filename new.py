from threading import Semaphore, Thread
import time

sem = Semaphore(2)

def task(name):
    sem.acquire()
    print(f"{name} is running")
    time.sleep(2)
    print(f"{name} is done")
    sem.release()

threads = []
for i in range(4):
    t = Thread(target=task, args=(f"Task {i+1}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
