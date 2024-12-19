from dataclasses import dataclass
from datetime import datetime

@dataclass
class BaseEvent:
    event_type: str
    timestamp: datetime

    def to_dict(self):
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
        }

@dataclass
class CustomerCreatedEvent(BaseEvent):
    customer_id: str
    first_name: str
    last_name: str
    email: str

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "data": {
                "customer_id": self.customer_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
            }
        })
        return base_dict

@dataclass
class CustomerUpdatedEvent(BaseEvent):
    customer_id: str
    first_name: str
    last_name: str
    email: str

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "data": {
                "customer_id": self.customer_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
            }
        })
        return base_dict
    
@dataclass
class CustomerDeletedEvent(BaseEvent):
    customer_id: str

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "data": {
                "customer_id": self.customer_id,
            }
        })
        return base_dict