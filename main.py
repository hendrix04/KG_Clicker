import pprint, os, logging
from time import sleep
from pathlib import Path
from kg.vnc import VNC
from kg.kingdom_clicker import KingdomClicker
from apscheduler import Scheduler
from apscheduler.triggers.interval import IntervalTrigger
from pypyr import pipelinerunner
from pypyr.config import config
import pypyr.log.logger

# optional - one-time loading of config from files
config.init()

# initialize logging once
# use the same log format & level defaults as the cli
pypyr.log.logger.set_root_logger()


pp = pprint.PrettyPrinter(indent=4)


# Generate the schedule based off of "whatever"
def main():
    print("hello")
    # Register adv_mith
    context = pipelinerunner.run(
        pipeline_name="tasks/adv_mith",
        dict_in={"arbkey": "pipe", "anotherkey": "song"},
    )


if __name__ == "__main__":
    main()
