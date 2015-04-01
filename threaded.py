import requests
import concurrent.futures
from datetime import datetime as dt

def fetch_pages(urls):
    timings = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(timed_request, url): url for url in urls}
        for f in concurrent.futures.as_completed(future_to_url.keys()):
            url = future_to_url[f]
            try:
                _, timing = f.result()
                timings[url] = timing
            except Exception as exc:
                print('{0} generated an exception: {1}'.format(url, exc))
    return timings   

def timed_request(url):
    start = dt.now()
    page = fetch_page(url)
    return page, dt.now() - start

def fetch_page(url):
    r = requests.get(url)
    assert r.status_code == 200
    return r.text

def main():
    from test_urls import urls
    print(fetch_pages(urls))

if __name__ == "__main__":
    main()
