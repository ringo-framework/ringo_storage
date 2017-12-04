# -*- coding: utf-8 -*-
from .rdbms.storage import DB_URI
from .rdbms.base import init_storage, get_storage, RDBMSStorageBase

__all__ = [init_storage, get_storage, RDBMSStorageBase, DB_URI]

__author__ = """Torsten Irländer"""
__email__ = 'torsten.irlaender@googlemail.com'
__version__ = '0.1.0'
