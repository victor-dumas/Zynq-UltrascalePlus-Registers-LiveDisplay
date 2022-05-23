###############################################################################
# Project      :
# Reference    :
# Design       :
# Title        : component
###############################################################################
# File         : component.py
# Author       : NSA
# Company      :
# Created      : 27/03/2021
# Last update  :
# Platform     :
###############################################################################
# Description  :   Module Component that provides a log
##
##
##
###############################################################################
from logging_colorlog import create_logging_with_color
from logging_colorlog import color_green_if_true_and_red_if_false

import logging

class Component():

    def __init__(self, log_name, log_level= logging.DEBUG  ):
        self.log= create_logging_with_color(log_name, log_level= log_level  )
        self.log.info("Creating ")
        self.log_name= log_name

    def menu(self):
        print ("*" * 80)
        print ("{:^80}".format(self.log_name))
        print ("-" * 80)
        print(self) # Call method __str__(self):


###############################################################################
# Class test
###############################################################################
if __name__ == '__main__':
    compo = Component(log_name = "Test_name")
    compo.menu()
