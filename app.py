from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)

# Database connection setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:iCjjjBFSqvSGPIGNWMreFQBpFKifJngN@junction.proxy.rlwy.net:53974/railway")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS statuses (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    status TEXT NOT NULL,
    timestamp BIGINT NOT NULL
)
""")
conn.commit()

@app.route('/log_status', methods=['POST'])
def log_status():
    try:
        data = request.get_json()
        username = data.get('username')
        status = data.get('status')
        timestamp = data.get('timestamp')

        if not username or not status or not timestamp:
            return jsonify({"error": "Invalid data"}), 400

        cursor.execute(
            sql.SQL("INSERT INTO statuses (username, status, timestamp) VALUES (%s, %s, %s)"),
            (username, status, timestamp)
        )
        conn.commit()

        return jsonify({"message": "Status logged successfully"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == "__main__":
    app.run(debug=True)
