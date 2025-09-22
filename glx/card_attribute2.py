# Attribute object

import os
from glx.api.community import CommunityApi
import glx.helper as helper

class Attribute(object):
    def __init__(self, community_name,collection_id,card_id,attribute_id):
        self.community_name = community_name 
        self.collection_id = collection_id
        self.card_id = card_id
        self.id = attribute_id
        
        config = helper.load_community_config(community_name)
        self.api = CommunityApi(config["API_KEY"],config["api_root"])

    def interaction(self):
        # is_interactive: True / False
        # has_interacted: True / False
        # interacted_at : datetime
        a = self.api.get_attribute_interaction(self.collection_id,self.card_id,self.id)
        res = {}
        if not a:
            return False
        if "success" in a:
            res["success"] = a["success"]
        if "data" in a:
            if "is_interactive" in a["data"]:
                res["is_interactive"] = a["data"]["is_interactive"]
            if "interaction" in a["data"]:
                if "can_interact" in a["data"]["interaction"]:
                    res["has_interacted"] = not a["data"]["interaction"]["can_interact"]
                if "interacted_timestamp" in a["data"]["interaction"]:
                    res["interacted_timestamp"] = a["data"]["interaction"]["interacted_timestamp"]
                if "interacted_value" in a["data"]["interaction"]:
                    res["interacted_value"] = a["data"]["interaction"]["interacted_value"]

        return res

    def set_value(self,value):
        print("setting value:",value)
        return self.api.assign_attribute_to_card(self.collection_id,self.card_id,self.id,value)

    def data(self):
        data = self.api.get_attribute(self.collection_id,self.card_id,self.id)
        return data

    def value(self):
        d = self.data()
        if "value" in d:
            v = d["value"]
            if v:
                return float(v)
            else:
                return 0
        else:
            return 0
        
        return self.data()["value"]

    def was_interacted_with(self):
        a = self.api.get_attribute_interaction(self.collection_id,self.card_id,self.id)
        
        if not a:
            return False
        
        if not "data" in a:
            return False

        if "is_interactive" in a["data"]:
            if not a["data"]["is_interactive"]:
                return False
        else:
            return False

        return not a["data"]["interaction"]["can_interact"]

    def remove(self):
        return self.api.remove_attribute_from_card(self.collection_id,self.card_id,self.id)

    @classmethod
    def get_instance(cls,community_name,collection_id,card_id,attribute_id):
        # try to get api
        config = helper.load_community_config(community_name)
        if not config:
            #print("can not get attribute, no such community:",community_name)
            return None

        api = CommunityApi(config["API_KEY"],config["api_root"])
        attr = api.get_attribute(collection_id,card_id,attribute_id)
        if attr:
            return cls(community_name,collection_id,card_id,attribute_id)
        else:
            #print("no such attribute:",community_name,collection_id,card_id,attribute_id)
            return None
