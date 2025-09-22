#!/usr/bin/env python

import glx.utils as gu
from glx.community import Community
import argparse
import toml

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
    config = gu.get_config()
    community = config["community"]

    if not community:
        print("no community specified, exiting.")
        exit(1)

    c = Community(community)
    collection = c.collection(config["collection"])

    attributes = collection.attributes()


    if args.id:
        att = collection.attribute(args.id)
        print(att.name)

        # find local config if any
        config = gu.load_attrib_config(att.id)

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
            config[key] = value
            gu.save_attrib_config(att.id,config)

    else:
        gu.list_options(attributes,config["attribute"])

if __name__ == "__main__":
    main()
