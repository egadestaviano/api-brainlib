from peewee import DatabaseProxy

# Initialize at runtime with the actual database instance
# Example:
# from peewee import SqliteDatabase
# database.initialize(SqliteDatabase('db.sqlite3'))
database = DatabaseProxy()
