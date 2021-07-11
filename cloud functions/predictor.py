import requests
import numpy as np
import tempfile
import googleapiclient.discovery
from google.cloud import storage
from PIL import Image

storage_client = storage.Client.from_service_account_json("service_account_json_here")


url = ' https://us-west2-custom-hold-311317.cloudfunctions.net/publish'
PROJECT_ID = 'custom-hold-311317'
TOPIC_ID = 'fire-preds-topic'
MODEL_NAME = 'FireSage'
VERSION_NAME = 'FireSage_v1'

def predict(data, context):
    try:
        file_data = data

        file_name = file_data["name"]
        bucket_name = file_data["bucket"]

        blob = storage_client.bucket(bucket_name).get_blob(file_name)
        
        _, temp_local_filename = tempfile.mkstemp()

        # Download file from bucket.
        blob.download_to_filename(temp_local_filename)

        file_name = blob.name
        print(f"Image {file_name} was downloaded to {temp_local_filename}.")

        img = Image.open(temp_local_filename)
        instance = {}

        instance['input_3'] = np.resize(np.array(img), (224,224,3)).tolist()

        ml = googleapiclient.discovery.build('ml', 'v1')
        name = f'projects/{PROJECT_ID}/models/{MODEL_NAME}/versions/{VERSION_NAME}'

        response = ml.projects().predict(
            name=name,
            body={
                'instances': [instance,]
            }
        ).execute()

            # prediction = response.predictions[0]
        requests.post(url, data=response)
    except Exception as e:
            print('EXCEPTION:', str(e))
            return 'Error processing image', 500

