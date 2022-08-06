# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved
# Author: Subin. Gopi (subing85@gmail.com)
# Studio-Pipe Project Management in-house Tool
# Last modified: 2021:December:30:Thursday-10:42:04:PM.
# WARNING! All changes made in this file will be lost!
# Description: studio-pipe event commands

import optparse

from apis.studio import Event
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def execute():
    """
    :description
        studio-pipe event commands.
        to query and execute the studio-pipe events

    :examples
        \u2022 pipe event setWorkspace
            to execute the event based on the event name.
                :param <str>

        \u2022 pipe event-all
            get all available stuido-pipe events.
                :param None

        \u2022 pipe event-name
            get all specific event based on name.
                :param <str>
    """

    parser = optparse.OptionParser(
        usage="usage: %prog [options] studio-pipe event commands.",
        version="0.0.1",
    )

    option_list = [
        optparse.make_option(
            "--event",
            dest="event",
            action="store",
            type="string",
            help="to execute event commands",
        ),
        optparse.make_option(
            "--event-all",
            dest="eventall",
            action="store_true",
            default=False,
            help="to execute event commands",
        ),
        optparse.make_option(
            "--event-name",
            dest="eventname",
            action="store",
            type="string",
            help="to execute event commands",
        ),
    ]

    parser.add_options(option_list)
    (options, args) = parser.parse_args()

    if options.event:
        event = Event(name=options.event)
        event.execute()
        return

    if options.eventall:
        event = Event(name=None)
        event.get()
        return

    if options.eventname:
        event = Event(name=options.eventname)
        event.get()
        return


if __name__ == "__main__":
    execute()
