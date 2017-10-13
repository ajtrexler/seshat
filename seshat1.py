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
import pymongo
import ConfigParser

CONFIG_PATH = '/home/adam/scripts/seshat/config.txt'
config = ConfigParser.ConfigParser()
config.readfp(open(CONFIG_PATH))

CRYPTO_PATH = config.get('seshat1 config','crypto_path')
SALT_PATH = config.get('seshat1 config','salt_path')
CRYPTO_NAME = config.get('seshat1 config','crypto_file')

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
token=decryptor(CRYPTO_PATH+CRYPTO_NAME,key,iv)  
token=token.strip()  


client = asana.Client.access_token(str(token))
me = client.users.me()

workspace_id = me['workspaces'][0]['id']

projects = client.projects.find_by_workspace(workspace_id,iterator_type=None)
print 'welcome', me['name']

all_tasks=[]
for project in projects:
    print project['name']
    project_id = project['id']
    project_tasks = client.tasks.find_by_project(project_id,iterator_type=None)
    
    for task in project_tasks:
        all_tasks.append(task['id'])

#check all_tasks against DB 
#get info and make DB entry for new tasks.

#read 
for task in all_tasks:
    client.tasks.find_by_id(task)
    


def newTask(tid):
    task_info = client.tasks.find_by_id(tid)
    task_info['name']
    task_info['projects']
    task_info['due_on']
    task_info['created_at']
    task_info['completed_at']
    task_info['completed']
    task_info['assignee']
    task_info['type']
    
    
    

