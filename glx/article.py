import json
import os
from glx.card import Card
from glx.attribute import Attribute
from glx.api.community import CommunityApi
import glx.helper as helper

class Article(object):
    def __init__(self, community_name,article_id):
        self.id = article_id
        self.community_name = community_name
        self.api = CommunityApi(community_name)
        self.dt = None
    ###############################################################
    # data
    ###############################################################
    def data(self,d=None):
        if not self.dt:
            self.dt = self.api.get_article(self.id)
        if d:
            return self.dt[d]
        else:
            return self.dt
        
    ###############################################################
    # attributes
    ###############################################################

    def update(self,param,value):
        # params:
        #
        # title              string
        # body               string (html)
        # cover_image_upload string($binary)
        # cover_image        string($uri)
        # pin_to_highlights  boolean
        # publication_date   string($date-time)
        # meta_keywords      string (JSON array of keywords as string)
        # meta_description   string
        # members_only       boolean <-- these two can't be true at the same time
        # publish_to_galaxis boolean <-- these two can't be true at the same time
        # address            string Community owner/admin wallet address (required for signature auth)
        # signed_message     string Signed message for authentication (required for signature auth)
        # custodial_address  string
        
        params = "title body cover_image_upload cover_image pin_to_highlights publication_date meta_keywords meta_description members_only publish_to_galaxis address signed_message custodial_address".split(" ")
        if not param in params:
            return False

        if param == "meta_keywords":
            value = json.dumps(value.split(" "))

        return self.api.update_article(self.id,param,value)
