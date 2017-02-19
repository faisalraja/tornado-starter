import os
import redis
import config
from rq import Worker, Queue, Connection


listen = ['high', 'default', 'low']


if __name__ == '__main__':

    with Connection(config.rc):
        worker = Worker(map(Queue, listen))
        worker.work()
