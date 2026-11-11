"""Local static server for FATHER Future Lab."""

from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os


HOST = "127.0.0.1"
PORT = 8771


def main() -> None:
    site = Path(__file__).resolve().parent / "site"
    os.chdir(site)
    server = ThreadingHTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
    print(f"FATHER Future Lab: http://{HOST}:{PORT}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
