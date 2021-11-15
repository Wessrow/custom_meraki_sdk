#!/usr/bin/python3

"""
Code written by Gustav Larsson
Logging setup and handler
"""

import os
import sys
import logging

class LogHandler:
    """
    Class to handle logging
    """

    def __init__(self, instance):
        """ Sets upp logger """

        try:
            LOGLEVEL = os.environ["LOGLEVEL"]
            
        except KeyError:
            LOGLEVEL = "INFO"

        logging.basicConfig(stream=sys.stdout,
                        level=LOGLEVEL,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                        )

        self.logger = logging.getLogger(instance)

    def format_logs(self, level, message_type, message):
        """ Helper function to format error messages """

        info = {"type": message_type,
                    "message": message
        }

        self.logger.log(level, info)
