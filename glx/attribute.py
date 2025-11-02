# Attribute object
from glx.api.community import CommunityApi
import glx.helper as helper

class Attribute(object):
    LOCAL_SETTINGS=["leak","max"]

    def __init__(self, community_name, collection_id, attribute_id):
        self.collection_id = collection_id
        self.id = attribute_id
        self.api = CommunityApi(community_name)
        # self.data = self.api.get_attribute(self.collection_id,self.id)
        # load config if any
        self.data = helper.load_attrib_config(community_name,collection_id,attribute_id) | self.api.get_attribute(self.collection_id,self.id)
        for s in self.LOCAL_SETTINGS:
            if s not in self.data:
                self.data[s]=None
        self.name = self.data["name"]
        self.description = self.data["description"]

    def config(self,c=None):
        if c:
            if c in self.data:
                return self.data[c]
            else:
                return None
        else:
            return self.data

    def instances(self,**kwargs):
        # get the attribute instances that have this attribute
        # FIXME later use gt
        query = kwargs.get('query', None)
        data = self.api.get_attribute_instances(self.collection_id,self.id,query=query)
        if data:
            return data
        else:
            return []

    def update(self, upd):
        return self.api.update_attribute(self.collection_id,self.id,upd)
