#!/usr/bin/env python

# community                                 | lists known communities
# community set [communityname]             | sets active community
# community init [communityname]            | initializes new community
# community [communityname] att             | lists attributes
# community [communityname] att --refresh   | refreshes attributes

from glx.community import Community
import sys
import os
import toml
import glx.helper as helper
from glx.logger import Logger

APPNAME = "glx"

def main():
    communities = helper.communities()
    lg = Logger()
    lg.logger.info("test log")

    config = helper.load_or_create_app_config(APPNAME,helper.GLX_DEFAULT_CONFIG)
    
    if len(sys.argv) == 1:
        # list communities, mark active if any
        
        for community in communities:
            if community == config["community_name"]:
                x = " * "
                y = " < "
            else:
                x = "   "
                y = "   "
            print(x+community+y)

    elif sys.argv[1] == "init":
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
        print(d)
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
        # download attributes
        c.attributes()

    elif sys.argv[1] == "set":
        # sets active community
        helper.set_app_config(APPNAME,"community_name",sys.argv[2])

if __name__ == "__main__":
    main()
