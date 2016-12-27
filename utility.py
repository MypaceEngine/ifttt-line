from google.appengine.api import urlfetch
from google.appengine.api import memcache
from google.appengine.api import images
import json
import logging
import urllib
import uuid
import hashlib
import const

def getAddress(longitude,latitude):
    gsp_key="gps-"+str(longitude)+","+str(latitude)
    resultData= memcache.get(key = gsp_key)
    if resultData == None:
        url = "https://maps.googleapis.com/maps/api/geocode/json?language=ja&sensor=false&key="+const.GOOGLE_API_KEY+"&latlng="+str(longitude)+","+str(latitude)
        logging.debug(url)
        result = urlfetch.fetch(
                                url=url,
                                method=urlfetch.GET,
                                headers={
                                      }
                                )
        if result.status_code == 200:
            logging.debug(result.content)
        else:
            logging.debug(result.content)
        jsonstr = result.content
        jsonobj = json.loads(jsonstr)
        if len(jsonobj["results"])>0:
            memcache.set(key = gsp_key,value=jsonobj, time=3600)
        resultData=jsonobj;
    else:
        logging.debug(resultData)
    return resultData["results"]

def getThmbnail(self):
    getImageDataExternal(self,240,240)

def getOriginal(self):
    getImageDataExternal(self,1024,1024)

def getImageDataExternal(self,width,heigh):
    logging.debug(self.request.path)
    picture_key= self.request.path[11:75]
    encodeUrl= self.request.path[76:]
    originalUrl= urllib.unquote(encodeUrl)
    logging.debug(picture_key+" "+encodeUrl+ " "+originalUrl)

    if originalUrl == None:
        logging.debug("URL Failure("+picture_key+")")
        self.response.status = 301
        self.response.headers['Location'] ="https://ifttt-line.appspot.com/images/preview_image.jpg?"+str(uuid.uuid4())
    elif picture_key  == getHash(originalUrl):
        logging.debug("Key is correct! "+picture_key+")")
        result = urlfetch.fetch(
                                url=originalUrl,
                                method=urlfetch.GET,
                                headers={
                                      }
                                )
        if result.status_code == 200:
            logging.debug(result.content)
            photo_data = result.content
            thumb=image_Transform(photo_data,width,heigh)
            contentLegth=len(thumb)
            self.response.headers['Content-Type'] = result.headers['Content-Type']
            if result.headers.has_key("content-disposition"):
                self.response.headers['content-disposition'] = result.headers['content-disposition']
            self.response.headers['date'] = result.headers['date']
            self.response.headers['content-length'] =contentLegth
            self.response.out.write(thumb)
        else:
            self.response.status = 301
            self.response.headers['Location'] ="https://ifttt-line.appspot.com/images/preview_image.jpg?"+str(uuid.uuid4())
            logging.debug("Image Load Failure("+originalUrl+")")
    else:
        logging.debug("Key Failure("+picture_key+")")
        self.response.status = 301
        self.response.headers['Location'] ="https://ifttt-line.appspot.com/images/preview_image.jpg?"+str(uuid.uuid4())

def getRealURL(url):
    return urllib.urlopen(url).geturl().lower()

def getHash(original):
    return hashlib.sha256((const.HASH_SEEDS+original).encode('utf-8')).hexdigest()

def image_Transform(imageData,width,heigh):
    img = images.Image(imageData)
    img._update_dimensions()
    thumb=imageData
    if img._height > width or img._width > heigh:
        thumb = images.resize(imageData,width, heigh)
#            thumb = img.execute_transforms(output_encoding=images.JPEG)
    return thumb

def getContentURL(self,url):
    picture_key=getHash(url)
    encodeURL=urllib.quote(url)
    return "https://ifttt-line.appspot.com/content/"+ picture_key+"/"+encodeURL
