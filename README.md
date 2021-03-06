## Telegram бот для поиска вакансий
Описание: Поиск вакансий по ключевому слову в режиме вопрос - ответ. Для поиска используется обратный индекс, 
для увеличения полноты индекса - w2v обученный на hr данных. Движок автоматически обновляет вакансии и индексы.

В дальнейшем в шедуллер планируется добавить рассылку вакансий, что повлечет за собой интеграцию с базой данных.

## Запуск движка

Для работы движка требуется memcache, поэтому внутри Dockerfile есть скрипты сборки как memcached так и самого проекта.
Далее представлена шаги и сборки до деплоя.

Объявление глобальных переменных:
PROJECT_ID - имя вашего проекта в gcp
APP_NAME - имя вашей программы(можно выбрать любой)
```
PROJECT_ID=botfind
APP_NAME=BotFinder
```
Сборка образа:
```
docker build -t gcr.io/${PROJECT_ID}/${APP_NAME} .
```
Запуск контейнера для проверки работоспособность:
```
docker run -p 8080:8081 --name APP_NAME
```
Загрузка контейнера в gcp:
```
docker push gcr.io/${PROJECT_ID}/${APP_NAME}
```
Деплой контейнера:
```
gcloud app deploy --image-url gcr.io/${PROJECT_ID}/${APP_NAME}
```
В случае успешного завершения деплоя, gcloud вернет ссылку на проект. Далее, нужно дать понять сервису
телеграмм куда слать запросы. GET запрос:
```
https://api.telegram.org/<BOT_TOKEN>/setWebhook?url=https://velvety-harbor-284611.ew.r.appspot.com/
```
Должен вернуть ок.


## Особенности

Если требуется горизонтальное масштабирование, то memcache нужно вынести за пределы контейра.

## Описание конфиг файла

```
{
  "url_fasttext": url_fasttext
  "token_fastext": "token_fastext",
  "server_memcached": server_memcached,
  "bot_token": bot_token
}
```


## TODO

1. Описать  конфиги в yaml файле
2. Добавить рассылку пользователям с самой подходящей вакансией
2.1 C помощью orm подключиться к базе и записать туда chat_id
3. Переделать ux схему управлениями вакансиями и вообще переделать ее черех callback
4. Возможно стоит перенести w2v в основной сервис
5. Перенести файлы установки в отдельную папку... а потом может и удалять их
6. Подключить jaeger для описания api


