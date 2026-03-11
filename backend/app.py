from flask import Flask, jsonify, request
import os
import psycopg2
from flask_cors import CORS
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            password=os.getenv('DB_PASS'),
            port=os.getenv('DB_PORT', '5432')
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

@app.route("/")
def home():
    logger.info(f"HOME called from {request.remote_addr}")
    return jsonify({"message": "Backend running successfully in ECS", "version": "1.0"})

@app.route("/health")
def health():
    logger.info(f"HEALTH called from {request.remote_addr}")
    db_status = "disconnected"
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            db_status = "connected"
    except:
        pass
    return jsonify({"status": "healthy", "database": db_status, "service": "backend-api"})

@app.route("/api/data")
def get_data():
    logger.info(f"API/DATA called from {request.remote_addr}")
    return jsonify({"data": [{"id": 1, "name": "Sample Item 1"}, {"id": 2, "name": "Sample Item 2"}]})

@app.route('/test')
def test():
    logger.info(f"TEST called from {request.remote_addr}")
    return jsonify({"status": "success", "message": "Backend is working!", "timestamp": datetime.now().isoformat(), "version": "1.0.1"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
