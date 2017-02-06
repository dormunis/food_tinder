from types import NoneType
from uuid import uuid4
import psycopg2
import psycopg2.extensions
from psycopg2._json import Json

# register these types as soon as possible, returns strings as <type 'unicode'>
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


class PostgresConnector(object):
    def __init__(self, connection, fetch_count):
        self.__connection = connection
        self.__fetch_count = fetch_count

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__connection.close()

    @classmethod
    def get_connector(cls, connection_config, fetch_count=2000):
        """
        create a new connection to postgres.
        :param connection_config: example => {
            "database": "postgres",
            "user": "postgres",
            "host": "evrdvtapp01.gartner.com",
            "port": "5432"
        }
        :param fetch_count: note that the optimum size to fetch at a time is about 100KB (roughly 2000 rows).
        :return: a new connection to postgres
        """
        connection = psycopg2.connect(**connection_config)
        return cls(connection, fetch_count)

    def fetchall(self, sql_statement, *args, **kwargs):
        with self.__connection.cursor() as cursor:
            cursor.execute(sql_statement, *args, **kwargs)
            return cursor.fetchall()

    def fetchmany(self, sql_statement, *args, **kwargs):
        """
        returns a named cursor (server-side cursor) that iterable.
        MUST CLOSE THIS CURSOR OR SERVER-SIDE RESOURCES WILL HANG UNTIL CONNECTION IS CLOSED.
        :param sql_statement:
        :param args: arguments for the sql_statement (referenced in the sql as %s)
        :param kwargs: named arguments for the sql_statement (referenced in the sql as %(NAME)s)
        :return: iterable results.
        """
        random_name = str(uuid4())
        cursor = self.__connection.cursor(name=random_name, scrollable=False)
        cursor.itersize = self.__fetch_count
        cursor.execute(sql_statement, *args, **kwargs)
        return cursor

    def insert(self, sql_statement, *args, **kwargs):
        with self.__connection:
            with self.__connection.cursor() as cursor:
                cursor.execute(sql_statement, *args, **kwargs)

    def __insert_many(self, cursor, table_name, columns, rows):
        """
        multi_insert will look like (row1col1, row1col2),(row2col1,row2col2),...
        :param cursor: cursor with transaction opened
        :param table_name:
        :param columns:
        :param rows:
        :return:
        """
        multi_insert = ','.join([cursor.mogrify("(%s)" % ','.join(("%s",) * len(columns)), row) for row in rows])
        columns = "(%s)" % ','.join(columns)
        query = "INSERT INTO %s %s VALUES %s ON CONFLICT DO NOTHING".decode('ascii')

        query = query % (table_name, columns, multi_insert.decode('utf-8'))

        cursor.execute(query.encode('utf-8'))

    def insert_many(self, table_name, columns, rows):
        """
        inserts in a single statement a large amount of rows.
        :param table_name:
        :param columns:
        :param rows:
        :return:
        """
        with self.__connection:
            with self.__connection.cursor() as cursor:
                self.__insert_many(cursor, table_name, columns, rows)

    def replace_table_content(self, table_name, columns, rows):
        with self.__connection:
            with self.__connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE %s" % table_name)
                self.__insert_many(cursor, table_name, columns, rows)

    def copy_table(self, origin, destination, origin_columns=None):
        assert isinstance(origin_columns, (list, NoneType)), "origin_columns must be list or not specified, not %s" % type(origin_columns)

        if origin_columns:
            copy_query = "INSERT INTO %(dest)s (%(cols)s) SELECT %(cols)s FROM %(origin)s" % \
                         {"dest": destination, "cols": ', '.join(origin_columns), "origin": origin}
        else:
            copy_query = "INSERT INTO %(dest)s SELECT * FROM %(origin)s" % {"dest": destination, "origin": origin}

        with self.__connection:
            with self.__connection.cursor() as cursor:
                cursor.execute('TRUNCATE TABLE %s' % destination)
                cursor.execute(copy_query)

    @staticmethod
    def dict_as_json(dictionary):
        return Json(dictionary)
