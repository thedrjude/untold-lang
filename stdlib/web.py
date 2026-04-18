import urllib.request
import urllib.parse
import urllib.error
import json
import threading

class UntoldWeb:
    """untold.web — HTTP, REST & web module"""

    @staticmethod
    def get(url, headers=None):
        try:
            req = urllib.request.Request(url, headers=headers or {})
            req.add_header("User-Agent", "UntoldLang/0.1")
            with urllib.request.urlopen(req, timeout=15) as r:
                body = r.read().decode(errors="replace")
                return {
                    "body":    body,
                    "status":  r.status,
                    "ok":      r.status < 400,
                    "headers": dict(r.headers)
                }
        except urllib.error.HTTPError as e:
            return {"body": str(e), "status": e.code, "ok": False, "headers": {}}
        except Exception as e:
            return {"body": str(e), "status": 0,      "ok": False, "headers": {}}

    @staticmethod
    def post(url, data, headers=None):
        try:
            if isinstance(data, dict):
                payload = json.dumps(data).encode()
                content_type = "application/json"
            else:
                payload = str(data).encode()
                content_type = "text/plain"
            hdrs = {"Content-Type": content_type, "User-Agent": "UntoldLang/0.1"}
            if headers:
                hdrs.update(headers)
            req = urllib.request.Request(url, data=payload, headers=hdrs, method="POST")
            with urllib.request.urlopen(req, timeout=15) as r:
                body = r.read().decode(errors="replace")
                return {"body": body, "status": r.status, "ok": r.status < 400}
        except urllib.error.HTTPError as e:
            return {"body": str(e), "status": e.code, "ok": False}
        except Exception as e:
            return {"body": str(e), "status": 0, "ok": False}

    @staticmethod
    def post_form(url, fields):
        data = urllib.parse.urlencode(fields).encode()
        req  = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("User-Agent", "UntoldLang/0.1")
        with urllib.request.urlopen(req, timeout=15) as r:
            return {"body": r.read().decode(), "status": r.status, "ok": r.status < 400}

    @staticmethod
    def get_json(url, headers=None):
        res = UntoldWeb.get(url, headers)
        try:
            res["json"] = json.loads(res["body"])
        except:
            res["json"] = None
        return res

    @staticmethod
    def download(url, save_path):
        urllib.request.urlretrieve(url, save_path)
        return save_path

    @staticmethod
    def url_encode(text):
        return urllib.parse.quote(str(text))

    @staticmethod
    def url_decode(text):
        return urllib.parse.unquote(str(text))

    @staticmethod
    def parse_json(text):
        return json.loads(text)

    @staticmethod
    def to_json(obj):
        return json.dumps(obj, indent=2)

    @staticmethod
    def serve(port=8080, handler=None):
        """Start a simple HTTP server with a custom handler."""
        from http.server import HTTPServer, BaseHTTPRequestHandler

        user_handler = handler

        class _Handler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                print(f"[untold.web] {self.address_string()} — {format % args}")

            def do_GET(self):
                if user_handler:
                    response = user_handler({
                        "method":  "GET",
                        "path":    self.path,
                        "headers": dict(self.headers),
                        "body":    ""
                    })
                else:
                    response = {"status": 200, "body": "Untold Lang Web Server running!",
                                "content_type": "text/plain"}

                status       = response.get("status", 200)
                body         = response.get("body", "").encode()
                content_type = response.get("content_type", "text/html")

                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", len(body))
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                length = int(self.headers.get("Content-Length", 0))
                body   = self.rfile.read(length).decode()
                if user_handler:
                    response = user_handler({
                        "method":  "POST",
                        "path":    self.path,
                        "headers": dict(self.headers),
                        "body":    body
                    })
                else:
                    response = {"status": 200, "body": "OK"}
                status       = response.get("status", 200)
                out          = response.get("body", "").encode()
                content_type = response.get("content_type", "text/html")
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", len(out))
                self.end_headers()
                self.wfile.write(out)

        srv = HTTPServer(("", int(port)), _Handler)
        print(f"[untold.web] Server running at http://localhost:{port}")
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print("\n[untold.web] Server stopped.")