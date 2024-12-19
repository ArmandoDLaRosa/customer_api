class ListCustomersQuery:
    def __init__(self, uow_factory):
        self.uow_factory = uow_factory

    def execute(self, offset=0, limit=10):
        with self.uow_factory as uow:
            return uow.customer_repository.list_customers(offset=offset, limit=limit)