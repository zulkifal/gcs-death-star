import threading
import urllib.request
import argparse
import concurrent.futures

parser = argparse.ArgumentParser(description='GCS death star driver.')
parser.add_argument('--url', required=True, help="http[s]://URL?bucket=BUCKET_NAME&threads=NUM_THREADS&debug=BOOL")
parser.add_argument('--token', help="Provide identity token $(gcloud auth print-identity-token)")

args = parser.parse_args()
URLS = [args.url] * 200

def load_url(url, timeout):
    req = urllib.request.Request(url)
    if args.token:
        req.add_header("Authorization", f"Bearer {args.token}")
    with urllib.request.urlopen(req, timeout=timeout) as conn:
        try:
            return conn.read()
        except:
            return "Exception encountered."

with concurrent.futures.ThreadPoolExecutor() as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 200): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print(f'{url} page is {data}')