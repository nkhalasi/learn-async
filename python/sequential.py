import requests
from datetime import datetime as dt

def fetch_pages(urls):
    timings = {}
    for url in urls:
        _, timing = timed_request(url)
        timings[url] = timing
    return timings

def timed_request(url):
    start = dt.now()
    page = fetch_page(url)
    return page, dt.now() - start

def fetch_page(url):
    r = requests.get(url)
    #assert r.status_code == 200
    #return r.text
    return r.text if r.status_code == 200 else None

def main():
    from test_urls import urls
    print(fetch_pages(urls))

if __name__ == "__main__":
    main()
