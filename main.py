import time
import threading
from google.cloud import storage

client = storage.Client()


def worker(bucket_name, debug):
    try:
        # bucket = client.get_bucket(bucket_name)
        bucket = storage.Bucket(client, bucket_name)
    except:
        return None
    # each thread trying to upload 10 objects
    for _ in range(10):
        object_id = f"object.txt-{time.time()}-{threading.get_ident()}"
        # blob = bucket.blob(object_id)
        blob = storage.Blob(object_id, bucket)
        # try to upload, fail silently
        try:
            blob.upload_from_string(
                f"New contents-{time.time()}-{threading.get_ident()}"
            )
            if debug == True:
                print(
                    f"tid: {threading.get_ident()} created gs://{bucket_name}/{object_id}"
                )
        except:
            print("Exception encountered, upload failed.")
            pass


def handle(request):
    t_list = []
    debug = False
    if request.args and "bucket" in request.args:
        bucket = request.args.get("bucket")
    else:
        return f"Usage: http[s]://URL?bucket=BUCKET_NAME&threads=NUM_THREADS&debug=BOOL"

    if request.args and "threads" in request.args:
        n_threads = int(request.args.get("threads"))
    else:
        n_threads = 1000
    
    if request.args and "debug" in request.args:
        debug = True
    
    for _ in range(n_threads):
        t = threading.Thread(target=worker, args=(bucket, debug))
        t.start()
        t_list.append(t)

    for t in t_list:
        t.join()

    return f"Done."
