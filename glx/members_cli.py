#!/usr/bin/env python

import glx.helper as helper
from glx.community import Community
import argparse

def main():
    parser = argparse.ArgumentParser(
            prog='attribute',
            description='shows / manages members of a galaxis community',
            epilog='Let\'s fix the world together.')

    parser.add_argument('-f', '--filter')
    parser.add_argument('-r', '--refresh', action="store_true")

    args = parser.parse_args()

    # community
    config = helper.load_local_config()
    if not config["community"]:
        print("run `communities set [communityname]` first")
        exit()
    c = Community(config["community"])

    # refresh or read?
    if args.refresh:
        print("refreshing from server")
        members = c.refresh_members()
    else:
        members = c.members()

    # filter
    if args.filter:
        # we need to filter the members
        # filter by owner address
        # filter by attribute
        # filter by citizenship
        # filter by coin (amount?)
        # filter by galaxis assets (engines etc)
        pass

    counter = 0
    for member in members:
        counter +=1
        pc = ("    "+str(counter))[-5:]
        prid = ("   "+str(member["id"]))[-4:]
        print(pc,c.name[:3],prid,member["owner"])
