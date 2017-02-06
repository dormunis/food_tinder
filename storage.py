import psycopg2
import psycopg2.extras


class Storage(object):
    def __init__(self, postgres_settings):
        self.postgres_settings = postgres_settings
        self.conn = psycopg2.connect(**postgres_settings)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def get(self, query, vars=()):
        self.cursor.execute(query, vars)
        try:
            return self.cursor.fetchall()
        except psycopg2.ProgrammingError, e:
            raise psycopg2.DatabaseError("Error occurred when requesting from DB; err: {err}".format(err=str(e)))

    def insert(self, query):
        self.cursor.execute(query)
        self.conn.commit()
