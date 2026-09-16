from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)


def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "172.17.0.1"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "banco_db"),
        user=os.environ.get("DB_USER", "admin_banco"),
        password=os.environ.get("DB_PASS", "SecretPassword123!")
    )


@app.route("/venta", methods=["POST"])
def registrar_venta():
    data = request.get_json()
    monto = data.get("monto", 0)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO ventas (monto) VALUES (%s)", (monto,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success", "monto_registrado": monto}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
