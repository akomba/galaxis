#!/usr/bin/env python
# manages all the leaking attributes
# runs every 10 minutes
# since leak is set by day,
# we need to divide the amount by (24*6) = 144

# find all leaking attributes
# loop through all members
# loop through all leaking attributes
# reduce them according to the leak
import glx.helper as helper
from glx.community import Community
def main():
    config = helper.load_local_config()
    community_name = config["community"]
    if not community_name:
        print("please set a community first")
        exit()

    community = Community(community_name)
    for collection in community.collections():
        print("collection:",collection)
        #collection = community.collection(config["collection"]) 
        # find all leaking attributes
        leakers = {}
        for att in collection.attributes():
            if "leak" in att.config():
                print("leaker:",att.name,att.config("leak"))
                leakers[att.id] = att

        # get all members
        cards = collection.cards()
        for card in cards:
            #print(card)
            #catts = [c["attribute_id"] for c in card.attributes(raw=True)]
            catts = card.attributes(raw=True)
            #print(catts)
            for catt in catts:
                if catt["attribute_id"] in leakers.keys():
                    attribute = leakers[catt["attribute_id"]]
                    value = card.attribute(attribute.id).value()
                    reduce_by = attribute.config("leak")/24 
                    new_value = value - reduce_by
                    if new_value <= 0:
                        print(card.id,"remove attribute",attribute.name)
                        card.remove_attribute(attribute.id)
                    else:
                        print(card.id,"new value for",attribute.name,":",new_value)
                        card.add_attribute(attribute.id,new_value)

if __name__ == "__main__":
    main()
