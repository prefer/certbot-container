import asyncio
import json
import logging
import sys
from uuid import uuid4

import aiohttp

logging.basicConfig(
    format=u'%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG,
    filename=u'client.log')

logger = logging.getLogger(__name__)


async def fetch(session, url, data, seconds):
    await asyncio.sleep(seconds)
    print('run with {}'.format(seconds))
    with aiohttp.Timeout(180):
        async with session.post(
            url,
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        ) as response:
            response = await response.text()
            return response


def main(params):
    loop = asyncio.get_event_loop()

    with aiohttp.ClientSession(loop=loop) as session:
        total = len(params)
        # 2 sec delay between tasks  - experimental
        coefficient = 2 * total
        tasks = [asyncio.ensure_future(fetch(
            session, 'http://{}/.certs/'.format(domain), {
                'domains': [domain],
                'email': email,
                'certbot-additional-params': [
                    '-v',
                    '--staging'
                ]
            }, i * 1.0 / total * coefficient
        )) for i, (domain, email) in enumerate(params)]

        loop.run_until_complete(
            asyncio.wait(tasks)
        )
        for i, task in enumerate(tasks):
            print(i, task.result())


def _create_fixtures(prefix, domain, email, n=1):
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
    # python3.5 test_client.py a cl-owncloud.pro ntelepenin@cloudlinux.com 5
    prefix = sys.argv[1]
    domain = sys.argv[2]
    email = sys.argv[3]
    n = sys.argv[4]

    assert prefix
    assert domain
    assert email

    _create_fixtures(
        '{}-{}-'.format(prefix, str(uuid4())[:8]),
        '{}'.format(domain),
        '{}'.format(email),
        int(n)
    )
    with open('fixtures.json', 'r') as f:
        params = json.loads(f.read())

    logger.info('Start requesting')
    main(params)
    logger.info('End requesting')
