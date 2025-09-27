import os
import json
import toml
        
GLX_DEFAULT_CONFIG = {"community_name":False,"collection_id":1}
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
    log_folder = os.path.join(croot,community_name,"log")
    os.makedirs(config_folder,exist_ok=True) 
    os.makedirs(data_folder,exist_ok=True) 
    os.makedirs(log_folder,exist_ok=True) 
    # load communtity specific config
    config_file = os.path.join(config_folder,"config.toml")
    if not os.path.isfile(config_file):
        print("no such config file:",config_file)
        return None

    with open(config_file,"r") as f:
        cfg = toml.load(f)

    cfg["config_folder"] = config_folder
    cfg["data_folder"] = data_folder
    cfg["log_folder"] = log_folder
    cfg["api_root"] = gc["API_ROOT"].replace("%COMMUNITY_ID%",cfg["COMMUNITY_ID"])

    return cfg

##############################################################
#
# local app configs
#
##############################################################
def cfg_filename(appname):
    return "."+appname+".toml"

def save_app_config(appname,config):
    fname = cfg_filename(appname)
    with open(fname,"w") as f:
        toml.dump(config,f)
    return fname

def set_app_config(appname,k,v):
    config = load_app_config(appname)
    config[k] = v
    save_app_config(appname,config)
    return config

def load_app_config(appname):
    fname = cfg_filename(appname)
    if os.path.isfile(fname):
        with open(fname) as f:
            config = toml.load(f)
        return config
    else:
        return {}

def create_app_config(appname,config):
    # check if there is a glx config
    # if so, use that as the default
    glx_config = load_app_config("glx")
    if not glx_config:
        glx_config = GLX_DEFAULT_CONFIG
    # merge glx config wit app config
    config = config | glx_config
    fname = save_app_config(appname,config)
    return fname

def load_or_create_app_config(appname,config_template):
    config = load_app_config(appname)
    if not config:
        fn = create_app_config(appname,config_template)
        print("Config file created:",fn)
        print("Please fill it out carefully and run this app again")
        exit()
    if not config["community_name"]:
        print("Community name is not set.")
        print("Check your config file:",cfg_filename(appname))
        exit() 
    
    print("config -------")
    for k,v in config.items():
        print(k,":",v)
    print("--------------")
    
    return config

##############################################################
#
# local glx configs
#
##############################################################
#def set_active_community(community_name):
#    if not community_name in [c for c in communities()]:
#        print("unknown community, exiting.")
#        exit(1)
#
#    config = load_local_config()
#    config["community"] = community_name
#    if not config["collection"]:
#        config["collection"] = 1
#    save_local_config(config)

def save_local_config(config):
    with open(".config.toml","w") as f:
        toml.dump(config,f)

#def set_local_config(k,v):
#    config = load_local_config()
#    config[k] = v
#    save_local_config(config)
#    return config

def load_local_config():
    if os.path.isfile(".config.toml"):
        with open(".config.toml") as f:
            config = toml.load(f)
        return config
    else:
        config = {"community":False,"collection":1,"attribute":False,"card":False}
        save_local_config(config)
    return config

def get_active_community():
    c = load_local_config()
    return c["community"]
##############################################################
#
# attributes
#
##############################################################
def load_attrib_config(community_name,collection_id,attribute_id):
    # get folder
    gc = load_global_config()

    config_file = os.path.join(gc["COMMUNITIES"],community_name,"config",str(collection_id)+"_"+str(attribute_id)+".toml")

    if os.path.isfile(config_file):
        with open(config_file) as f:
            config = toml.load(f)
        return config
    else:
        return {}

def save_attrib_config(community_name,collection_id,attribute_id,config):
    # get folder
    gc = load_global_config()

    config_file = os.path.join(gc["COMMUNITIES"],community_name,"config",str(collection_id)+"_"+str(attribute_id)+".toml")
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

