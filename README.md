# Distributed Robot Mission System

A fault-tolerant cloud platform for scheduling missions across a fleet of simulated robots.

## Overview

The Distributed Robot Mission System is a distributed, multi-service application that receives mission requests, selects suitable simulated robots, tracks mission progress, and stores execution results. The project explores how microservices can support reliable mission execution under concurrent workloads, service failures, and changing resource demands.

The robots are software simulations that move on a two-dimensional grid. Physical robots, cameras, OpenCV, edge AI, Gazebo, and Isaac Sim are outside the scope of the core system.

## Research Question

**How can a distributed mission scheduling system maintain consistency, fault tolerance, and scalability under concurrent workloads, scheduler replication, service failures, and dynamic resource demands?**

The project examines how distributed scheduling, service recovery, horizontal scaling, and database-backed coordination can be combined to support reliable mission execution.

## System Architecture

The current system is organized around the following services and supporting components:

- **Mission Service** – Validates mission requests, creates missions, and reports mission status.
- **Scheduler Service** – Selects available robots and assigns missions.
- **Robot Simulator Service** – Simulates robot movement and mission completion.
- **Robot Status Service** – Tracks robot availability, position, and operational state as the system is extended.
- **PostgreSQL** – Stores missions, robot states, assignments, and execution results.
- **Prometheus and Grafana** – Planned monitoring components for collecting and visualizing performance metrics.

## Main Workflow

1. A client submits a mission request to the Mission Service.
2. The Mission Service validates the request and stores it in PostgreSQL.
3. The Scheduler Service selects a suitable available robot.
4. The mission is assigned to the selected robot.
5. The Robot Simulator executes the mission on a two-dimensional grid.
6. Robot state and mission results are updated in the database.
7. The client retrieves the mission status and final result.

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- Docker and Docker Compose
- Pytest
- Python-based load testing or Locust
- Prometheus and Grafana for planned monitoring support
- GitHub

## Requirements

- Docker Desktop
- Python 3
- The Python `requests` package for the test scripts

## Running the Project

Run all commands from the project root directory.

### 1. Start the services

```bash
docker compose up --build -d
```

### 2. Check the containers

```bash
docker compose ps
```

All required containers should be running before continuing.

### 3. Run the repository check

```bash
python3 scripts/design_review_check.py
```

This verifies that the required runtime files, service paths, database initialization, tests, and design-review documents are present.

### 4. Run the end-to-end smoke test

```bash
python3 scripts/smoke_test.py
```

The smoke test checks the Mission Service, creates a mission, waits for execution, and verifies that the mission reaches the `COMPLETED` state.

### 5. Run the concurrent load test

```bash
python3 scripts/load_test.py
```

The load test submits multiple missions concurrently and reports successful requests, failed requests, average latency, p95 latency, and total test time.

## API Documentation

When the Mission Service is running, interactive FastAPI documentation is available at:

[http://localhost:5000/docs](http://localhost:5000/docs)

The service health endpoint is available at:

[http://localhost:5000/health](http://localhost:5000/health)

If port `5000` is already being used on macOS, either stop the application using that port or change the host-side port mapping in `docker-compose.yml`. If the host port is changed, update the URLs in `scripts/smoke_test.py` and `scripts/load_test.py` as well. The container port should remain `5000`.

## Viewing Logs

To follow logs from all services:

```bash
docker compose logs -f
```

To view logs for a specific service:

```bash
docker compose logs -f mission-service
docker compose logs -f scheduler-service
docker compose logs -f robot-simulator
```

## Stopping the Project

Stop and remove the project containers while preserving the PostgreSQL data volume:

```bash
docker compose down
```

To remove the containers and the PostgreSQL data volume, use the following command carefully:

```bash
docker compose down -v
```

Removing the volume deletes the database data stored by Docker.

## Planned Demonstrations

### Failure Demonstration

One Scheduler Service instance will be stopped while missions are being processed under load. The remaining scheduler instances should continue processing missions without losing requests or creating duplicate assignments.

This demonstration evaluates service failure detection, recovery, assignment consistency, duplicate prevention, and continued availability.

### Scaling Demonstration

The system will be tested with one service instance and then with additional instances under comparable workloads. The results will be compared using throughput, p50 latency, p99 latency, queue length, error rate, CPU usage, and memory usage.

### Concurrent Mission Demonstration

Multiple missions will be submitted simultaneously to evaluate assignment conflicts, scheduling consistency, robot availability management, mission completion rates, and scheduling latency.

## Performance Evaluation

The system will be evaluated through controlled experiments using different workloads, service configurations, and failure scenarios.

| Metric | Purpose |
|---|---|
| Throughput | Measures completed missions per unit of time. |
| p50 latency | Measures median mission scheduling latency. |
| p99 latency | Measures tail scheduling latency. |
| Queue length | Measures pending mission workload. |
| Error rate | Measures failed requests and operations. |
| CPU usage | Measures computational resource consumption. |
| Memory usage | Measures memory consumption. |
| Recovery time | Measures the time required to recover from a service failure. |

## Design Review Documentation

The design-review checkpoint is documented in `docs/design-review.md`. Related documents describe the system architecture, data ownership, consistency decisions, failure behavior, scaling limits, service instances, and estimated cost at higher workloads.

Run the repository check with:

```bash
python3 scripts/design_review_check.py
```

## Optional ROS 2 Integration

ROS 2 integration is an optional extension for exploring communication between the cloud scheduling platform and robotic middleware. Possible extensions include sending mission commands through ROS 2, publishing robot status and telemetry, and connecting simulated robots to ROS 2 nodes.

The core platform operates independently of ROS 2, so ROS 2 is not required to build or run the current system. For installation information, see the [official ROS 2 documentation](https://docs.ros.org/en/rolling/Installation.html).

## Repository Structure

```text
services/          Application services
database/          Database initialization and seed data
scripts/            Repository checks and test scripts
docs/              Architecture and design-review documentation
tests/              Unit, integration, and concurrency tests
monitoring/        Prometheus and Grafana configuration
docker-compose.yml Local multi-service deployment
```

## Project Checkpoints

The first checkpoint includes:

- Fresh-clone Docker setup
- FastAPI services
- PostgreSQL database
- End-to-end smoke test
- Concurrent load test

The second checkpoint includes design-review documentation covering:

- Service instances
- Failure behavior
- Scaling limits
- Data ownership
- Consistency decisions
- Estimated cost
