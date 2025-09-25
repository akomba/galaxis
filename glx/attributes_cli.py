#!/usr/bin/env python

import glx.helper as helper
from glx.collection import Collection
import argparse
import toml

APPNAME = "glx"

def main():
    parser = argparse.ArgumentParser(
            prog='attribute',
            description='shows / manages attributes of a galaxis community',
            epilog='Let\'s fix the world together.')

    parser.add_argument('-i', '--id')
    parser.add_argument('-l', '--list', action="store_true")
    parser.add_argument('-s', '--set')
    args = parser.parse_args()

    # community
    config = helper.load_or_create_app_config(APPNAME,helper.GLX_DEFAULT_CONFIG)

    if not config["community_name"]:
        print("no community specified, exiting.")
        exit(1)

    collection = Collection(config["community_name"],config["collection_id"])
    attributes = collection.attributes(raw=True)


    if args.id:
        att = collection.attribute(args.id)
        print(att.name)

        # find local config if any
        config = helper.load_attrib_config(collection.id,att.id)

        if config:
            print("======")
            for k,v in config.items():
                print(k,v)

        if args.list:
            print("======")
            print("cards:")
            for card in att.instances():
                print(card)

        if args.set:
            key,value = args.set.split("=")
            config[key] = float(value)
            helper.save_attrib_config(config["community_name"],collection.id,att.id,config)

    else:
        helper.list_options(attributes)

if __name__ == "__main__":
    main()
