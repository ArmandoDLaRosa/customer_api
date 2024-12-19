from abc import ABC, abstractmethod
from typing import List
from domain.models.customer import Customer

class CustomerRepository(ABC):
    @abstractmethod
    def add(self, customer: Customer) -> int:
        pass

    @abstractmethod
    def get_by_id(self, customer_id: int) -> Customer | None:
        pass

    @abstractmethod
    def list_customers(self, offset=0, limit=10) -> List[Customer]:
        pass

    @abstractmethod
    def update(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def soft_delete(self, customer_id: int) -> None:
        pass
