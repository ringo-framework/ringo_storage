#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import sqlalchemy as sa


class UUID(sa.TypeDecorator):
    """Json Datatype is used to implement a field which can store a UUID"""

    impl = sa.String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return uuid.UUID(value)
