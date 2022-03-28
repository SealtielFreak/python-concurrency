#!/usr/bin/python

from random import randint, shuffle
from threading import Thread
from time import sleep
from typing import List


def random_sleep(ran=(0, 3)):
    sleep(randint(*ran))


def random_array(x: int, ran=(0, 5)) -> List[int]:
    arr = [randint(*ran) for y in range(x)]

    shuffle(arr)

    return arr


def multiply(name: str, arr: List[int], mult: int) -> List[int]:
    size = len(arr)

    print(f"Thread {name} is started")

    for i in range(size):
        if i % mult == 0:
            print(f"Thread {name} access to index [{i}] = {arr[i]}")
            arr[i] *= mult
        
        random_sleep()

    print(f"Thread {name} is finished, final array: {arr}")

    return arr


if __name__ == '__main__':
    print("Main thread is started")

    arr = random_array(10, (0, 100))

    print(f"Initial arr: {arr}")

    threads = [Thread(target=multiply, args=(f"{n}'", arr, n)) for n in [2, 3]]


    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    print("Main thread is finished")
