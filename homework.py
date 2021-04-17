import logging
import os
import requests
import telegram
import time

from dotenv import load_dotenv


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s')

load_dotenv()

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
PRAKTIKUM_URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
HOMEWORK_STATUSES = {
    'reviewing': 'Работа еще проверяется.',
    'rejected': 'К сожалению в работе нашлись ошибки.',
    'approved': ('Ревьюеру всё понравилось, '
                 'можно приступать к следующему уроку.')}


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    status = homework.get('status')
    if status is None or status not in HOMEWORK_STATUSES:
        return 'Домашка не найдена или статус неизвестен'
    if status == 'reviewing':
        return f'Работа "{homework_name}" еще проверяется'
    else:
        return (f'У вас проверили работу "{homework_name}"!\n\n'
                f'{HOMEWORK_STATUSES[status]}')


def get_homework_statuses(current_timestamp):
    if current_timestamp is None:
        current_timestamp = int(time.time())
    try:
        homework_statuses = requests.get(
            PRAKTIKUM_URL,
            headers={'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'},
            params={'from_date': current_timestamp})
    except ValueError as e:
        logging.error(e, exc_info=True)
    except requests.HTTPError as e:
        logging.error(e, exc_info=True)
    except requests.ConnectionError as e:
        logging.error(e, exc_info=True)
    except requests.Timeout as e:
        logging.error(e, exc_info=True)
    except requests.RequestException as e:
        logging.error(e, exc_info=True)
    return homework_statuses.json()


def send_message(message, bot_client):
    return bot_client.send_message(CHAT_ID, message)


def main():
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    current_timestamp = int(time.time())
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    logger.debug('Бот запустился!')
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
            logging.exception(f'Бот столкнулся с ошибкой: {e}', exc_info=True)
            send_message(f'Бот столкнулся с ошибкой: {e}', bot, exc_info=True)
            time.sleep(5)


if __name__ == '__main__':
    main()
