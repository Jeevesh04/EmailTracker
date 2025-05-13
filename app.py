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

    # Support both 'T' and space-separated datetime
    after_str = after_str.replace("T", " ")

    try:
        after_time = datetime.fromisoformat(after_str)
    except ValueError:
        return "❌ Invalid datetime format. Use YYYY-MM-DDTHH:MM:SS or with space", 400

    log_path = "opens.log"
    if not os.path.exists(log_path):
        return "❌ Log file not found.", 404

    filtered_lines = []
    with open(log_path, "r") as f:
        for line in f:
            try:
                timestamp_str = line.split(" - ")[0].strip()
                log_time = datetime.fromisoformat(timestamp_str)
                if log_time > after_time:
                    filtered_lines.append(line)
            except Exception as e:
                print(f"Skipping line: {e}")
                continue

    return Response("".join(filtered_lines), mimetype="text/plain")

if __name__ == "__main__":
    app.run()

