from domain.models.customer import Customer
from domain.events import CustomerCreatedEvent
from datetime import datetime


class CreateCustomerCommand:
    def __init__(self, uow_factory, event_publisher):
        self.uow_factory = uow_factory
        self.event_publisher = event_publisher

    def execute(self, customer: Customer) -> str:
        try:
            with self.uow_factory as uow:
                customer = uow.customer_repository.add(customer)
                
                event = CustomerCreatedEvent(
                    event_type="CustomerCreated",
                    timestamp=datetime.utcnow(),
                    customer_id=customer.id,
                    first_name=customer.first_name,
                    last_name=customer.last_name,
                    email=customer.email,
                )

                self.event_publisher.publish(event)

                return customer
        except Exception as e:
            raise e
