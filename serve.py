#!/usr/bin/env python3
"""Lokale preview zoals op Vercel: /dakwerken serveert dakwerken.html, onbekende adressen krijgen 404.html met status 404.
Gebruik: python3 serve.py  (daarna http://localhost:8000)"""
import http.server, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)

    def send_head(self):
        pad = self.path.split("?")[0].split("#")[0]
        if pad != "/" and not os.path.splitext(pad)[1] and (ROOT / (pad.strip("/") + ".html")).exists():
            self.path = pad.rstrip("/") + ".html"
        elif not (ROOT / pad.lstrip("/")).exists() and pad != "/":
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            return open(ROOT / "404.html", "rb")
        return super().send_head()


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("", 8000), Handler).serve_forever()
