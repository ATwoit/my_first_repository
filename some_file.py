# print("This file is my first project")

import requests
import time

API_URL: str = 'https://api.telegram.org/bot'
API_CATS_URL: str = 'https://api.thecatapi.com/v1/images/search'
API_DOGS_URL: str = 'https://random.dog/woof.json'
API_FOXS_URL: str = 'https://randomfox.ca/floof/'
BOT_TOKEN: str = 'Здесь должен быть ваш токен'
ERROR_TEXT: str = 'Здесь должны быть фотки животных'
UNKNOWN_COMMAND_TEXT: str = 'Я не знаю такого животного. Напишите "кот", "собака" или "лиса".'

offset: int = -2
counter: int = 0
response: requests.Response
link: str

while counter < 100:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']

            # Проверяем, что сообщение содержит текст
            if 'text' in result['message']:
                user_message = result['message']['text'].lower()

                # Отправляем фото только после получения сообщения с ключевыми словами
                if 'кот' in user_message:
                    response = requests.get(API_CATS_URL)
                    link = response.json()[0]['url']
                elif 'собак' in user_message or 'собач' in user_message:
                    response = requests.get(API_DOGS_URL)
                    link = response.json()['url']
                elif 'лиса' in user_message:
                    response = requests.get(API_FOXS_URL)
                    link = response.json()['image']
                else:
                    # Если команда не распознана, бот отправит сообщение с ошибкой
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={UNKNOWN_COMMAND_TEXT}')
                    continue  # Пропускаем отправку фото в этом случае

                # Если запрос успешен, бот отправляет изображение
                if response.status_code == 200:
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={link}')
                else:
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

    time.sleep(1)
    counter += 1
