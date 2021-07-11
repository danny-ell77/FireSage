import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "custom-hold-311317-fcf198d7be95.json"

PROJECT_ID = 'custom-hold-311317'
SUBSCRIPTION_ID = 'fire-preds-sub'
MODEL_NAME = 'FireSage'
VERSION_NAME = 'FireSage_v1'
timeout = 700.0


subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

def callback(message):
    print(f"Recieved message: {message}")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"listening for predictions on {subscription_path}... \n")

with subscriber:
    try: 
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
