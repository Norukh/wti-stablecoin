from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

from constants import OIL_DB_PATH
from price import get_latest_price

app = Flask(__name__)
CORS(app)


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
def adjust_entry():
    update_data = request.get_json()
    adjustment_value = update_data.get('adjustment')
    if adjustment_value is None or not isinstance(adjustment_value, int):
        return jsonify({"error": "Invalid adjustment value. Please provide an integer."}), 400

    conn = sqlite3.connect(OIL_DB_PATH)
    cursor = conn.cursor()

    try:
        # Fetch the current value
        cursor.execute("SELECT value FROM entries WHERE name = 'Oil'")
        entry = cursor.fetchone()

        if not entry:
            return jsonify({"error": "Oil entry not found"}), 404

        current_value = entry[0]
        # Adjust the value
        new_value = current_value + adjustment_value

        # Update the database with the new value
        cursor.execute("UPDATE entries SET value = ? WHERE name = 'Oil'", (new_value,))
        conn.commit()
        return jsonify({
            "message": "Oil value adjusted successfully",
            "adjustment": adjustment_value,
            "new_value": new_value
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route('/price', methods=['GET'])
def get_current_price():
    latest_price = get_latest_price()
    return jsonify(latest_price)

if __name__ == '__main__':
    init_db()
    app.run(use_reloader=False, host='0.0.0.0')


