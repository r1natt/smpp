from flask import Flask, Response, request

from actions import User, Users

app = Flask("DB_API")


"""
Для себя
GET — получение ресурса
POST — создание ресурса
PUT — обновление ресурса
DELETE — удаление ресурса

Методы которые нужны smpp_core:
    is_user_in_db - (get) запрашивается в момент подключения нового 
        пользователя к системе
    sms_request - (post) отправляется в момент когда приходит запрос на 
        отправку сообщения, этот метод буквально оповещает бд, что сообщение 
        есть, но пока не обработалось, в обратку метод посылает id сообщения, 
        которое дало бд
    sms_request_update - обновляет статус сообщения из sms_request
"""


users = Users()

@app.route("/new_user", methods=["POST"])
def new_user():
    system_id = request.args["system_id"]
    password = request.args["password"]
    tag = request.args["tag"]
    api_key = request.args["api_key"]
    user = User(system_id=system_id,
                password=password,
                tag=tag,
                api_key=api_key)
    status_code = users.add_user(user)
    match status_code:
        case True:
            return Response('{"status":"successfully"}', 
                            status=200, 
                            mimetype="application/json")
        case False:
            return Response('{"status":"error"}', 
                            status=500, 
                            mimetype="application/json")

    return Response("correct", status=200, mimetype="text/plain")

@app.route("/is_user_in_db", methods=["GET"])
def is_user_in_db():
    system_id = request.args["system_id"]
    password = request.args["password"]
    is_user_in_db = users.is_user_in_db(system_id, password)
    if is_user_in_db:
        user = users.get_user(system_id, password)
        print(user)
        return Response(f"{user}",
                        status=200,
                        mimetype="application/json")
    else:
        return Response("no", status=200, mimetype="text/plain")

