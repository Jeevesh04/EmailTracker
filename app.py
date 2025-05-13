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


@app.route('/download/log/time')
def download_log_by_time():
    after_str = request.args.get("after")

    if not after_str:
        return "❌ Missing 'after' query parameter", 400

    try:
        after_time = datetime.fromisoformat(after_str)
    except ValueError:
        return "❌ Invalid datetime format. Use YYYY-MM-DDTHH:MM:SS", 400

    filtered_lines = []
    with open("opens.log", "r") as f:
        for line in f:
            # Extract timestamp from each line
            timestamp_str = line.split(" - ")[0]
            try:
                log_time = datetime.fromisoformat(timestamp_str.strip())
                if log_time > after_time:
                    filtered_lines.append(line)
            except Exception:
                continue  # skip lines that don't parse

    return Response("".join(filtered_lines), mimetype="text/plain")

if __name__ == "__main__":
    app.run()

