from __future__ import absolute_import

import os
from readsettings import ReadSettings
import logging


def get_config():
    """
    :return: a dict parsed from a SafeConfigParser object, with config values loaded from file_path
    """
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'dev.yml'
    )
    config = ReadSettings(file_path)
    logging.info("config {}".format(config.data))
    return config.data

Config = get_config()

