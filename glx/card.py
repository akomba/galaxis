# card object
from glx.card_attribute import CardAttribute
from glx.api.community import CommunityApi
import glx.helper as helper
import glx.scheduler as sc
from glx.logger import Logger

class Card(object):
    def __init__(self,community_name,collection_id,card_id,dt=None):
        self.id = card_id
        self.community_name = community_name
        self.collection_id = collection_id
        self.api = CommunityApi(community_name)
        self.dt = dt
        Logger().init(community_name)

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

    def attribute(self,attribute_id, **kwargs):

        ca = self.api.get_card_attribute(self.collection_id,self.id,attribute_id)
        if ca:
            if kwargs.get("raw",None):
                return ca
            else:
                return CardAttribute(self.community_name, self.collection_id, self.id, attribute_id,ca)
        else:
            return None

    def has_attribute(self, attribute_id):
        if not attribute_id:
            return False
        return attribute_id in [x["attribute_id"] for x in self.attributes(raw=True)]

    def add_attribute(self,attribute_id,attribute_value=None):
        self.api.add_attribute_to_card(self.collection_id,self.id,attribute_id)
        ca = self.attribute(attribute_id)
        Logger().logger.info("CARD "+str(self.id)+" "+str(self.collection_id)+" add attribute "+str(attribute_id)+" value "+str(attribute_value))
        if attribute_value:
            ca.set_value(attribute_value)
        return ca

    def increase_attribute_value(self,attribute_id,value,expiration=None):
        # if attribute is already there, we take its value
        if self.has_attribute(attribute_id):
            ca = self.attribute(attribute_id)
            value = ca.value() + value
            ca.set_value(value)
            Logger().logger.info("CARD "+str(self.id)+" "+str(self.collection_id)+" inc attribute "+str(attribute_id)+" value "+str(value))
        else:
            self.add_attribute(attribute_id,value)

        if expiration:
            # create scheduler event to decrease it later
            fn = sc.schedule_expiring_value(self.community_name,self.collection_id,self.id,attribute_id,value,expiration)

    def remove_attribute(self,attribute_id):
        Logger().logger.info("CARD "+str(self.id)+" "+str(self.collection_id)+" rem attribute "+str(attribute_id))
        return self.api.remove_attribute_from_card(self.collection_id,self.id,attribute_id)
