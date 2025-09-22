# community
import os
from glx.api.community import CommunityApi
from glx.member import Member
from glx.collection import Collection
import json
import glx.helper as helper

class Community(object):
    def __init__(self, community_name):
        self.name = community_name
        self.config = helper.load_community_config(community_name)
        self.api = CommunityApi(community_name)

    ###############################################################
    # collections
    ###############################################################
    def collections(self):
        # id
        # name
        return self.api.get_collections()

    def collection(self,collection_id):
        return Collection(self.name,collection_id)
    ###############################################################
    # members
    ###############################################################
    def _refresh_members(self):
        # get members from api
        members = self.api.get_members()
        helper.save_as_json(os.path.join(self.config["data_folder"],"members.json"),members)
        return members

    def members(self):
        members = self._refresh_members()
        return members

    def member(self,member_id):
        return Member(self.name,member_id)
    ###############################################################

    #@classmethod
    #def get_community_instance(cls,community_name):
    #    gc = helper.load_global_config()
    #    croot = gc["COMMUNITIES"]
    #    # check for config file. Just checking the existence of the file, not its content.
    #    config_file = os.path.join(croot,community_name,"config","config.toml")
    #    if not os.path.isfile(config_file):
    #        #print("Community Creation Error: config file not found:",config_file)
    #        return None

    #    return cls(community_name)

