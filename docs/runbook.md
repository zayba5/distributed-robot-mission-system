# Design-review runbook

Run these commands from the repository root.

## Start and verify

```bash
docker compose up --build -d
docker compose ps
python3 scripts/smoke_test.py
python3 scripts/load_test.py
```

The smoke test submits one mission and waits for completion. The load test
submits 100 mission requests using 20 concurrent workers and reports average
and p95 request latency.

## Scaling demonstration

The scheduler is designed to use database row locks so multiple instances can
share the queue:

```bash
docker compose up -d --scale scheduler-service=2
python3 scripts/load_test.py
```

Compare successful requests, latency, and completed missions with one
scheduler instance. The current Compose file exposes only the Mission Service;
the scheduler replicas communicate through the internal Compose network.

## Failure demonstration

In a second terminal, submit load and then stop one scheduler container:

```bash
docker compose ps
docker stop <one-scheduler-container>
docker compose ps
```

Queued missions should remain in PostgreSQL and the surviving scheduler should
continue processing them. Do not claim full recovery for a simulator failure:
the design review records the missing lease/heartbeat mechanism as a known
limitation.

## Cleanup

```bash
docker compose down
```

Use `docker compose down -v` only when intentionally deleting the local
PostgreSQL volume and all checkpoint data.
