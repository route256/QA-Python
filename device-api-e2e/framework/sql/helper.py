from urllib.parse import urlparse


def dsn_parse(dsn):
    _dsn = urlparse(dsn)
    return {
        'dbname': _dsn.path.strip('/'),
        'user': _dsn.username,
        'password': _dsn.password,
        'port': _dsn.port,
        'host': _dsn.hostname,
    }
