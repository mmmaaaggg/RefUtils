#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/10/25 下午9:19
@File    : joinable_queue_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

# Author: Yaoyu Hu <yyhu_live@outlook.com>

import argparse
import multiprocessing
from queue import Empty
import time


def cprint(msg, flagSilent=False):
    if (not flagSilent):
        print(msg)


def process_single_file(name, jobStr, flagSilent=False):
    """
    name is the name of the process.
    """

    startTime = time.time()

    cprint("%s. " % (jobStr))

    endTime = time.time()

    s = "%s: %ds for processing." % (name, endTime - startTime)

    cprint(s, flagSilent)
    cprint("%s: " % (name), flagSilent)

    return s


def worker(name, q, p, rq, flagSilent=False):
    """
    name: String, the name of this worker process.
    q: A JoinableQueue.
    p: A pipe connection object. Only for receiving.
    """

    cprint("%s: Worker starts." % (name), flagSilent)

    while (True):
        if (p.poll()):
            command = p.recv()

            cprint("%s: %s command received." % (name, command), flagSilent)

            if ("exit" == command):
                break

        try:
            jobStrList = q.get(True, 1)
            # print("{}: {}.".format(name, jobStrList))

            s = process_single_file(name, jobStrList[0], flagSilent)

            rq.put([s], block=True)

            q.task_done()
        except Empty as exp:
            pass

    cprint("%s: Work done." % (name), flagSilent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter the files.")

    parser.add_argument("--jobs", type=int, default=100, help="The number of jobs for testing.")

    parser.add_argument("--np", type=int, default=2, help="The number of processes.")

    args = parser.parse_args()

    assert args.jobs > 0
    assert args.np > 0

    startTime = time.time()

    print("Main: Main process.")

    jobQ = multiprocessing.JoinableQueue()
    resultQ = multiprocessing.Queue()

    processes = []
    pipes = []

    print("Main: Create %d processes." % (args.np))

    for i in range(int(args.np)):
        [conn1, conn2] = multiprocessing.Pipe(False)
        processes.append(multiprocessing.Process(target=worker, args=["P%03d" % (i), jobQ, conn1, resultQ, False]))
        pipes.append(conn2)

    for p in processes:
        p.start()

    print("Main: All processes started.")

    for dj in range(args.jobs):
        jobQ.put([str(dj)])

    print("Main: All jobs submitted.")

    resultList = []
    resultCount = 0

    while (resultCount < args.jobs):
        try:
            print("Main: Get index %d. " % (resultCount))
            r = resultQ.get(block=True, timeout=1)
            resultList.append(r)
            resultCount += 1
        except Empty as exp:
            if (resultCount == args.jobs):
                print("Main: Last element of the result queue is reached.")
                break

    jobQ.join()

    print("Main: Queue joined.")

    for p in pipes:
        p.send("exit")

    print("Main: Exit command sent to all processes.")

    for p in processes:
        p.join()

    print("Main: All processes joined.")

    print("Main: Starts process the result.")

    print(resultList)

    endTime = time.time()

    print("Main: Job done. Total time is %ds." % (endTime - startTime))
