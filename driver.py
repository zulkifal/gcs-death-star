import concurrent.futures
import urllib.request

URLS = ['https://us-central1-izul-training.cloudfunctions.net/py-death-star'] * 100

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    req = urllib.request.Request(url)
    req.add_header("Authorization", "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImYwNTQxNWIxM2FjYjk1OTBmNzBkZjg2Mjc2NWM2NTVmNWE3YTAxOWUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA3MzMxMDQ2NTM3MjE1MTY4ODg0IiwiaGQiOiJnb29nbGUuY29tIiwiZW1haWwiOiJpenVsQGdvb2dsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6ImZ5SzRDeFFFS3JFLTdYUU9zdElDZGciLCJpYXQiOjE1OTY2OTQ1NjEsImV4cCI6MTU5NjY5ODE2MX0.My2JAk2ujy91K7V5k5okgbcCvD1PJdLWhIxMu1OE5uV7klb8Ce9rQjvCMgfkv8ABsdLGnl14SIC6orVK7g7AOFZPSYCMvyf7WBj6v_yiwTqg3EFXgpFbtrBm4ZZ2j1e8D_ed0mSUETVZeeVIoRrlEjSvK6hPfygQD4KzDnDpGAd77xrWkNf39QgT16MqIkqp-tTlI_KIuoLNK2_HxSdrR1R4FyRu4NFBx7_mvxXXT3s1zoC9uDIvDLWQAnVTie8t0fRrmSvziZGHwpspQJel09GdHw_6HscgIZH8QzEFdMyppdTpttZlz0dYtxomyYA2fU-FWJpZLvR5Ok8_ev3fdw")
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))