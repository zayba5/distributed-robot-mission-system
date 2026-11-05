import os
import threading
import time

import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Robot Simulator")


class ExecutionRequest(BaseModel):
    mission_id: int
    robot_id: int


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


@app.post("/execute")
def execute(request: ExecutionRequest):
    threading.Thread(
        target=run_mission,
        args=(request.mission_id, request.robot_id),
        daemon=True,
    ).start()
    return {"message": "Mission execution started"}


def run_mission(mission_id: int, robot_id: int):
    print(f"Robot {robot_id} executing mission {mission_id}")

    for step in range(1, 4):
        time.sleep(1)
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE robots
                SET x_position = %s, y_position = %s,
                    last_telemetry = CURRENT_TIMESTAMP
                WHERE id = %s;
                """,
                (step, step, robot_id),
            )
            conn.commit()
            cur.close()
        finally:
            conn.close()

    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE missions
            SET status = 'COMPLETED', completed_at = CURRENT_TIMESTAMP
            WHERE id = %s;
            """,
            (mission_id,),
        )
        cur.execute(
            "UPDATE robots SET status = 'AVAILABLE' WHERE id = %s;",
            (robot_id,),
        )
        conn.commit()
        cur.close()
    finally:
        conn.close()

    print(f"Mission {mission_id} completed")
