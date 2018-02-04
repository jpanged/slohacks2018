import io
import os
import json
blockBounds = open("blockBounds.json",'w')
blockContents = open("blockContents.json",'w')

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file("..//slohacks-feb4bf79b42b.json")

# Instantiates a client
client = vision.ImageAnnotatorClient(credentials=credentials)

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'test1.jpg')
    #'..\\images\\test1.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs detection on the image file
response = client.text_detection(image=image)
document = response.full_text_annotation
texts = response.text_annotations
blockBounds.write(str(response))

tupList = []
index = 0;

for response in response.text_annotations:
    x1 = response.bounding_poly.vertices[0].x
    y1 = response.bounding_poly.vertices[0].y
    x2 = response.bounding_poly.vertices[1].x
    y2 = response.bounding_poly.vertices[1].y
    x3 = response.bounding_poly.vertices[2].x
    y3 = response.bounding_poly.vertices[2].y
    x4 = response.bounding_poly.vertices[3].x
    y4 = response.bounding_poly.vertices[3].y

    p1 = (x1, y1)
    p2 = (x2, y2)
    p3 = (x3, y3)
    p4 = (x4, y4)

    c1 = (p1, p2, p3, p4)
    testTuple = (response.description, c1)
    tupList.append(testTuple)
    index += 1



# print(response.text_annotations[0].description)

#print(document.pages.blocks)


# def detect_document(path):
#     """Detects document features in an image."""
#     client = vision.ImageAnnotatorClient(credentials=credentials)
#
#     with io.open(path, 'rb') as image_file:
#         content = image_file.read()
#
#     image = types.Image(content=content)
#
#     # JSON result
#     response = client.document_text_detection(image=image)
#     document = response.full_text_annotation
#
#     for page in document.pages:
#         for block in page.blocks:
#             block_words = []
#             for paragraph in block.paragraphs:
#                 block_words.extend(paragraph.words)
#
#             block_symbols = []
#             for word in block_words:
#                 block_symbols.extend(word.symbols)
#
#             block_text = ''
#             for symbol in block_symbols:
#                 block_text = block_text + symbol.text
#
#             print('Block Content: {}'.format(block_text))
#             print('Block Bounds:\n {}'.format(block.bounding_box))
#             blockContents.write(str(document))
#             blockBounds.write(str(document))
#
#
# detect_document('..\\images\\test1.jpg')
