from flask import Flask, jsonify
import os
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "https://main.d2yzt563jf258w.amplifyapp.com",
    "https://backend.usmanali.site",
    "http://localhost:3000"
])

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME', 'appdb'),
            user=os.getenv('DB_USER', 'dbadmin'),
            password=os.getenv('DB_PASS'),  # Changed to DB_PASS
            port=os.getenv('DB_PORT', '5432')
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route("/")
def home():
    return jsonify({"message": "Backend running successfully in ECS", "version": "1.0"})

@app.route("/health")
def health():
    db_status = "disconnected"
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            db_status = "connected"
    except:
        pass
    return jsonify({
        "status": "healthy",
        "database": db_status,
        "service": "backend-api"
    })

@app.route("/api/data")
def get_data():
    return jsonify({
        "data": [
            {"id": 1, "name": "Sample Item 1"},
            {"id": 2, "name": "Sample Item 2"}
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
