#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.event import listen
from sqlalchemy import create_engine


@contextmanager
def scoped_session():
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def sqlite_do_connect(dbapi_connection, connection_record):
    # disable pysqlite's emitting of the BEGIN statement entirely.
    # also stops it from emitting COMMIT before any DDL.
    dbapi_connection.isolation_level = None


def sqlite_do_begin(conn):
    # emit our own BEGIN
    conn.execute("BEGIN")
    return ENGINE


class Storage(object):
    """Docstring for Storage. """

    def __init__(self, engine=None):
        """TODO: to be defined1.

        :engine: TODO

        """
        self.engine = engine
        #RDBMSStorageBase.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_value, tb):
        if e_type is not None:
            self.session.rollback()
            raise
        else:
            self.session.commit()
        self.session.close()
        return True

    def create(self, item):
        item_id = None
        self.session.begin_nested()
        try:
            self.session.add(item)
            self.session.commit()
            item_id = item.id
        except:
            self.session.rollback()
            raise
        return item_id

    def read(self, clazz, id=None):
        return self.session.query(clazz).filter(clazz.id == id).one()

    def update(self, item):
        return self.session.flush()

    def delete(self, item):
        self.session.delete(item)


DEFAUL_DB_URI = "sqlite:///:memory:"
DB_URI = os.environ.get("TEDEGA_STORAGE_URI", DEFAUL_DB_URI)
ENGINE = create_engine(DB_URI, echo=False)
if str(ENGINE.url).find("sqlite") > -1:
    #  SQLite doesn not support nested transactions directly.
    #  But there is a workaround. See
    #  http://docs.sqlalchemy.org/en/rel_1_0/dialects/sqlite.html#pysqlite-serializable
    #  for more details.
    listen(ENGINE, "connect", sqlite_do_connect)
    listen(ENGINE, "begin", sqlite_do_begin)
STORAGE = Storage
