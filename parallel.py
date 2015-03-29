import asyncio
import aiohttp
from datetime import datetime as dt

@asyncio.coroutine
def fetch_urls(urls):
	timings = {}
	for url in urls:
		site, timing = yield from timed_request(url)
		timings[site] = timing
	return timings

@asyncio.coroutine
def timed_request(url):
	start = dt.now()
	print('Invoking async call to fetch {}'.format(url))
	res_details = yield from fetch_page(url)
	print('Done fetching {0}'.format(url))
	return (url, dt.now() - start)

@asyncio.coroutine
def fetch_page(url):
    response = yield from aiohttp.request('GET', url)
    assert response.status == 200
    return (yield from response.read())

def main():
	loop = asyncio.get_event_loop()
	try:
		x = loop.run_until_complete(
			fetch_urls(
				('http://www.yahoo.com', 
	    		'http://www.google.com',
				'http://www.bing.com')
			))
		print(x)
	finally:
		loop.close()

if __name__ == '__main__':
	main()