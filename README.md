# KantSelfieBot  
Telegram-бот для получения фото со стенда по коду.  
## Сборка проекта
Используется Python 3.8.6, очень вероятно(но это не точно) будет 
работать и для Python 3.7-3.9.
Перед первым запуском введите в терминал (удостоверьтесь, 
что pip относится к нужной версии python, с помощью `pip -V`):  
`pip install -r requirements.txt`  
## Настройка конфига
Зайдите в файл `config.py` и измените требуемые переменные, там есть комменты
После успешной установки зависимостей запустите bot.py и проверьте, 
что всё работает через long polling, если всё ок, то приступайте к настройке webhook
## Настройка webhook
Если у вас есть уже готовые SSL-ключи, используйте их, или создайте грязные с помощью следующих команд.
Выполните следующие две команды в консоли в директории со скриптом bot.py:  
`openssl genrsa -out webhook_pkey.pem 2048`  
`openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem`
Можно пропустить все поля, кроме Common Name (FQDN) и Email: там указываем то же значение, 
что и в переменной HOSTNAME в config.py, и соответственно ваш email.

Разкомменчиваем команды связанные с webhook'ом в конце скрипта и закомменчиваем команду `bot.polling()`  
(Удостоверьтесь, что у вас открыт порт 8443)