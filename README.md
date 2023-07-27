API сервиса для публикации и работы с .csv файлами
=====================
Тестовое задание

Развертка
-----------------------
Рекомендуется использовать Python версии 3.8.5

В папке проекта `создаем виртуальное окружение`:
```bash
$ python -m venv venv
```

Активируем виртуальное окружение:
```bash
Windows:
$ venv\Script\activate

Linux:
$ source venv\bin\activate
```

Устанавливаем необходимые зависимости:
```bash
(venv) $ pip install -r requirements.txt
```

Применяем миграции к нашей базе данных:
```bash
(venv) $ python manage.py migrate
```

Проект готов к запуску!
```bash
(venv) $ python manage.py runserver
```

Если всё было сделано правильно, то в терминале видим подобный текст:
```
System check identified no issues (0 silenced).
July 27, 2023 - 13:51:54
Django version 4.2.3, using settings 'file_api.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
Сервер будет запущен локально по адресу http://127.0.0.1:8000/


Описание API проекта
-----------------------


### api/datasets/
**GET:** Получение списка всех csv файлов с пагинацией. Для перехода между страница используется параметр `page`:

    api/datasets/?page=2


### api/datasets/create/
**POST:** Загрузка нового csv файла. Необходимо передать csv файл в поле `file`


### api/datasets/{id}/
**GET:** Получение более подробной информации о датасете, в том числе количество записей (rows), колонках (columns) и ссылкой на скачку файла (file).

**DELETE:** Удаление выбранного датасета из базы данных сервиса


### api/datasets/{id}/data
**GET:** Получение данных из файла с пагинацией, возможностью фильтрации и сортировки.

Пример запроса с сортировкой по полю hero_id в порядке убывания:

    /api/datasets/20/data/?order_by=hero_id

Пример запроса с сортировкой по полю hero_id в порядке возрастания:

    /api/datasets/20/data/?order_by=-hero_id

Пример запроса с получением записей, где значние hero_id больше 30, а значение 1_win меньше или равно 1000:

    /api/datasets/20/data/?hero_id=>30&1_win=<=1000
