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


def receiveExec_Text(self):
    logging.debug('ENTER receiveExec_Text')
    logging.debug(self.request.headers)
    logging.debug(self.request.body)

    # create jsonobj from request.body
    # if(self.request.headers['Content-Type']=='text/plain'):
    request_headers = self.request.headers
    jsonstr_body = self.request.body
    jsonstr_body = jsonstr_body.replace('\r', '')
    jsonstr_body = jsonstr_body.replace('\n', '\\n')
    request_bodies = json.loads(jsonstr_body)

    # if dashId is specified
    if request_bodies.get(u'dash') != None:
        dashId = request_bodies[u'dash']
    # if ButtonMac in header is specified
    elif request_headers.get('ButtonMAC') != None:
        dashId = request_headers.get('ButtonMAC')
    else:
        logging.error(u'dasherからの送信されたデータが不正です。dasherの設定を見直してください。')
        return

    lineId = userinfo_utility.getUserByDashId(dashId)

    # if the dashId is not assigned to lineId, assign together
    if lineId == None:
        result = userinfo_utility.setUserByDashIdWithCurrentUser(dashId)
        if result:
            logging.debug(u'該当するLINE IDが見つかりませんでしたので登録しました。')
        else:
            logging.error(u'DashIdとLineIdの紐付けができませんでした。')
        return

    # generate and send message
    message = userinfo_utility.getUserMessageByLineId(lineId)

    if not userinfo_utility.isExistUserData(lineId):
        logging.error(u'該当するLINE IDが見つかりませんでした')
        return

    displayName = getFromLine.getUserProfine(lineId)["displayName"]
    send2Line.sendText(lineId, displayName + u'さん、' + message)

    # response to HTTP requester
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Received!\n')


# TEST
# TODO: テストは別のクラスや別のファイル、別のフォルダに移動することを検討

def receiveExec_Test(self):
    logging.debug(self.request.headers)
    logging.debug(self.request.body)

    # create jsonobj from request.body
    # if(self.request.headers['Content-Type']=='text/plain'):
    jsonstr = self.request.body
    jsonstr = jsonstr.replace('\r', '')
    jsonstr = jsonstr.replace('\n', '\\n')
    jsonobj = json.loads(jsonstr)
    logging.debug(jsonobj)

    dash = jsonobj[u'dash']
    text = jsonobj[u'text']

    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('dash:' + dash + '\n')
    self.response.out.write('text:' + text + '\n')

    # datastore test
    #   creating
    self.response.out.write('creating user data onto datastore\n')
    userinfo_utility.createUserData(dash)
    self.response.out.write('finished\n')
    #   checking if exists
    self.response.out.write('checking created datastore entity\n')
    self.response.out.write(str(userinfo_utility.test_isExistUserData(dash)) + '\n')
    self.response.out.write('finished\n')

    #   getting if exists
    self.response.out.write('getting datastore entity\n')
    self.response.out.write(str(userinfo_utility.test_getLineIdFromId(dash)) + '\n')
    self.response.out.write('finished\n')

    #   getting from lineId
    self.response.out.write('getting datastore entity from lineId\n')
    self.response.out.write(str(userinfo_utility.test_getDashIdFromLineId('dummy-line-id')) + '\n')
    self.response.out.write('finished\n')

    # memcache test
    # memcache.set(key = "USER-"+"dash_id_for_test",value="DUMMY")
    # if userinfo_utility.isExistUserData(dash):
    #     self.response.out.write('existed\n')
    # else:
    #     self.response.out.write('not existed\n')

    self.response.out.write('dash:' + dash + '\n')
    self.response.out.write('text:' + text + '\n')

    self.response.out.write('Finished!\n\n')
