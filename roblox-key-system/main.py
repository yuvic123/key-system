import sqlite3
from flask import Flask, request, render_template_string
import uuid

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS keys (key TEXT, hwid TEXT, status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/generate')
def generate():
    new_key = "WORK-" + str(uuid.uuid4())[:8].upper()
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Key is generated but has no HWID yet
    c.execute("INSERT INTO keys (key, hwid, status) VALUES (?, ?, ?)", (new_key, "NONE", "PENDING"))
    conn.commit()
    conn.close()
    return f"<h1>Your Key: {new_key}</h1><p>Go to Discord and use /redeem to activate.</p>"

@app.route('/verify')
def verify():
    hwid = request.args.get('hwid')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM keys WHERE hwid=? AND status='ACTIVE'", (hwid,))
    result = c.fetchone()
    conn.close()
    return "success" if result else "invalid"

init_db()
