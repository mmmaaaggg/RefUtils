from multiprocessing import Pool
import time


def f(x):
    print('x is %d' % x)
    return x * x

if __name__ == '__main__':
    pool = Pool(processes=4)              # start 4 worker processes

    result = pool.apply_async(f, (10,))   # evaluate "f(10)" asynchronously in a single process
    print(result.get(timeout=3))           # prints "100" unless your computer is *very* slow

    print(pool.map(f, list(range(10))))          # prints "[0, 1, 4,..., 81]"

    it = pool.imap(f, list(range(10)))
    print(next(it))                       # prints "0"
    print(next(it))                       # prints "1"
    print(it.next(timeout=1))              # prints "4" unless your computer is *very* slow

    result = pool.apply_async(time.sleep, (10,))
    print(result.get(timeout=1))           # raises multiprocessing.TimeoutError
