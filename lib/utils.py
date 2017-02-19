import inspect
import logging
import sys
import os
import config
from rq import Queue


def get_path(*path):

    return os.path.join(os.path.dirname(__file__), '..', *path)


def get_members_by_parent(module, parent):
    """Get all models that extends BaseModel
    :return:
    """
    return dict(member
                for member in inspect.getmembers(sys.modules[module if type(module) is str else module.__name__],
                                                 lambda c: inspect.isclass(c) and c.__base__ is parent))


def get_queue():

    return Queue(connection=config.redis_conn)
