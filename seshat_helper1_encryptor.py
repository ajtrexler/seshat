# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 16:13:01 2017

@author: adam
"""

from Crypto.Cipher import AES
from Crypto import Random
import hashlib


def encryptor(filename,keypass,iv):
    chunk_size = 8192
    cryptor = AES.new(keypass,AES.MODE_CFB,iv)
    with open(filename,'r') as f:
        with open(filename+'.enc','w') as outfile:
            while True:
                chunk = f.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk+= ' ' * (16-len(chunk)%16)
                outfile.write(cryptor.encrypt(chunk))

def decryptor(filename,keypass,iv):
    chunk_size = 8192
    cryptor = AES.new(keypass,AES.MODE_CFB,iv)
    with open(filename,'r') as f:
        with open(filename+'.plain','w') as outfile:
            while True:
                chunk= f.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(cryptor.decrypt(chunk))

password = raw_input('enter passphrase:')
key = hashlib.sha256(password).digest()
targetFile= '/home/adam/Desktop/newfile.txt'
iv = Random.get_random_bytes(16)
encryptor(targetFile,key,iv) 

with open('/home/adam/Desktop/seshat_salts.txt','a') as fid:
    fid.write(iv)

decryptor('/home/adam/Desktop/newfile.txt.enc',key,iv)    

      

