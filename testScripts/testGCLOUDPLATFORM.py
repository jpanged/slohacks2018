import io
import os
import json
import re
#import file

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

#print(response.text_annotations[0].description)

#Full string of data
t = response.text_annotations[0].description

#print (t)

#Removes everything before phone #
r = re.search('([0-9]|\s]*)[0-9|\s]*-[0-9|\s]*', t)
i = r.end(0)

t = t[i+1:]

#Removes everything after subtotal
r = re.search('\n[S]*[U]*[B]*[T]*[O]*[T]*[A]*[L]*\n', t)
i = r.start(0)

t = t[:i]

# Splitting data into 3 components
#Item # and Item names
r = re.findall('\n[0-9]+\s.+', t) # might need to remove \n for other OS in deployment

no_and_names = []
for p in r:
    no_and_names.append(p)

#Item price
item_prices = []
r = re.findall('[0-9]+\.[0-9]+', t)
for p in r:
    item_prices.append(p)

#print (item_prices)

item_nos = []
item_names = []
for element in no_and_names:
    i = element.find(' ')
    item_nos.append(element[1:i])
    item_names.append(element[i + 1:])

#print(item_nos)
#print(item_names)
#print(item_prices)
item_nos.extend(['0', '0', '0'])
item_names.extend(['SUBTOTAL', 'TAX', 'TOTAL'])
#print (type(item_prices[-2]))
#item_prices.append(sum(float(item_prices[-2]), float(item_prices[-1])))

master_list = []
min_length = min([len(item_nos), len(item_names), len(item_prices)])
for i in range(0, min_length):
    master_list.append((item_nos[i], item_names[i], item_prices[i]))

#print(master_list)
with open('masterData.json', 'w') as f:
#file = FILE("masterData.json", "w")
    f.write(json.dumps([{"itemID": mList[0], "itemName": mList[1], "itemPrice": mList[2]} for mList in master_list], indent =4, sort_keys = False))
#print(json.dumps([{"itemID": mList[0], "itemName": mList[1], "itemPrice": mList[2]} for mList in master_list], indent =4, sort_keys = False))






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
