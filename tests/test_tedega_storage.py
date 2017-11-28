#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tedega_storage
----------------------------------

Tests for `tedega_storage` module.
"""
import sqlalchemy as sa
import pytest
import datetime
from tedega_storage.storage import (
    ENGINE,
    RDBMSStorageBase,
    get_storage,
    scoped_session,
    init_storage
)


class Testmodel(RDBMSStorageBase):
    __tablename__ = "teststorage"
    id = sa.Column("id", sa.Integer, primary_key=True)
    dummy_date = sa.Column("dummy_date", sa.Date)
    dummy_string = sa.Column("dummy_string", sa.String)


def test_engine():
    assert ENGINE is not None


def test_storage():
    with get_storage() as storage:
        assert storage is not None
        assert storage.engine is not None


def test_scoped_session():
    with pytest.raises(Exception):
        with scoped_session() as session:
            session.execute("Foo")

    with scoped_session() as session:
        session.execute("SELECT * from teststorage")


def test_storage_crud():
    new_id = None
    with get_storage() as storage:
        new = Testmodel()
        new.dummy_string = "Foo"
        new.dummy_date = datetime.date.today()
        new_id = storage.create(new)
        assert new.dummy_string == "Foo"
        assert new.id is not None
        assert new_id == new.id
    assert new_id is not None

    with pytest.raises(Exception):
        with get_storage() as storage:
            new = Testmodel()
            new.dummy_string = "Foo"
            new.dummy_date = "XXX"
            new_id = storage.create(new)

    with get_storage() as storage:
        loaded = storage.read(Testmodel, new_id)
        assert loaded.dummy_string == "Foo"
        loaded.dummy_string = "Foo2"
        storage.update(loaded)

    with get_storage() as storage:
        loaded = storage.read(Testmodel, new_id)
        assert loaded.dummy_string == "Foo2"

    with get_storage() as storage:
        loaded = storage.read(Testmodel, new_id)
        storage.delete(loaded)

    with pytest.raises(Exception):
        with get_storage() as storage:
            loaded = storage.read(Testmodel, new_id)

    # DetachedInstanceError
    with pytest.raises(Exception):
        assert new_id == new.id

def test_storage_without_scope():
    storage = get_storage()


init_storage()
