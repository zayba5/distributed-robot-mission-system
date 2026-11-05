from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)


def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        database=os.getenv("DB_NAME", "robotdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


@app.route("/missions", methods=["POST"])
def create_mission():
    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO missions
        (start_x, start_y, destination_x, destination_y, priority)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, status;
        """,
        (
            data["start_x"],
            data["start_y"],
            data["destination_x"],
            data["destination_y"],
            data.get("priority", 1)
        )
    )

    mission_id, status = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "mission_id": mission_id,
        "status": status
    }), 201


@app.route("/missions/<int:mission_id>", methods=["GET"])
def get_mission(mission_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, start_x, start_y, destination_x,
               destination_y, priority, status,
               assigned_robot_id
        FROM missions
        WHERE id = %s;
        """,
        (mission_id,)
    )

    mission = cur.fetchone()

    cur.close()
    conn.close()

    if mission is None:
        return jsonify({"error": "Mission not found"}), 404

    return jsonify({
        "mission_id": mission[0],
        "start_x": mission[1],
        "start_y": mission[2],
        "destination_x": mission[3],
        "destination_y": mission[4],
        "priority": mission[5],
        "status": mission[6],
        "assigned_robot_id": mission[7]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
