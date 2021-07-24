import os
from PIL import Image
from numpy import array
from numpy import expand_dims
# import tempfile
import googleapiclient.discovery
# from google.cloud import storage
from PIL import Image

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "bubbly-mantis-311315-d7ae76acdf25.json"


PROJECT_ID = 'bubbly-mantis-311315'
MODEL_NAME = 'FireSage'
VERSION_NAME = 'Xception_v1'

img = Image.open("Images/normal/71x71(norm).jpg")
instance = {}

img_arr = array(img).astype('float32')/255
instance['xception_input'] = img_arr.tolist()

ml = googleapiclient.discovery.build('ml', 'v1')
name = f'projects/{PROJECT_ID}/models/{MODEL_NAME}/versions/{VERSION_NAME}'

response = ml.projects().predict(
    name=name,
    body={
        'instances': [instance, ]
    }
).execute()

print(response)

# prediction = response.predictions[0]
