# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 22:07:01 2017

@author: kevinkit

This script is for the purpose of finding different kind of words that will be pushed into the search later
"""


import urllib2
import numpy as np;
from sys import platform

from joblib import Parallel, delayed


init_language = "en";
transfer_languages = ['ar','bg','zh','zh-TW','hr','cs','da','nl','eo','et','tl','fi','fr','ka','de','el','iw','hu','is','id','ga','it','ja','jw','ko','la','ms','no','fa','pl','pt','ru','sk','sl','es','sv','th','tr','uk','vi']
words = ["Bike","Car","Train","Person"]

MT = 0;

x = np.chararray([])

#Abuse Google Translate
def translate(word, sourceLanguage, targetLanguage):
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (targetLanguage, sourceLanguage, word)
    request = urllib2.Request(link, headers=agents)
    page = urllib2.urlopen(request).read()
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    return (result,page)


def translateWrapper(i,transfer_languages,words):
    return translate(words[i], init_language, transfer_languages[i])
    
    

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
                x = np.append(x,t[0])
        if i == 0:
            u = np.unique(x);
            s = np.asarray(len(u));
        else:
            u = np.append(u,np.unique(x));
            s = np.append(s,len(np.unique(x)))

