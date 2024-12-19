from domain.exceptions import CustomerNotFoundException
from datetime import datetime
from domain.events import CustomerUpdatedEvent

class UpdateCustomerCommand:
    def __init__(self, uow_factory, event_publisher):
        self.uow_factory = uow_factory
        self.event_publisher = event_publisher

    def execute(self, customer_id, first_name, last_name, email):
        try:
            with self.uow_factory as uow:
                customer = uow.customer_repository.get_by_id(customer_id)
                if not customer or customer.is_deleted:
                    raise CustomerNotFoundException("Customer not found or deleted.")
                
                customer.first_name = first_name
                customer.last_name = last_name
                customer.email = email
                uow.customer_repository.update(customer)

                event = CustomerUpdatedEvent(
                    event_type="CustomerUpdated",
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