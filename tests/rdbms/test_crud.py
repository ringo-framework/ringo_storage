#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_crud
----------------------------------

Tests for `tedega_storage.rdbms.crud` module.
"""
import pytest
from tedega_storage.rdbms import (
    RDBMSStorageBase as Base,
    BaseItem
)
from tedega_storage.rdbms.mixins import Protocol


class Dummy(Protocol, BaseItem, Base):
    """Dummy class"""
    __tablename__ = "dummys"


def test_searech_fail_because_not_base(storage):
    from tedega_storage.rdbms.crud import search
    with pytest.raises(TypeError):
        search(storage, object)


def test_create_fail_because_not_base(storage):
    from tedega_storage.rdbms.crud import create
    with pytest.raises(TypeError):
        create(storage, object, {})


def test_read_fail_because_not_base(storage):
    from tedega_storage.rdbms.crud import read
    with pytest.raises(TypeError):
        read(storage, object, 12)


def test_read_fail_because_not_integer(storage):
    from tedega_storage.rdbms.crud import read
    with pytest.raises(TypeError):
        read(storage, Dummy, "12")


def test_update_fail_because_not_base(storage):
    from tedega_storage.rdbms.crud import update
    with pytest.raises(TypeError):
        update(storage, object, 12, {})


def test_update_fail_because_not_integer(storage):
    from tedega_storage.rdbms.crud import update
    with pytest.raises(TypeError):
        update(storage, Dummy, "12", {})


def test_create_fail_because_not_dict(storage):
    from tedega_storage.rdbms.crud import create
    with pytest.raises(TypeError):
        create(storage, Dummy, "Value")


def test_update_fail_because_not_dict(storage):
    from tedega_storage.rdbms.crud import update
    with pytest.raises(TypeError):
        update(storage, Dummy, 12, "Value")


def test_create_fail_because_wrong_paramaters(storage):
    from tedega_storage.rdbms.crud import create
    with pytest.raises(TypeError):
        # Dummy create does not expect "foo"
        create(storage, Dummy, {"foo": "bar"})


def test_search():
    from tedega_storage.rdbms import get_storage
    from tedega_storage.rdbms.crud import search
    from tedega_view import ClientError

    # Search
    with get_storage() as storage:
            search(storage, Dummy, search="id::1")
    with pytest.raises(ClientError):
        with get_storage() as storage:
            search(storage, Dummy, search="xxx::1")
    with pytest.raises(ClientError):
        with get_storage() as storage:
            search(storage, Dummy, search="id:1")
    # Sort
    with get_storage() as storage:
        search(storage, Dummy, sort="-id")
    with get_storage() as storage:
        search(storage, Dummy, sort="id")
    with pytest.raises(ClientError):
        with get_storage() as storage:
            search(storage, Dummy, sort="-xxx")


def test_crud():
    from tedega_storage.rdbms import get_storage
    from tedega_storage.rdbms.crud import create, read, update, delete
    with get_storage() as storage:
        item = create(storage, Dummy, {})
        read(storage, Dummy, item.id)
        item = update(storage, Dummy, item.id, {'id': 2})
        delete(storage, Dummy, 2)


def test_notfound_error():
    from tedega_view import NotFound
    from tedega_storage.rdbms import get_storage
    from tedega_storage.rdbms.crud import read, update, delete
    with pytest.raises(NotFound):
        with get_storage() as storage:
            read(storage, Dummy, 12)
    with pytest.raises(NotFound):
        with get_storage() as storage:
            update(storage, Dummy, 12, {})
    with pytest.raises(NotFound):
        with get_storage() as storage:
            delete(storage, Dummy, 12)
