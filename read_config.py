""" парсим файлик """

import yaml
import re
import os

from typing import List

from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    username: str


@dataclass
class Web:
    port: int
    hostname: str


@dataclass
class Db:
    hosts: List[str]
    username: str
    password: str
    dbname: str


@dataclass
class Config:
    tg_bot: TgBot
    web: Web
    db: Db


def get_os_env(row_pass: str) -> str:
    """ превращаем переменную из текста в переменную из ОС """

    env = re.search(r'^\$(\w+)', row_pass)
    if env:
        os_env = os.getenv(env.group(1))
        return os_env
    else:
        print(f"Ошибка в парсинге значения из ОС:  {row_pass}")


def load_config(path: str) -> Config:
    """ ф-я инициализации параметров из ямл файла """

    with open(path, 'r') as f:
        params = yaml.safe_load(f)

    return Config(
        tg_bot=TgBot(
            token=get_os_env(params["telegram"]["token"]),
            username=params["telegram"]["username"],
        ),
        web=Web(
            hostname=params["web"]["hostname"],
            port=params["web"]["port"],
        ),
        db=Db(
            hosts=params["db"]["hosts"],
            username=params["db"]["username"],
            password=get_os_env(params["db"]["password"]),
            dbname=params["db"]["dbname"],
        )
    )