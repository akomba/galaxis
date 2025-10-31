import glx.helper as helper
import importlib
import argparse
import socketio
import asyncio
import os

sio = socketio.AsyncClient()
community_name=None
interactions = []

# loop all communities
# read app configs
# find interactions and listen to them

@sio.on('CardAttributeInteracted')
async def any_event(data):
    if "token_id" in data:
        data["card_id"] = data["token_id"] # I don't want to work wit token_id

    for i in interactions:
        if i["attribute_id"] == data["attribute_id"] and i["collection_id"] == data["collection_id"]:
            m = importlib.import_module(i["module"])
            m.interact(community_name,i["app_name"],data["card_id"],data["data"])

@sio.event
async def connect():
    global community_name
    print("Connected to",community_name)
    await sio.emit("joinRooms", {"rooms":["CardAttributeInteracted"]})

@sio.event
async def connect_error(data):
    print("The connection failed!")

@sio.event
async def disconnect(reason):
    print("I'm disconnected! reason:", reason)

async def listen(cn,community_id,api_key):
    global community_name
    community_name = cn
    url = "https://app.galaxis-community.com"
    path = "/"+community_id+"/communityserver/socket.io"
    auth = {'apiKey': api_key}
    await sio.connect(url, auth=auth, socketio_path=path)
    await sio.wait()

def main():
    global community_name
    global interactions
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--community")
    args = parser.parse_args()
    if args.community:
        # get the list of interactions here
        config = helper.load_global_config()
  
        print(args.community)
        community_config = helper.load_community_config(args.community)
        apps = community_config["apps_folder"]
        # let's collect interactions from config files
        for app in os.listdir(apps):
            # read config file
            conf = helper.load_app_config(args.community,app)
            if "interactions" in conf:
                for i in conf["interactions"]:
                    # fill in the ids if needed.
                    # this replaces the key names with the actual value
                    for k,v in i.items():
                        if v and type(v) is str and v[0]=="!":
                            print("replacing",v)
                            i[k] = conf[v[1:]]

                    i["app_name"] = app
                    interactions.append(i)
        print("known interactions:",[i["name"] for i in interactions])
        asyncio.run(listen(args.community,community_config["COMMUNITY_ID"],community_config["API_KEY"]))
    else:
        print("no community name given, exiting.")
        return(False)

if __name__ == '__main__':
    main()
