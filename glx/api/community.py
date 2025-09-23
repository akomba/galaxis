import glx.__helpers.api_helper as api_helper
import glx.helper as helper

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class CommunityApi(metaclass=Singleton):
    def __init__(self,community_name):
        config = helper.load_community_config(community_name)
        self.key = config["API_KEY"]
        self.url = config["api_root"]

    ##################################################################################
    #
    # collections
    #
    ##################################################################################
    def get_collections(self):
        # id
        # name
        url=self.url+"/collections"
        res = api_helper.call_api(url)

        # FIXME temp data massage
        collections = []
        for old in res:
            c = {}
            c["id"]                     = old["collection_id"]
            c["name"]                   = old["collection_name"]
            collections.append(c)
        return collections
    
    def get_collection(self,collection_id):
        url=self.url+"/collections/"+str(collection_id)
        old = api_helper.call_api(url)
        
        # FIXME temp data massage
        c = {} 
        c["id"]                     = old["collection_id"]
        c["global_collection_id"]   = old["backend_collection_id"]
        c["asset_hash"]             = old["assetHash"]
        c["is_infinite"]            = old["is_infinite"]
        c["name"]                   = old["collection_name"]
        c["badge_registry_address"] = old["badge_registry_address"]
        c["is_on_chain"]            = old["is_on_chain"]
        c["contract_address"]       = old["token_address"]

        return c
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
        url=self.url+"/collections/"+str(collection_id)+"/cards"
        res = api_helper.call_api(url)
        # FIXME: why is it wrapped in data while in attributes it isn't?
        # FIXME temp data massage
        # card list
        res = res["data"]
        cards = []
        for c in res:
            card = {}
            card["id"] = c["token_id"]
            card["owner"] = c["owner"]
            card["image"] = c["image"]
            cards.append(card)

        return cards

    def get_card(self,collection_id, card_id):
        url=self.url+"/collections/"+str(collection_id)+"/cards/"+str(card_id)
        res = api_helper.call_api(url)
        # FIXME temp data massage
        # get card attribute ids

        card = {}
        card["id"] = res["token_id"]
        card["owner"] = res["owner"]
        card["image"] = res["image"]
        card["citizenship_status"] = "FIXME" # FIXME
        card["subscription_data"] = res["subscription_data"]
        card["is_banned_from_commenting"] = res["is_banned_from_commenting"]
        card["referrer"] = res["referrer"]
        card["attribute_ids"] = [a["attribute_id"] for a in self.get_card_attributes(collection_id,card_id)]

        return card
    
    #def get_cards_with_attribute(self,attribute_id):
    #    url= self.url+"/attributes/"+str(attribute_id)+"/cards"
    #    res = api_helper.call_api(url)
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
        url = self.url+"/attributes"
        res = api_helper.call_api(url)

        # list of attributes
        # id
        # name

        attributes = []
        for att in res:
            a = {}
            a["id"] = att["id"]
            a["name"] = att["name"]
            attributes.append(a)

        return attributes

    def get_attribute(self,collection_id,attribute_id):
        url = self.url+"/attributes/"+str(attribute_id)
        res = api_helper.call_api(url)

        # FIXME temp data massage
        att = {
            "id"                 : res["id"],
            "collection_id"      : res["collection_id"],
            "name"               : res["name"],
            "description"        : res["description"],
            "enabled"            : res["enabled"],
            "decorator_type"     : res["decorator_type"],
            "is_blockchain"      : res["is_blockchain"],
            "is_interactive"     : res["interactive"],
            "interactive_config" : res["interactive_config"],
            "decorator_file_name": res["icon"],
            "decorator_url"      : res["icon_url"],
            "icon_file_name"     : "",
            "icon_url"           :""}

        return att

    ##################################################################################
    #
    # attribute instances
    #
    ##################################################################################
    def get_attribute_instances(self,collection_id,attribute_id,**kwargs):
        # FIXME collection id is missing from the current api
        # FIXME temp data massage
        # /api/attributes/{id}/cards
        query = kwargs.get('query', None)
        url = self.url+"/attributes/"+str(attribute_id)+"/cards"
        res = api_helper.call_api(url)["data"]
      
        if not query:
            query={}
        
        card_attributes = []
        for r in res:
            card_id = int(r["token_id"])
            instance = self.get_card_attribute(collection_id,card_id,attribute_id)
            if instance:
                # implementing api filter
                proceed = True
                for k in query.keys():
                    if not k in instance or query[k] != instance[k]:
                        proceed = False
                if proceed:
                    card_attributes.append(instance)
        return card_attributes

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
        url = self.url+"/collections/"+str(collection_id)+"/cards/"+str(card_id)+"/attributes/"+str(attribute_id)
        res = api_helper.call_api(url)
        # FIXME temp data massage
        if not res:
            return None
        return self.ca_massager(res,card_id)

    def get_card_attributes(self,collection_id,card_id):
        url = self.url+"/collections/"+str(collection_id)+"/cards/"+str(card_id)+"/attributes"
        res = api_helper.call_api(url)
        # FIXME temp data massage
        card_attributes = []
        for ca in res:
            card_attributes.append(self.ca_massager(ca,card_id))
        return card_attributes
    ##################################################################################
    def get_attribute_interaction(self,collection_id,card_id,attribute_id):
        url = self.url+"/collections/"+str(collection_id)+"/cards/"+str(card_id)+"/attributes/"+str(attribute_id)+"/interactions"
        res = api_helper.call_api(url,self.key)
        return res

    ##################################################################################
    def add_attribute_to_card(self,collection_id, card_id, attribute_id, attribute_value=None):
        url = self.url+"/collections/"+str(collection_id)+"/cards/"+str(card_id)+"/attributes"
        att = {"attribute_id": attribute_id}
        if not attribute_value is None:
            att["attribute_value"] = attribute_value
        data = {"attributes":[att]}
        response = api_helper.put(url,self.key,data)
        return response

    def add_attribute_to_cards(self,collection_id,attribute_id,payload):
        url = self.url+"/collections/"+str(collection_id)+"/attributes/"+str(attribute_id)+"/assign"
        
        data = {"assignments":payload}
        response = api_helper.put(url,self.key,data)
        return response
    
    ##################################################################################
    def remove_attribute_from_card(self,collection_id,card_id,attribute_id):
        url = self.url+"/collections/"+str(collection_id)+"/attributes/"+str(attribute_id)+"/remove"
        data = {"token_ids":[card_id]}

        response = api_helper.delete(url,self.key,data)
        return response

    def remove_attribute_from_cards(self,collection_id,attribute_id,payload):
        #/api/collections/{collectionId}/attributes/{attributeId}/assign
        url = self.url+"/collections/"+str(collection_id)+"/attributes/"+str(attribute_id)+"/remove"
        
        data = {"token_ids":payload}
        response = api_helper.delete(url,self.key,data)
        return response
