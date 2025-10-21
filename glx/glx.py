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

__version__ = "0.4"

def main():
    if "--version" in sys.argv[1:]:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--community")
    parser.add_argument("-l", "--list")
    parser.add_argument('init', nargs='?')
    args = parser.parse_args()

    communities = helper.communities()
    config = helper.load_global_config()

    if args.init:
        community_name = input("community name (no spaces pls): ")

        # check if name is taken
        if community_name in communities:
            print("community name already exists. Exiting.")
            exit(1)

        #if not, create folder structure and ask for api key and community id
        api_key = input("api key (blank for read only community): ")
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

        # data folder
        os.makedirs(os.path.join(d,"data"), exist_ok = True)

        # apps folder
        os.makedirs(os.path.join(d,"apps"), exist_ok = True)

        #############################################

        c = Community(config["COMMUNITY_NAME"])
        print("name:",c.name )
        exit(0)

    if "communities" in sys.argv[1:]:
        for community in communities:
            print(community)
        exit(0)

    elif args.community and args.list:
        if args.list == "attributes":
            collection = Collection(args.community,1)
            helper.list_options(collection.attributes(raw=True))
        exit()

    # try to get apps
    # don't worry how the apps get there
    # read the config and execute based on that
    # get a counter going
    # and execute scripts when the modulo is zero
    
    # local config to read iterations from
    lc = helper.load_local_config()
    print("ITER:",lc["iteration"])
    for community in communities:
        config = helper.load_community_config(community)
        apps = config["apps_folder"]
        for app in os.listdir(apps):
            # read config file
            conf = helper.load_app_config(community,app)
            if "repeat" in conf:
                if conf["repeat"] == 1 or lc["iteration"] % conf["repeat"] == 0:
                    print("*",community,"> running",app,"(every",conf["repeat"],"iterations)")
                    m = importlib.import_module(app+"."+app)
                    m.main(community)
    # increase iteration
    lc["iteration"] += 1
    helper.save_local_config(lc)

if __name__ == "__main__":
    main()
