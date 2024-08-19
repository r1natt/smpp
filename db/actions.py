from typing import TypedDict

from engine import users_col


class User(TypedDict):
    _id: int
    system_id: int
    password: str
    tag: str
    api_key: str


class Users:
    def __init__(self):
        pass

    def add_user(self, user: User) -> bool:
        # В данном случае возвращение True/False означает успешное или 
        # неуспешное действие
        if not self.is_user_in_db(user["system_id"], user["password"]):
            users_col.insert_one(user)
            return True
        return False

    def is_user_in_db(self, system_id: int, password: str) -> bool:  
        user = self.get_user(system_id, password)
        if user is None:
            return False
        return True

    def get_user(self, system_id: int, password: str) -> User | None:
        pap_dict = {"system_id": system_id, "password": password}
        # PAP - Password Authentication Protocol (связка логин + пароль)
        query = users_col.find_one(pap_dict)

        if query is None:
            return None
        user = User(_id=str(query["_id"]),
                    system_id=query["system_id"],
                    password=query["password"], 
                    tag=query["tag"],
                    api_key=query["api_key"])
        return user
        
