.PHONY: lint format test run-tests frontend-lint all clean up down run

# Build project (run in background)
build:
	docker compose -p ttai build

dev-build:
	docker compose -f docker-compose.dev.yaml -p ttai-dev build

# Run migrations
upgrade:
	docker compose -p ttai exec backend alembic upgrade head

dev-upgrade:
	docker compose -f docker-compose.dev.yaml -p ttai-dev exec backend-dev alembic upgrade head

# Up project (run in background)
up:
	docker compose up -p ttai -d

dev-up:
	docker compose -f docker-compose.dev.yaml -p ttai-dev up -d

# Stop project
down:
	docker compose -p ttai down

dev-down:
	docker compose -f docker-compose.dev.yaml -p ttai-dev down

# Run project
run:
	docker compose -p ttai up

dev-run:
	docker compose -f docker-compose.dev.yaml -p ttai-dev up

# Logs
logs:
	docker compose -p ttai logs

dev-logs:
	docker compose -f docker-compose.dev.yaml -p ttai-dev logs

# Create migrations
migrate:
	docker compose -p ttai exec backend alembic revision --autogenerate -m "init migration"

dev-migrate:
	docker compose -f docker-compose.dev.yaml -p ttai-dev exec backend-dev alembic revision --autogenerate -m "init migration"

# Backend code check
lint:
	cd backend && pylint app tests --disable=all --enable=C0114,C0115,C0116,C0411,W0611,W1201,W0401,W0231

# Import formatting
format-imports:
	cd backend && isort app tests

# Code formatting
format-black:
	cd backend && black app tests

# Run all formatting
format: format-black format-imports

# Run tests in Docker
test:
	docker compose -f docker-compose.test.yml -p ttai-test up --build backend

# Frontend check
frontend-lint:
	cd frontend && npm run lint

# Run all checks
checks: test format lint frontend-lint

# Clean temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +

# Help
help:
	@echo "Available commands:"
	@echo "Docker:"
	@echo "  make run           - Run project"
	@echo "  make up            - Build and run project (in background)"
	@echo "  make down          - Stop project"
	@echo "  make logs          - Show logs of project"
	@echo "  make migrate       - Create migrations"
	@echo "  make test          - Run tests in Docker"
	@echo "Docker dev:"
	@echo "  make dev-run       - Run project in dev"
	@echo "  make dev-up        - Build and run project in dev (in background)"
	@echo "  make dev-down      - Stop project in dev"
	@echo "  make dev-logs      - Show logs of project in dev"
	@echo "  make dev-migrate   - Create migrations in dev"
	@echo ""
	@echo "Code quality:"
	@echo "  make lint          - Run pylint"
	@echo "  make format        - Format code (isort + black)"
	@echo "  make frontend-lint - Check frontend code"
	@echo ""
	@echo "Helpful:"
	@echo "  make checks        - Run all checks"
	@echo "  make clean         - Clean temporary files"
