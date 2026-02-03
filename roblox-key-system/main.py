from flask import Flask, request, render_template_string
import datetime
import uuid
import os

app = Flask(__name__)
keys_db = {}

# Simple, clean HTML for the user to see on their Mac/Phone
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Vault Farm Key System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="background:#121212; color:white; font-family:sans-serif; text-align:center; padding-top:50px;">
    <h1>Key System</h1>
    {% if key %}
        <div style="background:#222; padding:20px; border-radius:10px; display:inline-block; border:1px solid #00ff00;">
            <p>Your Key (Valid 24h):</p>
            <h2 style="color:#00ff00; letter-spacing:2px;">{{ key }}</h2>
            <p style="font-size:12px; color:#888;">Linked to: {{ hwid }}</p>
        </div>
    {% else %}
        <form action="/generate" method="get">
            <p>Paste your HWID from the script below:</p>
            <input type="text" name="hwid" placeholder="8839988e-..." style="padding:12px; width:80%; max-width:300px; border-radius:5px; border:none;"><br><br>
            <input type="submit" value="Get My Key" style="padding:10px 20px; background:#00ff00; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">
        </form>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def home():
    # Detect if HWID was passed automatically, otherwise show the empty form
    hwid = request.args.get('hwid')
    if hwid and hwid not in ["[1]", "{{hwid}}", "[hwid]"]:
        return generate_logic(hwid)
    return render_template_string(HTML_PAGE, key=None)

@app.route('/generate')
def generate_route():
    hwid = request.args.get('hwid')
    return generate_logic(hwid)

def generate_logic(hwid):
    if not hwid or hwid in ["[1]", "{{hwid}}", "[hwid]"]:
        return render_template_string(HTML_PAGE, key=None)
    
    new_key = "VAULT-" + str(uuid.uuid4())[:8].upper()
    keys_db[new_key] = {
        "hwid": hwid,
        "expires": datetime.datetime.now() + datetime.timedelta(hours=24)
    }
    return render_template_string(HTML_PAGE, key=new_key, hwid=hwid)

@app.route('/verify')
def verify():
    key, hwid = request.args.get('key'), request.args.get('hwid')
    if key in keys_db:
        data = keys_db[key]
        if data['hwid'] == hwid and datetime.datetime.now() < data['expires']:
            return "success"
    return "invalid"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
