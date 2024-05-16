from databases import Database


DATABASE_URL = 'postgresql://app@localhost/app'
SALT = '08299abd2a9b6090ccac621a4bb64f8c326820240b26abfeed359822cf5e78b3'

database = Database(DATABASE_URL)


class DataBaseExecuteException(Exception):
    pass
