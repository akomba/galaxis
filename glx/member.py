# member object
from glx.card import Card

class Member(Card):
    def __init__(self, community_name,member_id):
        collection_id = 1 
        super().__init__(community, collection_id, member_id)
