import asyncio
import aiohttp
from datetime import datetime as dt
from contextlib import closing

@asyncio.coroutine
def fetch_urls(urls):
    timings = {}
    for url in urls:
        _, timing = yield from timed_request(url)
        timings[url] = timing
    return timings

@asyncio.coroutine
def timed_request(url):
    start = dt.now()
    #print('Invoking async call to fetch {}'.format(url))
    res_details = yield from fetch_page(url)
    #print('Done fetching {0}'.format(url))
    return res_details, dt.now() - start

@asyncio.coroutine
def fetch_page(url):
    response = yield from aiohttp.request('GET', url)
    assert response.status == 200
    return (yield from response.read())

def main():
    urls = ('http://www.google.com', 'http://www.yahoo.com', 'http://www.bing.com', 'http://www.google.co.in')
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        x = loop.run_until_complete(fetch_urls(urls))
        print(x)
    finally:
        loop.close()

if __name__ == '__main__':
    main()
