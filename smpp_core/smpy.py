import asyncio
from api import Api, InnerAPI
from logger import logger, api_logger
from typing import Union, List
from typing import List
from server import SmppClient, Application, UnknownUserException
from os import getenv

users = {
    "111111": "asdf",
    "1234": "qwerty" # smpp test client
}

HOST = "0.0.0.0"
PORT = "2775"
IS_TEST_RUN = False

if getenv("TEST_RUN"):
    """
    Тестовое решение, запускается с портом 2773, если скрипт запущен из докера
    Только потому что TEST_RUN прописан в docker-compose.yml
    """
    IS_TEST_RUN = True
    PORT = "2773"

class MySmppApp(Application):
    def __init__(self, name: str, logger):
        self.clients: List[SmppClient] = []
        super(MySmppApp, self).__init__(name=name, logger=logger)
        self.api = Api()

    async def handle_bound_client(self, client: SmppClient) -> Union[SmppClient, None]:
        print(InnerAPI().is_user_in_db(client.system_id, client.password))
        if client.system_id in users and\
                client.password == users[client.system_id]:
            self.clients.append(client)
            self.logger.info(f'Client {client.system_id}:{client.password} connected.')
            return client
        else:
            raise UnknownUserException()

    async def handle_unbound_client(self, client: SmppClient):
        self.clients.remove(client)

    async def handle_sms_received(self, client: SmppClient, source_number: str,
                                  dest_number: str, text: str):
        self.logger.debug(f'Received {text} from {source_number}')
        await client.send_sms(source=dest_number, dest=source_number,
                              text=f'You have sent {text} to me...')
        self.logger.debug(f'Send confirm "You have sent..."')

        if not IS_TEST_RUN:
            self.api.send_wa_msg(dest_number, text)
        api_logger.info(f'Message sent: Phone: {dest_number}, Message: "{text}"')


loop = asyncio.get_event_loop()

app = MySmppApp(name='smppy', logger=logger)
app.run(loop=loop, host=HOST, port=PORT)
