import threading
import time

var = 0

def add():
    global var
    var = var + 1

def minus():
    global var
    var = var - 1

def main():
    thread_list = []
    start = time.time()
    for i in range(5000000):
        add()
        minus()
    end = time.time()
    print("Running Time with for loop: %.5f s" % (end - start))
    print(var)

    start = time.time()
    for i in range(5000000):
        thd = threading.Thread(target=add)
        thread_list.append(thd)
        thd.start()
        thd = threading.Thread(target=minus)
        thread_list.append(thd)
        thd.start()

    # for thread in thread_list:
    #     thread.start()
    for thread in thread_list:
        thread.join()

    end = time.time()
    print("Running Time with threading: %.5f s" % (end - start))
    print(var)

if __name__ == '__main__':
    main()
