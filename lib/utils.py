import inspect
import logging
import sys
import os
from peewee import SqliteDatabase
import config


def get_db():
    """Get Application Database
    :return: DB
    """
    global DB
    if DB is None:
        DB = SqliteDatabase(config.db)

    return DB


def get_path(*path):

    return os.path.join(os.path.dirname(__file__), '..', *path)


def get_members_by_parent(module, parent):
    """Get all models that extends BaseModel
    :return:
    """
    return dict(member
                for member in inspect.getmembers(sys.modules[module if type(module) is str else module.__name__],
                                                 lambda c: inspect.isclass(c) and c.__base__ is parent))