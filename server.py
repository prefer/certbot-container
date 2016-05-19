import base64
import itertools
import os
import subprocess

import bottle
from bottle import request

app = application = bottle.Bottle()


@app.get('/.well-known/acme-challenge/<filename:path>')
def challenge(filename):
    """
    Acme challenge for letsencrypt
    https://letsencrypt.github.io/acme-spec/

    :param filename:
    :return:
    """
    return bottle.static_file(
        filename,
        root=os.path.join('./challenge', '.well-known', 'acme-challenge'))


# If need to get certs uncomment below
# @app.get('/.certs/')
# def get_certs():
#     domain = request.query.get('domain')
#     assert domain
#
#     cert, privkey = _get_certs(domain)
#     return {
#         'cert': cert,
#         'privkey': privkey
#     }


@app.post('/.certs/')
def create_certs():
    """
    Create certificate by letsencrypt for list of domains

    :return:
    """
    domains = request.json.get('domains')
    email = request.json.get('email')
    assert domains, "List of domains should be define"
    assert isinstance(domains, list), "Domains should be list"
    assert email, "Email should be define"

    result = subprocess.check_call(
        [
            '/opt/certbot/certbot-auto',
            'certonly',
            '--webroot',
            '--no-self-upgrade',
            '--agree-tos',
            '-n',
            '-w', 'challenge/',
            '--email', email
        ] + [item for sublist in itertools.product(['-d'], domains)
             for item in sublist]
    )
    if result != 0:
        raise SystemExit("Script ended with errors")

    # Folder with certs created by default for first domain
    cert, privkey = _get_certs(domains[0])
    return {
        'cert': cert,
        'privkey': privkey
    }


def _get_certs(domain):
    """
    Return base64 cert and private key from default location for store of
    certbot

    :param domain: domain for cert
    :return: tuple base64 encoded cert and private key files
    """
    certs_path = os.path.join('/etc', 'letsencrypt', 'live', domain)
    with open(os.path.join(certs_path, 'cert.pem'), 'r') as f:
        cert = base64.b64encode(f.read())

    with open(os.path.join(certs_path, 'privkey.pem'), 'r') as f:
        privkey = base64.b64encode(f.read())

    return cert, privkey


if __name__ == '__main__':
    import sys

    port = sys.argv[1]
    assert port, "Port should be define"
    bottle.run(
        app=app,
        host='0.0.0.0',
        port=port)
