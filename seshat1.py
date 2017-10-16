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
from pymongo import MongoClient
from datetime import datetime
from sys import argv
import random
import time
import getpass

CONFIG_PATH = '/home/adam/scripts/seshat/config.txt'
config = ConfigParser.ConfigParser()
config.readfp(open(CONFIG_PATH))

CRYPTO_PATH = config.get('seshat1 config','crypto_path')
SALT_PATH = config.get('seshat1 config','salt_path')
CRYPTO_NAME = config.get('seshat1 config','crypto_file')
DB_PATH = config.get('seshat1 config','mongodb_path')
dbName = config.get('seshat1 config','mongodb_name')
OUTPUT_PATH = config.get('seshat1 config','output_path')






def decryptor(filename,keypass,iv):
    chunk_size = 8192
    cryptor = AES.new(keypass,AES.MODE_CFB,iv)
    with open(filename,'r') as f:
        while True:
            chunk= f.read(chunk_size)
            if len(chunk) == 0:
                break
            return cryptor.decrypt(chunk)

def checkAsana():   

    ## on start-up.
    password = getpass.getpass('enter passphrase:')
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
        #print project['name']
        project_id = project['id']
        project_tasks = client.tasks.find_by_project(project_id,iterator_type=None)
        
        for task in project_tasks:
            all_tasks.append(task['id'])
    return client, all_tasks

def updateAsana(client,db):
    masterTasks = db.masterTasks
    comTasks=0
    for t in masterTasks.find({'type':'asana','completed':''}):
        
        fTask = client.tasks.find_by_id(t['_id'])
        
        if fTask['completed']==True:

            masterTasks.update_one({'_id':t['_id']},{'$set':{'completed':'True',
                                                                'completed_on':t['completed_at']
                                                                }}) 
            comTasks+=1
    print comTasks,'completed tasks!'                                                
    


def newTask(tid,sysflag,db,task_info=None):
    newDoc={}
    if sysflag=='asana':
        time.sleep(1)
        task_info = client.tasks.find_by_id(tid)
        newDoc['type']='asana'
        newDoc['_id']=tid
        newDoc['name']=task_info['name']
        newDoc['projects']=task_info['projects']
        try:
            newDoc['due_on']=task_info['due_on'][0:10]
        except:
            newDoc['due_on']=''

        newDoc['created_at']=task_info['created_at'][0:10]
        try:
            newDoc['completed_at']=task_info['completed_at'][0:10]
            newDoc['completed']=task_info['completed']
        except: 
            newDoc['completed_at']=''
            newDoc['completed']=''
        
        newDoc['assignee']=task_info['assignee']
        
    else:
        newDoc=task_info
        #print newDoc
        newDoc['type']=sysflag
        timestamp=datetime.strftime(datetime.now(),'%Y-%m-%d')
        newDoc['created_at']=timestamp
        newDoc['completed']=''
        newDoc['_short_id']=str(newDoc['_id'])[0:4]
   
    masterTasks = db.masterTasks
    masterTasks.insert_one(newDoc)
    
    #return flag or log msg for successful DB entry.

def checkDB(db,tasks,sysflag,task_info=None):
#check DB over Asana entries to update from API.
#if new Asana tasks present, then update in DB. 
    masterTasks = db.masterTasks
    for t in tasks:
        if masterTasks.find_one({'_id':t}):
            #print 'old task.'
            continue
        elif task_info==None:
            newTask(t,sysflag,db)


def updateTXT(db,sysflag=None):
    if sysflag!=None:
        masterTasks = db.masterTasks
        tl=[]
        for i in masterTasks.find({'type':sysflag,'completed':''}):
            tl.append(str(i['_short_id'])+':   '+str(i['text']))
            
        try:
            with open(OUTPUT_PATH+sysflag+'.txt','w') as fid:
                for item in tl:
                    fid.write('%s\n' % str(item))
        except:
            print 'likely todo or idea file open; try again.'
        
        
    
def getArgs(argv):
    args = {}
    while argv:
        if argv[0][0] == '-':
            args[argv[0]]=argv[1]
        argv=argv[1:]
    return args
    
def main(argflag,argcheck,entry=None):
    #argflag denotes type of entry (idea,todo,finance)
    #argcheck denotes if the task is done.
    #entry is text to add to DB for each  task.
    global client
    client, all_tasks = checkAsana()
    #fire up mongodb.
    themongo = MongoClient()
    db = themongo[dbName]
    checkDB(db,all_tasks,'asana')
    if datetime.now().minute % 3==0:
        updateAsana(client,db) #call func to check for completed asana tasks approx 1/3 of time.
        
    if argcheck!=None:
        try:
            todolist=[]
            with open(OUTPUT_PATH+argflag+'.txt','r') as fid:
                for i,f in enumerate(fid.readlines()):
                    print '{x}.  '.format(x=i+1),f
                    todolist.append(f)
            selection = 0
            tries=0
            while selection<1 and tries<5:
                selection=int(raw_input('enter number of {x} to delete: '.format(x=argflag)))
                if selection > i+1:
                    selection=0
                    tries+=1
            masterTasks = db.masterTasks
            masterTasks.update_one({'_short_id':str(todolist[selection-1])},{'$set':{'completed':'yes',
                                                                'completed_on':datetime.strftime(datetime.now(),'%Y-%m-%d')
                                                                }})
        except:
            print 'no {x} file found or could not open!'.format(x=argflag)
            exit
            
    elif argflag=='idea' or argflag=='todo':
 
        #newIdea entered; make DB entry.
        newIdea={}
        newIdea['_id']=int(random.random()*10**15)
        newIdea['text']=entry
        newTask(newIdea['_id'],argflag,db,newIdea)
        #call func to update output text files.
    elif argflag=='fin':
        print 'finance is a todo.'
    elif argflag!=None:
        print 'unknown argument, try again.'
    
    updateTXT(db,argflag) 


    
if __name__=='__main__':
    
    args = getArgs(argv)
    if '-t' in args.keys():
        argflag=args['-t'] #argflag indicates idea/todo/fin
    else:
        argflag=None
    if '-d' in args.keys():
        argcheck=1 #1 is flag that an item is deleted
    else:
        argcheck=None
        
    if '-e' in args.keys():
        entry=args['-e'] #entry is text for new idea/todo/fin
    else:
        entry=None
          
    main(argflag,argcheck,entry)
        
        
        

        
    
    
    
    
    
