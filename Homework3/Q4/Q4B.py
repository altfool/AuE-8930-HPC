import threading

var=0
lock = threading.Lock()
def thread_1():
    for i in range(500000):
        global var
        with lock:
            var = var + 1

def thread_2():
    for i in range(500000):
        global var
        with lock:
            var = var - 1

t1 = threading.Thread(target=thread_1, args=(), name='Thread_1')
t2 = threading.Thread(target=thread_2, args=(), name='Thread_2')

t1.start()
t2.start()
t1.join()
t2.join()
print(var)