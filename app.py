# KR2: <Poskryakov>
import os
import socket
import redis
from flask import Flask, request

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    password=os.getenv("REDIS_PASSWORD") or None,
    decode_responses=True,
    socket_connect_timeout=2,
)

STUDENT = os.getenv("STUDENT", "unknown")
CONTAINER_ID = socket.gethostname()[:12]

@app.route("/")
def index():
    hits = redis_client.incr("hits")
    return f"KR2 | {STUDENT} | container {CONTAINER_ID} | hits: {hits}\n"

@app.route("/health")
def health():
    return "ok\n"

@app.route("/whoami")
def whoami():
    scheme = request.headers.get("X-Forwarded-Proto") or "none"
    client = request.headers.get("X-Real-IP") or "none"
    host = request.headers.get("Host") or "none"
    return f"scheme: {scheme}\nclient: {client}\nhost: {host}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8002")))