
config = {
    'dbname': 'dbmarket',
    'user': 'dbmarket',
    'password': 'dtmorgan',
    'port': '5438',
    'host': '185.143.173.37'
}


def db_config():
    return 'pq://{user}:{password}@{host}:{port}/{dbname}'.format(
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port'],
        dbname=config['dbname']
    )
