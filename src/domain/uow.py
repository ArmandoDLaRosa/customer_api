from abc import ABC, abstractmethod

class UnitOfWork(ABC):
    customers = None

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @abstractmethod
    def commit(self):
        pass
