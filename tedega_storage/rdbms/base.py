#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from tedega_storage.rdbms.storage import ENGINE, STORAGE
from tedega_storage.rdbms.datatypes import UUID


def get_storage():
    return STORAGE(ENGINE)


def init_storage():
    RDBMSStorageBase.metadata.create_all(ENGINE)


RDBMSStorageBase = declarative_base()


class BaseFactory(object):

    """Factory for base objects"""

    def __init__(self, clazz, storage):
        self.clazz = clazz
        self.storage = storage

    def create(self):
        """Will create a new :class:`Base` object.
        :returns: :class:`Base` object.

        """
        return self.clazz()

    def load(self, item_id):
        """Will create a new :class:`Base` object.
        :returns: :class:`Base` object.

        """
        return self.storage.read(self.clazz, item_id)


class BaseItem(object):
    """Base for all models in Tedega"""
    __table_args__ = {'extend_existing': True}

    id = sa.Column("id", sa.Integer, primary_key=True)
    """Local unique identifier within the database. Used to load datasets
    from the database."""

    uuid = sa.Column("uuid", UUID, unique=True)
    """Globally unique indentifier."""

    def __init__(self):
        super(BaseItem, self).__init__()
        self.id = None
        self.uuid = uuid.uuid4()

    def __json__(self):
        """Method which returns the values of the item in a form which
        can basically be serialised into JSON (e.g using
        voorhees.to_json). In the default implementation this is a
        dictionary with all values of the item."""
        return self.get_values()

    @classmethod
    def get_factory(cls, storage):
        """Return an instance of a factory for this class."""
        return BaseFactory(cls, storage)

    @property
    def fields(self):
        mapper = sa.inspect(self)
        return [column.key for column in mapper.attrs]

    def get_values(self, fields=None):
        """Returns the values of the item as a dictionary.
        :fields: List of fieldnames which should be included.
        :returns: Dictionary of values of the item.
        """
        values = {}
        for field in self.fields:
            if fields is None or field in fields:
                values[field] = getattr(self, field)
        return values

    def set_values(self, values):
        """Will set values of the item based on the given dictionary. If
        the dictionary contains values which are not part of the item
        (within self.fields) the value will be silently ignored.

        :values: Dictionary of values.
        """
        for field in self.fields:
            value = values.get(field)
            if value is not None:
                setattr(self, field, value)
