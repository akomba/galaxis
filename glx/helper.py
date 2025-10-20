import os
import json
import toml
import datetime

GLX_DEFAULT_CONFIG = {"iteration":0}
GLX_CONFIG_NAME = ".config.toml"
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
    gc = { "SERVER_URL":    "https://app.galaxis-community.com/%COMMUNITY_ID%/communityserver" }
    #gc = { "API_ROOT":    "https://app.galaxis-community.com/%COMMUNITY_ID%/communityserver/api" }
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
    apps_folder = os.path.join(croot,community_name,"apps")
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
    cfg["apps_folder"] = apps_folder
    cfg["server_url"] = gc["SERVER_URL"].replace("%COMMUNITY_ID%",cfg["COMMUNITY_ID"])
    cfg["api_root"] = cfg["server_url"]+"/api"
    cfg["socketio_url"] = cfg["server_url"]

    return cfg

##############################################################
#
# local app data
#
##############################################################
def save_app_data(community_name,app_name,title,data):
    cc = load_community_config(community_name)
    data_folder = os.path.join(cc["apps_folder"],app_name,"data")
    os.makedirs(data_folder,exist_ok=True)
    fn= os.path.join(data_folder,title+".json")
    #print("save app data:",fn)
    save_as_json(fn,data)

def load_app_data(community_name,app_name,title):
    cc = load_community_config(community_name)
    data_folder = os.path.join(cc["apps_folder"],app_name,"data")
    fn= os.path.join(data_folder,title+".json")
    if os.path.isfile(fn):
        return load_json(fn)
    else:
        return None

##############################################################
#
# local app configs
#
##############################################################
def cfg_filename(community_name, app_name):
    # find proper config path
    cc = load_community_config(community_name)
    appconf_folder =  os.path.join(cc["apps_folder"],app_name)
    os.makedirs(appconf_folder,exist_ok=True) 
    return os.path.join(appconf_folder,"."+app_name+".toml")

def save_app_config(community_name, app_name,config):
    fname = cfg_filename(community_name,app_name)
    with open(fname,"w") as f:
        toml.dump(config,f)
    return fname

def set_app_config(community_name, app_name,k,v):
    config = load_app_config(app_name)
    config[k] = v
    save_app_config(community_name, app_name,config)
    return config

def load_app_config(community_name, app_name):
    fname = cfg_filename(community_name,app_name)
    
    if os.path.isfile(fname):
        with open(fname) as f:
            config = toml.load(f)
        # dynamically add data folder
        cc = load_community_config(community_name)
        config["data_folder"] = os.path.join(cc["apps_folder"],app_name,"data")
        os.makedirs(config["data_folder"],exist_ok=True) 
        config["logs_folder"] = os.path.join(cc["apps_folder"],app_name,"logs")
        os.makedirs(config["logs_folder"],exist_ok=True) 
        return config
    else:
        return {}

def create_app_config(community_name, app_name,config):
    # check if there is a glx config
    # if so, use that as the default
    #glx_config = load_local_config()
    #if not glx_config:
    #    glx_config = GLX_DEFAULT_CONFIG
    # merge glx config wit app config
    #config = config | glx_config
    fname = save_app_config(community_name,app_name,config)
    return fname

def load_or_create_app_config(community_name, app_name, config_template):
    config = load_app_config(community_name, app_name)
    if not config:
        fn = create_app_config(community_name, app_name, config_template)
        print("Config file created:",fn)
        print("Please fill it out carefully and run this app again")
        exit()
    
    #print("config -------")
    #for k,v in config.items():
    #    print(k,":",v)
    #print("--------------")
    
    return config

##############################################################
#
# local glx configs
#
##############################################################
# this is only to save the community's name
# in the local folder

def set_local_config(k,v):
    config = load_local_config()
    config[k] = v
    save_local_config(config)
    return config

def create_local_config():
    fname = save_local_config(GLX_DEFAULT_CONFIG)
    return GLX_DEFAULT_CONFIG

def load_local_config():
    if os.path.isfile(GLX_CONFIG_NAME):
        with open(GLX_CONFIG_NAME) as f:
            config = toml.load(f)
        return config
    else:
        return create_local_config()

def save_local_config(config):
    with open(GLX_CONFIG_NAME,"w") as f:
        toml.dump(config,f)

def get_active_community():
    c = load_local_config()
    return c["community_name"]
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

def isoslug(dt=None):
    if not dt:
        dt = datetime.datetime.now()
    return dt.isoformat().replace(":","_").replace(".","_")
