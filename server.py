import asyncio
import base64
import itertools
import json
import logging
import os
import subprocess
import sys

from aiohttp import web

logging.basicConfig(
    format=u'%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG,
    filename=u'server.log')

logger = logging.getLogger(__name__)


async def create_certs(request):
    """
    Create certificate by letsencrypt for list of domains

    :return:
    """
    logger.debug("Start request with id '{}'".format(id(request)))
    data = await request.json()
    domains = data.get('domains')
    email = data.get('email')

    assert domains, "List of domains should be define"
    assert isinstance(domains, list), "Domains should be list"
    assert email, "Email should be define"

    additional_params = data.get('certbot-additional-params', [])

    process = await asyncio.create_subprocess_exec(
        *[
             '/opt/certbot/certbot-auto',
             'certonly',
             '--webroot',
             '--no-self-upgrade',
             '--agree-tos',
             '-n',
             '-w', 'challenge/',
             '--email', email
         ] + [item for sublist in itertools.product(['-d'], domains)
              for item in sublist] + additional_params,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    await process.communicate()

    if process.returncode != 0:
        raise SystemExit("Script ended with errors")

    # Folder with certs created by default for first domain
    cert, private_key = await _get_certs(domains[0])

    logger.debug("Finish with id '{}'".format(id(request)))
    return web.Response(body=json.dumps({
        'cert': cert,
        'private_key': private_key
    }).encode('utf-8'), content_type='application/json')


async def _get_certs(domain):
    """
    Return base64 cert and private key from default location for store of
    certbot

    :param domain: domain for cert
    :return: tuple base64 encoded cert and private key files
    """
    certs_path = os.path.join('/etc', 'letsencrypt', 'live', domain)
    with open(os.path.join(certs_path, 'cert.pem'), 'rb') as f:
        cert = base64.b64encode(f.read()).decode("utf-8")

    with open(os.path.join(certs_path, 'privkey.pem'), 'rb') as f:
        private_key = base64.b64encode(f.read()).decode("utf-8")

    return cert, private_key


app = web.Application()
app.router.add_static(
    prefix='/.well-known/acme-challenge/',
    path='/opt/certbot/challenge/.well-known/acme-challenge/', )
app.router.add_route(
    'POST', '/.certs/', create_certs)

if __name__ == '__main__':
    logger.info("Start server")
    port = sys.argv[1]
    assert port
    web.run_app(app, port=int(port))
    logger.info("Finish server")
