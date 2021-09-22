import os


def get_connection_string():
    return 'mysql+pymysql://%s:%s@%s:%s/%s' % (
        os.environ['MYSQL_USER'],
        os.environ['MYSQL_PASSWORD'],
        os.environ['MYSQL_HOST'],
        os.environ['MYSQL_PORT'],
        os.environ['MYSQL_DATABASE'],
    )
