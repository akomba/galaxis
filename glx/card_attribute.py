# CardAttribute object
from glx.api.community import CommunityApi
from glx.attribute import Attribute

class CardAttribute(object):
    def __init__(self, community_name, collection_id, card_id, attribute_id):
        self.card_id = card_id
        self.community_name = community_name
        self.collection_id = collection_id
        self.id = attribute_id
        self.api = CommunityApi(community_name)
        self.attribute = Attribute(community_name, collection_id, attribute_id)
    
    def value(self):
        res = self.api.get_card_attribute(self.collection_id,self.card_id,self.id)
        return res["value"]

    def interacted_at(self):
        res = self.api.get_card_attribute(self.collection_id,self.card_id,self.id)
        return res["interacted_at"]

    def set_value(self,value):
        if self.attribute.config("max"):
            value = self.attribute.config("max") if self.attribute.config("max") < value else value
        return self.api.add_attribute_to_card(self.collection_id,self.card_id,self.id,value)

    def remove(self):
        return self.api.remove_attribute_from_card(self.collection_id,self.card_id,self.id)

    #def get_instance(cls,community_name, collection_id, card_id, attribute_id):
    #    api = CommunityApi(community_name)
    #    res = api.get_card_attribute(collection_id,card_id,attribute_id)
    #    if res:
    #        collection = Collection(c,collection_id)
    #        card = Card(collection,card_id)
    #        return cls(CardAttribute(collection_id, card_id, attribute_id))
    #    else:
    #        return None


