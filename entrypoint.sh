#!/usr/bin/env bash
set -e

echo "Running Alembic migrations..."

alembic -c alembic.ini revision --autogenerate -m "Initial migration"
alembic -c alembic.ini upgrade head
echo "Alembic migrations applied."

echo "Initializing Terraform..."
cd /app/infra/terraform
terraform init

echo "Applying Terraform infrastructure..."
terraform apply -auto-approve

cd /app/src

exec "$@"