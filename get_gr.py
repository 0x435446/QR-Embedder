from PIL import Image
import cv2
import numpy as np
import sys
import time



im = Image.open('result.png')
pixelMap = im.load()

img = Image.new( im.mode, (90,90),'white')
pixelsNew = img.load()
x=0
y=0
for i in range(5,95):
    for j in range(5,95):
            pixelsNew[i-5,j-5] = pixelMap[i,j]
img.save("qr.png")

image = cv2.imread("qr.png")
qrDecoder = cv2.QRCodeDetector()

data,bbox,rectifiedImage = qrDecoder.detectAndDecode(image)
if len(data)>0:
    print data
else:
    print("QR inexistent!")

