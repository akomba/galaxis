# Attribute object
from glx.api.community import CommunityApi
import glx.helper as helper

class Attribute(object):
    def __init__(self, community_name, collection_id, attribute_id):
        self.collection_id = collection_id
        self.id = attribute_id
        self.api = CommunityApi(community_name)
        self.data = self.api.get_attribute(self.collection_id,self.id)
        self.name = self.data["name"]
        self.description = self.data["description"]
        # load config if any
        self.cnf = helper.load_attrib_config(collection_id,attribute_id)        

    def config(self,c=None):
        if c:
            if c in self.cnf:
                return self.cnf[c]
            else:
                return None
        else:
            return self.cnf

    def instances(self,**kwargs):
        # get the attribute instances that have this attribute
        # FIXME later use gt
        query = kwargs.get('query', None)
        data = self.api.get_attribute_instances(self.collection_id,self.id,query=query)
        if data:
            return data
        else:
            return []
