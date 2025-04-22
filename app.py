import psycopg2
from flask import Flask, request, jsonify
from psycopg2 import OperationalError
from datetime import datetime
import pytz

app = Flask(__name__)

# Define the local timezone
local_tz = pytz.timezone("Africa/Nairobi")


# Function to connect to the database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="172.18.0.2",  # Use your DB container's host/IP
            dbname="magic",
            user="root",
            password="root",
        )
        conn.autocommit = True
        return conn, conn.cursor()
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        return None, None


# Connect to DB
conn, cur = get_db_connection()

# Create the table if it doesn't exist
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


# Route to receive POST requests
@app.route("/log", methods=["POST"])
def log_data():
    data = request.get_json()
    if data is None:
        return jsonify({"status": "failure", "message": "No JSON data received"}), 400

    smoke = data.get("smoke")
    if smoke is None:
        return jsonify({"status": "failure", "message": "Missing smoke value"}), 400

    # Get current time in Nairobi time zone
    utc_time = datetime.now(pytz.utc)
    nairobi_time = utc_time.astimezone(local_tz)

    # Debug print
    print(f"Inserting smoke={smoke} at Nairobi time: {nairobi_time}")

    # Insert into database
    try:
        cur.execute(
            "INSERT INTO smoke_data_new (smoke_value, timestamp) VALUES (%s, %s)",
            (smoke, nairobi_time),
        )
        conn.commit()
    except Exception as e:
        return jsonify({"status": "failure", "message": f"DB insert error: {e}"}), 500

    return jsonify({"status": "success", "timestamp": nairobi_time.isoformat()}), 200


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
