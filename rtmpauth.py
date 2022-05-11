import logging
from aiohttp import web
import sys
import json
from configparser import ConfigParser

configfile = 'config.ini'
config = ConfigParser()
config.read(configfile)
hostName = config.get('main', 'bind_to_ip')
hostPort = config.getint('main', 'bind_to_port')
authfile = config.get('main', 'authentication_file')
logfile = config.get('main', 'log_to_file')
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler(logfile), logging.StreamHandler()])

def read_auth():
    with open(authfile) as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            logging.error('Could not decode JSON authentication file! Exiting...')
            sys.exit()
        return data

async def authhandle(request):
    ipaddress = request.remote
    logging.info('--------------------')
    logging.info('Recieved new auth request from IP: ' + str(ipaddress))
    authtable = read_auth()
    body = await request.post()
    if 'app' in body.keys() and body['app'] in authtable.keys():
        if body['name'] in authtable[body['app']]:
            logging.info('Publish authenticated. (App: {}, Streamname {})'.format(body['app'], body['name']))
            return web.Response(status=200)
        else:
            logging.warning('Publish failed to authenticate. (App: {}, Streamname {})'.format(body['app'], body['name']))
            return web.Response(status=401)
    return web.Response(status=404)

app = web.Application()
app.add_routes([web.post('/auth/', authhandle)])
web.run_app(app, host=hostName, port=hostPort)
