Тестовое задание:
    Развернуть систему docker-контейнеров (с использованием docker-compose) в составе:
        worker - на базе python:3.12. Слушает очередь rabbit. Имеет примонтированную директорию по пути /reports
        rabbit - на базе rabbitmq:management. Брокер очереди
        uwsgi - на базе python:3.12. Имеет веб-интерфейс. Отправляет события в очередь rabbit
    worker:
        должен слушать очередь rabbit
        получив сообщение от rabbit должен:
            доставать из сообщения ссылку на репозиторий github для клонирования репозитория
            клонировать репозиторий по полученной ссылке
            запускать проверку исходного кода при помощи сканера semgrep (который должен находиться в этом же контейнере)
            складывать результат проверки в файл в директорию /reports (в названии должно быть указано название репозитория)
    uwsgi:
        должен работать на django
        должен иметь страницу с полем для ввода и кнопкой (доступна по http://localhost:8000)
        при нажатии на кнопку, содержимое поля должно отправляться в обработчик запроса "/check/repo/" в теле POST запроса
        внутри обработчика проводится проверка на URL (проверка, что полученное значение является http ссылкой на репозиторий)
        если проверка успешна, то ссылка отправляется в очередь rabbit (можно использовать стандартную библиотеку pika)
    Как проверить, что работает:
        Запускаем систему контейнеров через "docker-compose up --build"
        Заходим на страницу http://localhost:8000
        Видим поле для ввода и кнопку
        Вводим в поле для ввода http ссылку для клонирования открытого репозитория github и нажимаем кнопку
        Ждем (смотрим логи)
        В какой-то момент видим в примонтированной директории файл с названием репозитория github, в котором лежит отчет по уязвимостям