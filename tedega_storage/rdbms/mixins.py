#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mixin modul"""
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import event


class Protocol(object):
    """Mixin which adds based protocol functionallity to Items."""

    created = sa.Column("created", sa.DateTime)
    """Datetime when the dataset was created."""
    updated = sa.Column("updated", sa.DateTime)
    """Datetime when the dataset was last modfied."""

    def __init__(self):
        super(Protocol, self).__init__()
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()


@event.listens_for(Protocol, 'before_update', propagate=True)
def protocol_update(mapper, connection, target):
    """Listen for the 'before_update' event. Make sure that the last
    updated field is updated as soon as the item has been modified.
    """
    if hasattr(target, "updated"):
        target.updated = datetime.utcnow()
