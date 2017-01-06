# -*- coding: utf-8 -*-
from google.appengine.api import urlfetch
import send2Line
import getFromLine
import userinfo_utility
import time
import send2IFTTT
import const
import utility
import logging


def receiveExec(self, msg):
    logging.debug('ENTER receiveExec()')
    toType_id = str(msg["source"]["type"])
    sender_id = str(msg["source"]["userId"])

    timestamp = str(msg["timestamp"])

    if msg['type'] == "follow":
        logging.debug(msg['type'])
        displayName = getFromLine.getUserProfine(sender_id)["displayName"]
        replyToken = str(msg["replyToken"])
        # send2Line.sendText( sender_id,const.MSG_FIRSTMSG)
        # send2Line.sendText( sender_id,sender_id)
        # send2Line.sendText( sender_id,const.MSG_NONREGISTRATION )
        # send2Line.sendText( sender_id,unicode(displayName)+"さん、こんにちは!"+const.MSG_DASH_BTN_REQ )
        send2Line.sendText(sender_id, const.MSG_DASH_BTN_REQ)

        userinfo_utility.createUserData(sender_id)
    elif msg["type"] == "unfollow":
        userinfo_utility.deleteUserData(sender_id)
    elif msg["type"] == "message":
        replyToken = str(msg["replyToken"])
        message_id = msg["message"]["id"];
        secret = userinfo_utility.getUser_MakerSecret(sender_id)
        displayName = getFromLine.getUserProfine(sender_id)["displayName"]
        createTime = time.ctime(msg["timestamp"] / 1000 + 9 * 60 * 60)
        # createTime= 0
        if msg["message"]["type"] == "text":
            # TEXT Message


            text = msg["message"]["text"]
            logging.debug('text: ' + text)
            if 'ifttt:reg:' in text:
                send2IFTTT.sendData("LINE-TEXT", secret, sender_id, displayName, createTime, text)
            elif 'dash:reg:message:' in text:
                new_message = text[17:]
                if userinfo_utility.setUserMessageByLineId(sender_id, new_message):
                    send2Line.sendText(sender_id, u'メッセージの変更に成功しました')
            else:
                id = text[10:]
                userinfo_utility.setUser_MakerSecret(sender_id, id)
                send2Line.sendText(sender_id, const.MSG_REGISTRATION)

        elif msg["message"]["type"] == "image":
            # Image Message

            send2IFTTT.sendData("LINE-IMAGE", secret, sender_id, displayName, createTime,
                                utility.getContentURL(self, message_id))
        elif msg["message"]["type"] == "video":
            # Video Message
            send2IFTTT.sendData("LINE-VIDEO", secret, sender_id, displayName, createTime,
                                utility.getContentURL(self, message_id))

        elif msg["message"]["type"] == "audio":
            # Audio Message
            send2IFTTT.sendData("LINE-AUDIO", secret, sender_id, displayName, createTime,
                                utility.getContentURL(self, message_id))

        elif msg["message"]["type"] == "location":
            # Location Message
            # displayName=getFromLine.getUserProfine([str(msg["content"]["from"])])[0]["displayName"]
            # form_fields = {
            #                     "title": msg["content"]["location"]["title"],
            #                     "address": msg["content"]["location"]["address"],
            #                     "latitude": msg["content"]["location"]["latitude"],
            #                     "longitude": msg["content"]["location"]["longitude"],
            # }
            eccapePlace = urllib.quote(str(msg["content"]["location"]["title"]).encode('utf-8') + " " + str(
                msg["content"]["location"]["address"]).encode('utf-8'))
            eccapePlace = msg["message"]["address"]

            url = "http://maps.google.co.jp/maps?z=18&q=" + str(msg["message"]["latitude"]) + "," + str(
                msg["message"]["longitude"]) + " (" + eccapePlace + ")"
            send2IFTTT.sendData("LINE-LOCATION", secret, sender_id, displayName, createTime, url)

        elif msg["message"]["type"] == "sticker":
            # Sticker Message
            # displayName=getFromLine.getUserProfine([str(msg["content"]["from"])])[0]["displayName"]
            # form_fields = {
            #                     "STKPKGID": msg["content"]["contentMetadata"]["STKPKGID"],
            #                     "STKID": msg["content"]["contentMetadata"]["STKID"],
            #                     "STKVER": msg["content"]["contentMetadata"]["STKVER"],
            #                     "STKTXT": msg["content"]["contentMetadata"]["STKTXT"],
            # }
            #  url="https://sdl-stickershop.line.naver.jp/products/0/0/"+msg["message"]["STKVER"]+"/"+msg["content"]["contentMetadata"]["STKPKGID"]+"/android/stickers/"+msg["content"]["contentMetadata"]["STKID"]+".png"
            url = "https://sdl-stickershop.line.naver.jp/products/0/0/1/" + msg["message"][
                "packageId"] + "/android/stickers/" + msg["message"]["pstickerId"] + ".png;compress=true"
            send2IFTTT.sendData("LINE-STICKER", secret, sender_id, displayName, createTime, url)
            # elif msg["content"]["contentType"]==10 :
            #     #Contact Message
            #     createTime= time.ctime(msg["content"]["createdTime"]/1000+9*60*60)
            #     displayName=getFromLine.getUserProfine([str(msg["content"]["from"])])[0]["displayName"]
            #     contactInfo=getFromLine.getUserProfine([msg["content"]["contentMetadata"]["mid"]])
            #     name=contactInfo[0]["displayName"]
            #     url=contactInfo[0]["pictureUrl"]
            #     statusMessage=contactInfo[0]["statusMessage"]
            #     info=name+" ("+url+") "+statusMessage
            #     send2IFTTT.sendData("LINE-CONTACT",secret, sender_id,displayName, createTime, info)
