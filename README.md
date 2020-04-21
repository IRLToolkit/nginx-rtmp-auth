# nginx-rtmp-auth
A Python script that allows you to authenticate RTMP publishers in nginx-rtmp-module.

## Usage:
- Build NGINX with nginx-rtmp-module and see [the example conf](/example-nginx.conf) for how to setup authentication with the script.
- Install dependencies: `python3.7 -m pip install configparser aiohttp`
- 
- Run with `sudo python3.7 rtmpauth.py`

Run with `sudo python3 rtmpauth.py` (Sudo because it needs to bind to a network interface)
