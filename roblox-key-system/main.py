from flask import Flask, request, jsonify
import datetime
import uuid

app = Flask(__name__)

# This dictionary stores keys in memory. 
# Format: {"KEY-123": {"hwid": "XYZ", "expires": datetime_object}}
keys_db = {}

@app.route('/')
def home():
    return "Key System API is Online and Protected by UptimeRobot!"

# 1. GENERATE KEY (Point Linkvertise here)
# URL: https://your-app.onrender.com/generate?hwid=USER_HWID
@app.route('/generate', methods=['GET'])
def generate():
    hwid = request.args.get('hwid')
    if not hwid:
        return "Error: No HWID provided. Use /generate?hwid=your_id", 400
    
    # Generate a unique key
    new_key = "FLUX-" + str(uuid.uuid4())[:8].upper()
    
    # Set expiration (24 hours from now)
    expiry = datetime.datetime.now() + datetime.timedelta(hours=24)
    
    # Store in our dictionary
    keys_db[new_key] = {
        "hwid": hwid,
        "expires": expiry
    }
    
    # Return just the key as text so it's easy for the user to copy
    return f"{new_key}"

# 2. VERIFY KEY (Roblox Script calls this)
# URL: https://your-app.onrender.com/verify?key=KEY-123&hwid=USER_HWID
@app.route('/verify', methods=['GET'])
def verify():
    key = request.args.get('key')
    hwid = request.args.get('hwid')
    
    if key in keys_db:
        data = keys_db[key]
        # Check if HWID matches and if it hasn't expired
        if data['hwid'] == hwid:
            if datetime.datetime.now() < data['expires']:
                return "success", 200
            else:
                return "expired", 403
                
    return "invalid", 403

if __name__ == "__main__":
    # Render provides a PORT environment variable
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)