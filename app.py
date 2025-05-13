from flask import Flask, send_file, request
import datetime
import os

app = Flask(__name__)
LOG_FILE = "opens.log"
PIXEL_PATH = "pixel.png"

@app.route('/track/<recipient_id>.png')
def track(recipient_id):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} - {recipient_id} opened\n")
    return send_file(PIXEL_PATH, mimetype="image/png")

@app.route("/")
def home():
    return "📬 Email tracker is running!"

if __name__ == "__main__":
    app.run()

