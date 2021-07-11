from datetime import datetime
from google.cloud import pubsub_v1
import json

PROJECT_ID = 'custom-hold-311317'
TOPIC_ID = 'fire-preds-topic'

def publish(request):
    pred_json = request.get_json()
    print(pred_json)
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    pred_json = json.loads(pred_json)
    pred = pred_json['prediction']
    # data = f'fire prediction: {(1-prediction)*100:2d}'
    data = f"fire prediction: {1-pred}"
    data = data.encode('utf-8')

    future = publisher.publish(topic_path, data)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(pred_json, current_time, type(pred_json))
    return future.result()

