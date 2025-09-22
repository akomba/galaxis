# CardAttribute object
from glx.api.community import CommunityApi
import glx.helper as helper

class CardAttribute(object):
    def __init__(self, card,attribute_id):
        self.card = card
        self.id = attribute_id
        self.api = self.card.collection.community.api
    
    def value(self):
        res = self.api.get_card_attribute(self.card.collection.id,self.card.id,self.id)
        return res["value"]

    def interacted_at(self):
        res = self.api.get_card_attribute(self.card.collection.id,self.card.id,self.id)
        return res["interacted_at"]

    def set_value(self,value):
        return self.api.add_attribute_to_card(self.card.collection.id,self.card.id,self.id,value)

    def remove(self):
        return self.api.remove_attribute_from_card(self.card.collection.id,self.card.id,self.id)

    @classmethod
    def get_instance(cls,community_name, collection_id, card_id, attribute_id):
        import glx
        c = glx.community.Community(community_name)
        res = c.api.get_card_attribute(collection_id,card_id,attribute_id)
        if res:
            collection = glx.collection.Collection(c,collection_id)
            card = glx.card.Card(collection,card_id)
            ca = glx.card_attribute.CardAttribute(card,attribute_id)
            return ca
        else:
            return None


