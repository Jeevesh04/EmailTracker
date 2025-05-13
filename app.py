from flask import Flask, send_file, request
import datetime
import os

app = Flask(__name__)

LOG_FILE = "opens.log"
PIXEL_PATH = "logo.png"  # Make sure this file exists (1x1 transparent PNG)

@app.route('/track/<recipient_id>.png')
def track_open(recipient_id):
    print(f"📬 Email opened by {recipient_id}")
    
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} - {recipient_id} opened\n")

    return send_file(PIXEL_PATH, mimetype="image/png")

if __name__ == "__main__":
    app.run(port=5000)
