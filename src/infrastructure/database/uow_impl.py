class UnitOfWorkImpl:
    def __init__(self, session_factory, customer_repository_class):
        self.session = session_factory()
        self.customer_repository = customer_repository_class(session=self.session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type:
                self.rollback()
            else:
                self.commit()
        except Exception as e:
            self.rollback()
            raise e
        finally:
            self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
