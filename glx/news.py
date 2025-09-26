import os
from glx.api.community import CommunityApi
from glx.member import Member
from glx.collection import Collection
from glx.article import Article
import json
import glx.helper as helper

class News(object):
    def __init__(self, community_name):
        self.name = community_name
        self.config = helper.load_community_config(community_name)
        self.api = CommunityApi(community_name)


