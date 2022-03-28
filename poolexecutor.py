#!/usr/bin/python

from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from random import shuffle, randint
from threading import Condition, Lock
from time import sleep


def sleep_random(a, b=None):
    if not b:
        b = a
        a = 0

    sleep(randint(a, b))


class EntityCallable:
    def __init__(self, id: int, lock: Lock, cond: Condition):
        self._id = id
        self._lock = lock
        self._cond = cond

    def __call__(self):
        raise NotImplementedError()


class Master(EntityCallable):
    def __init__(self, lock: Lock, cond: Condition):
        super().__init__(0, lock, cond)
        self.__ready = False

    @property
    def is_ready(self):
        return self.__ready

    def __call__(self):
        with self._cond:
            print("Master is ready!")
            self.__ready = True
            self._cond.notify_all()


class Reader(EntityCallable):
    def __init__(self, id: int, master: Master, lock: Lock, cond: Condition):
        super().__init__(id, lock, cond)
        self._master = master

    def __call__(self):
        with self._cond:
            while not self._master.is_ready:
                self._cond.wait()

            sleep_random(5)
            print(f"Reader[{self._id}] is ready!")
            self._cond.notify_all()


if __name__ == '__main__':
    entities = []
    lock = Lock()
    cond = Condition(lock)
    master = Master(lock, cond)

    entities.append(master)
    [entities.append(Reader(i, master, lock, cond)) for i in range(1, 15)]

    shuffle(entities)

    with PoolExecutor() as pool:
        [pool.submit(entity) for entity in entities]

    print("Pool executor is over!")
