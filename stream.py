import os
from datetime import datetime
from google.cloud import storage
from PIL import Image
import cv2 as cv


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "custom-hold-311317-aa296314ddd8.json"

capture = cv.VideoCapture('video/video1.mp4')

storage_client = storage.Client.from_service_account_json("custom-hold-311317-aa296314ddd8.json")
bucket = storage_client.bucket("flamedatastore")

i = 1
while True:
    
    isTrue, frame = capture.read()
    img = cv.resize(frame, (224,224))
    
    pil_image = Image.fromarray(cv.cvtColor(img, cv.COLOR_RGB2BGR))
    # img_bytes = io.BytesIO(img)
    # payload = {'image_bytes': pil_image}
       
    filename = f"tmp/{str(i)}.jpg"
    if i % 10 == 0:
        pil_image.save(filename)
    
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        blob_name = f"cam1-{current_time}.jpg"
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(filename)
        print(f"uploaded {filename} to {blob_name}")
        
    i+=1

    if cv.waitKey(20) & 0xFF==ord('d'):
            break

capture.release()

cv.destroyAllWindows()

'''
The `predictor` is invoked when an image is upoaded to `flamedatastore` through the cloud storage
tigger for cloud functions. On invocation the predictor requests for a prediction on the image 
the prediction is posted to the `publisher` which publishes the prediction to all subscribing 
applications. 
'''
