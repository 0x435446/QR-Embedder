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
from Crypto.Random import new as Random
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




def get_steg(image,message,key):
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
    ok=0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if(i>=100 or j>=100):
              if(index<len(val1)):
                x=img[i,j][2]
                y=int(val1[index])
                if(x%2!=y):
                 print "DIFERIT"
                 exit()
                index+=1
    print "Imaginea este valida"

if __name__ == '__main__':
    img=Image.open(sys.argv[1])
    message=sys.argv[2]
    password=sys.argv[3]
    get_steg(img,message,password)


