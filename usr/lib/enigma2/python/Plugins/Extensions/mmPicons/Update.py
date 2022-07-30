#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, re, sys
from twisted.web.client import downloadPage
PY3 = sys.version_info.major >= 3
print("Update.py")
def upd_done():        
    print( "In upd_done")
    xfile ='http://patbuweb.com/mmpicons/mmpicons.tar'
    print('xfile: ', xfile)
    if PY3:
        xfile = b"http://patbuweb.com/mmpicons/mmpicons.tar"
    print("Update.py not in PY3")
    fdest = "/tmp/mmpicons.tar"
    print("upd_done xfile =", xfile)
    downloadPage(xfile, fdest).addCallback(upd_last)

def upd_last(fplug): 
    upw= '/tmp/mmpicons.tar'
    if os.path.isfile(upw) and os.stat(upw).st_size > 0:
        cmd = "tar -xvf /tmp/mmpicons.tar -C /"
        print( "cmd A =", cmd)
        os.system(cmd)
        pass

