# API contracts

The externally exposed endpoint is the Mission Service at
`http://localhost:5000`.

## Health

```http
GET /health
```

Expected response:

```json
{"status": "healthy"}
```

## Create a mission

```http
POST /missions
Content-Type: application/json
```

Request:

```json
{
  "start_x": 0,
  "start_y": 0,
  "destination_x": 5,
  "destination_y": 5,
  "priority": 1
}
```

The response is `201 Created`:

```json
{"mission_id": 1, "status": "QUEUED"}
```

## Read a mission

```http
GET /missions/{mission_id}
```

The response includes the mission coordinates, priority, status, and assigned
robot ID. A missing mission returns `404`.
