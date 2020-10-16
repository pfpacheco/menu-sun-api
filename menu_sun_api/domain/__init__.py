import json

from sqlalchemy.inspection import inspect as sqlalchemyinspect

from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin

Base = declarative_base()

PRIMITIVE = (int, str, bool, float)


def is_primitive(thing):
    return isinstance(thing, PRIMITIVE)


class Default(SerializerMixin):
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(DateTime, onupdate=datetime.utcnow)
    id = Column(Integer, primary_key=True)

    @classmethod
    def from_dict(cls, source):
        obj = cls()
        for key, value in source.items():
            if hasattr(obj, key) and is_primitive(value):
                setattr(obj, key, value)
        return obj

    def update_from_dict(self, source):
        for key, value in source.items():
            if hasattr(self, key) and is_primitive(value):
                setattr(self, key, value)

    def update(self, source):
        if (not source):
            return None
        clazz = type(self)
        inspected_model = sqlalchemyinspect(clazz)
        for attr, column in inspected_model.columns.items():
            if (attr in source.__dict__):
                value = getattr(source, attr)
                setattr(self, attr, value)

    def accept(self, visitor):
        return visitor.visit(self)

    def __str__(self):
        payload = self.to_dict()
        text = json.dumps(payload, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
        return text.replace('\n', '')
