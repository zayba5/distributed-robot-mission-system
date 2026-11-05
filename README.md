# Distributed Robot Mission System

A fault-tolerant cloud platform for scheduling missions across a fleet of simulated robots.

## Project Overview

This project implements a distributed, multi-service cloud system that receives robot missions, selects suitable simulated robots, monitors robot state, and recovers from service failures.

The system is designed to explore distributed scheduling, fault tolerance, horizontal scalability, and reliable mission execution across multiple service instances.

The project focuses on:

- Cloud microservices
- Distributed systems
- Fault tolerance
- Horizontal scaling
- Mission scheduling
- Data consistency
- Monitoring and observability
- Performance evaluation

The robots are software simulations moving on a simple two-dimensional grid. This project does not require physical robots, cameras, OpenCV, edge AI, Gazebo, or Isaac Sim.

## Research Question

**How can a distributed mission scheduling system ensure consistency, fault tolerance, and scalability under concurrent workloads, scheduler replication, service failures, and dynamic resource demands?**

The research investigates how distributed scheduling, fault recovery, and horizontal scaling can be integrated to support reliable mission execution, particularly in ROS 2-compatible robotic systems.

## Main Services

- **Mission Service:** Receives, validates, and manages mission requests.
- **Robot Status Service:** Tracks robot availability, position, and operational state.
- **Scheduler Service:** Assigns missions to suitable robots and coordinates scheduling.
- **Robot Simulator Service:** Simulates robot movement and mission execution.
- **PostgreSQL:** Stores missions, robot states, and execution results.
- **Prometheus:** Collects system and service metrics.
- **Grafana:** Visualizes system performance and operational health.

## Technology Stack

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

## Main Workflow

1. A client submits a mission.
2. The Mission Service validates and stores the mission.
3. The Scheduler Service selects a suitable available robot.
4. The Robot Simulator executes the assigned mission.
5. The robot sends telemetry and state updates.
6. Mission execution results are stored.
7. The client retrieves the mission status and result.

## Optional ROS 2 Integration

ROS 2 integration is an optional extension for exploring communication between the cloud-based mission scheduling system and robotic middleware.

Potential capabilities include:

- Sending mission commands through ROS 2.
- Publishing robot status and telemetry.
- Connecting simulated robots to ROS 2 nodes.

The core platform operates independently of ROS 2. Installing ROS 2 is not required to build or run the system.

For installation instructions, refer to the [official ROS 2 documentation](https://docs.ros.org/en/rolling/Installation.html).

## Planned Demonstrations

### 1. Failure Demonstration

We will stop one Scheduler Service instance while the system is processing missions under load.

The remaining scheduler instances should continue assigning missions without losing missions or creating duplicate assignments.

This demonstration evaluates:

- Scheduler fault detection.
- Recovery and continued mission processing.
- Assignment consistency.
- Duplicate mission prevention.
- Service availability during failures.

### 2. Scaling Demonstration

We will run the system with one service instance and then add more instances while generating load.

We will compare:

- Throughput
- p50 latency
- p99 latency
- Queue length
- Error rate
- CPU usage
- Memory usage

This demonstration evaluates how additional service instances affect system performance and resource utilization.

### 3. Concurrent Mission Demonstration

We will submit multiple missions simultaneously to evaluate how the scheduling system handles concurrent workloads.

The demonstration will examine:

- Mission assignment conflicts.
- Scheduling consistency.
- Robot availability management.
- Mission completion rates.
- Scheduling latency under load.

## Performance Evaluation

The system will be evaluated through controlled experiments involving different workloads, service configurations, and failure scenarios.

Key evaluation metrics include:

| Metric | Purpose |
|---|---|
| Throughput | Measures completed missions per unit of time. |
| p50 latency | Measures median mission scheduling latency. |
| p99 latency | Measures tail scheduling latency. |
| Queue length | Measures pending mission workload. |
| Error rate | Measures failed requests and operations. |
| CPU usage | Measures computational resource consumption. |
| Memory usage | Measures memory consumption. |
| Recovery time | Measures time required to recover from service failures. |

## Repository Structure

```text
services/          Application services
database/          Database setup and seed data
scripts/           Testing and operational scripts
docs/              Architecture and project documentation
tests/             Unit, integration, and concurrency tests
monitoring/        Prometheus and Grafana configuration

## Design review

The design-review checkpoint is documented in `docs/design-review.md`. It
covers service instance counts, failure impact, state placement, scaling
limits, data ownership, consistency, and the dominant cost at 10x load.

Run the repository checks with:

```bash
python3 scripts/design_review_check.py
```
