from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from random import randint, shuffle
from threading import Condition, Semaphore
from time import sleep


class ExtSemaphore(Semaphore):
    def __init__(self, size: int):
        super(ExtSemaphore, self).__init__(value=size)
        self.__size = size

    def __len__(self) -> int:
        return self.__size


class CenterAdministration:
    def __init__(self, necessary=9):
        self.semaphore = ExtSemaphore(3)
        self.factory_condition = Condition()
        self.workers = []
        self.__necessary = necessary
        self.workers_ready = False

    @property
    def workers_capacity(self) -> int:
        return self.__necessary

    def waiting_workers(self):
        while len(admin.workers) < admin.workers_capacity:
            self.factory_condition.wait()



class Entity:
    def __call__(self, admin: CenterAdministration):
        raise NotImplementedError


class Manager(Entity):
    def __call__(self, admin: CenterAdministration):
        with admin.factory_condition:
            while len(admin.workers) < admin.workers_capacity:
                print("Factory is still suspended for vacation")
                admin.factory_condition.wait(timeout=1)

            print("Factory ready to start production!")


class Worker(Entity):
    def __init__(self, id: int, names_type=["Elf", "Reindeer"]):
        self.__type = names_type[randint(0, len(names_type) - 1)]
        self.__id = id
        self.__time_vacations = randint(1, 10)


    @property
    def id(self) -> int:
        return self.__id

    @property
    def type_worker(self):
        return self.__type

    def __call__(self, admin: CenterAdministration):
        sec = self.__time_vacations

        print(f"Worker[{self.id}] {self.type_worker}: is on vacation for {sec}s")
        sleep(sec)

        print(f"Worker[{self.id}] {self.type_worker}: is ready to work")
        admin.workers.append(self.id)

        with admin.factory_condition:
            if len(admin.workers) < admin.workers_capacity:
                print(f"Ready workers: {len(admin.workers)}, {admin.workers}")
                admin.factory_condition.wait()

            admin.factory_condition.notify_all()


if __name__ == "__main__":
    admin = CenterAdministration(16)
    entities = []

    [entities.append(Worker(i)) for i in range(admin.workers_capacity)]
    entities.append(Manager())

    shuffle(entities)

    print(f"Number of workers needed to open the factory: {admin.workers_capacity}")
    with PoolExecutor(max_workers=len(entities)) as pool:
        [pool.submit(entity, admin) for entity in entities]
