"""
Add yaml support to `logging.config` since the documentation has a lot
of examples in yaml, but doesn't actually support it.
"""

import logging.config
import yaml


def yamlFileConfig(fname: str):
    with open(fname, "r") as fh:
        yamlConfig(fh.read())


def yamlConfig(stream: str):
    config = yaml.safe_load(stream)
    logging.config.dictConfig(config)
