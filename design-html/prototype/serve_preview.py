"""Local static prototype preview for browser review and parallel audit requests."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path

class PreviewHandler(SimpleHTTPRequestHandler):
    def log_message(self,format,*args):
        pass

def main():
    ThreadingHTTPServer.request_queue_size=128
    root=Path(__file__).resolve().parents[1]
    with ThreadingHTTPServer(('127.0.0.1',8765),partial(PreviewHandler,directory=str(root)))as server:
        server.serve_forever()

if __name__=='__main__':main()
