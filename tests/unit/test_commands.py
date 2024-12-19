import pytest
from unittest.mock import MagicMock
from domain.models.customer import Customer
from application.commands.create_customer import CreateCustomerCommand
from application.commands.update_customer import UpdateCustomerCommand
from application.commands.delete_customer import DeleteCustomerCommand

@pytest.fixture
def mock_uow_factory():
    mock_uow = MagicMock()
    mock_uow.customer_repository = MagicMock()
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None
    return mock_uow

@pytest.fixture
def mock_event_publisher():
    return MagicMock()

def test_create_customer_command(mock_uow_factory, mock_event_publisher):
    customer = Customer(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
    )
    mock_uow_factory.customer_repository.add.return_value = customer

    command = CreateCustomerCommand(mock_uow_factory, mock_event_publisher)
    result = command.execute(customer)

    mock_uow_factory.customer_repository.add.assert_called_once_with(customer)
    mock_event_publisher.publish.assert_called_once()
    assert result == customer

def test_update_customer_command(mock_uow_factory, mock_event_publisher):
    customer = Customer(
        id="123",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
    )

    mock_uow_factory.customer_repository.get_by_id.return_value = customer
    command = UpdateCustomerCommand(mock_uow_factory, mock_event_publisher)
    updated_customer = command.execute(
        customer_id="123",
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
    )

    mock_uow_factory.customer_repository.update.assert_called_once()
    mock_event_publisher.publish.assert_called_once()
    assert updated_customer.first_name == "Jane"
    assert updated_customer.email == "jane.smith@example.com"

def test_delete_customer_command(mock_uow_factory, mock_event_publisher):
    customer = Customer(
        id="123",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
    )
    mock_uow_factory.customer_repository.get_by_id.return_value = customer

    command = DeleteCustomerCommand(mock_uow_factory, mock_event_publisher)
    command.execute("123")

    mock_uow_factory.customer_repository.soft_delete.assert_called_once_with("123")
    mock_event_publisher.publish.assert_called_once()
