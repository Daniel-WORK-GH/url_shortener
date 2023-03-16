from http.server import HTTPServer, BaseHTTPRequestHandler
import database as db
import linkdata as link
import validators
import urllib.parse
from config import WEBSITE_DOMAIN

HTML = """
<head>
</head>

<body>
    <h1>Shorten url</h1>

    <form method="post">
        <label name="button1" value="Button1">Full url :</label>
        <input type="text" id="full_link" name="full_link"><br><br>
        <input type="submit"/>
    </form>

    <p>{short_link}</p>
</body>
"""

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def check_redirect(self):
        arr = self.path.split('/')
        arr = list(filter(lambda x: x.strip() != '', arr))

        if len(arr) > 0:
            file = arr[-1]

            if file == 'favicon.ico':
                return False

            if len(arr) > 1:
                self.send_response(404)
                return True
              
            site_redirect = db.get_original_url(file)
            if not site_redirect:
                self.send_response(404)
                return True
            
            self.send_response(302)
            self.send_header('Location', site_redirect.full_link)
            self.end_headers()
            return True
        return False
    
    def do_GET(self):
        if self.check_redirect():
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(HTML.format(short_link="").encode())

    def do_POST(self):
        if self.check_redirect():
            return

        #send response after call
        self.send_response(200)
        self.end_headers()
    
        #get data from header
        content_length = int(self.headers['Content-Length'])
        data_input = bytes.decode(self.rfile.read(content_length))
        site_name = data_input.split('=')[1]
        url = urllib.parse.unquote(site_name)

        if validators.url(url):
            linkdata = db.get_value(url)
            if not linkdata:
                linkdata = db.generate_value(url)
            db.save_changes()
        else:
            linkdata = link.Linkdata("ERROR", "Invalid url.")

        #send html data back
        self.wfile.write(HTML.format(short_link=f"{WEBSITE_DOMAIN}/{linkdata.shortened}").encode())

server = WEBSITE_DOMAIN.split(':')
host = server[0]
port = int(server[1])

httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
httpd.serve_forever()
