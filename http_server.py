from http.server import HTTPServer, BaseHTTPRequestHandler

class HTTPHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    self.wfile.write(bytes("<html><body><p>You can close this page</p></body></html>", "utf-8"))
  def log_message(self, format, *args):
    return


class HTTP_Server(HTTPServer):
  def run(self):
    try:
      self.serve_forever()
    except KeyboardInterrupt:
      pass
    finally:
      # Clean-up server (close socket, etc.)
      self.server_close()
