# python3 server/server.py -p 8080 -d data-storage/

import http.server
import socketserver
import argparse
import os
import logging

logging.basicConfig(filename='server.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def end_headers(self):
        logging.info('Sending headers: %s' % self.headers)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        super().end_headers()
    
    def do_GET(self):
        logging.info('GET request received: %s' % self.directory)
        super().do_GET()
        
    def do_POST(self):
        logging.info('POST request received: %s' % self.directory)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        response = "Response on your data " + post_data
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def do_OPTIONS(self):
        logging.info('OPTIONS request received: %s' % self.directory)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP server')
    parser.add_argument('-p', '--port', type=int, default=8000, help='Port to listen on')
    parser.add_argument('-d', '--dir', default='.', help='Directory to serve files from')
    args = parser.parse_args()

    os.chdir(args.dir)
    with socketserver.TCPServer(("", args.port), MyHttpRequestHandler) as httpd:
        try:
            print("Server started on port", args.port)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutdown server...")
            httpd.shutdown()  
        except Exception as e:
            logging.info('Server error: %s' % e)
            print("Server error:", e)  
    httpd.server_close()
    print("Server stopped.")
