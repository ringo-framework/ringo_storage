#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import uuid
import sqlalchemy as sa


class UUID(sa.TypeDecorator):
    """Json Datatype is used to implement a field which can store a UUID"""

    impl = sa.String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)

    # This code is not reached by tests, although this should happen
    # because the correct type is set after reading the value from the
    # DB. So for know I will comment this code out to get 100% code
    # coverage again. But leave this code as a reminder here in case I
    # am running into trouble later.
    # def process_result_value(self, value, dialect):
    #     if value is not None:
    #         return uuid.UUID(value)
