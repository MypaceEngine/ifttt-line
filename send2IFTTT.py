from google.appengine.api import urlfetch
import send2Line
import logging
import json
import const

def sendData(ifttt_event, ifttt_key, senderID,from_id, event_type, msg_data):
    if ifttt_key ==None:
        send2Line.sendText( str(senderID),const.MSG_NONREGISTRATION )
        return
    if msg_data.count('\n'):
        msg_data=u"<pre>"+msg_data+u"</pre>"
    form_fields = {
                   "value1": from_id,
                   "value2": event_type,
                   "value3": msg_data,
                   }
    logging.debug(form_fields)
    logging.debug(ifttt_key)
    requestStr=json.dumps(form_fields,ensure_ascii=False)
#    requestStr=requestStr.replace('\n', '\\n').replace('\r', '')
    url = "https://maker.ifttt.com/trigger/"+ifttt_event+"/with/key/"+ifttt_key
    result = urlfetch.fetch(
                             url=url,
                             payload=requestStr,
                             method=urlfetch.POST,
                             headers={
                                      'Content-Type':' application/json'
                                      }
                                 )
    logging.debug(result.status_code)
    if result.status_code == 200:
        logging.debug(result.content)
    elif result.status_code == 401:
        send2Line.sendText( str(senderID),const.MSG_MAKERKEY_FAILED )
        logging.debug(result.content)
    else:
        logging.debug(result.content)
