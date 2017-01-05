# -*- coding: utf-8 -*-
from google.appengine.api import datastore
from google.appengine.api.datastore import Entity
from google.appengine.api.datastore_types import Key
from google.appengine.api import memcache
from google.appengine.ext import db
import datetime
import logging
import send2Line

class UserData(db.Model):
  lineId = db.StringProperty()
  dashId = db.StringProperty()
  registrationTime = db.StringProperty()
  message = db.StringProperty()

def createUserData(id):
    # entity = Entity('UserData', name=id)
    # entity.update({
    #     'registrationTime': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    #     'lineId': 'dummy-line-id',
    #     'dashId': id,
    # })
    # datastore.Put(entity)
    userData = UserData(
        key_name = id,
        lineId = id,
        dashId = 'not_registered_yet',
        registrationTime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        message = u'お電話ですので、きてください',
    )
    userData.put()

    setCurrentUser(id)
    # memcache.set(key = "USER-"+id,value="DUMMY")

def test_isExistUserData(id):

    result = False
    try:
        key = Key.from_path('UserData', id)
        entity = datastore.Get(key)
        if entity != None:
            logging.debug('entity: ' + str(entity))
            result=True
        else:
            logging.debug(id+u"は登録されていません。")
    except:
        logging.debug(id+u"は登録されていません。")

    return result

def isExistUserData(id):
    result=False
    # dummy=memcache.get(key = "USER-"+id)
    dummy = None
    if dummy!=None:
        result=True
    else:
        try:
            key = Key.from_path('UserData', id)
            entity = datastore.Get(key)
            if entity != None:
                result=True
                # memcache.set(key = "USER-"+id,value="DUMMY")
            else:
                logging.debug(id+u"は登録されていません。")
        except:
            logging.debug(id+u"は登録されていません。")

    return result

def getUser_MakerSecret(id):

    secret=memcache.get(key = "MakerSecret-"+id)
    if secret ==None:
        try:
            key = Key.from_path('UserData', id)
            entity = datastore.Get(key)
            secret=entity['maker_secret']
            memcache.set(key = "MakerSecret-"+id,value=secret)
        except:
            logging.debug(id+u"のIFTTT Maker Secretは登録されていません。")
    return secret

def setUser_MakerSecret(id,maker_secret):
    key = Key.from_path('UserData', id)
    entity = datastore.Get(key)
    entity.update({
                   'maker_secret': maker_secret

    })
    datastore.Put(entity)
    memcache.set(key = "MakerSecret-"+id,value=maker_secret)

def getUserByDashId(dashId):
    # id=memcache.get(key = "Dash-user-"+dashid)
    logging.debug('ENTER getUser_DashButton\n')
    found_lineId = None

    # get lineId from dashId
    try:
        q = UserData.all()
        q.filter('dashId = ', dashId)
        for p in q.run(limit=1):
            found_lineId = p.lineId
            logging.debug('  found: ' + str(p) + '\n')
    except:
        logging.error(u'dashIdからlineIdを検索する際に例外が発生しました')

    return found_lineId

def setUserByDashIdWithCurrentUser(dashId):
    # if not exists, assign the dashId to lineId
    result = False
    currentUser=getCurrentUser()

    if currentUser != None:
        # memcache.set(key = "Dash-user-"+dashid,value=currentUser, time=86400)
        # memcache.set(key = "User-dash-"+currentUser,value=dashid, time=86400 )
        logging.debug(dashId+u"のDashButtonは登録されていません。")

        try:
            lineId = currentUser
            key = db.Key.from_path('UserData', lineId)
            userData = db.get(key)
            userData.dashId = dashId
            userData.put()
            found_lineId = lineId
            clearCurrentUser()
            send2Line.sendText( currentUser,"DashButtonが登録されました")
            result = True
        except:
            logging.warning(u"currentUserに登録してある"+lineId+u"は登録されていません。")

    else:
        logging.warning(u"currentUserが設定されていないためコマンドを無視します。")

    return result


def getUserMessageByLineId(lineId):
    logging.debug('ENTER getUser_DashButtonMessage\n')
    result = 'dummy'

    try:
        key = db.Key.from_path('UserData', lineId)
        userData = db.get(key)
        logging.debug('userData: ' + str(userData))
        result = userData.message
    except:
        logging.debug(lineId+u"は登録されていません。")

    return result

def setUserMessageByLineId(lineId, new_message):
    logging.debug('ENTER setUser_DashButtonMessage\n')
    result = False

    try:
        key = db.Key.from_path('UserData', lineId)
        userData = db.get(key)
        logging.debug('userData: ' + str(userData))
        userData.message = new_message
        userData.put()
        result = True
    except:
        logging.debug(lineId+u"は登録されていません。")

    # try:
    #     key = Key.from_path('UserData', lineId)
    #     entity = datastore.Get(key)
    #     if entity != None:
    #         entity['message'] = new_message
    #         entity.put()
    #         result = True
    #     else:
    #         logging.debug(lineId+u"は登録されていません。")
    # except:
    #     logging.debug(lineId+u"は登録されていません。")

    return result

#    try:
#    entities=db.Query('UserData').filter("dash =", dashid)

#    logging.debug(type(entities));
#    for entity in entities.run(limit=1):
#    for entity in entities:
#        if dashid==entity['dash']:
#            logging.debug(dashid+u"のLineIDは"+entity['name'])
#            return entity['name']

#        id_path = Key.from_path('UserData', "dash",dashid)
#        if id_path !=None:
#            entity = datastore.Get(id_path)
#            return entity['name']
#    except:
#        logging.debug(dashid+u"のDashButtonは登録されていません。")

#    currentUser=getCurrentUser()
#    if currentUser !=None:
#        currentUser_path = Key.from_path('UserData', currentUser)
#        entity = datastore.Get(currentUser_path)
#        entity.update({
#                   'dash': dashid
#
 #       })
 #       datastore.Put(entity)

#        clearCurrentUser()
 #       return currentUser

#    return ""


def deleteUserData(id):
    # memcache.delete(key="MakerSecret-"+id)
    # memcache.delete(key="USER-"+id)
    # dashid=memcache.get(key="User-dash-"+id)
    # memcache.delete(key = "User-dash-"+id)
    # memcache.delete(key = "Dash-user-"+str(dashid))

    try:
        key = Key.from_path('UserData', id)
        entity = datastore.Delete(key)
    except:
        logging.debug(id+u"は登録されていません。")

def setCurrentUser(id):
    memcache.set(key = "CURRENTUSR",value=id)

def getCurrentUser():
    return memcache.get(key = "CURRENTUSR")

def clearCurrentUser():
    return memcache.delete(key = "CURRENTUSR")


### TEST

def test_getDashIdFromLineId(lineId):
    logging.debug('ENTER test_getDashIdFromLineId()\n')
    result = 'dummy'
    # return result
    try:
        q = UserData.all()
        q.filter('lineId = ', lineId)
        for p in q.run(limit=1):
            result = p.lineId
            logging.debug('  found: ' + str(p) + '\n')
            # logging.debug('    lineId: ' + p.lineId + '\n')
            # logging.debug('    dashId: ' + p.dashId + '\n')
            # logging.debug('    registrationTime: ' + p.registrationTime + '\n')
    except:
        logging.debug(id+u"は登録されていません。")

    return result

def test_getLineIdFromId(id):
    result = 'dummy'
    # return result
    try:
        key = Key.from_path('UserData', id)
        entity = datastore.Get(key)
        if entity != None:
            result = entity['lineId']
        else:
            logging.debug(id+u"は登録されていません。")
    except:
        logging.debug(id+u"は登録されていません。")

    return result

