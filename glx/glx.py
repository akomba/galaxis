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

__version__ = "0.5"

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-c", "--community")
    parser.add_argument("process", nargs='?')
    parser.add_argument("-a", "--attribute")
    parser.add_argument("-l", "--list")
    parser.add_argument('init', nargs='?')
    args = parser.parse_args()

    communities = helper.communities()
    config = helper.load_global_config()

    if args.version:
        print(__version__)
        exit(0)
    
    if "communities" in sys.argv[1:]:
        for community in communities:
            print(community)
        exit(0)

    if args.community:
        if not args.community in helper.communities():
            print("unknown community:",args.community)
            exit(0)
     
    if args.init:
        community_name = input("community name (no spaces pls): ")

        # check if name is taken
        if community_name in communities:
            print("community name already exists. Exiting.")
            exit(1)

        #if not, create folder structure and ask for api key and community id
        api_key = input("api key: ")
        community_id = input("community id: ")

        # create community root
        d = os.path.join(config["DATA_ROOT"],"communities",community_name)
        os.makedirs(d, exist_ok = True)

        # config folder
        os.makedirs(os.path.join(d,"config"), exist_ok = True)

        # config file
        config = {
                "API_KEY": api_key,
                "COMMUNITY_ID": community_id,
                "COMMUNITY_NAME": community_name
                }
        config_file = os.path.join(d,"config","config.toml")
        with open(config_file,"w") as f:
            toml.dump(config,f)

        print("community config file saved to",config_file)
        # data folder
        os.makedirs(os.path.join(d,"data"), exist_ok = True)

        # apps folder
        os.makedirs(os.path.join(d,"apps"), exist_ok = True)

        # create scheduler app
        os.makedirs(os.path.join(d,"apps","scheduler"), exist_ok = True)
        os.makedirs(os.path.join(d,"apps","scheduler","data","active"), exist_ok = True)
        os.makedirs(os.path.join(d,"apps","scheduler","data","processed"), exist_ok = True)
        # scheduler config
        config_template = {
                "module":"glx",
                "repeat":60
        }
        config = helper.load_or_create_app_config(community_name,"scheduler",config_template)

        #############################################

        c = Community(config["COMMUNITY_NAME"])
        print("name:",c.name )
        exit(0)

    if args.process and args.community:
        community = args.community
        lc = helper.load_local_config()
        if not community in lc:
            lc[community] = 0
        iteration = lc[community]

        print(community,"apps:",apps(community).keys())
        for appname,conf in apps(community).items():
            # read config file
            if "repeat" in conf:
                if conf["repeat"] == 1 or iteration % conf["repeat"] == 0:
                    print("*",community,"> running",appname,"(every",conf["repeat"],"iterations)")
                    # check for module info in the config file
                    if "module" in conf:
                        mname = conf["module"]
                    else:
                        mname = appname

                    m = importlib.import_module(mname+"."+appname)
                    m.main(community)
    
        # increase iteration
        lc[community] += 1
        helper.save_local_config(lc)

    elif args.community and args.list:
        if args.list == "attributes":
            collection = Collection(args.community,1)
            helper.list_options(collection.attributes(raw=True))
        elif args.list == "apps":
            for k,v in apps(args.community).items():
                print(k)
            if not apps(args.community):
                print("no apps found")
        else:
            print("unknown option:",args.list)
        exit(0)

    elif args.community and args.attribute:
        collection = Collection(args.community,1)
        attribute = collection.attribute(args.attribute)
        print(attribute.name)
        print("Cards:")
        for instance in attribute.instances():
            print("   "+str(instance["card_id"]))
        exit(0)
    # try to get apps
    # don't worry how the apps get there
    # read the config and execute based on that
    # get a counter going
    # and execute scripts when the modulo is zero
    
    # local config to read iterations from

def apps(community):
    config = helper.load_community_config(community)
    apps = {}
    for app in os.listdir(config["apps_folder"]):
        conf = helper.load_app_config(community,app)
        if conf:
            apps[app] =  conf
    
    return apps

if __name__ == "__main__":
    main()
