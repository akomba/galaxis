# card object
from glx.card_attribute import CardAttribute
from glx.api.community import CommunityApi
import glx.helper as helper
import glx.scheduler as sc

class Card(object):
    def __init__(self,community_name,collection_id,card_id):
        self.id = card_id
        self.community_name = community_name
        self.collection_id = collection_id
        self.api = CommunityApi(community_name)
        self.dt = None

    def data(self,d=None):
        if not self.dt:
            self.dt = self.api.get_card(self.collection_id,self.id)
        if d:
            return self.dt[d]
        else:
            return self.dt

    #def attributes_raw(self):
    #    return self.api.get_card_attributes(self.collection_id,self.id)
    
    def attributes(self,**kwargs):
        cas = self.api.get_card_attributes(self.collection_id,self.id)
        if kwargs.get("raw",None):
            return cas
        else:
            return [CardAttribute(self.community_name,self.collection_id,self.id,c["attribute_id"]) for c in cas]

    def attribute(self,attribute_id):
        return CardAttribute(self.community_name, self.collection_id, self.id, attribute_id)

    def has_attribute(self, attribute_id):
        if not attribute_id:
            return False
        return attribute_id in [x["attribute_id"] for x in self.attributes(raw=True)]

    def add_attribute(self,attribute_id,attribute_value=None):
        return self.api.add_attribute_to_card(self.collection_id,self.id,attribute_id,attribute_value)

    def increase_attribute_value(self,attribute_id,value,expiration=None):
        # if attribute is already there, we take its value
        if self.has_attribute(attribute_id):
            value = self.attribute(attribute_id).value() + value
        
        self.add_attribute(attribute_id,value)

        if expiration:
            # create scheduler event to decrease it later
            fn = sc.schedule_expiring_value(self.community_name,self.collection_id,self.id,attribute_id,value,expiration)

    def remove_attribute(self,attribute_id):
        return self.api.remove_attribute_from_card(self.collection_id,self.id,attribute_id)
