from typing import Optional

from domain.exceptions import EmailAlreadyExistsException
from domain.models.customer import Customer
from sqlalchemy.exc import IntegrityError

class CustomerRepositoryImpl:
    def __init__(self, session):
        self.session = session
        
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.session.query(Customer).filter(Customer.id == customer_id, Customer.is_deleted == False).first()

    def list_customers(self, offset=0, limit=10):
        return self.session.query(Customer)\
                    .filter(Customer.is_deleted == False)\
                    .offset(offset)\
                    .limit(limit)\
                    .all()
                  
    def add(self, customer):
        try:
            self.session.add(customer)
            self.session.flush()
            return customer
        except IntegrityError as e:
            if "Duplicate entry" in str(e.orig):
                raise EmailAlreadyExistsException("The email address already exists.") from e
            raise e
        
    def update(self, customer: Customer):
        self.session.merge(customer)
        self.session.flush()
        return customer

    def soft_delete(self, customer_id: int):
        c = self.session.query(Customer).filter(Customer.id == customer_id, Customer.is_deleted == False).first()
        if c:
            c.is_deleted = True
            self.session.flush()
            return c
        return None
