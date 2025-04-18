# Codebase

## Structure

```
- .describeignore
- Dockerfile
- README.md
- docker-compose.yml
- server.py
```

## Files

### .describeignore

```
.git/

```

### Dockerfile

```
FROM python:3-slim
WORKDIR /app
COPY server.py .
RUN mkdir -p data
RUN pip install flask gunicorn
CMD ["gunicorn", "-w", "8", "-b", "0.0.0.0:80", "--capture-output", "server:app"]
```

### README.md

```
# Crouton Server

Returns "crouton!", current time, and visitor count.

## Build & Run with Docker Compose
```sh
docker compose up --build -d
```

## Access
Visit: [http://localhost:1234](http://localhost:1234)
```

### docker-compose.yml

```
services:
  crouton:
    image: rodlaf/crouton:1.8
    container_name: crouton-server
    build: .
    ports:
      - "1234:80"
    volumes:
      - data:/app/data
    restart: unless-stopped

volumes:
  data:
```

### server.py

```
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
    print(f"{datetime.now()} - Request from {client_ip} | Visitors: {count}", file=sys.stdout)
    return f"crouton! {time} | Visitors: {count}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

