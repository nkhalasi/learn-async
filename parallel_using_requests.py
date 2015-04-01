import asyncio
import requests
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
    try:
        response = requests.get(url)
        assert response.status_code == 200
        return response.text
    except requests.exceptions.ConnectionError as ce:
        return None

def main():
    from test_urls import urls
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        x = fetch_pages(urls, loop)
        print(x)
    finally:
        loop.close()

if __name__ == '__main__':
    main()
