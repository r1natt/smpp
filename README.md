<h1 align="center">SMPP</h1>

<div align="center">
 
<img width="100" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/python.png" alt="Python" title="Python"/>
<img width="100" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/docker.png" alt="Docker" title="Docker"/>
<img width="100" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/rest.png" alt="REST" title="REST"/>
<img width="100" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/mongodb.png" alt="mongoDB" title="mongoDB"/>
    
</div>

**Данный проект является фриланс заказом и выложен с разрешения заказчика.**

# Задача

Задача состоит в получении сообщений от существубщего ПО заказчика и вызывает методы API, для отправки сообщений в WhatsApp

Проект является своего рода мостом между протоколами

Сложность состоит в самом SMPP протоколе (он древнейший). Похож на сокеты (нужно подсоединение пользователей). 

# Реализация

Сервис поделен на 2 микросервиса (2 контейнера Docker). Проект не такой сложный, чтобы разделять его на микросервисы, но мне захотелось поработать с Docker.

Микросервисы:

## Core

Содержит всю логику работы сервиса. Обработка сообщений, управление сообщениями, отправка запросов к апи рассылки WhatsApp. 

Файлы server.py и smpy.py содержат код https://github.com/devtud/smppy.
 * server.py - запускает smpp сервер, получает сообщения и сам отправляет кодовые ответы.
 * smpy.py - содержит функции коннекта пользователей и обработки поступающих сообщений.
 * api.py - содержит функции взаимодействия с апи сервиса рассылки и db микросервисом.

## DB

Является отдельным микросервисом MongoDB для хранения пользователей.

 * api.py - файл с эндпойтами api.
 * actions.py - файл с функциями, которые выполняют запросы к бдшке.
