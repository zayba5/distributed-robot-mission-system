# Design Review

This document answers the four review questions: how the system fits
together, how components change together, who owns each piece of data, and
what each arrow costs.

## 1. Instance count, loss impact, and state location

| Component | Checkpoint count | What happens if one instance is lost? | Where its state is |
|---|---:|---|---|
| Mission Service | 1; can scale horizontally | New HTTP requests fail while it is down; missions already stored remain safe | PostgreSQL; process is stateless |
| Scheduler Service | 1; demo with 2 replicas | Queued missions remain available; another scheduler can claim them | PostgreSQL rows and transaction locks |
| Robot Simulator | 1 | An in-flight mission may remain `ASSIGNED` and its robot may remain `BUSY` | PostgreSQL telemetry and mission rows; execution thread is volatile |
| PostgreSQL | 1 | Mission creation, scheduling, and telemetry stop | Named Docker volume |
| Robot Status Service | 0; placeholder only | No separate failure mode yet | Robot state is currently in PostgreSQL |

The main availability limitation is PostgreSQL being a single instance. The
main recoverability limitation is that simulator execution has no lease or
heartbeat. These are explicit boundaries of this checkpoint rather than
unstated guarantees.

## 2. How it scales and what limits it

| Workload | Scaling action | Expected limit |
|---|---|---|
| HTTP mission creation | Add Mission Service replicas behind a load balancer | PostgreSQL connection count and write throughput |
| Queue scheduling | Add Scheduler Service replicas | Database lock contention and polling interval |
| Mission execution | Add simulator workers/replicas | Robot-row contention, database writes, and Python thread capacity |
| Database state | Move to PostgreSQL HA/read replicas in a production design | Primary write capacity and coordination overhead |

The scheduler's `FOR UPDATE SKIP LOCKED` prevents two scheduler replicas from
claiming the same queued row at the same time. More replicas improve available
polling capacity only until database contention dominates. Scaling the current
Compose stack is therefore a useful demonstration of a bottleneck, not proof
of unlimited linear scaling.

## 3. Data ownership and consistency

The system uses one authoritative PostgreSQL database. Ownership is defined at
the field/transition level:

- Mission Service owns mission creation and request-field validation.
- Scheduler Service owns assignment and the mission-to-robot reservation.
- Robot Simulator owns telemetry and execution completion.
- The scheduler and simulator own robot status during their respective
  reservation and release transitions.

Assignment and robot reservation are one transaction. This is the key
consistency statement: a mission is not considered assigned unless its robot
reservation commits with it. Reads after commit see the database result.

The current design does not yet recover a simulator that dies after claiming a
robot. A production design would add `lease_expires_at`, heartbeats, and a
reaper that returns expired assignments to `QUEUED`.

## 4. Cost of each arrow

| Arrow | Cost at checkpoint scale | Cost at 10x | Dominant concern |
|---|---|---|---|
| Client → Mission Service | One local HTTP request per mission | 10x request rate and connection work | Mission-service workers and DB inserts |
| Mission Service → PostgreSQL | Insert or read plus connection overhead | 10x database writes unless pooled | PostgreSQL primary write capacity |
| Scheduler → PostgreSQL | Poll, lock, update mission, update robot | More competing polls and lock waits | Database contention and polling frequency |
| Scheduler → Robot Simulator | One internal HTTP dispatch per assignment | 10x dispatches and execution work | Simulator worker capacity |
| Simulator → PostgreSQL | Telemetry writes plus completion/release writes | 10x telemetry writes | Database write I/O |

The single resource most likely to dominate operating cost at 10x is the
PostgreSQL primary: every mission creation, claim, telemetry update, and
completion update crosses that boundary. Network traffic between containers
is comparatively small for this workload; database I/O and connection
management are the first scaling measurements to collect.

## Review evidence

The repository provides:

- `scripts/smoke_test.py` for one end-to-end mission.
- `scripts/load_test.py` for concurrent mission creation.
- `scripts/design_review_check.py` for repository-level design checks.
- `docs/runbook.md` for scaling and failure demonstrations.
- `docs/architecture.md`, `docs/consistency.md`, and this document for the
  design decisions and known limitations.

## Review conclusion

The design earns independence where it matters: mission scheduling can be
replicated without keeping queue state in a scheduler process, and a scheduler
failure does not erase queued work. The tradeoff is a shared PostgreSQL
dependency and a simulator recovery gap. Those two limits should be measured
and addressed before claiming production-grade fault tolerance.
