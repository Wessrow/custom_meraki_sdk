#!/usr/bin/python3

"""
Code written by Gustav Larsson
Logging setup and handler
"""

import sys
import logging

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                    )

logger = logging.getLogger("MerakiSDK")
