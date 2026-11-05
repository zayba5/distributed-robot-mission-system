from flask import Flask, request, jsonify
import psycopg2
import os
import threading
import time

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


@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()

    mission_id = data["mission_id"]
    robot_id = data["robot_id"]

    threading.Thread(
        target=run_mission,
        args=(mission_id, robot_id),
        daemon=True
    ).start()

    return jsonify({
        "message": "Mission execution started"
    })


def run_mission(mission_id, robot_id):
    print(
        f"Robot {robot_id} executing "
        f"mission {mission_id}"
    )

    # Simulate robot movement / work
    for step in range(1, 4):
        time.sleep(1)

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            UPDATE robots
            SET x_position = %s,
                y_position = %s,
                last_telemetry = CURRENT_TIMESTAMP
            WHERE id = %s;
        """, (step, step, robot_id))

        conn.commit()
        cur.close()
        conn.close()

        print(
            f"Robot {robot_id} telemetry: "
            f"({step}, {step})"
        )

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE missions
        SET status = 'COMPLETED',
            completed_at = CURRENT_TIMESTAMP
        WHERE id = %s;
    """, (mission_id,))

    cur.execute("""
        UPDATE robots
        SET status = 'AVAILABLE'
        WHERE id = %s;
    """, (robot_id,))

    conn.commit()
    cur.close()
    conn.close()

    print(f"Mission {mission_id} completed")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
