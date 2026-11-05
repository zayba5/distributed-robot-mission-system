from flask import Flask, jsonify
import psycopg2
import os
import time
import threading
import requests

app = Flask(__name__)


def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        database=os.getenv("DB_NAME", "robotdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


def scheduler_loop():
    while True:
        try:
            conn = get_db()
            cur = conn.cursor()

            # Find one queued mission
            cur.execute("""
                SELECT id
                FROM missions
                WHERE status = 'QUEUED'
                ORDER BY priority DESC, id ASC
                LIMIT 1
                FOR UPDATE SKIP LOCKED;
            """)

            mission = cur.fetchone()

            if mission:
                mission_id = mission[0]

                # Find an available robot
                cur.execute("""
                    SELECT id
                    FROM robots
                    WHERE status = 'AVAILABLE'
                    ORDER BY id
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED;
                """)

                robot = cur.fetchone()

                if robot:
                    robot_id = robot[0]

                    cur.execute("""
                        UPDATE missions
                        SET status = 'ASSIGNED',
                            assigned_robot_id = %s
                        WHERE id = %s;
                    """, (robot_id, mission_id))

                    cur.execute("""
                        UPDATE robots
                        SET status = 'BUSY'
                        WHERE id = %s;
                    """, (robot_id,))

                    conn.commit()

                    print(
                        f"Assigned mission {mission_id} "
                        f"to robot {robot_id}"
                    )

                    try:
                        requests.post(
                            "http://robot-simulator:5002/execute",
                            json={
                                "mission_id": mission_id,
                                "robot_id": robot_id
                            },
                            timeout=5
                        )
                    except Exception as e:
                        print("Robot request failed:", e)

            cur.close()
            conn.close()

        except Exception as e:
            print("Scheduler error:", e)

        time.sleep(2)


if __name__ == "__main__":
    threading.Thread(
        target=scheduler_loop,
        daemon=True
    ).start()

    app.run(host="0.0.0.0", port=5001)
