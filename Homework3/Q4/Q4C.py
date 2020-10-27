import time
import math
from multiprocessing import Pool

def check_prime_of_odd(num):
    if num < 2:
        return 0
    if num == 2 or num == 3:
        return num
    for i in range(3, math.ceil(math.sqrt(num))+1, 2):
        if num % i == 0:
            return 0
    return num

def main():
    start = time.time()
    N = 1000000
    my_pool = Pool()
    result = my_pool.map(check_prime_of_odd, range(3, N+1, 2))
    end = time.time()
    print("Running Time with multiprocessing: %.5f s" % (end - start))
    print(sum(result)+2)

if __name__ == '__main__':
    main()
