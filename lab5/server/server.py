import http.server
import socketserver
import argparse
import os


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', 'https://my-cool-site.com')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Origin', 'https://my-cool-site.com')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP server')
    parser.add_argument('-p', '--port', type=int, default=8000, help='Port to listen on')
    parser.add_argument('-d', '--dir', default='.', help='Directory to serve files from')
    args = parser.parse_args()

    os.chdir(args.dir)
    try:
        with socketserver.TCPServer(("", args.port), MyHttpRequestHandler) as httpd:
            print("Server started on port", args.port)
            httpd.serve_forever()
    except Exception:
        httpd.shutdown()