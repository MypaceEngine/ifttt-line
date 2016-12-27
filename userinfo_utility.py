# -*- coding: utf-8 -*-
from google.appengine.api import datastore
from google.appengine.api.datastore import Entity
from google.appengine.api.datastore_types import Key
from google.appengine.api import memcache
from google.appengine.ext import db
import datetime
import logging

def createUserData(id):
    entity = Entity('UserData', name=id)
    entity.update({
                   'registrationTime': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    })
    datastore.Put(entity)
    memcache.set(key = "USER-"+id,value="DUMMY")

def isExistUserData(id):
    result=False
    dummy=memcache.get(key = "USER-"+id)
    if dummy!=None:
        result=True
    else:
        try:
            key = Key.from_path('UserData', id)
            entity = datastore.Get(key)
            if entity != None:
                result=True
                memcache.set(key = "USER-"+id,value="DUMMY")
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

def getUser_DashButton(dashid):
    id=memcache.get(key = "Dash-user-"+dashid)
    if id !=None:
        logging.debug(dashid+u"のLineIDは"+id)
        return id

    else:
        currentUser=getCurrentUser()
        if currentUser !=None:
            memcache.set(key = "Dash-user--"+dashid,value=currentUser, time=86400)
            memcache.set(key = "User-dash--"+currentUser,value=dashid, time=86400 )
            logging.debug(dashid+u"のDashButtonは登録されていません。")
            return currentUser
    return "";
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
    memcache.delete(key="MakerSecret-"+id)
    memcache.delete(key="USER-"+id)
    dashid=memcache.get(key="User-dash--"+id)
    memcache.delete(key = "User-dash--"+id)
    memcache.delete(key = "Dash-user--"+dashid)

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
