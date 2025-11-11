from flask import Flask, jsonify
import psycopg2
import os
import logging
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='database',
            database='myapp',
            user='appuser',
            password='password123',
            port=5432
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

@app.route('/')
def hello():
    return jsonify({
        "message": "🚀 DevOps Lab 4 - Docker Compose",
        "status": "success",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health():
    db_status = "unhealthy"
    conn = get_db_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('SELECT 1;')
            cur.fetchone()
            cur.close()
            conn.close()
            db_status = "healthy"
        except Exception as e:
            logger.error(f"Health check error: {e}")
    
    return jsonify({
        "status": "running",
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/data')
def get_data():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('SELECT version();')
            db_version = cur.fetchone()
            
            cur.execute('SELECT * FROM app_info;')
            app_data = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return jsonify({
                "database_version": db_version[0] if db_version else "unknown",
                "app_data": app_data,
                "service": "backend-api"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Database connection failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
