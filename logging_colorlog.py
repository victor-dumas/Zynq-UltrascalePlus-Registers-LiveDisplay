###############################################################################
# Project      :
# Reference    :
# Design       :
# Title        : loggin_colorlog
###############################################################################
# File         : loggin_colorlog.py
# Author       : NSA
# Company      :
# Created      : 27/03/2021
# Last update  :
# Platform     :
###############################################################################
# Description  :   Module loggin_colorlog.
##
##
## To install: 
##  - pip3 install termcolor 
##  - pip3 install colorlog 
###############################################################################
import      logging
from        colorlog  import ColoredFormatter
from        termcolor import colored

def create_logging_with_color(  name,                                                                                       \
                                log_format = " %(asctime)s | %(log_color)s%(levelname)-8s%(reset)s | [ %(name)-22s ] | %(message)s", \
                                # log_format = " %(asctime)s | %(log_color)s%(levelname)-8s%(reset)s | [ %(name)-15s ] | %(log_color)s%(message)s%(reset)s", \
                                log_level= logging.INFO                                                                 \
                              ):
    logging.root.setLevel(log_level)
    formatter = ColoredFormatter(log_format)

    stream = logging.StreamHandler()
    stream.setLevel(log_level)
    stream.setFormatter(formatter)

    log = logging.getLogger(name)
    log.setLevel(log_level)
    log.propagate = False
    # As several logger with the same name is possible
    # we attach only a single handler to not duplicate messages
    if (log.hasHandlers() == False):
       log.addHandler(stream)
    # log.addHandler(stream)
    return log

def color_green_if_true(message, condition):
    if (condition == True):
        return colored(message,'green')
    else:
        return message

def color_red_if_true(message, condition):
    if (condition == True):
        return colored(message,'red')
    else:
        return message

def color_yellow_if_true(message, condition):
    if (condition == True):
        return colored(message,'yellow') 
    else:
        return message 

def color_green_if_true_and_red_if_false(message, condition):
    if (condition == True):
        return colored(message,'green')
    else:
        return colored(message,'red')

def print_arrow_if_true(result):
    if (result == True):
        return("-> ")
    else:
        return("   ")



###############################################################################
# Test du fichier
###############################################################################
if __name__ == '__main__':
    log = create_logging_with_color('test')
    log.debug("A quirky message only developers care about")
    log.info("Curious users might want to know this")
    log.warning("Something is wrong and any user should be informed")
    log.error("Serious stuff, this is red for a reason")
    log.critical("OH NO everything is on fire")
    log.error("Serious stuff, this is red for a reason")

    print(color_green_if_true(message="ok", condition= True))
