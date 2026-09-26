import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from harborstay.api import encode, get_reservation, health, post_confirm, post_reservation
from harborstay.store import Store

STORE = Store()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._send(*health())
            return
        if self.path.startswith("/reservations/"):
            parts = self.path.strip("/").split("/")
            if len(parts) == 2:
                self._send(*get_reservation(STORE, parts[1]))
                return
        self._send(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        body = json.loads(raw.decode("utf-8") or "{}")
        if self.path == "/reservations":
            self._send(*post_reservation(STORE, body))
            return
        parts = self.path.strip("/").split("/")
        if len(parts) == 3 and parts[0] == "reservations" and parts[2] == "confirm":
            key = self.headers.get("Idempotency-Key", "")
            self._send(*post_confirm(STORE, parts[1], key))
            return
        self._send(404, {"error": "not found"})

    def _send(self, status, payload):
        data = encode(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        return


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8080), Handler)
    print("Harbor Stay listening on http://127.0.0.1:8080 (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.shutdown()


if __name__ == "__main__":
    main()
