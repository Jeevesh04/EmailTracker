from flask import Flask, send_file, request
import datetime
import os

app = Flask(__name__)
LOG_FILE = "opens.log"
PIXEL_PATH = "pixel.png"

@app.route('/track/<recipient_id>.png')
def track(recipient_id):
    timestamp = datetime.datetime.now()
    log_entry = f"{timestamp} - {recipient_id} opened"
    
    # Save to file (local, temporary)
    with open("opens.log", "a") as f:
        f.write(log_entry + "\n")

    # Print to Render logs (visible in dashboard)
    print(log_entry)

    return send_file("pixel.png", mimetype="image/png")


@app.route("/")
def home():
    return "📬 Email tracker is running!"

@app.route('/download/log')
def download_log():
    if request.args.get("key") == "yoursecret":
        return send_file("opens.log", as_attachment=True)
    return "Unauthorized", 401


if __name__ == "__main__":
    app.run()

