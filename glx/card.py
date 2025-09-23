# card object
from glx.card_attribute import CardAttribute
from glx.api.community import CommunityApi
import glx.helper as helper
import glx.scheduler as sc

class Card(object):
    def __init__(self,community_name,collection_id,card_id):
        self.id = card_id
        self.collection_id = collection_id
        self.api = CommunityApi(community_name)

    def data(self):
        data = self.api.get_card(self.collection_id,self.id)
        return data

    def attributes_raw(self):
        return self.api.get_card_attributes(self.collection_id,self.id)
    
    def attributes(self):
        cas = self.api.get_card_attributes(self.collection_id,self.id)
        return [CardAttribute(self,c["attribute_id"]) for c in cas]

    def attribute(self,attribute_id):
        return CardAttribute(self,attribute_id)

    def has_attribute(self, attribute_id):
        if not attribute_id:
            return False
        return attribute_id in [x["attribute_id"] for x in self.attributes_raw()]

    def add_attribute(self,attribute_id,attribute_value=None):
        return self.api.add_attribute_to_card(self.collection_id,self.id,attribute_id,attribute_value)

    def increase_attribute_value(self,attribute_id,value,expiration=None):
        # if attribute is not there, create it with value 0
        if not self.has_attribute(attribute_id):
            self.add_attribute(attribute_id,value)
        else:
            # increase attribute's value with value
            current_value = self.attribute(attribute_id).value()
            self.add_attribute(attribute_id,(current_value+value))

        if expiration:
            # create scheduler event to decrease it later
            fn = sc.schedule_expiring_value(community_name,self.collection_id,self.id,attribute_id,value,expiration)

    def remove_attribute(self,attribute_id):
        return self.api.remove_attribute_from_card(self.collection_id,self.id,attribute_id)
