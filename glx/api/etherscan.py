import glx.__helpers.api_helper as api_helper
import time

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class EtherscanApi(metaclass=Singleton):
    def __init__(self,api_key):
        self.key = api_key
        self.url = "https://api.etherscan.io/v2/api"
        self.chains = {
                "ethereum":1,
                "polygon":137
                }
                #"base":8453,
                #"optimism":10
                #"arbitrum":42161,
                #"abstract":2741,
                #"gnosis":100,

    
    def _get_token_balances(self,address,chain_id):
        time.sleep(0.02) # to avoid rate limiting
        params=[
            "chainid="+str(chain_id),
            "module=account",
            "action=addresstokenbalance",
            "address="+address,
            "page=1",
            "offset=5000",
            "apikey="+self.key
            ]
        url = self.url+"?"+"&".join(params)
        res = api_helper.call_api(url,"get",api_key=self.key)
        return res

    def _get_native_balance(self,address,chain_id):
        time.sleep(0.02) # to avoid rate limiting
        params=[
            "chainid="+str(chain_id),
            "module=account",
            "action=balance",
            "address="+address,
            "tag=latest",
            "apikey="+self.key
            ]
        url = self.url+"?"+"&".join(params)
        res = api_helper.call_api(url,"get",api_key=self.key)
        return res


    def get_token_balances(self,address,chain_id=None):
        if not chain_id:
            c = {}
            for k,v in self.chains.items():
                c[k] = {"tokens":self._get_token_balances(address,v),"native":self._get_native_balance(address,v)}
        return c
