from domain.exceptions import CustomerNotFoundException

class GetCustomerByIdQuery:
    def __init__(self, uow_factory):
        self.uow_factory = uow_factory

    def execute(self, customer_id):
        with self.uow_factory as uow:
            customer = uow.customer_repository.get_by_id(customer_id)
            if not customer:
                raise CustomerNotFoundException("Customer not found")
            return customer
