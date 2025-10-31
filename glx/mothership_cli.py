from glx.mothership import Mothership
import argparse
import glx.helper as helper

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("assets", help="list of assets", nargs="?")
    parser.add_argument("-a","--asset", help="select a specific asset")
    parser.add_argument("-o","--owner", help="filter for a specific owner address")
    parser.add_argument("-i","--id", type=int, help="select a specific instance of an asset")
    parser.add_argument("-r","--refresh", help="refresh asset metadata", action="store_true")
    args = parser.parse_args()

    mothership = Mothership()

    if args.assets:
        for k,v in mothership.assets_dict.items():
            print(k,v)
        exit(0)

    if args.refresh:
        refresh=True
    else:
        refresh=False

    if args.id and args.owner:
        print("Either specify and id or an owner, not both.")
        exit(0)

    if args.asset:
        asset_name = args.asset
        print(">>>",asset_name)

        if args.id:
            project_dict = mothership.project_dict(asset_name,refresh)
            helper.pretty(project_dict[args.id])
        elif args.owner:
            owned = mothership.cards_by_owner(args.owner,asset_name)
            display_owned(owned)
        else:
            project_dict = mothership.project_dict(asset_name,refresh)
            print("Number of instances:",len(project_dict.keys()))

    elif args.owner:
        owned = mothership.cards_by_owner(args.owner)
        display_owned(owned)

def display_owned(owned):
    for o in owned:
        asset_name, asset_id, metadata = o
        print(asset_name, asset_id)
