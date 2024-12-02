from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import logging

from constants import OIL_DB_PATH
from price import get_latest_price

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    # Use an absolute path to ensure the database location is well-defined
    conn = sqlite3.connect(OIL_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            action TEXT,
            amount INTEGER,
            position TEXT DEFAULT 'OIL'
        )
    ''')
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS cummulative_transactions AS
            SELECT
                position,
                SUM(amount) AS cummulative_amount
            FROM transactions
            GROUP BY position
    ''')
    cursor.execute("SELECT * FROM transactions WHERE action = 'INITIAL'")
    entry = cursor.fetchone()

    if not entry:
        cursor.execute("INSERT INTO transactions (action, amount) VALUES ('INITIAL', 1000)")
        conn.commit()
        logger.info("Initialized database")

    conn.close()


with app.app_context():
    init_db()


@app.route('/transactions', methods=['GET'])
def get_transactions():
    conn = sqlite3.connect(OIL_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 10")
    transactions = cursor.fetchall()

    new_transactions = []
    for i, transaction in enumerate(transactions):
        new_transactions.append({
            "id": transaction[0],
            "timestamp": transaction[1],
            "action": transaction[2],
            "amount": transaction[3],
            "position": transaction[4]
        })

    conn.close()
    return jsonify(new_transactions)


@app.route('/oil', methods=['GET'])
def get_cummulative():
    conn = sqlite3.connect(OIL_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cummulative_transactions WHERE position = 'OIL'")
    entry = cursor.fetchone()
    conn.close()
    if entry:
        return jsonify({"position": entry[0], "amount": entry[1]})
    else:
        return jsonify({"error": "Oil entry not found"}), 404


@app.route('/oil', methods=['POST'])
def insert_transaction():
    update_data = request.get_json()

    amount_value = update_data.get('amount')
    action_value = update_data.get('action')

    if amount_value is None or not isinstance(amount_value, int):
        return jsonify({"error": "Invalid adjustment value. Please provide an integer."}), 400

    conn = sqlite3.connect(OIL_DB_PATH)
    cursor = conn.cursor()

    try:
        # Update the database with the new value
        cursor.execute("INSERT INTO transactions (action, amount) VALUES (?, ?)", (action_value, amount_value))
        conn.commit()

        return jsonify({
            "message": "Transaction successful",
            "amount": amount_value,
            "action": action_value,
            "new_cummulative": get_cummulative().get_json()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route('/price', methods=['GET'])
def get_current_price():
    latest_price = get_latest_price()
    return jsonify(latest_price)
