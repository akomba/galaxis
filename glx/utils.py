import os
from glx.community import Community
import toml
import glx.helper as helper

##############################################################
#
# utils
#
##############################################################
def set_active_community(community_name):
    if not community_name in [c.name for c in communities()]:
        print("unknown community, exiting.")
        exit(1)

    config = get_config()
    config["community"] = community_name
    if not config["collection"]:
        config["collection"] = 1
    save_config(config)

def save_config(config):
    with open(".config.toml","w") as f:
        toml.dump(config,f)

def set_config(k,v):
    config = get_config()
    config[k] = v
    save_config(config)
    return config

def get_config():
    if os.path.isfile(".config.toml"):
        with open(".config.toml") as f:
            config = toml.load(f)
        return config
    else:
        config = {"community":False,"collection":False,"attribute":False,"card":False}
        save_config(config)
    return config

def list_options(options,selected=None):
    for l in options:
        if selected and selected == int(l["id"]):
            s = "*"
        else:
            s = " "
        prid = s+("   "+str(l["id"]))[-4:]
        print(prid,l["name"])

##############################################################
#
# attributes
#
##############################################################
def load_attrib_config(attribute_id):
    # get folder
    gc = helper.config()

    # get community name from local config
    lc = get_config()
    if not lc["community"]:
        return {}

    config_file = os.path.join(gc["COMMUNITIES"],lc["community"],"config",str(attribute_id)+".toml")

    if os.path.isfile(config_file):
        with open(config_file) as f:
            config = toml.load(f)
        return config
    else:
        return {}

def save_attrib_config(attribute_id,config):
    # get folder
    gc = helper.config()

    # get community name from local config
    lc = get_config()
    if not lc["community"]:
        return None

    config_file = os.path.join(gc["COMMUNITIES"],lc["community"],"config",str(attribute_id)+".toml")
    with open(config_file,"w") as f:
        toml.dump(config,f)


##############################################################
#
# communities
#
##############################################################

def communities():
    # get community folders
    gc = helper.config()
    croot = gc["COMMUNITIES"]

    community_folders = [f for f in os.listdir(croot) if os.path.isdir(os.path.join(croot, f))]
   
    # find the ones with api keys
    # ideally I should also check if the api key is working...

    communities = []
    for c in community_folders:
        community = Community.get_community_instance(c)
        if community:
            communities.append(community)

    return communities
