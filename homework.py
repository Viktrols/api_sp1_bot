import logging
import os
import requests
import telegram
import time

from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler


load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    filename='logs.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s')
logger = logging.getLogger('__name__')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('my_logger.log', maxBytes=50000000,
                              backupCount=5)
logger.addHandler(handler)

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
PRAKTIKUM_URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    status = homework.get('status')
    if status == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    elif status == 'approved':
        verdict = ('Ревьюеру всё понравилось, '
                   'можно приступать к следующему уроку.')
    else:
        return f'Работа {homework_name} еще проверяется'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    try:
        homework_statuses = requests.get(
            PRAKTIKUM_URL,
            headers={'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'},
            params={'from_date': current_timestamp})
        return homework_statuses.json()
    except Exception:
        logger.exception('Ошибка')


def send_message(message, bot_client):
    return bot_client.send_message(CHAT_ID, message)


def main():
    current_timestamp = int(time.time())
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    logging.debug('Бот запустился!')
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                logger.info(new_homework.get('homeworks')[0])
                send_message(
                    parse_homework_status(new_homework.get('homeworks')[0]),
                    bot)
            current_timestamp = new_homework.get('current_date',
                                                 current_timestamp)
            time.sleep(300)
        except Exception as e:
            send_message(f'Бот столкнулся с ошибкой: {e}', bot)
            time.sleep(5)


if __name__ == '__main__':
    main()
