from flask import Flask, jsonify, request
import sqlite3
app = Flask(__name__)


def init_db():
    # Use an absolute path to ensure the database location is well-defined
    db_path = '/backend/src/Oil.db'
    conn = sqlite3.connect(db_path)
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
    db_path = '/backend/src/Oil.db'
    conn = sqlite3.connect(db_path)
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

    db_path = '/backend/src/Oil.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE entries SET value = ? WHERE name = 'Oil'", (new_value,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Oil value updated successfully", "new_value": new_value}), 200


if __name__ == '__main__':
    init_db()
    app.run(use_reloader=False, host='0.0.0.0')

