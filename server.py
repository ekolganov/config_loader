""" а тут юзаем """
import read_config

config = read_config.load_config("task_config.yaml")

API_TOKEN = config.tg_bot.token
ACCESS_ID = config.tg_bot.username

WEB_HOST = config.web.hostname
WEB_PORT = config.web.port

DB_HOSTS = config.db.hosts
DB_USERNAME = config.db.username
DB_NAME = config.db.dbname
DB_PASSWORD = config.db.password
