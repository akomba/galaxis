# collection
import os
from glx.card import Card
from glx.attribute import Attribute
from glx.api.community import CommunityApi
import json
import glx.helper as helper

class Collection(object):
    def __init__(self, community_name, collection_id):
        self.id = collection_id
        self.community_name = community_name
        self.api = CommunityApi(community_name)

    ###############################################################
    # data
    ###############################################################
    def data(self):
        return self.api.get_collection(self.id)
        
    ###############################################################
    # attributes
    ###############################################################
    def attributes(self,**kwargs):
        attributes = self.api.get_attributes(self.id)
        if kwargs.get("raw",None):
            return attributes
        else:
            return [Attribute(self.community_name,self.id,att["id"]) for att in attributes]

    def attribute(self,attribute_id,**kwargs):
        if kwargs.get("raw",None):
            return self.api.get_attribute(self.id,attribute_id)
        else:
            return Attribute(self.community_name,self.id,attribute_id)

    def add_attribute(self,attribute_id):
        # add attribute to all cards in this collection
        for card in self.cards():
            card.add_attribute(attribute_id)


    def remove_attribute(self,attribute_id):
        # remove attribute from all cards
        for card in self.cards():
            card.remove_attribute(attribute_id)

    ###############################################################
    # cards
    ###############################################################
    #def card_ids_with_attribute(self,attribute_id):
    #    card_ids = [m["token_id"] for m in self.api.get_cards_with_attribute(attribute_id)]
    #    return card_ids

    def card(self,card_id,**kwargs):
        if kwargs.get("raw",None):
            return self.api.get_card(self.id,card_id)
        else:
            return Card(self.community_name,self.id,card_id) 

    def cards(self,**kwargs):
        cards = self.api.get_cards(self.id) 
        if kwargs.get("raw",None):
            return cards
        else:
            return [Card(self.community_name,self.id,c["id"]) for c in cards]
