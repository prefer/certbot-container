import bottle
import subprocess
from bottle import request

app = application = bottle.Bottle()


@app.get('/.well-known/acme-challenge/<filename:path>')
def challenge(filename):
    return bottle.static_file(filename, root='./challenge')


@app.get('/.certs/<filename:path>')
def get_certs(filename):
    return bottle.static_file(filename, root='./certs')


@app.post('/.certs/')
def create_certs():
    domains = request.json.get('domains')
    email = request.json.get('email')

#     result = subprocess.check_call([
#                  "./certbot-auto", "certonly", "--standalone", "--agree-tos"
#
# "--standalone -d foo9.cl-owncloud.pro -n --agree-tos --email ntelepenin@cloudlinux.com --standalone-supported-challenges http-01 -v"
#     ])


if __name__ == '__main__':
    import sys

    port = sys.argv[1]
    bottle.run(app=app,
               host='0.0.0.0',
               port=port)
