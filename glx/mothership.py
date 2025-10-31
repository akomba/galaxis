from glx.api.mothership import MothershipApi
import glx.helper as helper
import os
import urllib.request
import json 
import shutil

# shows list of available assets
# shows list of instances of an asset
# shows details of an instance
   
# -o owner:
# get assets by owner
# either with or  without asset type
# implement these into functions that
# can be imported to other things
# include metadata if available

class Mothership(object):
    def __init__(self):
        self.mapi = MothershipApi()
        self.projects_data ={
            "ether-cards" : {"id_name":"id","metadata_url":"https://heroku.ether.cards/card/all"},
            "engines"     : {"id_name":"id","metadata_url":None},
            "tokaido-cats": {"id_name":"tokenId","metadata_url":"https://app.galaxis.xyz/3/1/metadata/all"},
            "gen-zero"    : {"id_name":"tokenId","metadata_url":"https://gen-zero-metadata.galaxis.xyz/api/metadata/all"},
            "grd"         : {"id_name":"tokenId","metadata_url":"https://metadata.grd.fan/api/metadata/all"}
        }

        self.gc = helper.load_global_config()
        self.assets_folder = os.path.join(self.gc["DATA_ROOT"],"assets")
        os.makedirs(self.assets_folder,exist_ok=True)
        self.old_assets_folder = os.path.join(self.assets_folder,"old")
        os.makedirs(self.old_assets_folder,exist_ok=True)

        self.mapi_assets = self.mapi.get_assets()["data"]

        for project in self.mapi_assets:
            self.projects_data[project["name"]]["mapi_id"] = project["uid"]
    
    def project_name(self,project_id):
        return self.mapi_assets[project_id]["name"]

    def _metadata_file(self,project_name):
        return os.path.join(self.assets_folder,project_name+"_metadata.json")

    def _owners_file(self,project_name):
        return os.path.join(self.assets_folder,project_name+"_owners.json")

    def update_metadata(self,project_name):
        # 1. save existing to old
        if os.path.isfile(self._metadata_file(project_name)):
            isoslug = helper.isoslug()
            shutil.copy(self._metadata_file(project_name),os.path.join(self.old_assets_folder,helper.isoslug()+"_"+project_name+"_metadata.json"))

        # 2. get fresh data from server
        url = self.projects_data[project_name]["metadata_url"]
        if url:
            #print("downloading from",url)
            with urllib.request.urlopen(url) as url:
                data = json.loads(url.read().decode())
        else:
            # we are dealing with the engines
            # let's fake metadata.
            # FIXME remove this asap
            owners = self.owners(project_name)
            data =[]
            for i in range(len(owners.keys())):
                data.append({"id":i+1,"name":"Engine #"+str(i+1),"image":"https://galaxis-metadata.com/engines/placeholder.jpg"})

        # 3. save fresh data, overwrite current list
        with open(self._metadata_file(project_name),"w") as f:
            json.dump(data,f,indent=4)

    def metadata(self,project_name, refresh=False):
        if (not os.path.isfile(self._metadata_file(project_name))) or refresh:
            print("downloading metadata, please stand by")
            print("downloading",self._metadata_file(project_name))
            self.update_metadata(project_name)

        # load metadata file
        with open(self._metadata_file(project_name)) as f:
            data = json.load(f)
        return data

    def owners(self,project_name, refresh=False):
        if (not os.path.isfile(self._owners_file(project_name))) or refresh:
            print("downloading owners file, please stand by")
            print("downloading",self._owners_file(project_name))
            self.update_owners(project_name)
        
        # load metadata file
        with open(self._owners_file(project_name)) as f:
            data = json.load(f)
        return data

    def update_owners(self,project_name):
        # 1. save existing to old
        if os.path.isfile(self._owners_file(project_name)):
            isoslug = helper.isoslug()
            shutil.copy(self._owners_file(project_name),os.path.join(self.old_assets_folder,helper.isoslug()+"_"+project_name+"_owners.json"))
        
        # 2. get fresh data from server
        owners = self.get_project_owners(project_name)

        # 3. save fresh data, overwrite current list
        with open(self._owners_file(project_name),"w") as f:
            json.dump(owners,f,indent=4)

    def get_project_owners(self,project_name):
        return self.mapi.get_asset_owners(project_name)


    ###########################
    #
    # end users...
    #
    ###########################
    def project_dict(self,project_name, refresh=False):
        # returns a list of all asset instances
        # combining metadata and owner info
        # as a dict, where assed_id is the key
        if not "dict" in self.projects_data[project_name]:
            metadata = self.metadata(project_name, refresh)
            project_dict = {}
            id_name = self.projects_data[project_name]["id_name"]
            for a in metadata:
                #print(a)
                project_dict[int(a[id_name])] = a
                project_dict[int(a[id_name])]["owner"] = None
       
            owners = self.owners(project_name,refresh)

            for k,v in owners.items():
                for i in v:
                    project_dict[int(i)]["owner"] = k
            
            self.projects_data[project_name]["dict"] = project_dict
        
        return self.projects_data[project_name]["dict"]

    def _assets_by_owner(self,owner_address,project_name):
        adict = self.project_dict(project_name)
        owned = []
        for k,v in adict.items():
            if v["owner"] == owner_address:
                owned.append((project_name,k,v))
        return owned

    def assets_by_owner(self,owner_address,project_name=None):
        if project_name:
            return self._assets_by_owner(owner_address,project_name)
        else:
            owned = []
            for k in self.projects_data.keys():
                owned += self._assets_by_owner(owner_address,k)
            return owned
