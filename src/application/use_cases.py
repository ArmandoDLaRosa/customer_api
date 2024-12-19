from domain.models.customer import Customer
from application.commands.create_customer import CreateCustomerCommand
from application.commands.update_customer import UpdateCustomerCommand
from application.commands.delete_customer import DeleteCustomerCommand
from application.queries.get_customer_by_id import GetCustomerByIdQuery
from application.queries.list_customers import ListCustomersQuery

class UseCases:
    def __init__(self, uow_factory, event_publisher):
        self.uow_factory = uow_factory
        self.event_publisher = event_publisher

    def create_customer_uc(self, first_name: str, last_name: str, email: str) -> str:
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        command = CreateCustomerCommand(self.uow_factory, self.event_publisher)
        return command.execute(customer)

    def update_customer_uc(self, customer_id: str, first_name: str, last_name: str, email: str) -> str:
        command = UpdateCustomerCommand(self.uow_factory, self.event_publisher)
        return command.execute(customer_id, first_name, last_name, email)

    def delete_customer_uc(self, customer_id: str):
        command = DeleteCustomerCommand(self.uow_factory, self.event_publisher)
        return command.execute(customer_id)

    def get_customer_uc(self, customer_id: str):
        query = GetCustomerByIdQuery(self.uow_factory)
        return query.execute(customer_id)

    def list_customers_uc(self, offset: int = 0, limit: int = 10):
        query = ListCustomersQuery(self.uow_factory)
        return query.execute(offset, limit)
