# COPYRIGHT (C) 2018 TT2468 (https://github.com/tt2468) DO NOT USE OR DISTRIBUTE WITHOUT EXPRESSED PERMISSION

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import sys
import logging
import json
from configparser import SafeConfigParser

rtmpconfigfile = 'rtmpconfig.ini'
config = SafeConfigParser()
config.read(rtmpconfigfile)
hostName = config.get('scriptconfig', 'bind_to_ip')
hostPort = config.getint('scriptconfig', 'bind_to_port')
logfile = config.get('scriptconfig', 'log_to_file')
logging.basicConfig(filename=logfile, level=logging.INFO)
sys.path.append('../')

class MyServer(BaseHTTPRequestHandler):
    def _auth_success(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def _auth_fail(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<h1>why hello there general kenobi.</h1>", "utf-8"))
        self.wfile.write(bytes("<h1>------------------</h1>", "utf-8"))
        self.wfile.write(bytes("<h1>you seem to have taken a wrong turn young jedi. you must leave before the the sith finds you.</h1>", "utf-8"))
        print('--------------------')
        ipaddress = self.client_address[0]
        print('GET request recieved from IP: ' + str(ipaddress))
        logging.info('--------------------')
        logging.info('GET request recieved from IP: ' + str(ipaddress))
    def do_POST(self):
        print('--------------------')
        logging.info('--------------------')
        ipaddress = self.client_address[0]
        print('Recieved new auth request from IP: ' + str(ipaddress))
        logging.info('Recieved new auth request from IP: ' + str(ipaddress))
        config.read(rtmpconfigfile)
        sections = config.sections()
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        data = post_data.decode('utf-8')
        params = dict(x.split('=') for x in data.split('&'))
        application = params['app']
        key = params['name']
        if application == 'scriptconfig': # Ignore script config calls
            logging.warning('User tried to call script config')
            return
        if application in sections:
            keys = json.loads(config.get(application, 'streamkeys'))
            if key in keys:
                logging.info('Connection authenticated on application: ' + str(application) + ' and stream key: ' + str(key))
                print('Connection authenticated on application: ' + str(application) + ' and stream key: ' + str(key))
                self._auth_success()
            else:
                logging.warning('User failed to authenticate.')
                print('User failed to authenticate.')
                self._auth_fail()

myServer = HTTPServer((hostName, hostPort), MyServer)
logging.info("Server Starts - %s:%s" % (hostName, hostPort))
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()

except KeyboardInterrupt:
    pass

myServer.server_close()
print('--------------------')
logging.info('--------------------')
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
logging.info("Server Stops - %s:%s" % (hostName, hostPort))
