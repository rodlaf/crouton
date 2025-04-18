from flask import Flask, request
from datetime import datetime
import threading, os
import sys

app = Flask(__name__)
lock = threading.Lock()
count_file = "data/count.txt"

if not os.path.exists(count_file):
    with open(count_file, "w") as f:
        f.write("0")


def get_count():
    with lock, open(count_file, "r+") as f:
        count = int(f.read()) + 1
        f.seek(0)
        f.write(str(count))
        f.truncate()
    return count


@app.route("/")
def index():
    count = get_count()
    time = datetime.now().strftime("%H:%M:%S")
    # Print the access log
    client_ip = request.remote_addr
    print(f"{datetime.now()} - Request from {client_ip} | Visitors: {count}", flush=True)
    return f"crouton! {time} | Visitors: {count}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)