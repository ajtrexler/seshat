# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 11:16:50 2017

@author: adam
"""

import asana
import hashlib
import Crypto
from Crypto.Cipher import AES
from Crypto import Random

CRYPTO_PATH = '/home/adam/scripts/seshat/crypto/'
SALT_PATH = '/home/adam/codebase/'   
def decryptor(filename,keypass,iv):
    chunk_size = 8192
    cryptor = AES.new(keypass,AES.MODE_CFB,iv)
    with open(filename,'r') as f:
        while True:
            chunk= f.read(chunk_size)
            if len(chunk) == 0:
                break
            return cryptor.decrypt(chunk)

        

## on start-up.
password = raw_input('enter passphrase:')
key = hashlib.sha256(password).digest()
with open(SALT_PATH+'seshat_salts.txt','r') as fid:
    iv=fid.read()   
iv=iv.strip()
token=decryptor(CRYPTO_PATH+'newfile.txt.enc',key,iv)  
token=token.strip()  


client = asana.Client.access_token(str(token))
me = client.users.me()

workspace_id = me['workspaces'][0]['id']

projects = client.projects.find_by_workspace(workspace_id,iterator_type=None)

for project in projects:
    print project['name']
    project_id = project['id']
    project_tasks = client.tasks.find_by_project(project_id,iterator_type=None)
    
    for task in project_tasks:
        task_id=task['id']
    

