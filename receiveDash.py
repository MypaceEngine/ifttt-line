# -*- coding: utf-8 -*-
from google.appengine.api import memcache
import logging
import json
import userinfo_utility
import send2Line
import getFromLine
import utility
import uuid
import urllib
import re

def receiveExec(self):
        self.receiveExec_Text()

def receiveExec_Text(self):
        logging.debug(self.request.headers)
        logging.debug(self.request.body)
        if(self.request.headers['Content-Type']=='text/plain'):
            jsonstr = self.request.body

            strArr=jsonstr.split("\\\\")
            to=strArr[0].strip()
            text="\\\\".join(strArr[1:]);
            text=text.lstrip('<.').rstrip('>').strip()
        else:
            jsonstr = self.request.body
            logging.debug(jsonstr)
            jsonstr=jsonstr.replace('\r', '')
            jsonstr=jsonstr.replace('\n', '\\n')
            logging.debug(jsonstr)
            jsonobj = json.loads(jsonstr)
            logging.debug(jsonobj)
#            to=str(jsonobj[u"to"])
            text=jsonobj[u"text"].lstrip('<.').rstrip('>').strip()

            id=userinfo_utility.getUser_DashButton(jsonobj[u"dash"])

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Received!')

        if not userinfo_utility.isExistUserData(id):
            return

        displayName=getFromLine.getUserProfine(id)["displayName"]
        send2Line.sendText( id,displayName+u"さん、"+text  )

def receiveExec_Image(self):
        if(self.request.headers['Content-Type']=='text/plain'):
            jsonstr = self.request.body
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Received!')
        else:
            jsonstr = self.request.body
            logging.debug(jsonstr)
            jsonobj = json.loads(jsonstr)
            logging.debug(jsonobj)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Received!')
            originalContentUrl=jsonobj[u"originalContentUrl"]
            picture_key=utility.getHash(originalContentUrl)
            encodeURL=urllib.quote(originalContentUrl)
            originalContentUrl_encode=self.request.host_url+"/originals/"+picture_key+"/"+encodeURL

            previewImageUrl=""
            if jsonobj.has_key(u"previewImageUrl"):
                previewImageUrl=jsonobj[u"previewImageUrl"]
            if  previewImageUrl == "" :
                previewImageUrl=self.request.host_url+"/thumbnail/"+picture_key+"/"+encodeURL

            id=userinfo_utility.getUser_DashButton(jsonobj[u"dash"])
            if not userinfo_utility.isExistUserData(id):
                return
            send2Line.sendImage( id,originalContentUrl_encode, previewImageUrl)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Received!')

def receiveExec_Video(self):
        if(self.request.headers['Content-Type']=='text/plain'):
            jsonstr = self.request.body
        else:
            jsonstr = self.request.body
            logging.debug(jsonstr)
            jsonobj = json.loads(jsonstr)
            logging.debug(jsonobj)

            previewImageUrl=""
            if jsonobj.has_key(u"previewImageUrl"):
                previewImageUrl=jsonobj[u"previewImageUrl"]
            if previewImageUrl == "" :
                previewImageUrl="https://ifttt-line.appspot.com/images/preview_image.jpg?"+str(uuid.uuid4())

            id=userinfo_utility.getUser_DashButton(jsonobj[u"dash"])
            if not userinfo_utility.isExistUserData(id):
                return
            send2Line.sendVideo( id,jsonobj[u"originalContentUrl"],previewImageUrl )

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Received!')

def receiveExec_Audio(self):

        if(self.request.headers['Content-Type']=='text/plain'):
            jsonstr = self.request.body
        else:
            jsonstr = self.request.body
            logging.debug(jsonstr)
            jsonobj = json.loads(jsonstr)
            logging.debug(jsonobj)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Received!')
            audioLen= 180000
            if jsonobj.has_key(u"AUDLEN") and isinstance(jsonobj.has_key(u"AUDLEN"),int):
                audioLen=jsonobj[u"AUDLEN"]
            if  audioLen=="":
                audioLen=180000

            id=userinfo_utility.getUser_DashButton(jsonobj[u"dash"])
            if not userinfo_utility.isExistUserData(id):
                return
            send2Line.sendAudio( id,jsonobj[u"originalContentUrl"],audioLen )

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Received!')

def receiveExec_Location(self):
        logging.debug(self.request.headers)
        if(self.request.headers['Content-Type']=='text/plain'):
            jsonstr = self.request.body
        else:
            jsonstr = self.request.body
            logging.debug(jsonstr)
            jsonobj = json.loads(jsonstr)
            logging.debug(jsonobj)
            latitude=0;
            longitude=0;
            title="";
            address="";
            if jsonobj.has_key("LocationMapUrl"):
                url=jsonobj["LocationMapUrl"]
                logging.debug(url)
                url=url.split(" ")[0]
                url=utility.getRealURL(url)
                logging.debug(url)
                r = re.compile("center=(-?[0-9]+\.?[0-9]*),(-?[0-9]+\.?[0-9]*)")
                m = r.search(url)
                if m!= None:
                    latitude=m.group(1)
                    longitude=m.group(2)
                r = re.compile("ll=(-?[0-9]+\.?[0-9]*),(-?[0-9]+\.?[0-9]*)")
                m = r.search(url)
                if m!= None:
                    latitude=m.group(1)
                    longitude=m.group(2)
                r = re.compile("q=(-?[0-9]+\.?[0-9]*),(-?[0-9]+\.?[0-9]*)")
                m = r.search(url)
                if m!= None:
                    latitude=m.group(1)
                    longitude=m.group(2)
                r = re.compile("\/maps\/search\/(-?[0-9]+\.?[0-9]*),(-?[0-9]+\.?[0-9]*)")
                m = r.search(url)
                if m!= None:
                    latitude=m.group(1)
                    longitude=m.group(2)
            if jsonobj.has_key("latitude"):
                latitude=jsonobj["latitude"];
            if jsonobj.has_key("longitude"):
                longitude=jsonobj["longitude"];
            if jsonobj.has_key("title"):
                title=jsonobj["title"];
            if jsonobj.has_key("address"):
                address=jsonobj["address"];
            if title =="":
                title_json=utility.getAddress(latitude,longitude)
                if len(title_json)>0:
                    title=title_json[0]["formatted_address"]
                    title=title.encode('utf_8')
            if title =="":
                title="位置情報"
            if address=="":
                address="位置情報"

            id=userinfo_utility.getUser_DashButton(jsonobj[u"dash"])
            if not userinfo_utility.isExistUserData(id):
                return
            send2Line.sendLocation( id,address,title,latitude,longitude)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Received!')

def receiveExec_Sticker(self):
        if(self.request.headers['Content-Type']=='text/plain'):
            jsonstr = self.request.body
        else:
            jsonstr = self.request.body
            logging.debug(jsonstr)
            jsonobj = json.loads(jsonstr)
            logging.debug(jsonobj)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Received!')
            STKID=0
            STKPKGID=0
            STKVER=0
            if jsonobj.has_key("ContentUrl"):
                url=jsonobj["ContentUrl"]
                url=utility.getRealURL(url)
                r = re.compile("\/products\/0\/0\/([0-9]+)\/([0-9]+)\/android\/stickers\/([0-9]+).png")
                m = r.search(url)
                if m!= None:
                    STKVER=m.group(1)
                    STKPKGID=m.group(2)
                    STKID=m.group(3)
            if jsonobj.has_key("STKVER"):
                    STKVER=jsonobj[u"STKVER"]
            if jsonobj.has_key("STKPKGID"):
                    STKPKGID=jsonobj[u"STKPKGID"]
            if jsonobj.has_key("STKID"):
                    STKID=jsonobj[u"STKID"]
            id=userinfo_utility.getUser_DashButton(jsonobj[u"dash"])
            if not userinfo_utility.isExistUserData(id):
                return
            send2Line.sendSticker( id,STKID ,STKPKGID,STKVER)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Received!')

#def receiveExec_MultiMessage(self):
#        if(self.request.headers['Content-Type']=='text/plain'):
#            jsonstr = self.request.body
#        else:
#            jsonstr = self.request.body
#            logging.debug(jsonstr)
#            jsonobj = json.loads(jsonstr)
#            logging.debug(jsonobj)
#            self.response.headers['Content-Type'] = 'text/plain'
#            self.response.out.write('Received!')
#            if not userinfo_utility.isExistUserData(str(jsonobj[u"to"])):
#               return
#            send2Line.sendMultiMessage( [str(jsonobj[u"to"])],jsonobj[u"messages"] )

#def receiveExec_RichMessage(self):
#        if(self.request.headers['Content-Type']=='text/plain'):
#            jsonstr = self.request.body
#        else:
#           jsonstr = self.request.body
#            logging.debug(jsonstr)
#            jsonobj = json.loads(jsonstr)
#            logging.debug(jsonobj)
#            self.response.headers['Content-Type'] = 'text/plain'
#            self.response.out.write('Received!')
#            if not userinfo_utility.isExistUserData(str(jsonobj[u"to"])):
#                return
#            send2Line.sendRichMessage( [str(jsonobj[u"to"])],jsonobj[u"MARKUP_JSON"] )