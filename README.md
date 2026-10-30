# Distributed Robot Mission System

A fault-tolerant cloud platform for scheduling missions across a fleet of simulated robots.

## Project overview

This project implements a multi-service cloud system that receives robot missions, selects suitable simulated robots, monitors robot state, and recovers from service failures.

The project focuses on:

- Cloud microservices
- Distributed systems
- Fault tolerance
- Horizontal scaling
- Mission scheduling
- Data consistency
- Monitoring
- Performance evaluation

The robots are software simulations moving on a simple two-dimensional grid. This project does not require physical robots, cameras, OpenCV, edge AI, Gazebo, or Isaac Sim.

## Main services

- Mission Service
- Robot Status Service
- Scheduler Service
- Robot Simulator Service
- PostgreSQL
- Prometheus
- Grafana

## Technology stack

- Python
- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- Prometheus
- Grafana
- Locust or Python load testing
- Pytest
- GitHub

## Main workflow

1. A client submits a mission.
2. The Mission Service stores the mission.
3. The Scheduler Service selects a suitable robot.
4. The Robot Simulator executes the mission.
5. The robot sends telemetry updates.
6. The mission result is stored.
7. The client retrieves the result.

## Planned demonstrations

### Failure demonstration

We will stop one Scheduler Service instance while the system is processing missions under load.

The remaining scheduler should continue assigning missions without losing missions or creating duplicate assignments.

### Scaling demonstration

We will run the system with one service instance and then add more instances while generating load.

We will compare:

- Throughput
- p50 latency
- p99 latency
- Queue length
- Error rate
- CPU usage
- Memory usage

## Repository structure

```text
services/          Application services
database/          Database setup and seed data
scripts/           Testing and operational scripts
docs/              Architecture and project documentation
tests/             Unit, integration, and concurrency tests
monitoring/        Prometheus and Grafana configuration
