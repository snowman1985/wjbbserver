from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.utils.translation import ugettext as _
import json
import os

def getcontent(loccode="101010100"):
    base = "http://m.weather.com.cn/data/"
#requests.get("http://m.weather.com.cn/data/101110102.html")
    urln = base+loccode
    print("urln:", urln)
    resp = requests.get(base+loccode+".html")
    content = resp.json()
    print content
    return content['weatherinfo']

def getweatherinfo(request, loccode="101010100"):
    wtinfo = getcontent(loccode)
    response_data = {}
    response_data['city'] = wtinfo['city']
    print wtinfo['city']
    print wtinfo['city'].encode('utf-8')
    response_data['date'] = wtinfo['date_y']
    response_data['temperature'] = wtinfo['temp1']
    response_data['weather'] = wtinfo['weather1']
    response_data['info'] = wtinfo['index']
    response_data['detailinfo'] = wtinfo['index_d']
    #return HttpResponse(json.dumps(response_data), content_type = "application/json; charset=utf-8")
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type = "application/json; charset=utf-8")
    #return HttpResponse(wtinfo, content_type = "text/plain")

def getweatherinfoconv(request, locstr=""):
   print("locstr:", locstr)
   print os.getcwd()
   curpath = os.getcwd()
   loccode = "101010100"
   with open(curpath+"/weather/locconv.txt") as f:
     for line in f:
       sline = line.split(" ")
       place = sline[0]
       #print place
       if locstr == unicode(place.decode('utf-8')):
         loccode = sline[1].strip()
         print("match:", loccode)
         break
   return getweatherinfo(request, loccode)
    


