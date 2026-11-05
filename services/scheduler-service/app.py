import os
import threading
import time

import psycopg2
import requests
from fastapi import FastAPI


app = FastAPI(title="Scheduler Service")


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


def scheduler_loop():
    while True:
        conn = None
        cur = None
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id
                FROM missions
                WHERE status = 'QUEUED'
                ORDER BY priority DESC, id ASC
                LIMIT 1
                FOR UPDATE SKIP LOCKED;
                """
            )
            mission = cur.fetchone()

            if mission:
                mission_id = mission[0]
                cur.execute(
                    """
                    SELECT id
                    FROM robots
                    WHERE status = 'AVAILABLE'
                    ORDER BY id
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED;
                    """
                )
                robot = cur.fetchone()

                if robot:
                    robot_id = robot[0]
                    cur.execute(
                        """
                        UPDATE missions
                        SET status = 'ASSIGNED', assigned_robot_id = %s
                        WHERE id = %s;
                        """,
                        (robot_id, mission_id),
                    )
                    cur.execute(
                        "UPDATE robots SET status = 'BUSY' WHERE id = %s;",
                        (robot_id,),
                    )
                    conn.commit()
                    print(f"Assigned mission {mission_id} to robot {robot_id}")

                    try:
                        requests.post(
                            "http://robot-simulator:5002/execute",
                            json={"mission_id": mission_id, "robot_id": robot_id},
                            timeout=5,
                        )
                    except Exception as exc:
                        print("Robot request failed:", exc)
        except Exception as exc:
            print("Scheduler error:", exc)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        time.sleep(2)


@app.on_event("startup")
def start_scheduler():
    threading.Thread(target=scheduler_loop, daemon=True).start()
