# -*- coding: utf-8 -*-
import webapp2
import logging
import json
import const
import hmac, hashlib, base64
import getFromLine
import receiveLine
import receiveIFTTT
import receiveDash
import utility

from google.appengine.api.labs import taskqueue


class LINEReceiver(webapp2.RequestHandler):
    def post(self):
        jsonstr = self.request.body
        logging.debug(jsonstr)
        logging.debug(self.request.headers)
        if self.request.headers.get('X-Line-Signature') != base64.b64encode(
                hmac.new(const.CHANNEL_SECRET, jsonstr, hashlib.sha256).digest()):
            self.response.status = 401
            return
        jsonobj = json.loads(jsonstr)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Received!')

        for msg in jsonobj['events']:
            logging.debug("Call")
            taskqueue.add(url='/line-receive-exec', params={"data": json.dumps(msg, ensure_ascii=False)})


class LINEReceiverExec(webapp2.RequestHandler):
    def post(self):
        if (int(self.request.headers.environ['HTTP_X_APPENGINE_TASKRETRYCOUNT']) > 3):
            logging.error('jog retry error(over 3 times)')
            return
        msg = json.loads(self.request.get("data"))
        logging.debug(msg)
        receiveLine.receiveExec(self, msg)


class IFTTTReceiver_Text(webapp2.RequestHandler):
    def post(self):
        receiveIFTTT.receiveExec_Text(self)


class IFTTTReceiver_Image(webapp2.RequestHandler):
    def post(self):
        receiveIFTTT.receiveExec_Image(self)


class IFTTTReceiver_Video(webapp2.RequestHandler):
    def post(self):
        receiveIFTTT.receiveExec_Video(self)


class IFTTTReceiver_Audio(webapp2.RequestHandler):
    def post(self):
        receiveIFTTT.receiveExec_Audio(self)


class IFTTTReceiver_Location(webapp2.RequestHandler):
    def post(self):
        receiveIFTTT.receiveExec_Location(self)


class IFTTTReceiver_Sticker(webapp2.RequestHandler):
    def post(self):
        receiveIFTTT.receiveExec_Sticker(self)


# class IFTTTReceiver_MultiMessage(webapp2.RequestHandler):
#
#    def post(self):
#        receiveIFTTT.receiveExec_MultiMessage(self)

# class IFTTTReceiver_RichMessage(webapp2.RequestHandler):
#
#    def post(self):
#        receiveIFTTT.receiveExec_RichMessage(self)


class DashReceiver_Text(webapp2.RequestHandler):
    def post(self):
        receiveDash.receiveExec_Text(self)

class DashReceiver_Test(webapp2.RequestHandler):
    def post(self):
        receiveDash.receiveExec_Test(self)


class CONTENT_Provider(webapp2.RequestHandler):
    def get(self):
        getFromLine.returnContent(self)


class THUMBNAIL_Provider(webapp2.RequestHandler):
    def get(self):
        utility.getThmbnail(self)


class ORIGINALS_Provider(webapp2.RequestHandler):
    def get(self):
        utility.getOriginal(self)


class Dummy(webapp2.RequestHandler):
    def post(self):
        logging.error('Empty')


app = webapp2.WSGIApplication([
    ('/line-receive', LINEReceiver),
    ('/line-receive-exec', LINEReceiverExec),
    ('/line-receiveExec', Dummy),
    ('/ifttt2line-text', IFTTTReceiver_Text),
    ('/ifttt2line-image', IFTTTReceiver_Image),
    ('/ifttt2line-video', IFTTTReceiver_Video),
    ('/ifttt2line-audio', IFTTTReceiver_Audio),
    ('/ifttt2line-location', IFTTTReceiver_Location),
    ('/ifttt2line-sticker', IFTTTReceiver_Sticker),
    # ('/ifttt2line-multimessage', IFTTTReceiver_MultiMessage),
    # ('/ifttt2line-richmessage', IFTTTReceiver_RichMessage),
    # ('/dash-receive', DashReceiver),
    ('/dash-receive-text', DashReceiver_Text),
    # ('/dash-receive-image', DashReceiver_Image),
    # ('/dash-receive-video', DashReceiver_Video),
    # ('/dash-receive-audio', DashReceiver_Audio),
    # ('/dash-receive-location', DashReceiver_Location),
    # ('/dash-receive-sticker', DashReceiver_Sticker),
    ('/dash-receive-test', DashReceiver_Test),
    ('/content/.*', CONTENT_Provider),
    ('/thumbnail/.*', THUMBNAIL_Provider),
    ('/originals/.*', ORIGINALS_Provider),
], debug=True)
