import json
import os
import glx.helper as helper
import datetime
from glx.card_attribute import CardAttribute
from glx.api.community import CommunityApi
from glx.community import Community
import time
from glx.logger import Logger

def list_active(community_name):
    conf = helper.load_app_config(community_name,"scheduler")
    sf = os.path.join(conf["data_folder"],"active")

    # get (active) schedules
    schedules = [os.path.join(sf,f) for f in os.listdir(sf) if f[0] != "x"]
    print("active schedules:",len(schedules))
    return schedules

def list_due(community_name):
    # lists the events that are already due
    events = list_active(community_name)
    due = []
    for event in events:
        e = helper.load_json(event)
        if datetime.datetime.fromisoformat(e["expiration"]) <= datetime.datetime.now():
            due.append(event)

    print("due schedules:",len(due))
    return due

def show_due(community_name):
    events = list_due(community_name)
    for event in events:
        print(event)

def process_leaks(community_name):
    community = Community(community_name)
    for collection in community.collections():
        leakers = {}
        for att in collection.attributes():
            if "leak" in att.config() and att.config("leak"):
                print("LK:",att.name,att.config("leak"))
                leakers[att.id] = att
        # get all members
        if not leakers:
            print("no leaking attributes found")
            return

        print("leakers:",[l.name for l in leakers])
        cards = collection.cards()
        for card in cards:
            catts = card.attributes(raw=True)
            for catt in catts:
                if catt["attribute_id"] in leakers.keys():
                    attribute = leakers[catt["attribute_id"]]
                    value = card.attribute(attribute.id).value()
                    reduce_by = attribute.config("leak")/24 
                    new_value = value - reduce_by
                    if new_value <= 0:
                        print("LK:",card.id,"DEL",attribute.name)
                        card.remove_attribute(attribute.id)
                    else:
                        card.add_attribute(attribute.id,new_value)
                        print("LK:",card.id,"VAL",attribute.name,":",card.attribute(attribute.id).value())

def main(community_name):
    process_leaks(community_name)
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
            if new_value <= 0:
                # removing attribute if value is 0
                message = "SCHE process: value <=0 removing"+" FILE "+event+" COLL "+str(e["collection_id"])+" CARD "+str(e["card_id"])+"  ATTR "+str(e["attribute_id"])+" VAL "+str(e["value"])
                attribute.remove()
            else:
                message = "SCHE process: set value"+" FILE "+event+" COLL "+str(e["collection_id"])+" CARD "+str(e["card_id"])+"  ATTR "+str(e["attribute_id"])+" VAL "+str(new_value)
                resp = attribute.set_value(new_value)
        else:
            message = "SCHE process: no such attribute"+" FILE "+event+" COLL "+str(e["collection_id"])+" CARD "+str(e["card_id"])+"  ATTR "+str(e["attribute_id"])
        print(message)
        Logger().logger.info(message)

        # move file
        fn = event.replace("active","processed")
        os.rename(event,fn)
