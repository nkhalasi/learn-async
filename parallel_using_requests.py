import asyncio
import requests
from datetime import datetime as dt

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
    res_details = yield from fetch_page(url)
    return res_details, dt.now() - start

@asyncio.coroutine
def fetch_page(url):
    response = requests.get(url)
    assert response.status_code == 200
    return response.text

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
