import threading
import urllib.request
import argparse

parser = argparse.ArgumentParser(description='GCS death star driver.')
parser.add_argument('--url', required=True, help="http[s]://URL?bucket=BUCKET_NAME&threads=NUM_THREADS&debug=BOOL")
parser.add_argument('--token', help="Provide identity token $(gcloud auth print-identity-token)")

args = parser.parse_args()

results = []
def load_url(url, timeout):
    req = urllib.request.Request(url)
    if args.token:
        req.add_header("Authorization", f"Bearer {args.token}")
    with urllib.request.urlopen(req, timeout=timeout) as conn:
        try:
            print(conn.read())
        except:
            print("Exception encountered.")
def main():
    t_list = []
    for _ in range(1000):
        t = threading.Thread(target=load_url, args=(args.url, 60))
        t_list.append(t)
        t.start()
    for t in t_list:
        t.join()

if __name__ == "__main__":
    main()