# CardAttribute object
from glx.api.community import CommunityApi
from glx.attribute import Attribute
from glx.logger import Logger

class CardAttribute(object):
    def __init__(self, community_name, collection_id, card_id, attribute_id,data=None):
        self.card_id = card_id
        self.community_name = community_name
        self.collection_id = collection_id
        self.id = attribute_id
        self.api = CommunityApi(community_name)
        self.attribute = Attribute(community_name, collection_id, attribute_id)
        self.data = data
        Logger().init(community_name)
    
    def value(self):
        if not self.data:
            self.data = self.api.get_card_attribute(self.collection_id,self.card_id,self.id)
        return self.data["value"]

    def interacted_at(self):
        if not self.data:
            self.data = self.api.get_card_attribute(self.collection_id,self.card_id,self.id)
        return self.data["interacted_at"]

    def set_value(self,value):
        if self.attribute.config("max"):
            value = self.attribute.config("max") if self.attribute.config("max") < value else value
        Logger().logger.info("CARD "+str(self.card_id)+" "+str(self.collection_id)+" set attr value "+str(self.id)+" value "+str(value))
        payload = {"value":value}
        return self.api.update_card_attribute(self.collection_id,self.card_id,self.id,payload)

    def remove(self):
        Logger().logger.info("CARD "+str(self.card_id)+" "+str(self.collection_id)+" rem attr "+str(self.id))
        return self.api.remove_attribute_from_card(self.collection_id,self.card_id,self.id)
