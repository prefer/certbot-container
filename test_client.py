import asyncio
import json
import sys

import aiohttp


async def fetch(session, url, data):
    with aiohttp.Timeout(10):
        async with session.post(
            url,
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        ) as response:
            return await response.text()


def main(url, domains, email):

    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        data = loop.run_until_complete(
            fetch(session, url, {'domains': domains, "email": email}))
        print(json.loads(data))


if __name__ == '__main__':
    # Usage:
    # python3.5 test_client.py http://localhost:8080/.certs/ a.co,c.po a@a.cp
    url = sys.argv[1]
    assert url, 'First parameter equals url and should be define'
    domains = sys.argv[2].split(',')
    assert domains
    email = sys.argv[3]
    assert email
    main(url, domains, email)
