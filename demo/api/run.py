from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

DATA_DIR = Path(__file__).resolve().parent.parent / "public" / "data"
ALLOWED = frozenset({"alert", "ticket", "release", "onboard", "advisory"})


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path not in ("/api/run", "/run"):
            self._json(404, {"error": "not found"})
            return
        trigger = parse_qs(parsed.query).get("trigger", ["alert"])[0].lower().strip()
        if trigger not in ALLOWED:
            self._json(400, {"error": f"invalid trigger; use one of {sorted(ALLOWED)}"})
            return
        path = DATA_DIR / f"{trigger}.json"
        if not path.is_file():
            self._json(404, {"error": f"missing demo data for {trigger}"})
            return
        body = path.read_text(encoding="utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()

    def _json(self, code, obj):
        import json

        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        return
