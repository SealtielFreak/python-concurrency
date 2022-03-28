from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from random import randint, shuffle
from threading import Condition, Semaphore
from time import sleep


class Bridge:
    def __init__(self, vias=1):
        self.order_list = Condition()
        self.semaphore = Semaphore(vias)
        self.cars_waiting = Semaphore(2)
        self.n_car = 0
        self.direction = ["left", "right"]


class Car:
    def __init__(self, id: int, direction: str):
        self.__id = id
        self.__direction = direction
        self.__time_arrival = randint(3, 15)
        self.__time_cross = randint(5, 7)

    def __call__(self, bridge: Bridge):
        with bridge.cars_waiting:
            sleep(self.__time_arrival)

        with bridge.order_list:
            while not bridge.n_car == self.__id:
                bridge.order_list.wait(0)

            bridge.n_car += 1
            print(f"Car[{self.__id}] arrived from {self.__direction}")
            bridge.order_list.notify_all()

        with bridge.semaphore:
            print(f"Car[{self.__id}] car entered the bridge")
            sleep(self.__time_cross)
            print(f"Car[{self.__id}] cross the bridge, in {self.__time_cross}s")


if __name__ == '__main__':
    cars = []
    bridge = Bridge()

    for i in range(8):
        direction = bridge.direction[randint(0, len(bridge.direction) - 1)]
        cars.append(Car(i, direction))

    shuffle(cars)

    with PoolExecutor(max_workers=len(cars)) as pool:
        [pool.submit(car, bridge) for car in cars]
