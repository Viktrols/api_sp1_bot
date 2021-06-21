<h1>Telegram-бот для взаимодеяствия с API сервиса Практикум.Домашка</h1>
Телеграм-бот периодически обращается к API сервиса Практикум.Домашка и узнаёт статус вашего домашнего задания - взято ли задание в ревью, проверено ли оно (провалено или принято).

Полученный статус отправляется в чат сботом-ассистентом.
В случае ошибки бот также пришлет сообщение в телеграм чат.

Бот разработан в учебных целях на курсе Python-разработчик от Yandex.Praktikum.

<h3>Используемые технологии</h3>
Python 3.8
python-telegram-bot 12.7
<h2>Установка</h2>
<li>Клонируйте репозиторий на локальную машину: git clone https://github.com/Viktrols/api_sp1_bot.git</li>
<li>Установите виртуальное окружение: python3 -m venv venv</li>
<li>Активируйте виртуальное окружение: (Windows: source venv\scripts\activate; Linux/Mac: source venv/bin/activate)</li>
  <li>Установите зависимости: pip install -r requirements.txt</li>
<h3>Для работы боту требуется файл .env со следующими переменными окружения:</h3>
<li>PRACTICUM_TOKEN=YOUR_PRACTICUM_TOKEN # Токен, полученный на платформе Яндекс.Практикум</li>
<li>TELEGRAM_TOKEN=YOUR_TELEGRAM_TOKEN # Токен вашего бота, полученный через @BotFather</li>
<li>TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID # Ваш Chat_id</li>
