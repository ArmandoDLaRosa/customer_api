# src/application/commands/delete_customer.py

from domain.exceptions import CustomerNotFoundException
from domain.events import CustomerDeletedEvent
from datetime import datetime

class DeleteCustomerCommand:
    def __init__(self, uow_factory, event_publisher):
        self.uow_factory = uow_factory
        self.event_publisher = event_publisher

    def execute(self, customer_id):
        try:
            with self.uow_factory as uow:
                customer = uow.customer_repository.get_by_id(customer_id)
                if not customer:
                    raise CustomerNotFoundException("Customer not found")

                uow.customer_repository.soft_delete(customer_id)

                event = CustomerDeletedEvent(
                    event_type="CustomerDeleted",
                    timestamp=datetime.utcnow(),
                    customer_id=customer.id,
                )
                self.event_publisher.publish(event)
        except Exception as e:
            raise e
