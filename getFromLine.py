from google.appengine.api import urlfetch
from google.appengine.api import memcache
import json
import const
import logging
import urllib
import utility
import uuid

#def getPrevious(messageId):
#    url = "https://trialbot-api.line.me/v1/bot/message/"+messageId+"/content/preview"
#    result = urlfetch.fetch(
#                             url=url,
#                             method=urlfetch.GET,
#                             headers={
#                                      'Authorization': 'Bearer '+const.ChannelAccessToken
#                                      }
#                            )
#    if result.status_code == 200:
#        logging.debug(result.content)
#    else:
#        logging.debug(result.content)
#    return result.content


def getUserProfine(mid):
#    midstr= ','.join(mids)
    url = "https://api.line.me/v2/bot/profile/"+mid
    result = urlfetch.fetch(
                             url=url,
                             method=urlfetch.GET,
                             headers={
                                      'Authorization': 'Bearer '+const.ChannelAccessToken
                                      }
                            )
    if result.status_code == 200:
        logging.debug(result.content)
    else:
        logging.debug(result.content)
    jsonstr = result.content
    jsonobj = json.loads(jsonstr)
    return jsonobj

def returnContent(self):
    logging.debug(self.request.path)
    picture_key= self.request.path[9:73]
    originalid= self.request.path[74:]
    logging.debug(picture_key+" "+ " "+originalid)

    if originalid == None:
        logging.debug("URL Failure("+picture_key+")")
        self.response.status = 301
        self.response.headers['Location'] ="https://ifttt-line.appspot.com/images/preview_image.jpg?"+str(uuid.uuid4())
    elif picture_key  == utility.getHash(originalid):
        url = "https://api.line.me/v2/bot/message/"+originalid+"/content"
        result = urlfetch.fetch(
                             url=url,
                             method=urlfetch.GET,
                             headers={
                                      'Authorization': 'Bearer '+const.ChannelAccessToken
                                      }
                                )
        logging.debug(result.headers)
        if result.status_code == 200:
            logging.debug(result.content)

            self.response.headers['Content-Type'] = result.headers['Content-Type']
            if result.headers.has_key("content-disposition"):
                self.response.headers['content-disposition'] = result.headers['content-disposition']
            self.response.headers['date'] = result.headers['date']
            self.response.headers['content-length'] = result.headers['content-length']

            self.response.out.write(result.content)
        else:
            logging.debug("Content Load Error")
            logging.debug(result.content)
            self.response.status = 301
            self.response.headers['Location'] ="https://ifttt-line.appspot.com/images/preview_image.jpg?"+str(uuid.uuid4())
    else:
        logging.debug("Key Failure")

