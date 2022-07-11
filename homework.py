import json
import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv
from requests import RequestException

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s]  [%(levelname)s] - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_message(bot, message):
    """Отправляет сообщение в телеграм-чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except telegram.TelegramError:
        raise telegram.TelegramError


def get_api_answer(current_timestamp):
    """Делает запрос к эндпоинту API-сервиса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=params
        )
        status = homework_statuses.status_code
    except Exception as error:
        raise RequestException(f'Ошибка эндпоинта {error}.')
    try:
        if status == HTTPStatus.OK:
            return homework_statuses.json()
        else:
            raise RequestException(f'Недоступность эндпоинта {ENDPOINT}.'
                                   f'Код ответа API: {status}'
                                   )
    except json.JSONDecodeError:
        raise json.JSONDecodeError('Сервер вернул невалидный json')


def check_response(response):
    """Проверяет ответ API на корректность.

    Если ответ API соответствует ожиданиям,
    то функция должна вернуть список домашних работ.
    """
    if not isinstance(response, dict):
        raise TypeError('Ответ API не является словарем.')
    if ('current_date' in response) and ('homeworks' in response):
        if not isinstance(response['homeworks'], list):
            raise TypeError('Ответ API не соответствует заданому типу.')
        homeworks = response.get('homeworks')
        return homeworks
    else:
        raise KeyError('В ответе нет нужных значений.')


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе статус этой работы.

    В случае успеха, функция возвращает подготовленную для отправки в Telegram
    строку, содержащую один из вердиктов словаря HOMEWORK_STATUSES.
    """
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if not homework_name:
        raise KeyError(f'отсутствует или пустое поле: {homework_name}')
    if homework_status not in HOMEWORK_STATUSES:
        raise KeyError(f'Неизвестный статус: {homework_status}')
    verdict = HOMEWORK_STATUSES.get(homework_status)
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения.

    Если отсутствует хотя бы одна переменная окружения —
    функция должна вернуть False, иначе — True.
    """
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical('Отсутствует токен')
        sys.exit()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    prev_message = ""
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if homeworks == []:
                logger.debug("Список домашних работ пустой")
            message = parse_status(homeworks[0])
            if prev_message != message:
                message = parse_status(homeworks[0])
                prev_message = message
                send_message(bot, message)
                logger.info(f'Отправлено сообщение: {message}')
            else:
                logger.debug('новые статусы в ответе отсутствуют')
            current_timestamp = response.get('current_date')
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            if prev_message != message:
                prev_message = message
                send_message(bot, message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
