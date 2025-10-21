# runs the scheduler loop
# adds items to be scheduled
# items: 
#   expiring values
#   expiring badges
# load scheduler dir (communities/scheduler)
# loop through items
# execute the ones that expired
# sleep a little

import os
import glx.helper as helper
import glx.scheduler as scheduler
import argparse

APPNAME = "glx"

def main():
    parser = argparse.ArgumentParser(
            prog='attribute',
            description='shows / manages members of a galaxis community',
            epilog='Let\'s fix the world together.')

    parser.add_argument('-l', '--list', action="store_true")
    parser.add_argument('-p', '--process', action="store_true")
    parser.add_argument('-d', '--due', action="store_true")

    args = parser.parse_args()
    
    config = helper.load_or_create_app_config(APPNAME,helper.GLX_DEFAULT_CONFIG)
    community_name = config["community_name"]

    if args.list:
        events = scheduler.list_due(community_name)
        for event in events:
            print(event)
        exit()

    if args.due:
        print("Due:")
        scheduler.show_due(community_name)
        exit()

    print("Active:",len(scheduler.list_active(community_name)))
    scheduler.main(community_name)

if __name__ == "__main__":
    main()
