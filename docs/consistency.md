# Consistency and data ownership

PostgreSQL is the authoritative store. There is no second cache or replica in
the current implementation.

## Ownership by data field

| Data | Owner of the write | Other services may | Consistency statement |
|---|---|---|---|
| Mission request fields and creation | Mission Service | Read | A successful `POST /missions` is committed before the ID is returned. |
| Mission assignment and `assigned_robot_id` | Scheduler Service | Read | Assignment and robot reservation commit together, so a claimed mission cannot be assigned twice by schedulers using row locks. |
| Mission execution status and completion time | Robot Simulator | Read | Completion is written after simulated execution; the mission remains durable if the simulator process is replaced, but an in-flight mission needs recovery handling. |
| Robot availability | Scheduler reserves; simulator releases | Read | Reservation occurs in the same transaction as assignment. Release occurs when execution finishes. |
| Robot position and telemetry | Robot Simulator | Read | Each telemetry update is committed to PostgreSQL and is visible to later reads. |

The important rule is that services do not maintain competing in-memory copies
of authoritative state. Shared database schema changes must be backward
compatible or coordinated with all service owners before deployment.

## Failure behavior

- Losing a Mission Service instance loses only that HTTP instance; queued and
  completed data remain in PostgreSQL.
- Losing a Scheduler Service instance leaves queued missions in PostgreSQL;
  another scheduler can claim them.
- Losing a Robot Simulator during execution can leave a robot marked `BUSY`
  and a mission marked `ASSIGNED`. A production version needs leases,
  heartbeats, and a recovery worker. This is an explicit checkpoint limitation.
- Losing PostgreSQL stops new mission creation and scheduling because it is the
  current durable consistency boundary.
