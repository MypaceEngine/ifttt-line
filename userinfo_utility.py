# -*- coding: utf-8 -*-
from google.appengine.api import datastore
from google.appengine.api.datastore import Entity
from google.appengine.api.datastore_types import Key
from google.appengine.api import memcache
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

def deleteUserData(id):
    memcache.delete(key="MakerSecret-"+id)
    memcache.delete(key="USER-"+id)
    try:
        key = Key.from_path('UserData', id)
        entity = datastore.Delete(key)
    except:
        logging.debug(id+u"は登録されていません。")
