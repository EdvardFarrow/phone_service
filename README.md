# Phone Address Microservice

[![Ru](https://img.shields.io/badge/lang-ru-grey.svg)](README_ru.md)

![CI Status](https://github.com/EdvardFarrow/phone_service/actions/workflows/tests.yml/badge.svg)
![Coverage](./coverage.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.124.2-009688.svg)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&logo=redis&logoColor=white)


A high-performance asynchronous microservice for managing phone-address associations.

---

## Functionality

The service provides a REST API for CRUD operations:

- **GET** `/phones/{phone}` — Get an address by number (O(1)).
- **POST** `/phones` — Create a record.
    - *Feature:* Atomic duplicate check (`SET NX`).
- **PUT** `/phones/{phone}` — Update an address.
    - *Feature:* Updates only exceptions (`SET XX`).
- **DELETE** `/phones/{phone}` — Delete a record.

## Tech Stack

- **Kernel:** Python 3.12, FastAPI, Pydantic 2.0.
- **Database:** Redis (asynchronous)
- **Infrastructure:** Docker, Docker Compose.
- **Testing:** Pytest, Fakeredis, Pytest-cov.
- **Tools:** Makefile, Black, Flake8, GitHub Actions.

---

## Installation and Run

The project is implemented entirely via `Makefile`.

### Option 1: Running in Docker (recommended)
Deploys an isolated environment with the application and Redis database.

```bash
# Building and running containers in the background
make up

# Viewing logs
make logs

# Stopping
make down
```

The API will be available at: http://127.0.0.1:8000

### Option 2: Local Development
Requires Python 3.11+ installed and Redis running locally.

```bash
# Installing dependencies
make install

# Run server
make run
```

## Testing and Quality
The project implements integration tests using fakeredis, allowing them to run instantly without increasing the database size.

```bash
# Running Tests + Reporting Corruption
make test

# Code Style Checking (Black+Flake8)
make lint
```

## API Documentation
After starting the application, the documentation is available automatically:

* Swagger UI: http://127.0.0.1:8000/docs — interactive testing.

* ReDoc: http://127.0.0.1:8000/redoc —  documentation.

## Project Structure
```plaintext
.
├── app
│ ├── main.py           # Entry point, routing, and logging
│ ├── schemas.py        # Pydantic models and validation
│ ├── deps.py           # Dependencies and Redis connections
│ └── config.py         # Configuration management
├── tests               # Tests (Pytest + Fakeredis)
├── docker-compose.yml  # Orchestration
├── Dockerfile          # Image build
├── Makefile            # Automation command
└── requirements.txt    # Dependencies
```