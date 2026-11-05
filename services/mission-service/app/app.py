import os

import psycopg2
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI(title="Mission Service")


class MissionRequest(BaseModel):
    start_x: int
    start_y: int
    destination_x: int
    destination_y: int
    priority: int = 1


def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        database=os.getenv("DB_NAME", "robotdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/missions", status_code=status.HTTP_201_CREATED)
def create_mission(mission: MissionRequest):
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO missions
            (start_x, start_y, destination_x, destination_y, priority)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, status;
            """,
            (
                mission.start_x,
                mission.start_y,
                mission.destination_x,
                mission.destination_y,
                mission.priority,
            ),
        )
        mission_id, state = cur.fetchone()
        conn.commit()
        cur.close()
        return {"mission_id": mission_id, "status": state}
    finally:
        conn.close()


@app.get("/missions/{mission_id}")
def get_mission(mission_id: int):
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, start_x, start_y, destination_x,
                   destination_y, priority, status,
                   assigned_robot_id
            FROM missions
            WHERE id = %s;
            """,
            (mission_id,),
        )
        mission = cur.fetchone()
        cur.close()
    finally:
        conn.close()

    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    return {
        "mission_id": mission[0],
        "start_x": mission[1],
        "start_y": mission[2],
        "destination_x": mission[3],
        "destination_y": mission[4],
        "priority": mission[5],
        "status": mission[6],
        "assigned_robot_id": mission[7],
    }
