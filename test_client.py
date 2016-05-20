import asyncio
import json
import logging

import aiohttp

logging.basicConfig(
    format=u'%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG,
    filename=u'client.log')

logger = logging.getLogger(__name__)


async def fetch(session, url, data):
    logger.debug('Request start for "{}"'.format(id(url)))
    async with session.post(
        url,
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    ) as response:
        response = await response.text()
        logger.debug('Request start for "{}"'.format(id(url)))
        return response


def main(params):
    loop = asyncio.get_event_loop()

    with aiohttp.ClientSession(loop=loop) as session:
        tasks = [asyncio.ensure_future(fetch(
            session, 'http://{}/.certs/'.format(domain), {
                'domains': [domain],
                'email': email
            }
        )) for domain, email in params]

        data = loop.run_until_complete(
            asyncio.wait(tasks)
        )
        for i, task in enumerate(tasks):
            print(i, task.result())


def _create_fixtures(prefix, domain, email, n=1):
    """

    :param prefix:
    :param domain:
    :param email:
    :return:
    """
    data = []
    for i in range(n):
        data.append([
            '{prefix}{i}.{domain}'.format(
                prefix=prefix,
                i=i,
                domain=domain),
            email
        ])
    with open('fixtures.json', 'w') as f:
        f.write(
            json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))
        )


if __name__ == '__main__':
    # Usage:
    # python3.5 test_client.py http://localhost:8080/.certs/ a.co,c.po a@a.cp
    with open('fixtures.json', 'r') as f:
        params = json.loads(f.read())

    logger.info('Start requesting')
    main(params)
    logger.info('End requesting')
