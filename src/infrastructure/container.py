from application.use_cases import UseCases
from dependency_injector import containers, providers
from infrastructure.config import settings
from infrastructure.database.db import create_engine_session_factory
from infrastructure.database.repository_impl import CustomerRepositoryImpl
from infrastructure.database.uow_impl import UnitOfWorkImpl
from infrastructure.events.event_publisher import EventPublisher


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["interfaces.http.v1.routes.customers"]
    )

    config = providers.Configuration()
    config.from_dict(settings)

    session_factory = providers.Singleton(
        create_engine_session_factory,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        db_name=config.DB_NAME,
        port=config.DB_PORT
    )


    uow_factory = providers.Factory(
        UnitOfWorkImpl,
        session_factory=session_factory,
        customer_repository_class=CustomerRepositoryImpl
    )

    event_publisher = providers.Singleton(
        EventPublisher,
        bucket_name=config.EVENT_BUCKET_NAME,
        environment=config.ENV,
    )

    use_cases = providers.Singleton(
        UseCases,
        uow_factory=uow_factory,
        event_publisher=event_publisher
    )