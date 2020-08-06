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
        bucket = "py-izul-bucket"

    if request.args and "threads" in request.args:
        n_threads = int(request.args.get("threads"))
    else:
        n_threads = 1000
    if request.args and "debug" in request.args:
        debug = True
    for _ in range(n_threads):
        t_list.append(threading.Thread(target=worker, args=(bucket, debug)))

    for t in t_list:
        t.start()

    for t in t_list:
        t.join()

    return f"Done."
