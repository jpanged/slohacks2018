import cv2
import os

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    '..\\images\\diamond.jpg')

rotationAngle = 45

img = cv2.imread(file_name)
imgRotated = img
# cv2.imshow('image',file_name)


# print (type(file_name))
'''
#print (type(file_name))
img = cv2.imread(file_name)
rows, cols = img.shape

M = cv2.getRotationMatrix2D((cols/2), rows/2, 90,1)
dst = cv2.warpAffine(img, M, (cols, rows))
# '''

(h,w) = imgRotated.shape[:2]
center = (w / 2, h / 2)
M = cv2.getRotationMatrix2D(center, rotationAngle, 1)
rotated = cv2.warpAffine(img, M, (w, h))
cv2.imshow("original", img)
cv2.imshow("rotated", rotated)

cv2.waitKey(0)
