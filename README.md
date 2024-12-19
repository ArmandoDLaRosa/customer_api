# Customer API

## Overview
The **Customer API** is a Flask application designed to manage customer data effectively. It provides functionality to create, update, retrieve, and delete customer records. The API includes JWT authentication, centralized error handling, and integration with AWS S3 for event publishing. The system is designed following the **Hexagonal Architecture** principles, enabling a clear separation of concerns and high testability. The **CQRS (Command Query Responsibility Segregation)** pattern is applied to divide the application's write and read operations, ensuring scalability and maintainability.

---

## Project Setup Instructions

### Prerequisites
1. Python 3.10 or higher
2. Docker and Docker Compose
3. MySQL (if not using Docker for the database)
4. AWS CLI and LocalStack (for testing AWS services locally)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/customer_api.git
   cd customer_api
   ```
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate    # Windows
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your environment variables:
   Copy `.env.example` to `.env` and update the values as needed.

### Environment Variables
Here’s a list of essential environment variables:
- **Database Configuration:**
  - `DB_HOST`: Database hostname (default: `localhost`)
  - `DB_PORT`: Database port (default: `3306`)
  - `DB_USER`: Database username
  - `DB_PASSWORD`: Database password
  - `DB_NAME`: Name of the database
- **JWT Configuration:**
  - `JWT_SECRET_KEY`: Secret key for JWT token generation
- **AWS Configuration:**
  - `AWS_ACCESS_KEY_ID`: AWS access key ID
  - `AWS_SECRET_ACCESS_KEY`: AWS secret access key
  - `AWS_REGION`: AWS region
  - `EVENT_BUCKET_NAME`: Name of the S3 bucket for publishing events
  - `LOCALSTACK_URL`: LocalStack endpoint URL (for local AWS testing)

### Running Locally
1. Apply database migrations:
   ```bash
   FLASK_APP=src/main.py flask db upgrade
   ```
2. Start the application:
   ```bash
   FLASK_APP=src/main.py flask run --host=0.0.0.0 --port=5000
   ```
3. Access the API documentation at:
   [Swagger UI](http://localhost:5000/apidocs)

### Running With Docker
1. Build and start the services:
   ```bash
   docker-compose up --build
   ```
2. Access the services:
   - **API:** [http://localhost:5000](http://localhost:5000)
   - **LocalStack:** [http://localhost:4566](http://localhost:4566) (for S3 testing)

### Running Tests with GitHub Actions
This project includes a GitHub Actions workflow to automate testing. The workflow is located in `.github/workflows/test.yml` and runs on every push or pull request to the `main` branch. It sets up the environment, installs dependencies, and executes the test suite using `pytest`.

#### How to Test the Workflow:
1. Ensure the workflow file exists in your repository:
   ```plaintext
   .github/workflows/test.yml
   ```
2. Push changes to the `main` branch or create a pull request targeting `main`.
3. Monitor the workflow execution under the **Actions** tab in your GitHub repository.

## API Documentation

### Authentication
- **Login** (`POST /v1/auth/login`): Generates a JWT token for secure API access.

### Customer Management
- **List Customers** (`GET /v1/customers`): Retrieve a paginated list of customers.
- **Get Customer** (`GET /v1/customers/{id}`): Fetch details of a specific customer by ID.
- **Create Customer** (`POST /v1/customers`): Add a new customer record.
- **Update Customer** (`PUT /v1/customers/{id}`): Modify an existing customer record.
- **Delete Customer** (`DELETE /v1/customers/{id}`): Soft-delete a customer record.

### Metrics
- **Health Check** (`GET /health`): Verify application health.
- **Metrics** (`GET /metrics`): Retrieve Prometheus metrics including:
  - `request_count`: Total number of requests processed
  - `request_latency_seconds`: API response times in seconds

---

## Architecture Diagrams

### High-Level Architecture
1. **Backend**: Flask application handling business logic.
2. **Database**: MySQL database for persistent storage.
3. **S3 Integration**: AWS S3 for event publishing.

```plaintext
+-------------+      +-------------+      +----------------+      +---------+
|   Consumer  | ---> | Flask API   | ---> | MySQL Database | ---> |  S3     |
+-------------+      +-------------+      +----------------+      +---------+
```

### Component Breakdown (Hexagonal Architecture)
```plaintext
+-------------------+
| Application Core  |
+-------------------+
| - REST Adapters   |
| - Use Cases       |
| - Domain Models   |
| - Infrastructure  |
+-------------------+
```

### CQRS Workflow
```plaintext
Command Flow (Write Operations):
+------------+      +----------------+      +-------------------+
|   Client   | ---> |   Flask API    | ---> |  Command Handlers |
+------------+      +----------------+      +-------------------+
                                         |
                                         v
                                 +-------------------+
                                 | Repository Layer |
                                 +-------------------+
                                         |
                                         v
                                 +-------------------+
                                 | Database         |
                                 +-------------------+

Query Flow (Read Operations):
+------------+      +----------------+      +-------------------+
|   Client   | ---> |   Flask API    | ---> |   Query Handlers  |
+------------+      +----------------+      +-------------------+
                                         |
                                         v
                                 +-------------------+
                                 | Read Models      |
                                 +-------------------+
```

### Database Interaction
```plaintext
+-------------------+
|   MySQL DB       |
+-------------------+
| Tables:          |
| - Customers      |
| - Migrations     |
+-------------------+
```

### Data Flow Diagram
```plaintext
Request Flow:
+------------+      +----------------+      +-------------------+
|   Client   | ---> |   Flask API    | ---> |   Use Case Layer  |
+------------+      +----------------+      +-------------------+
                                         |
                                         v
                                 +-------------------+
                                 | Repository Layer |
                                 +-------------------+
                                         |
                                         v
                                 +-------------------+
                                 | Database         |
                                 +-------------------+
```

---

## Testing Instructions

### Unit Tests
1. Run unit tests:
   ```bash
   PYTHONPATH=$(pwd)/src pytest tests/ --verbose
   ```
2. Check test coverage:
   ```bash
   pytest --cov=src tests/
   ```

### Integration Testing
Use Postman or a similar API testing tool to manually test endpoints. You can import the Swagger documentation to streamline setup.

### Test Environment
Prepare a `.env.test` file for testing purposes with:
- Test database credentials
- LocalStack configurations for AWS resources

---

## Task Management

### Next Steps
1. Add AWS S3 rollback functionality.
2. Expand test coverage to include edge cases.
3. Add detailed logging for event publishing failures.

