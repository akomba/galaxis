import os
import json
import toml

# config = helper.load_community_config(community_name)
# self.api = CommunityApi(config["API_KEY"],config["api_root"])

def save_as_json(fname,data):
    with open(fname, 'w') as f:
        json.dump(data, f, indent=4)

def load_json(fname):
    with open(fname, 'r') as f:
        return json.load(f)

def dict_by_attr(l,attr,make_it_int=False):
    d = {}
    for x in l:
        if make_it_int:
            d[int(x[attr])] = x
        else:
            d[x[attr]] = x
    return d

def config():
    # load global config
    gc = { "API_ROOT":    "https://app.galaxis-community.com/%COMMUNITY_ID%/communityserver/api" }
    gc["DATA_ROOT"] = os.path.join(os.path.expanduser("~user"),".local/share/glx/data")
    gc["COMMUNITIES"] = os.path.join(gc["DATA_ROOT"],"communities")
    os.makedirs(gc["DATA_ROOT"],exist_ok=True)
    os.makedirs(gc["COMMUNITIES"],exist_ok=True)
    return gc

def load_community_config(community_name):
    # load global config
    gc = config()
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
