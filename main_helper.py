# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 13:47:40 2017

@author: adam
"""
import random
from sys import argv

def main():
    print 'blah main sep func.'
    print random.random()
    
def getArgs(argv):
    args = {}
    while argv:
        if argv[0][0] == '-':
            args[argv[0]]=argv[1]
        argv=argv[1:]
    return args


if __name__=='__main__':
    
    args = getArgs(argv)
    if '-t' in args.keys():
        argflag=args['-t']
    else:
        argflag=None
    if '-d' in args.keys():
        argcheck=args['-d']
    else:
        argcheck=None
        
    if '-e' in args.keys():
        entry=args['-e']
    else:
        entry=None
          
    print entry,argflag,argcheck
        
    