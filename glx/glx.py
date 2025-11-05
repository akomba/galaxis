#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import glx.helper as helper
from glx.logger import Logger
import os
import toml
from glx.community import Community
from glx.collection import Collection
import importlib
import argparse
import json
import ast

__version__ = "0.5.8"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("comm", help="process or init a community", nargs="?", choices=("process","init","communities"))
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-c", "--community")
    parser.add_argument("--collection")
    parser.add_argument("-p", "--process", action="store_true")
    parser.add_argument("-a", "--attribute")
    parser.add_argument("-l", "--list")
    parser.add_argument("-s", "--set")
    parser.add_argument("-i", "--info", action="store_true")
    parser.add_argument('--init', action="store_true")
    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit(0)
    
    if args.comm == "communities":
        for community in helper.communities():
            print(community)
        exit(0)

    if args.comm == "init":
        init_new_community()

    ###################################################
    #
    # from this point
    # we need a community selected
    # eithe by the --communnity command
    # or defaulting to the singular existing one
    #
    ###################################################

    community_name = helper.select_community(args.community)
   
    # from this point community_name is guaranteed

    if args.comm == "process":
        lc = helper.load_local_config()
        if not community_name in lc:
            lc[community_name] = 0
        iteration = lc[community_name]


        # looping through installed apps of the community
        # and executing the loops if their time came
        print(community_name,"apps:",",".join([a["name"] for a in apps(community_name)]),iteration)
        for app in apps(community_name):
            # read config file
            if "loops" in app["config"]:
                for l in app["config"]["loops"]:
                    if "repeat" in l and "module" in l and "name" in l:
                        if l["repeat"] == 1 or iteration % l["repeat"] == 0:
                            print("  *",community_name,"> running",l["name"],"(every",l["repeat"],"iterations)")
                            m = importlib.import_module(l["module"])
                            m.main(community_name)
    
        # increase iteration
        lc[community_name] += 1
        helper.save_local_config(lc)

    # collection
    if args.collection:
        collection_id = args.collection
    else:
        collection_id = 1

    # if a single attribute is selected
    if args.attribute:
        if args.attribute.isnumeric():
            attid = int(args.attribute)
        else:
            # get list of attributes
            attributes = _list_of_attributes(community_name,collection_id)
            atts = []
            for att in attributes:
                if args.attribute.lower() in att["name"].lower():
                    atts.append(att)
            if len(atts)==0:
                print("Attribute not found:",args.attribute)
                exit(0)
            elif len(atts) > 1:
                print("Multiple attributes found for",args.attribute,":")
                for a in atts:
                    print(a)
                print("Be more specific or use the ID.")
                exit(0)
            print(atts)
            attid = int(atts[0]["id"])
        collection = Collection(community_name,collection_id)
        attribute = collection.attribute(attid)
        print(attribute.name)
        #print("Todo: properties (leaking, max value, etc)")
        #print("Cards: todo: show  attribute value on cards")
        if args.info:
            # check for local modifiers
            # check for online settings
            print("Config:")
            helper.pretty(_attribute_config_list(attribute))
        if args.list:
            if args.list == "cards":
                # list cards with the given attribute
                print("Cards with",attribute.name+":")
                for instance in sorted(attribute.instances(), key=lambda d: d["card_id"]):
                    print(" ",instance["card_id"],":",instance["value"])
                    if instance["interacted_with"]:
                        print("   intercated at:",instance["interacted_at"])
                        print("   int value    :",instance["interacted_value"])
        if args.set:
            upd = ast.literal_eval(args.set)
            if not type(upd) is dict:
                print("error: the set argument has to be a dictionary.")
                exit()

            # do the update
            attribute.update(upd)
        exit(0)

    # lists about the selected community
    if args.list:
        #if args.list in ["attributes","apps","cards","communities"]:
        if args.list == "attributes":
            helper.list_options(_list_of_attributes(community_name,collection_id))
        elif args.list == "apps":
            applist = apps(community_name)
            if applist:
                helper.list_options(applist)
            else:
                print("no apps found")
        elif args.list == "cards":
            collection = Collection(community_name,collection_id)
            print(collection.data())
            for card in collection.cards():
                print(card.id)
        elif args.list == "communities":
            for community in helper.communities():
                print(community)
        else:
            print("unknown option:",args.list)
        exit(0)

def _attribute_config_list(attribute):
    config = attribute.config()
    if "interactive_config" in config.keys() and config["interactive_config"]:
        ic = config.pop("interactive_config")
        for k,v in ic.items():
            config["ic_"+k] = v
    return config


def _list_of_attributes(community_name,collection_id):
    collection = Collection(community_name,collection_id)
    return collection.attributes(raw=True)

def init_new_community():
    community_name = input("community name (no spaces pls): ")
    
    # check if name is taken
    if community_name in helper.communities():
        print("Community name already exists. Exiting.")
        exit(1)

    #if not, create folder structure and ask for api key and community id
    api_key = input("api key: ")
    community_id = input("community id: ")

    # create community root
    gc = helper.load_global_config()
    d = os.path.join(gc["DATA_ROOT"],"communities",community_name)
    os.makedirs(d, exist_ok = True)

    # config folder
    os.makedirs(os.path.join(d,"config"), exist_ok = True)

    # config file
    community_config = {
            "API_KEY": api_key,
            "COMMUNITY_ID": community_id,
            "COMMUNITY_NAME": community_name
    }
    config_file = os.path.join(d,"config","config.toml")
    with open(config_file,"w") as f:
        toml.dump(community_config,f)

    print("Community config file saved to",config_file)
    # data folder
    os.makedirs(os.path.join(d,"data"), exist_ok = True)

    # apps folder
    os.makedirs(os.path.join(d,"apps"), exist_ok = True)

    # create scheduler app
    os.makedirs(os.path.join(d,"apps","scheduler"), exist_ok = True)
    os.makedirs(os.path.join(d,"apps","scheduler","data","active"), exist_ok = True)
    os.makedirs(os.path.join(d,"apps","scheduler","data","processed"), exist_ok = True)
    # scheduler config
    scheduler_config_template = {
        "loops":[{
            "module": "glx.scheduler",
            "repeat": 60,
            "name"  : "scheduler loop"
        }]
    }
    helper.create_app_config(community_name,"scheduler",scheduler_config_template)

    #############################################

    c = Community(community_config["COMMUNITY_NAME"])
    print("Name:",c.name )
    exit(0)

def apps(community_name):
    config = helper.load_community_config(community_name)
    apps = []
    counter = 1
    for app in os.listdir(config["apps_folder"]):
        conf = helper.load_app_config(community_name,app)
        if conf:
            apps.append({"config":conf,"id": counter,"name":app})
    return apps

