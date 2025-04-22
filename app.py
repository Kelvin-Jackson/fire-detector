import psycopg2
from flask import Flask, request, jsonify
from psycopg2 import OperationalError
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="172.18.0.4", dbname="magic", user="root", password="root"
        )
        conn.autocommit = True
        return conn, conn.cursor()
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        return None, None


conn, cur = get_db_connection()

if cur:
    try:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS smoke_data_new (
                id SERIAL PRIMARY KEY,
                smoke_value INTEGER,
                timestamp TIMESTAMP
            );
        """
        )
        print("Table `smoke_data_new` is ready.")
    except Exception as e:
        print(f"Error creating table: {e}")


@app.route("/log", methods=["POST"])
def log_data():
    data = request.get_json()
    if data is None:
        return jsonify({"status": "failure", "message": "No JSON data received"}), 400
    smoke = data.get("smoke")
    if smoke is None:
        return jsonify({"status": "failure", "message": "Missing smoke value"}), 400
    timestamp = datetime.now()

    cur.execute(
        "INSERT INTO smoke_data_new (smoke_value, timestamp) VALUES (%s, %s)",
        (smoke, timestamp),
    )
    conn.commit()

    return jsonify({"status": "success", "timestamp": timestamp.isoformat()}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
