from dotenv import load_dotenv
from dataclasses import dataclass
import json
import requests
from typing import Literal, Dict
from logger import api_logger
import os
import roundrobin  # Для балансировки нагрузки


load_dotenv("config.env")

required_env_vars = ["API_KEY"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")


@dataclass
class Account:
    _id: int
    phone: str
    unique_id: str
    status: str
    created: str


class InnerAPI:
    def is_user_in_db(self, system_id: int, password:str):
        is_user_in_db = requests.get("http://172.19.0.1:5000/is_user_in_db",
                                     params={
                                         "system_id": system_id,
                                         "password": password
                                         },
                                     timeout=10
                                     )
        print(is_user_in_db)
        return False


class WA_Accounts:
    def __init__(self, api_key):
        self.domain = "https://isender.org"
        self.api_key = api_key
        self.accs = self._get_wa_accounts()
        self.load_balancer = roundrobin.basic(self.accs)

    # Нужно будет сделать обновление wa_accs каждый n часов

    def _get_wa_accounts(self) -> Dict[Literal["id"], Account] | None:
        """
        Важно, что эта функция выполняется один раз за всю работу программы, 
        не подразумевается, что можно будет менять количество аккаунтов в течении работы
        """
        for _ in range(5):
            """
            Сервис может не ответить или выкинет единичную ошибку, но если такое 
            происходит в течении 5ти попыток, то ошибка серьезная
            """
            try:
                req = requests.get(self.domain + "/api/get/wa.accounts", 
                                   params={"secret": self.api_key})
                data = json.loads(req.text)["data"]
                api_logger.debug(f'Get wa accs status: {req.text}')
                
                accs = {}
                for acc in data:
                    account_data = Account(
                            _id=acc["id"],
                            phone=acc["phone"],
                            unique_id=acc["unique"],
                            status=acc["status"],
                            created=acc["created"])
                    accs[acc["id"]] = account_data

                return accs
            except Exception as e:
                api_logger.error(f'Get wa accs error: {e}')
            return {}

    def get_unique(self):
        _id = self.load_balancer()
        return self.accs[_id].unique_id
    

class Api:
    def __init__(self):
        self.domain = "https://isender.org"
        self.api_key = os.getenv("API_KEY")
        self.wa_accs = WA_Accounts(self.api_key)

    def _phone_format(self, phone: str) -> str:
        if phone[0] != "+":
            if phone[0] != "7":
                phone = "7" + phone
            phone = "+" + phone
        return phone
    
    def is_msg_sent_success(self, response):
        status = response["status"]
        match status:
            case 200:
                return True
            case 400, 401, 403, 404, 500:
                return False
            case _:
                return False

    def send_msg_request(self, chat: dict) -> dict:
        try:
            response = requests.post(self.domain + "/api/send/whatsapp", params=chat)
            api_logger.debug(f"Sent msg status: {response.text}")
            return json.loads(response.text)
        except Exception as e:
            api_logger.error(f'Exception in send wa msg: {e}')

    def send_wa_msg(self, phone: str, message: str):
        is_success = False
        tested_unique = set()
        """
        tested_unique - множество опробованных номеров, это множество нужно, чтобы 
        сверять с каких номеров я уже пробовал отправлять сообщения, тк балансировщик
        нагрузки циклический, если цикл замкнулся и все номера выдавали ошибку при 
        исполнении, то нет больше смысла в цикле while пытатся отправить сообщение. 
        Поэтому я выдаю критическую ошибку в коде ниже
        """
        while not is_success:
            unique = self.wa_accs.get_unique()
            if unique not in tested_unique:
                tested_unique.add(unique)
                chat = {
                    "secret": self.api_key,
                    "recipient": self._phone_format(phone),
                    "account": unique,
                    "type": "text",
                    "message": message
                }
                response = self.send_msg_request(chat)
                if self.is_msg_sent_success(response):
                    is_success = True
            else:
                api_logger.critical("При попытке отправить сообщение, все номера выдали ошибку")
                # Пока что выхожу из цикла так и не отправив сообщение
                # Потом нужно будет прикрутить очередь сообщений, и пытаться отправлять
                # Когда будет возможность
                break

