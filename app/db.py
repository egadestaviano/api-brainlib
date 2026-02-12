from peewee import DatabaseProxy
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin

class ReconnectPooledMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass

database = DatabaseProxy()
