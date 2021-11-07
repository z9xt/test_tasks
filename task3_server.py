from http.server  import HTTPServer, CGIHTTPRequestHandler
from socketserver import ThreadingMixIn
from threading    import Thread
from http         import HTTPStatus
import cgitb
import sys

if sys.version_info >= (3, 7):
    from http.server import ThreadingHTTPServer
else:
    
    class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
        daemon_threads = True


class Handler8000(CGIHTTPRequestHandler):
    cgi_directories=['/']
    homepage="/index.py"
    def do_GET(self):
        if self.path != self.homepage:
            self.send_response(HTTPStatus.MOVED_PERMANENTLY)
            self.send_header('Location', self.homepage)
            self.end_headers()
        else:
            CGIHTTPRequestHandler.do_GET(self)


class Handler8001(Handler8000):
    homepage="/index2.py"


def serve_on_port(port, Handler):
    try:
        server = ThreadingHTTPServer(("localhost",port), Handler)
        print('Server start on port: %i' % port)
        server.serve_forever()
    except:
        print("Ctrl+C pressed, shutting down server")
    finally:
        server.socket.close()

if __name__=='__main__':
    
    cgitb.enable() # CGI error report
    Thread(target=serve_on_port, args=[8000, Handler8000]).start()
    serve_on_port(8001, Handler8001)
