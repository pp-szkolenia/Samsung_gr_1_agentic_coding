#!/usr/bin/env python3
"""Slides Generator — minimalny serwer HTTP.

Użycie: python3 server.py [port]
Domyślny port: 8080
"""
import json
import sys
import uuid
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).parent
DOCS = HERE / "documents"
STATIC = HERE / "static"
EXAMPLES = HERE / "examples"
DOCS.mkdir(exist_ok=True)

MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".png": "image/png",
}


def _init_examples():
    """Kopiuje przykłady do documents/ jeśli folder jest pusty."""
    if list(DOCS.glob("*.json")):
        return
    if not EXAMPLES.exists():
        return
    for ex_dir in sorted(EXAMPLES.iterdir()):
        if not ex_dir.is_dir():
            continue
        data_file = ex_dir / "data.json"
        if not data_file.exists():
            continue
        try:
            data = json.loads(data_file.read_text("utf-8"))
            doc_id = ex_dir.name[:8]
            now = datetime.now().isoformat(timespec="seconds")
            data.update({"_id": doc_id, "_created": now, "_updated": now})
            (DOCS / f"{doc_id}.json").write_text(
                json.dumps(data, ensure_ascii=False, indent=2), "utf-8"
            )
            print(f"  Załadowano przykład: {ex_dir.name}")
        except Exception as e:
            print(f"  Błąd przykładu {ex_dir.name}: {e}")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"  {self.command} {self.path}")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def send_err(self, status, msg):
        self.send_json({"error": msg}, status)

    def read_body(self):
        n = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(n) if n else b""

    def safe_id(self, doc_id):
        return bool(doc_id) and "/" not in doc_id and ".." not in doc_id

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        p = urlparse(self.path).path.rstrip("/") or "/"

        # API: list all documents
        if p == "/api/documents":
            docs = []
            for f in sorted(DOCS.glob("*.json")):
                try:
                    d = json.loads(f.read_text("utf-8"))
                    docs.append({
                        "id": f.stem,
                        "type": d.get("type", "unknown"),
                        "title": d.get("title", f.stem),
                        "created": d.get("_created", ""),
                        "updated": d.get("_updated", ""),
                    })
                except Exception:
                    pass
            self.send_json(docs)
            return

        # API: get one document
        if p.startswith("/api/documents/"):
            doc_id = p[len("/api/documents/"):]
            if not self.safe_id(doc_id):
                self.send_err(400, "Nieprawidłowe ID")
                return
            f = DOCS / f"{doc_id}.json"
            if not f.exists():
                self.send_err(404, "Nie znaleziono dokumentu")
                return
            self.send_json(json.loads(f.read_text("utf-8")))
            return

        # Static files
        rel = p.lstrip("/") or "index.html"
        fp = STATIC / rel
        if not fp.exists() or not fp.is_file():
            fp = STATIC / "index.html"
        if not fp.exists():
            self.send_err(404, "Nie znaleziono")
            return
        body = fp.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", MIME.get(fp.suffix.lower(), "application/octet-stream"))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        p = urlparse(self.path).path.rstrip("/")
        if p != "/api/documents":
            self.send_err(404, "Nie znaleziono")
            return
        try:
            data = json.loads(self.read_body())
        except json.JSONDecodeError:
            self.send_err(400, "Nieprawidłowy JSON")
            return
        doc_id = uuid.uuid4().hex[:8]
        now = datetime.now().isoformat(timespec="seconds")
        data.update({"_id": doc_id, "_created": now, "_updated": now})
        (DOCS / f"{doc_id}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), "utf-8"
        )
        self.send_json(data, 201)

    def do_PUT(self):
        p = urlparse(self.path).path.rstrip("/")
        if not p.startswith("/api/documents/"):
            self.send_err(404, "Nie znaleziono")
            return
        doc_id = p[len("/api/documents/"):]
        if not self.safe_id(doc_id):
            self.send_err(400, "Nieprawidłowe ID")
            return
        f = DOCS / f"{doc_id}.json"
        if not f.exists():
            self.send_err(404, "Nie znaleziono dokumentu")
            return
        try:
            data = json.loads(self.read_body())
        except json.JSONDecodeError:
            self.send_err(400, "Nieprawidłowy JSON")
            return
        existing = json.loads(f.read_text("utf-8"))
        now = datetime.now().isoformat(timespec="seconds")
        data.update({
            "_id": doc_id,
            "_created": existing.get("_created", now),
            "_updated": now,
        })
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
        self.send_json(data)

    def do_DELETE(self):
        p = urlparse(self.path).path.rstrip("/")
        if not p.startswith("/api/documents/"):
            self.send_err(404, "Nie znaleziono")
            return
        doc_id = p[len("/api/documents/"):]
        if not self.safe_id(doc_id):
            self.send_err(400, "Nieprawidłowe ID")
            return
        f = DOCS / f"{doc_id}.json"
        if not f.exists():
            self.send_err(404, "Nie znaleziono dokumentu")
            return
        f.unlink()
        self.send_json({"deleted": doc_id})


if __name__ == "__main__":
    _init_examples()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    server = HTTPServer(("", port), Handler)
    print(f"✅  Slides Generator → http://localhost:{port}  (Ctrl+C aby zatrzymać)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nZatrzymano.")
