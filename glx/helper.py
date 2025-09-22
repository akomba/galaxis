import os
import json
import toml
##############################################################
#
# load and save files
#
##############################################################
def save_as_json(fname,data):
    with open(fname, 'w') as f:
        json.dump(data, f, indent=4)

def load_json(fname):
    with open(fname, 'r') as f:
        return json.load(f)

##############################################################
#
# global configs
#
##############################################################
def load_global_config():
    # load global config
    gc = { "API_ROOT":    "https://app.galaxis-community.com/%COMMUNITY_ID%/communityserver/api" }
    gc["DATA_ROOT"] = os.path.join(os.path.expanduser("~user"),".local/share/glx/data")
    gc["COMMUNITIES"] = os.path.join(gc["DATA_ROOT"],"communities")
    os.makedirs(gc["DATA_ROOT"],exist_ok=True)
    os.makedirs(gc["COMMUNITIES"],exist_ok=True)
    return gc

def load_community_config(community_name):
    gc = load_global_config()
    croot = gc["COMMUNITIES"]
    config_folder = os.path.join(croot,community_name,"config")
    data_folder = os.path.join(croot,community_name,"data")
        
    # load communtity specific config
    config_file = os.path.join(config_folder,"config.toml")
    if not os.path.isfile(config_file):
        print("no such config file:",config_file)
        return None

    with open(config_file,"r") as f:
        cfg = toml.load(f)

    cfg["config_folder"] = config_folder
    cfg["data_folder"] = data_folder
    cfg["api_root"] = gc["API_ROOT"].replace("%COMMUNITY_ID%",cfg["COMMUNITY_ID"])

    return cfg

##############################################################
#
# local configs
#
##############################################################
def set_active_community(community_name):
    if not community_name in [c for c in communities()]:
        print("unknown community, exiting.")
        exit(1)

    config = load_local_config()
    config["community"] = community_name
    if not config["collection"]:
        config["collection"] = 1
    save_local_config(config)

def save_local_config(config):
    with open(".config.toml","w") as f:
        toml.dump(config,f)

def set_local_config(k,v):
    config = load_local_config()
    config[k] = v
    save_local_config(config)
    return config

def load_local_config():
    if os.path.isfile(".config.toml"):
        with open(".config.toml") as f:
            config = toml.load(f)
        return config
    else:
        config = {"community":False,"collection":False,"attribute":False,"card":False}
        save_local_config(config)
    return config

##############################################################
#
# attributes
#
##############################################################
def load_attrib_config(collection_id,attribute_id):
    # get folder
    gc = load_global_config()

    # get community name from local config
    lc = load_local_config()
    if not lc["community"]:
        return {}

    config_file = os.path.join(gc["COMMUNITIES"],lc["community"],"config",str(collection_id)+"_"+str(attribute_id)+".toml")

    if os.path.isfile(config_file):
        with open(config_file) as f:
            config = toml.load(f)
        return config
    else:
        return {}

def save_attrib_config(collection_id,attribute_id,config):
    # get folder
    gc = load_global_config()

    # get community name from local config
    lc = load_local_config()
    if not lc["community"]:
        return None

    config_file = os.path.join(gc["COMMUNITIES"],lc["community"],"config",str(collection_id)+"_"+str(attribute_id)+".toml")
    with open(config_file,"w") as f:
        toml.dump(config,f)

##############################################################
#
# other
#
##############################################################
def dict_by_attr(l,attr,make_it_int=False):
    d = {}
    for x in l:
        if make_it_int:
            d[int(x[attr])] = x
        else:
            d[x[attr]] = x
    return d

def communities():
    # get community folders
    gc = load_global_config()
    croot = gc["COMMUNITIES"]

    communities = [f for f in os.listdir(croot) if os.path.isdir(os.path.join(croot, f))]
   
    # find the ones with api keys
    # ideally I should also check if the api key is working...

    #communities = []
    #for c in community_folders:
    #    community = Community.get_community_instance(c)
    #    if community:
    #        communities.append(community)

    return communities

def list_options(options,selected=None):
    for l in options:
        if selected and selected == int(l["id"]):
            s = "*"
        else:
            s = " "
        prid = s+("   "+str(l["id"]))[-4:]
        print(prid,l["name"])

