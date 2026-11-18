"""Petit serveur local qui reçoit les transcriptions envoyées depuis le navigateur."""
import json, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Access-Control-Allow-Private-Network", "true")
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
        d = json.loads(self.rfile.read(int(self.headers["content-length"])))
        (OUT / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
ThreadingHTTPServer(("127.0.0.1", 8833), H).serve_forever()
