import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "banco_db")
DB_USER = os.environ.get("DB_USER", "admin_banco")
DB_PASS = os.environ.get("DB_PASS", "Secret123!")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )

@app.route("/")
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route("/venta", methods=["POST"])
def registrar_venta():
    data = request.get_json() or {}
    monto = data.get("monto", 0.0)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS ventas (id SERIAL PRIMARY KEY, monto NUMERIC);")
        cur.execute("INSERT INTO ventas (monto) VALUES (%s) RETURNING id;", (monto,))
        venta_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "id": venta_id, "monto": monto}), 201
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)