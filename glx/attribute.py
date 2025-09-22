# Attribute object
# this is Attribute, NOT CardAttribute!
import os

class Attribute(object):
    def __init__(self, collection,attribute_id):
        self.collection = collection
        self.id = attribute_id
        self.api = self.collection.api
        self.data = self.data()
        self.name = self.data["name"]
        self.description = self.data["description"]

    def data(self):
        data = self.api.get_attribute(self.collection.id,self.id)
        return data

    def instances(self,**kwargs):
        # get the attribute instances that have this attribute
        # FIXME later use gt
        query = kwargs.get('query', None)
        data = self.api.get_attribute_instances(self.collection.id,self.id,query=query)
        if data:
            return data
        else:
            return []
