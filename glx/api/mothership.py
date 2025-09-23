import glx.__helpers.api_helper as api_helper

class MothershipApi(object):
    def __init__(self):
        self.url = "https://mothership.galaxis.xyz/api"

    def get_assets(self):
        url = self.url+"/assets"
        res = api_helper.call_api(url)
        return res

    def get_asset_owners(self,asset_name):
        url = self.url+"/assets/name/"+asset_name+"/owner-assets"
        res = api_helper.call_api(url)
        return res["data"]

    def get_asset_for_owner(self,asset_name,owner):
        url = self.url+"/assets/name/"+asset_name+"/owner-assets/address/"+owner
        res = api_helper.call_api(url)
        return res["data"]
