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

APPNAME = "glx"

def main():
    config = helper.load_or_create_app_config(APPNAME,helper.GLX_DEFAULT_CONFIG)
    community = Community(config["community_name"])
    for collection in community.collections():
        leakers = {}
        for att in collection.attributes():
            if "leak" in att.config():
                print("LK:",att.name,att.config("leak"))
                leakers[att.id] = att
        # get all members
        cards = collection.cards()
        for card in cards:
            print("LK: card:", card.id)
            catts = card.attributes(raw=True)
            for catt in catts:
                if catt["attribute_id"] in leakers.keys():
                    attribute = leakers[catt["attribute_id"]]
                    value = card.attribute(attribute.id).value()
                    reduce_by = attribute.config("leak")/24 
                    new_value = value - reduce_by
                    if new_value <= 0:
                        print("LK:",card.id,"DEL",attribute.name)
                        card.remove_attribute(attribute.id)
                    else:
                        card.add_attribute(attribute.id,new_value)
                        print("LK:",card.id,"VAL",attribute.name,":",card.attribute(attribute.id).value())

if __name__ == "__main__":
    main()
