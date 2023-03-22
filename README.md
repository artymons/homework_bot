# Телеграмм бот «yandex-telegrambot»

### Описание
Telegram-бот обращается к API сервису Яндекс.Практикум и узнает статус домашней работы пользователя: взята ли работа в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

Что делает бот:
* раз в 10 минут опрашивает API сервиса Яндекс.Практикум и проверяет статус отправленной на ревью работы;
* при обновлении статуса анализирует ответ API и отправляет вам соответствующее уведомление в Telegram;
* логирует свою работу и сообщает вам о важных проблемах сообщением в Telegram.

### Технологии
* Python 3.7
* python-dotenv 0.19.0
* python-telegram-bot 13.7
* requests 2.26.0

### Запуск проекта на Linux
Клонировать проект c GitHub
```
git clone git@github.com:boginskiy/yandex-telegrambot.git
```
Установить виртуальное окружение venv
```
python3 -m venv venv
```
Активировать виртуальное окружение venv
```
source venv/bin/activate
```
Обновить менеджер пакетов pip
```
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
Запуск
```
python3 homework.py
```

### **Дополнительная информация**
Ознакомьтесь с **.env.example** файлом. На его основе со своими данными создайте **.env** файл в директории проекта.
```
.env.example

PRACTICUM_TOKEN = Токен для доступа к данным Яндекс.Практикум
TELEGRAM_TOKEN = API токен вашего бота
TELEGRAM_CHAT_ID = Id идентификатор вашего чата
```
У вас должно получиться примерно так:
```
.env

PRACTICUM_TOKEN = y0_AgAAAABbsMPDAAYckQAAAADPSrFmdbIiI6wdQYeQw6APl2vZaC1B-KG
TELEGRAM_TOKEN = 5314486465:AAFxdybGdScu3aj0WPmnLnunVru7JuOdMtA
TELEGRAM_CHAT_ID = 5339854955
```
---

**PRACTICUM_TOKEN** - доступ к API Яндекс.Практикум возможен только по токену. Получить токен можно по адресу: _https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a_, при условии, что вы зарегистрированы.

**TELEGRAM_TOKEN** - API токен вашего бота получаем путем отправки сообщения _/mybots_ в телеграмм канале _BotFather_, далее кликаем  бота, после проходим по кнопке _API Token_.

**TELEGRAM_CHAT_ID** - id вашего чата получаем путем отправки сообщения в телеграмм канале _userinfobot_.

---
