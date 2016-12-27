from google.appengine.api import urlfetch
import json
import logging
import const

def sendData(form_field):
    url = "https://api.line.me/v2/bot/message/push"
    result = urlfetch.fetch(
                             url=url,
                             payload=json.dumps(form_field,ensure_ascii=False),
                             method=urlfetch.POST,
                             headers={
                                      'Content-type':'application/json',
                                      'Authorization': 'Bearer '+const.ChannelAccessToken
                                      }
                                 )
    if result.status_code == 200:
        logging.debug(result.content)
    else:
        logging.debug(result.content)

def sendText(to_ids, msg_data):
    #msg_data=msg_data.encode('utf-8');
    if len(msg_data)>2000 :
                msg_data= msg_data[:2000]
    form_fields = {
                   "to": to_ids,
                   "messages":[{
                              "type":"text",
                              "text":msg_data
                              }]
                   }
    logging.debug(json.dumps(form_fields,ensure_ascii=False))
    logging.debug(form_fields)
    sendData(form_fields)

def sendImage(to_ids, originalContentUrl,previewImageUrl):
    form_fields = {
                   "to": to_ids,
                   "messages":[{
                              "type":"image",
                              "originalContentUrl":originalContentUrl,
                              "previewImageUrl":previewImageUrl
                              }]
                   }
    logging.debug(json.dumps(form_fields,ensure_ascii=False))
    logging.debug(form_fields)
    sendData(form_fields)

def sendVideo(to_ids, originalContentUrl,previewImageUrl):
    form_fields = {
                   "to": to_ids,
                   "messages":[{
                              "type":"video",
                              "originalContentUrl":originalContentUrl,
                              "previewImageUrl":previewImageUrl
                              }]
                   }
    logging.debug(json.dumps(form_fields,ensure_ascii=False))
    logging.debug(form_fields)
    sendData(form_fields)

def sendAudio(to_ids, originalContentUrl,audioLen):
    form_fields = {
                   "to": to_ids,
                   "messages":[{
                              "type":"audio",
                              "originalContentUrl":originalContentUrl,
                              "duration":audioLen
                              }]
                   }
    logging.debug(json.dumps(form_fields,ensure_ascii=False))
    logging.debug(form_fields)
    sendData(form_fields)

def sendLocation(to_ids, text,title,latitude,longitude):
    form_fields = {
                   "to": to_ids,
                   "messages":[{
                              "type":"location",
                              "title":title,
                              "address":text,
                              "latitude":latitude,
                              "longitude":longitude
                              }]
                   }
    logging.debug(json.dumps(form_fields,ensure_ascii=False))
    logging.debug(form_fields)
    sendData(form_fields)

def sendSticker(to_ids, stkid,sktpkgid):
    form_fields = {
                   "to": to_ids,
                   "messages":[{
                              "type":"sticker",
                              "packageId":stkid,
                              "stickerId":sktpkgid,
                              }]
                   }
    logging.debug(json.dumps(form_fields,ensure_ascii=False))
    logging.debug(form_fields)
    sendData(form_fields)

#Image map Message
#Template Message

#def sendMultiMessage(to_ids, content):
#    form_fields = {
#                   "to": to_ids,
#                   "toChannel": 1383378250,
#                   "eventType": 140177271400161403,
#                   "content":{
#                              "messageNotified": 0,
#                              "messages":content
#                              }
#                   }
#    logging.debug(json.dumps(form_fields,ensure_ascii=False))
#    logging.debug(form_fields)
#    sendData(form_fields)

#def sendRichMessage(to_ids, url,text,markup):
#    form_fields = {
#                   "to": to_ids,
#                   "toChannel": 1383378250,
#                   "eventType": 138311608800106203,
#                   "content":{
#                              "contentType":12,
#                              "toType":1,
#                              "contentMetada":{
#                                               "DOWNLOAD_URL": url,
#                                               "SPEC_REV": "1",
#                                               "ALT_TEXT": text,
#                                               "MARKUP_JSON": markup
#                                               }
#                              }

#                   }
#    logging.debug(json.dumps(form_fields,ensure_ascii=False))
#    logging.debug(form_fields)
#    sendData(form_fields)