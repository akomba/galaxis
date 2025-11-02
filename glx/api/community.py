import glx.__helpers.api_helper as api_helper
import glx.helper as helper
from glx.logger import Logger

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#class CommunityApi(metaclass=Singleton):
class CommunityApi(object):
    def __init__(self,community_name):
        config = helper.load_community_config(community_name)
        if not config:
            print("could not load config for community >"+str(community_name)+"<. Exiting.")
        self.key = config["API_KEY"]
        self.urlv1 = config["api_root"]
        self.urlv2 = config["api_root"]+"/v2"
        Logger().init(community_name)

    ##################################################################################
    #
    # articles
    #
    ##################################################################################
    def get_articles(self):
        url = self.urlv1+"/news/admin/all"
        res = api_helper.call_api(url,"get",api_key=self.key)
        return res["data"]

    def update_article(self,article_id,param,value):
        url=self.urlv1+"/news/"+str(article_id)
        data = {param:value}
        response = api_helper.call_api(url,"put",api_key=self.key,data=data)
        return response

    def get_article(self,article_id):
        url = self.urlv1+"/news/"+str(article_id)
        res = api_helper.call_api(url,"get")
        return res["data"]

    ##################################################################################
    #
    # comments
    #
    ##################################################################################
    def get_article_comments(self,article_id):
        url = self.urlv1+"/comments/news/"+str(article_id)
        res = api_helper.call_api(url,"get",api_key=self.key,paginate=False)
        return res["data"]
        pass

    ##################################################################################
    #
    # collections
    #
    ##################################################################################
    def get_collections(self):
        # id
        # name
        url=self.urlv2+"/collections"
        return api_helper.call_api(url,"get",api_key=self.key)

        # FIXME temp data massage
        #collections = []
        #for old in res:
        #    c = {}
        #    c["id"]                     = old["collection_id"]
        #    c["name"]                   = old["collection_name"]
        #    collections.append(c)
        #return collections
    
    def get_collection(self,collection_id):
        url=self.urlv2+"/collections/"+str(collection_id)
        return api_helper.call_api(url,"get",api_key=self.key)
        
        # FIXME temp data massage
        #c = {} 
        #c["id"]                     = old["collection_id"]
        #c["global_collection_id"]   = old["backend_collection_id"]
        #c["asset_hash"]             = old["assetHash"]
        #c["is_infinite"]            = old["is_infinite"]
        #c["name"]                   = old["collection_name"]
        #c["badge_registry_address"] = old["badge_registry_address"]
        #c["is_on_chain"]            = old["is_on_chain"]
        #c["contract_address"]       = old["token_address"]

        #return c
    ##################################################################################
    #
    # members
    #
    ##################################################################################
    def get_members(self):
        return self.get_cards(1)

    def get_member(self,member_id):
        return self.get_card(1,member_id)
    ##################################################################################
    #
    # cards
    #
    ##################################################################################
    def get_cards(self,collection_id):
        url=self.urlv2+"/collections/"+str(collection_id)+"/cards"
        res = api_helper.call_api(url,"get",api_key=self.key)
        return res

    def get_card(self,collection_id, card_id):
        url=self.urlv2+"/collections/"+str(collection_id)+"/cards/"+str(card_id)
        res = api_helper.call_api(url,"get",api_key=self.key)
        return res
    
    #def get_cards_with_attribute(self,attribute_id):
    #    url= self.urlv1+"/attributes/"+str(attribute_id)+"/cards"
    #    res = api_helper.call_api(url,"get")
    #    return res["data"]
    ##################################################################################
    #
    # attributes
    #
    ##################################################################################
    def get_attributes(self,collection_id):
        # FIXME temp data massage
        # now we are just eat the collection id
        # because only collection 1 works
        # also data massage
        url = self.urlv2+"/collections/"+str(collection_id)+"/attributes"
        return api_helper.call_api(url,"get",api_key=self.key)

    def get_attribute(self,collection_id,attribute_id):
        url = self.urlv2+"/collections/"+str(collection_id)+"/attributes/"+str(attribute_id)
        return api_helper.call_api(url,"get",api_key=self.key)

    def update_attribute(self,collection_id,attribute_id,payload):
        url = self.urlv2+"/collections/"+str(collection_id)+"/attributes/"+str(attribute_id)
        return api_helper.call_api(url,"patch",api_key=self.key,data=payload)

    ##################################################################################
    #
    # attribute instances
    #
    ##################################################################################
    def get_attribute_instances(self,collection_id,attribute_id,**kwargs):
        url = self.urlv2+"/collections/"+str(collection_id)+"/attributes/"+str(attribute_id)+"/cards"
        return api_helper.call_api(url,"get",api_key=self.key)

    ##################################################################################
    #
    # card attributes
    #
    ##################################################################################
    def ca_massager(self,res,card_id):
        if res["is_interactive"]:
            if res["interaction"]["can_interact"]:
                interacted_at = False
                interacted_value = None
            else:
                interacted_at = True
                interacted_value = res["interaction"]["config"]["button_text"]
        else:
            interacted_at = False
            interacted_value = None

        if not res["value"]:
            v = 0
        else:
            v = float(res["value"])

        ca = {}
        ca["card_id"] = card_id
        ca["attribute_id"] = int(res["id"])
        ca["interacted_at"]   = interacted_at
        ca["interacted_result"] = interacted_value
        ca["value"] = v
        return ca

    def get_card_attribute(self,collection_id,card_id,attribute_id):
        url = self.urlv2+"/collections/"+str(collection_id)+"/cards/"+str(card_id)+"/attributes/"+str(attribute_id)
        return api_helper.call_api(url,"get",api_key=self.key)

    def get_card_attributes(self,collection_id,card_id):
        url = self.urlv2+"/collections/"+str(collection_id)+"/cards/"+str(card_id)+"/attributes"
        return api_helper.call_api(url,"get",api_key=self.key)
    ##################################################################################
    def get_attribute_interaction(self,collection_id,card_id,attribute_id):
        url = self.urlv1+"/collections/"+str(collection_id)+"/cards/"+str(card_id)+"/attributes/"+str(attribute_id)+"/interactions"
        res = api_helper.call_api(url,"get",api_key=self.key)
        return res

    ##################################################################################
    def add_attribute_to_card(self,collection_id, card_id, attribute_id, attribute_value=None):
        url = self.urlv2+"/collections/"+str(collection_id)+"/cards/"+str(card_id)+"/attributes"
        att = {"attribute_id": attribute_id}
        if not attribute_value is None:
            att["attribute_value"] = attribute_value
        #data = {"attributes":[att]}
        response = api_helper.call_api(url,"post",api_key=self.key,data=att)
        return response

    def update_card_attribute(self,collection_id, card_id, attribute_id, payload):
        url = self.urlv2+"/collections/"+str(collection_id)+"/cards/"+str(card_id)+"/attributes/"+str(attribute_id)
        response = api_helper.call_api(url,"patch",api_key=self.key,data=payload)
        return response

    def add_attribute_to_cards(self,collection_id,attribute_id):
        url = self.urlv2+"/collections/"+str(collection_id)+"/attributes/"+str(attribute_id)+"/instances"
        return api_helper.call_api(url,"post",api_key=self.key)
    
    ##################################################################################
    def remove_attribute_from_card(self,collection_id,card_id,attribute_id):
        url = self.urlv2+"/collections/"+str(collection_id)+"/cards/"+str(card_id)+"/attributes/"+str(attribute_id)

        response = api_helper.call_api(url,"delete",api_key=self.key)
        return response

    def remove_attribute_from_cards(self,collection_id,attribute_id):
        url = self.urlv2+"/collections/"+str(collection_id)+"/attributes/"+str(attribute_id)+"/instances"
        return api_helper.call_api(url,"delete",api_key=self.key)
