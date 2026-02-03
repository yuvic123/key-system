import sqlite3
from flask import Flask, request, render_template_string
import uuid
import os

app = Flask(__name__)
DB_PATH = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Status can be 'PENDING' (not used) or 'ACTIVE' (linked to HWID)
    c.execute('''CREATE TABLE IF NOT EXISTS keys 
                 (key TEXT PRIMARY KEY, hwid TEXT, status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/generate')
def generate():
    new_key = "VAULT-" + str(uuid.uuid4())[:8].upper()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO keys (key, hwid, status) VALUES (?, ?, ?)", (new_key, "NONE", "PENDING"))
    conn.commit()
    conn.close()
    return f"<h1>Key Generated!</h1><p>Your Key: <b>{new_key}</b></p><p>Go to Discord to redeem this with your HWID.</p>"

@app.route('/verify')
def verify():
    hwid = request.args.get('hwid')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM keys WHERE hwid=? AND status='ACTIVE'", (hwid,))
    result = c.fetchone()
    conn.close()
    return "success" if result else "invalid"

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
