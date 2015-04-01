import asyncio
import aiohttp
from datetime import datetime as dt

def fetch_pages(urls, loop):
    done_tasks, pending_tasks = loop.run_until_complete(asyncio.wait([timed_request(url) for url in urls]))
    timings = {}
    for task in done_tasks:
        url, _, timing = task.result()
        timings[url] = timing
    return timings

@asyncio.coroutine
def timed_request(url):
    start = dt.now()
    res_details = yield from fetch_page(url)
    return url, res_details, dt.now() - start

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
        x = fetch_pages(urls, loop)
        print(x)
    finally:
        loop.close()

if __name__ == '__main__':
    main()
