#!/usr/bin/python

import sys
from PIL import Image
import qrcode
import numpy as np
import cv2
import os
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long
from base64 import b64encode,b64decode

class AESCipher:
  def __init__(self,data,key):
    self.block_size = 16
    self.data = data
    self.key = sha256(key.encode()).digest()[:32]
    self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr (self.block_size - len(s) % self.block_size)
    self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

  def encrypt(self):
    plain_text = self.pad(self.data)
    cipher = AES.new(self.key,AES.MODE_ECB)
    return cipher.encrypt(plain_text.encode())





def watermarking(imgBaza, imgMarca, numBits):
  imgBazaMarca = imgBaza.copy()
  imgBazaMarca = imgBazaMarca//(2**(8-numBits))
  imgBazaMarca = imgBazaMarca*(2**(8-numBits))
  imgBazaMarca = imgBazaMarca + imgMarca//(2**numBits)
  return imgBazaMarca



def paste_qr(image1,image2,x,y):
    image = Image.new( 'RGB', (image1.size[0],image1.size[1]),(255, 0, 0, 0))
    img=image.load()
    img1=image1.load()
    img2=image2.load()
    for i in range(image2.size[0]):
        for j in range(image2.size[1]):
            if(img2[i,j]<10):
                img[i,j]=img2[i,j]
            else:
                img[i,j]=(255,255,255)
    for i in range(image1.size[0]):
        for j in range(image1.size[1]):
            if(i>=image2.size[0] or j>=image2.size[1]):
                img[i,j]=img1[i,j]
    return image



def add_watermark(image, result, qr, position):
    imagine = Image.open(image)
    imagine=paste_qr(imagine,qr,100,100)
    imagine.show()
    imagine.save(result)


def add_steg(image,message,key):
    img=image.load()
    message+="_SECRET"
    message=sha256(message).hexdigest()
    cipher = AESCipher(message,key)
    val=cipher.encrypt() 
    val=bytes_to_long(val)
    val1=bin(val)
    while(len(val1)%8!=0):
     val1="0"+val1
    val1=val1.replace('b','')
    index=0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if(i>=100 or j>=100):
              if(index<len(val1)):
                ok=1
                x=img[i,j][2]
                y=int(val1[index])
                if(x%2==y):
                 ok=1
                else:
                 ok=0
                if(ok==0):
                 if(x==0):
                  x+=1
                 else:
                  x-=1
                #print img[i,j][2],
                z=list(img[i,j])
                z[2]=x
                img[i,j]=tuple(z)
                #print img[i,j][2],y
                index+=1
    image.save("res_stego.png")
if __name__ == '__main__':
    qr = qrcode.QRCode()
    qr.add_data(sys.argv[2])
    qr.make()
    qr = qr.make_image()
    qr = qr.resize((100,100), Image.ANTIALIAS)
    img=sys.argv[1]
    add_watermark(img, img+'_watermarked.png', qr, position=(0,0))

    qr.save("qrimg.png")
    name=img+'_watermarked.png'

    imagine = Image.open(str(sys.argv[1]))
    qr_LSB=paste_qr(imagine,qr,100,100)
    qr_LSB.save("blank.png")

    imgMarca = cv2.imread('blank.png')
    imgBaza = cv2.imread(name, cv2.IMREAD_UNCHANGED)
    numBits = 5
    imgBazaMarca = np.zeros(imgBaza.shape, np.uint8)
    imgBazaMarca[:,:,0] = watermarking(imgBaza[:,:,0], imgMarca[:,:,0], numBits)
    imgBazaMarca[:,:,1] = watermarking(imgBaza[:,:,1], imgMarca[:,:,1], numBits)
    imgBazaMarca[:,:,2] = watermarking(imgBaza[:,:,2], imgMarca[:,:,2], numBits)
    os.system("rm qrimg.png")
    os.system("rm blank.png")
    os.system("rm "+name)
    cv2.imwrite( 'result.png', imgBazaMarca );
    
    imagine = Image.open('result.png')
    add_steg(imagine,sys.argv[3],sys.argv[4])
    





