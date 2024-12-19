from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
import uuid
import re
from domain.exceptions import EmailNotUniqueException

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    def validate_email(self):
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(email_regex, self.email):
            raise ValueError(f"Invalid email format: {self.email}")

    def to_dict(self):
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_deleted": self.is_deleted,
        }
