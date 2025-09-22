#!/usr/bin/env python

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
import glx.utils as gu

def main():
    conf = helper.config()
    
    parser = argparse.ArgumentParser(
            prog='attribute',
            description='shows / manages members of a galaxis community',
            epilog='Let\'s fix the world together.')

    parser.add_argument('-l', '--list', action="store_true")
    parser.add_argument('-p', '--process', action="store_true")
    parser.add_argument('-d', '--due', action="store_true")

    args = parser.parse_args()
    
    config = gu.get_config()
    community = config["community"]

    if args.list:
        events = scheduler.list_due(community)
        for event in events:
            print(event)

    if args.process:
        print("Active:",len(scheduler.list_active(community)))
        scheduler.process(community)

    if args.due:
        print("Due:")
        scheduler.show_due(community)


if __name__ == "__main__":
    main()
