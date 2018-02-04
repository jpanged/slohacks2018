import io
import os
import json
import re
# import file

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

from google.oauth2 import service_account

def makeList(filepath):

    credentials = service_account.Credentials.from_service_account_file("..//slohacks-feb4bf79b42b.json")

    # Instantiates a client
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # The name of the image file to annotate
    file_name = os.path.join(os.path.dirname(__file__), filepath)
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
        f.write(json.dumps([{"itemID": mList[0], "itemName": mList[1], "itemPrice": mList[2]} for mList in master_list], indent =4, sort_keys = False))

# list formatted as big list holding lists (or tuples) of size 2,
# each representing an item.
def listToText(list, name):
    total = 0
    s = "Here are the items that you will pay for:\n"
    for(item in list):
        s.append(item[0] + ", you pay " + item[1] + "\n")
        total = item[i] + total
    s.append("Please pay " + name + " $" + total + " on Venmo.\n")
    return s;
