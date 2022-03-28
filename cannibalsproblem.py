from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from random import randint, shuffle
from threading import Condition, Semaphore
from time import sleep


class Cook:
    def __init__(self, rations_n=3):
        self.rations = Semaphore(rations_n)
        self.waiting = Condition()
        self.__rations_necessary = rations_n
        self.rations_n = rations_n

    @property
    def rations_necessary(self):
        return self.__rations_necessary

    def wake(self):
        with self.waiting:
            print("cook opened the kitchen")

            while self.rations_n < self.rations_necessary:
                sleep(randint(1, 3))
                self.rations_n += 1

                print("Cook finished cooking a portion")

            print("Cook closed the kitchen")
            self.waiting.notify_all()


class Cannibal:
    def __init__(self, id: int):
        self.__id = id

    def __call__(self, cook: Cook):
        with cook.rations:
            with cook.waiting:
                while not cook.rations_n > 0:
                    print("No more food rations")
                    cook.wake()
                    cook.waiting.wait()

            cook.rations_n -= 1
            print(f"Cannibal[{self.__id}] is eating")

            sleep(randint(3, 5))

        print(f"Cannibal[{self.__id}] finished eating")



if __name__ == "__main__":
    cook = Cook(3)
    cannibals = []

    [cannibals.append(Cannibal(i)) for i in range(5)]
    shuffle(cannibals)

    print(f"Maximum portions that the cook can prepare: {cook.rations_necessary}")
    with PoolExecutor() as pool:
        [pool.submit(cannibal, cook) for cannibal in cannibals]
