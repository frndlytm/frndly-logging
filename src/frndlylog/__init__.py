"""
Top-level package for Friendly Python Logging
"""
import os


__author__ = "Christian J. DiMare-Baits"
__email__ = "frndlytm@gmail.com"
__version__ = "0.1.0"


here = os.path.dirname(os.path.abspath(__file__))


def basicConfig() -> None:
    from frndlylog.config import yamlFileConfig
    fname = os.path.join(here, "basicConfig.yaml")
    yamlFileConfig(fname)
