from dataclasses import dataclass
import json
from logger import logger
from typing import Dict, Literal


@dataclass
class User:
    client_id: str
    password: str
    api_key: str


class Users:
    def __init__(self):
        self.users = self._fill_users()

    def _get_data_from_file(self) -> Dict[Literal["client_id"], Dict]:
        try:
            with open("./config.json") as file:
                users = json.load(file)
            return users
        except Exception as e:
            logger.error(f"Файл users.json поврежден: {e}")
        return {}

    def _fill_users(self) -> Dict[str, User]:
        users = self._get_data_from_file()
        users_as_objs = {}
        for user in users:
            client_id = users[user]["client_id"]
            password = users[user]["password"]
            api_key = users[user]["api_key"]
            users_as_objs[user] = User(
                    client_id=client_id,
                    password=password,
                    api_key=api_key)
        return users_as_objs

    def is_known_user(self, client_id: str, password: str) -> bool:
        if client_id in self.users:
            if password == self.users[client_id].password:
                return True
            else:
                return False
        else:
            return False

