import http.server
import socketserver
import requests
import threading

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/'
        
        try:
            response = requests.get(f'http://localhost:5000{self.path}')
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                if key.lower() not in ['content-length', 'transfer-encoding']:
                    self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response.content)
        except Exception as e:
            self.send_error(500, str(e))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            response = requests.post(f'http://localhost:5000{self.path}',
                                   data=post_data,
                                   headers=dict(self.headers))
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                if key.lower() not in ['content-length', 'transfer-encoding']:
                    self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response.content)
        except Exception as e:
            self.send_error(500, str(e))

def start_proxy():
    with socketserver.TCPServer(('0.0.0.0', 8080), ProxyHandler) as httpd:
        print('Proxy server running on port 8080')
        httpd.serve_forever()

if __name__ == '__main__':
    start_proxy()
