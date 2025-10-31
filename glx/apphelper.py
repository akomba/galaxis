import glx.helper as helper
from glx.logger import Logger
from glx.collection import Collection
from glx.api.mothership import MothershipApi
from glx.api.community import CommunityApi
import glx.helper as helper
import argparse
import os

def setup_parser():
    p = argparse.ArgumentParser()
    p.add_argument("-v", "--version", action="store_true")
    p.add_argument("-i", "--info", action="store_true")
    p.add_argument("-c", "--community")
    p.add_argument("--collection")
    return p

def process_common_args(args,version,app_name):
    if args.version:
        if version:
            print(version)
        exit(0)

    community_name = helper.select_community(args.community)

    if args.info:
        # app name
        print("Name:",app_name)
        print("Version:",version)
        
        # config location
        config_loc = helper.config_location(community_name,app_name)
        print("Config location:",config_loc)

        config = helper.load_app_config(community_name,app_name)
        # app status
        print("= config =========")
        helper.pretty(config)
        print("==================")
        exit(0)
    return community_name

def appupdate(cv,APPNAME,config,asset_name,community_name):
    #community_name = appstart(version,community_name)
    
    Logger().init(community_name)
    
    collection = Collection(community_name,config["collection_id"])
    mapi = MothershipApi()
    assets = mapi.get_asset_owners(asset_name)
    cards = collection.cards(raw=True)
    instances = collection.attribute(config["attribute_id"]).instances()

    cards_by_owner = {}
    cards_by_id = {}
    for k in cards:
        k["owner"] = k["owner"].lower()
        cards_by_id[k["id"]] = k
        cards_by_owner[k["owner"]] = k

    #print("cards by id")
    #for k,v in cards_by_id.items():
    #    print(k,v)

    #print("community:",community_name)
    print("      ",asset_name, "assets:",len(assets),"cards:",len(cards),"instances:",len(instances))
    # three lists:
    # 1. assets: the list of owners based on the mothership
    # 2. instances: the list of cards with benefits based on the community server
    # 3. cards: the full list of cards, for the owner addresses

    # 4. save the updated list in logs (or data...)
    isoslug = helper.isoslug()
    helper.save_app_data(community_name,APPNAME,isoslug+"_assets",assets) 
    helper.save_app_data(community_name,APPNAME,isoslug+"_cards",cards) 
    helper.save_app_data(community_name,APPNAME,isoslug+"_instances",instances) 
    
    # 1. remove the benefits from the cards if it is not on the ownership list (asset was removed)
    for instance in instances:
        o = cards_by_id[instance["card_id"]]["owner"]
        if not o in assets:
            print("no more assets for",o)
            # remove attribute
            card = collection.card(instance["card_id"])
            card.remove_attribute(config["attribute_id"])
            print("removing attribute from card",card.id)

    # 2. add the attribute if it is on the asset list but not on the instance list (asset was added)
    instance_owners = [cards_by_id[i["card_id"]]["owner"] for i in instances]
    
    for k,v in assets.items():
        if not k in instance_owners:
            value = cv(v)
            if k in cards_by_owner:
                card = collection.card(cards_by_owner[k]["id"])
                card.add_attribute(config["attribute_id"],value)

                print("adding attribute to card",card.id,"with value",value)

    # 3. update benefit is asset changed. (easier to loop through whole list)
    for instance in instances:
        o = cards_by_id[instance["card_id"]]["owner"]
        old_val = instance["value"]
        new_val = cv(assets[o])
        if old_val != new_val:
            print("card",instance["card_id"],"value changed from",old_val,"to",new_val)
            card = collection.card(instance["card_id"])
            card.add_attribute(config["attribute_id"],new_val)
