#!/bin/bash -e
clear
echo "Сегодня " `date`
echo 'Выполняется обновление данных'
git pull
echo 'Создание среды окружения Python'
python3 -m venv venv
source venv/bin/activate
sleep 1
echo 'Установка зависимостей '
pip install -r requirements.txt
pip install django-extensions
pip install rollbar
clear
echo 'Установка NodeJS '
npm ci --dev
#./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./" &
echo 'Сбор статики '
python3 manage.py collectstatic
echo 'Выполнение миграции '
python3 manage.py migrate
clear
echo 'Перезапуск служб '

FILE=/etc/systemd/system/burger-shop-devman.service
if test -f "$FILE"; then
	systemctl restart burger-shop-devman.service
else
	echo -n "Отсутствует файл для работы сервиса"$'\n'$FILE$'\n'"Необходимо создать. Используйте Readme проекта"
fi

FILE=/etc/systemd/system/certbot-renewal.service
if test -f "$FILE"; then
	systemctl restart certbot-renewal.service
else
	echo -n "Отсутствует файл для работы сервиса"$'\n'$FILE$'\n'"Необходимо создать. Используйте Readme проекта"
fi

FILE=/etc/systemd/system/certbot-renewal.timer
if test -f "$FILE"; then
	systemctl restart certbot-renewal.timer
else
	echo -n "Отсутствует файл для работы сервиса"$'\n'$FILE$'\n'"Необходимо создать. Используйте Readme проекта"
fi

FILE=/etc/systemd/system/nginx.service
if test -f "$FILE"; then
	systemctl restart nginx.service
else
	echo -n "Отсутствует NGINX сервис"$'\n'$FILE$'\n'"Необходимо установить"
fi

FILE=/opt/star-burger/.env
if test -f "$FILE"; then
	source .env
	cd /opt/star-burger
	git_id="$(git rev-parse --verify HEAD)"
	user="$(whoami)"
	echo $ROLLBAR_TOKEN_KEY
	curl --request POST \
	     --url https://api.rollbar.com/api/1/deploy \
	     --header 'X-Rollbar-Access-Token: '$ROLLBAR_TOKEN_KEY \
	     --header 'accept: application/json' \
	     --header 'content-type: application/json' \
	     --data '
	{
	  "rollbar_username": "'user'",
	  "environment": "PyCharm",
	  "revision": "1",
	  "local_username": "Max",
	  "comment": "Comment git: '$git_id'",
	  "status": "succeeded"
	}'
else
	echo -n "Отсутствует основной файл конфигурации .env"$'\n'$FILE$'\n'"Необходимo прочесть Readme"
fi

echo -n "Ok..."
