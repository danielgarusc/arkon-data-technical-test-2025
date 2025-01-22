from decouple import config

TYPE_DB = config('TYPE_DB', 'mysql')
PATH_RULE_DB = config('PATH_RULE_DB')
FILE_NAME = config('FILE_NAME')
FILE_PATH = config('FILE_PATH')
URL_BASE = config('URL_BASE')
CELERY_BROKER_URL = config('CELERY_BROKER_URL', None)
