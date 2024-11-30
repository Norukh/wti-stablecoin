from flask import Flask, jsonify, request
import sqlite3

from constants import OIL_DB_PATH
from price import get_latest_price, get_historical_data

app = Flask(__name__)


def init_db():
    # Use an absolute path to ensure the database location is well-defined
    conn = sqlite3.connect(OIL_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            value INTEGER
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO entries (id, name, value) VALUES (1, 'Oil', 1000)")
    conn.commit()
    conn.close()


@app.route('/oil', methods=['GET'])
def get_entries():
    conn = sqlite3.connect(OIL_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries WHERE name = 'Oil'")
    entry = cursor.fetchone()
    conn.close()
    if entry:
        return jsonify({"name": entry[1], "value": entry[2]})
    else:
        return jsonify({"error": "Oil entry not found"}), 404


@app.route('/oil', methods=['POST'])
def update_entry():
    update_data = request.get_json()
    new_value = update_data.get('value')
    if new_value is None or not isinstance(new_value, int):
        return jsonify({"error": "Invalid value. Please provide an integer."}), 400

    conn = sqlite3.connect(OIL_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE entries SET value = ? WHERE name = 'Oil'", (new_value,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Oil value updated successfully", "new_value": new_value}), 200


@app.route('/price', methods=['GET'])
def get_current_price():
    latest_price = get_latest_price()
    return jsonify(latest_price)

if __name__ == '__main__':
    init_db()
    app.run(use_reloader=False, host='0.0.0.0')

