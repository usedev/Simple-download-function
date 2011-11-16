#!/usr/bin/env python2
# coding:utf-8

import os
import sys
import urllib2

def download(url, destination, blocksize=8192):
    print "Downloading to {0}".format(destination)
    
    resume = os.path.exists(destination)
    with open(destination, "ab") as fh:
        if resume:
            print "Resuming download"
            fh.seek(0, 2)
            curpos = fh.tell()
            header =  {'Range':'bytes={0}-'.format(curpos)}
            request = urllib2.Request(url, headers=header)
            
            try:
                wh = urllib2.urlopen(request)
            except urllib2.HTTPError, inst:
                if inst.code == 416:
                    print "Download already completed"
                    return
                    
            try:
                size = int(wh.info().getheaders("Content-Length")[0]) + curpos
            except IndexError:
                size = 999999999
            cur = curpos
            if size == cur:
                print "Download already completed"
                return
        else:
            wh = urllib2.urlopen(url)
            try:
                size = int(wh.info().getheaders("Content-Length")[0]) 
            except IndexError:
                size = 999999999
            cur = 0
            
        content = wh.read(blocksize)
        while content:
            cur += len(content)
            fh.write(content)
            content = wh.read(blocksize)
            sys.stdout.write("Progress: {0:8}% \t {1}k of {2}k \r".format(round((float(cur)/size)*100.0,2), cur/1024.0, size/1024.0))
            sys.stdout.flush()
        


download("http://www.ubuntu.com/start-download?distro=desktop&bits=32&release=latest", "tmp")
