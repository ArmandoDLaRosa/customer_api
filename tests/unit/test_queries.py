import pytest
from unittest.mock import MagicMock
from domain.models.customer import Customer
from application.queries.get_customer_by_id import GetCustomerByIdQuery
from application.queries.list_customers import ListCustomersQuery
from domain.exceptions import CustomerNotFoundException

@pytest.fixture
def mock_uow_factory():
    mock_uow = MagicMock()
    mock_uow.customer_repository = MagicMock()
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None
    return mock_uow

def test_get_customer_by_id_query(mock_uow_factory):
    customer = Customer(
        id="123",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
    )
    mock_uow_factory.customer_repository.get_by_id.return_value = customer

    query = GetCustomerByIdQuery(mock_uow_factory)
    result = query.execute("123")

    assert result.id == customer.id
    assert result.email == customer.email

def test_get_customer_by_id_query_not_found(mock_uow_factory):
    mock_uow_factory.customer_repository.get_by_id.return_value = None

    query = GetCustomerByIdQuery(mock_uow_factory)
    try:
        result = query.execute("123")
    except CustomerNotFoundException as e:
        assert str(e) == "Customer not found"
        return

    pytest.fail("CustomerNotFoundException was not raised")

def test_list_customers_query(mock_uow_factory):
    customers = [
        Customer(first_name="John", last_name="Doe", email="john.doe@example.com"),
        Customer(first_name="Jane", last_name="Smith", email="jane.smith@example.com"),
    ]
    mock_uow_factory.customer_repository.list_customers.return_value = customers

    query = ListCustomersQuery(mock_uow_factory)
    result = query.execute(offset=0, limit=10)

    assert len(result) == 2
    assert result[0].first_name == "John"
    assert result[1].email == "jane.smith@example.com"