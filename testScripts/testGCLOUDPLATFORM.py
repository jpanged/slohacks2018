import io
import os
import json
jsonOutput = open("jsonoutput.json",'w')
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file("C:\\utilities\\slohacks-feb4bf79b42b.json")

# Instantiates a client
client = vision.ImageAnnotatorClient(credentials=credentials)

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    '..\\images\\test1.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.text_detection(image=image)
#labels = response.label_annotations
print(response)
texts = response.text_annotations


print('Text:')
# print(texts)
jsonOutput.write(str(response))
# print('"{}"'.format(texts[0].description))
# for text in texts:
#     print('"{}"'.format(text.description))
