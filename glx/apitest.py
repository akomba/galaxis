import glx.helper as helper

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Apitest(metaclass=Singleton):
    def __init__(self,community_name):
        config = helper.load_community_config(community_name)
        self.key = config["API_KEY"]
        self.url = config["api_root"]
        print("yup executed")
    
    def api1():
        return "yo"
