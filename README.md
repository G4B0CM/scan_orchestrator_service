# Scan Orchestrator Service

## Overview

The **Scan Orchestrator Service** is the entry point for initiating a new cybersecurity risk assessment. Authenticated users submit a target domain, and this service is responsible for validating the request, creating a new scan record, and triggering the asynchronous analysis pipeline by publishing an event to an Apache Kafka topic.

This service is a critical component in our **Event-Driven Architecture**. Its sole synchronous responsibility is to accept and acknowledge a scan request, ensuring a fast response time for the user. The heavy lifting of asset discovery, vulnerability scanning, and risk calculation is handled by other downstream microservices that consume the events produced by this service.

## Tech Stack

- **Framework:** FastAPI
- **Language:** Python 3.11+
- **Database:** PostgreSQL (for persisting scan records)
- **Messaging:** Apache Kafka (for event publishing)
- **ORM:** SQLAlchemy
- **Data Validation:** Pydantic
- **Containerization:** Docker

## Architecture

This service adheres to **Clean Architecture**, separating concerns into four layers:

1.  **Domain:** Contains the core `Scan` entity, business rules, and abstract repository interfaces for both persistence (`IScanRepository`) and messaging (`IMessagingProducer`).
2.  **Application:** Houses the `InitiateScanUseCase` which orchestrates the domain logic.
3.  **Infrastructure:** Provides concrete implementations for the domain's interfaces, including the `PostgresScanRepository` and the `KafkaProducer`.
4.  **API (Presentation):** The FastAPI layer that handles HTTP requests, authentication via JWT, and presents data to the client.

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL instance
- Apache Kafka instance

### Installation & Running

1.  **Clone, create venv, and install dependencies:**
    ```bash
    git clone <your-repo-url>
    cd scan-orchestrator-service
    python -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Set up environment variables:**
    Copy `.env.example` to `.env` and configure your database, Kafka, and JWT secret.
    ```bash
    cp .env.example .env
    ```

3.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    API docs will be at `http://127.0.0.1:8001/docs`.

## API Endpoints

### Initiate a new scan

- **URL:** `/api/v1/scans`
- **Method:** `POST`
- **Authentication:** `Bearer <JWT_TOKEN>` required.
- **Request Body:**
  ```json
  {
    "domain_name": "example.com",
    "acceptable_loss": 50000.00
  }

### Success Response (202 Accepted):
The 202 status code indicates that the request has been accepted for processing, but the processing has not been completed.
Generated json
{
  "scan_id": "some-uuid",
  "domain_name": "example.com",
  "status": "PENDING",
  "message": "Scan initiated successfully. Processing has started."
}


**`scan-orchestrator-service/.env.example`**
```ini
# --- Database ---
DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/scan_db"

# --- JWT ---
# MUST BE THE SAME AS THE ONE IN THE AUTH SERVICE
SECRET_KEY="a_very_secret_key_that_should_be_long_and_random"
ALGORITHM="HS256"

# --- Kafka ---
KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
KAFKA_SCAN_TOPIC="scan.started"