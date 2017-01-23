# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 22:07:01 2017

@author: kevinkit

This script is for the purpose of finding different kind of words that will be pushed into the search later
"""


import urllib2
import numpy as np;
from sys import platform
import simplejson
import cStringIO
from joblib import Parallel, delayed

from bs4 import BeautifulSoup
import requests
import re

import os
import cookielib
import json
import hashlib
import urllib
import time
from PIL import Image
init_language = "en";
transfer_languages = [init_language,'ar','bg','zh','zh-TW','hr','cs','da','nl','eo','et','tl','fi','fr','ka','de','el','iw','hu','is','id','ga','it','ja','jw','ko','la','ms','no','fa','pl','pt','ru','sk','sl','es','sv','th','tr','uk','vi']
#words = ["Bike","Car","Train","Person"]
words = ["kittens","puppies"]

MT = 0;

x = np.chararray([])

#Abuse Google Translate
def translate(word, sourceLanguage, targetLanguage):
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (targetLanguage, sourceLanguage, word)
    print link
    request = urllib2.Request(link, headers=agents)
    
    try:
        page = urllib2.urlopen(request).read()
    except IOError:
        print "could not connect, trying to sleep for 5 seconds";
        time.sleep(5);
        print "a good nap"
        try:
            page = urllib2.urlopen(request).read()
        except IOError:          
            print "The language" + str(targetLanguage) + "could not be translated";        
            return -1;
        
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    return (result,page)


def translateWrapper(i,transfer_languages,words):
    return translate(words[i], init_language, transfer_languages[i])
    
def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')
    

#Multithreading under windows sucks
if MT == 1 and platform != "win32" and platform != "win64":
        n = Parallel(n_jobs = 4)(delayed(translateWrapper)(i,transfer_languages,words) for i in range(0,len(transfer_languages)))
else:
    print "Change to Linux for multitthreading!";
    for i in range(0,len(words)):
        for j in range(0,len(transfer_languages)):
            t = translate(words[i],init_language,transfer_languages[j])
            if j == 0:
                x = t[0]
                print "init"
            else:
                if t != -1:
                    x = np.append(x,t[0])
        if i == 0:
            u = np.unique(x);
            s = np.asarray(len(u));
        else:
            u = np.append(u,np.unique(x));
            s = np.append(s,len(np.unique(x)))


len_s = [];
len_s.append(0);
for i in range(0,len(s)):
    len_s.append(s[i]);



ActualImages=[]# contains the link for Large original images, type of  image
len_counter = [];
for j in range(0,len(words)):
    if not os.path.exists(words[j]):
        os.mkdir(words[j]);
    cnt = 0;
    for i in range(len_s[j],len_s[j+1]):        

        print "now language: " + str(transfer_languages[i])    
        query = u[i]
        print query    
        
        #query = raw_input(u[0])# you can change the query for the image  here
        image_type="ActiOn"
        #query= query.split()
        #query='+'.join(query)
        query = u[i]
        url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
        print url
        #add the directory for your image here
        DIR="new"
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
        try:
            soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')
        except IOError:
            print "could not connect, trying to sleep for 5 seconds";
            time.sleep(5);
            print "a good nap"
            try:
                soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')
            except IOError:          
                print "The language" + str(transfer_languages[i]) + "could not be translated";        
        
         

        for a in soup.find_all("div",{"class":"rg_meta"}):
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((link,Type))
            cnt = cnt +1;
    
    len_counter.append(cnt);
    print  "there are total" , len(ActualImages),"images"

n = 0;
w_jumper = 0;
correct = 1;
for i in range(0,len(ActualImages)):
    h =   hashlib.md5(ActualImages[i][0])
    try:
        urllib.urlretrieve(ActualImages[i][0],words[w_jumper] + "/" + str(h.hexdigest()) + "." + ActualImages[i][1]); 
        correct = correct + 1;
        
    except IOError:
        print "could not connect, trying to sleep for " + str(15 + n) +  " seconds";
        time.sleep(15 + n);
        print "a good nap, will try again,..."
        try:
            urllib.urlretrieve(ActualImages[i][0],words[w_jumper] + "/" + str(h.hexdigest()) + "." + ActualImages[i][1]);
        except IOError:          
            print "The image " + ActualImages[i][0] + " could not be used";                
            print "Problem found"
            print "skipped image..."
            n = n +1;

            print "now skipped: " + str(n) + " images" 
            print "correct found: " + str(correct) + " images";
        
            
        
    if i == len_counter[w_jumper]:
        w_jumper = w_jumper +1;



"""
if not os.path.exists(DIR):
            os.mkdir(DIR)
            print "Could not find folder!,making new one"
DIR = os.path.join(DIR, query.split()[0])

if not os.path.exists(DIR):
            os.mkdir(DIR)
###print images
for i , (img , Type) in enumerate( ActualImages):
    try:
        req = urllib2.Request(img, headers={'User-Agent' : header})
        raw_img = urllib2.urlopen(req).read()

        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
        print cntr
        if len(Type)==0:
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
        else :
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')


        f.write(raw_img)
        f.close()
    except Exception as e:
        print "could not load : "+img
        print e
"""
