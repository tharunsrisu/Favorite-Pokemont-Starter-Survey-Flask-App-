""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from contextlib import contextmanager
import logging
import os

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

# pool variable. -- this is being used as a global will be shared across threads, not processes
# (which shoudl be good enough for a project of this scale.)

pool = None

# request this to run before first request and seup a connection pool
def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')


# use the contect manager annotation to let us use generator-style python
# code to create a context-manager all our own -- this makes _using_ the library easy
# even if it's more python-magic than you're used to on this end.
@contextmanager
def get_db_connection():
    try:
        connection = None
        while connection is None:
            try:
                connection = pool.getconn()
            except:
                current_app.logger.info("failed to get connection. retrying immediately.")

        yield connection
    finally:
        if connection is not None:
            pool.putconn(connection)

# use the contect manager annotation to let us use generator-style python
# code to create a context-manager all our own -- this makes _using_ the library easy
# even if it's more python-magic than you're used to on this end.

@contextmanager
def get_db_cursor(commit=False):
    '''use commit = true to make lasing changes. Call this function in a with statement'''
    with get_db_connection() as connection:
      # I haven't checked -- but this _should_ make our cursors return dicts instead of tuples
      # this is a big improvement IMHO
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()