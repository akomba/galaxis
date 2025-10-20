import json
import os
import glx.helper as helper
import datetime
from glx.card_attribute import CardAttribute
from glx.api.community import CommunityApi
import time
from glx.logger import Logger

def setup(community_name):
    # get folder
    config = helper.load_global_config()
    
    #scheduler folder
    sf = os.path.join(config["DATA_ROOT"],"communities",community_name,"scheduler")
    os.makedirs(sf,exist_ok=True)

    return config, sf

def schedule_expiring_value(community_name, collection_id, card_id, attribute_id, value, expiration):
    config,sf = setup(community_name)
    Logger().init(community_name)

    # expiration in minutes
    exp = datetime.datetime.now() + datetime.timedelta(minutes=expiration)

    # schedule structure
    schedule = {
            "community_name": community_name,
            "collection_id" : collection_id,
            "card_id"       : card_id,
            "attribute_id"  : attribute_id,
            "value"         : value,
            "expiration"    : exp.isoformat()
            }

    # save file
    filename = exp.isoformat().replace(":","_").replace(".","_")
    filename = "_".join([filename,community_name,str(collection_id),str(card_id),str(attribute_id),str(value)])
    filename = os.path.join(sf,filename+".json")

    Logger().logger.info("SCHE create FILE "+filename+" COLL "+str(collection_id)+" CARD "+str(card_id)+"  ATTR "+str(attribute_id)+" VAL "+str(value))
    helper.save_as_json(filename,schedule)
    return filename

def list_active(community_name):
    config,sf = setup(community_name)

    # get (active) schedules
    schedules = [os.path.join(sf,f) for f in os.listdir(sf) if f[0] != "x"]

    return schedules

def list_due(community_name):
    # lists the events that are already due
    events = list_active(community_name)
    due = []
    for event in events:
        e = helper.load_json(event)
        if datetime.datetime.fromisoformat(e["expiration"]) <= datetime.datetime.now():
            due.append(event)

    return due

def show_due(community_name):
    events = list_due(community_name)
    for event in events:
        print(event)

def process(community_name):
    events = list_due(community_name)
    api = CommunityApi(community_name)
    for event in events:
        # load event
        e = helper.load_json(event)
       
        # check if attribute exists
        attdata = api.get_card_attribute(e["collection_id"],e["card_id"],e["attribute_id"])
        if attdata:
            attribute = CardAttribute(e["community_name"],e["collection_id"],e["card_id"],e["attribute_id"])
            # get current value on attribute
            current_value = attribute.value()

            # setting new value
            new_value = current_value - e["value"]
            if new_value < 0:
                # removing attribute if value is 0
                Logger().logger.info("SCHE process: value <=0 removing"+" FILE "+event+" COLL "+str(e["collection_id"])+" CARD "+str(e["card_id"])+"  ATTR "+str(e["attribute_id"])+" VAL "+str(e["value"]))
                attribute.remove()
            else:
                Logger().logger.info("SCHE process: set value"+" FILE "+event+" COLL "+str(e["collection_id"])+" CARD "+str(e["card_id"])+"  ATTR "+str(e["attribute_id"])+" VAL "+str(new_value))
                resp = attribute.set_value(new_value)
        else:
            Logger().logger.info("SCHE process: no such attribute"+" FILE "+event+" COLL "+str(e["collection_id"])+" CARD "+str(e["card_id"])+"  ATTR "+str(e["attribute_id"]))

        # rename file
        t = event.split("/")
        t[-1] = "x"+t[-1]
        fn = "/".join(t)
        os.rename(event,fn)
