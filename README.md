# YaCut
## Проект YaCut — это сервис укорачивания ссылок. 
Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.
## Ключевые возможности сервиса:
- генерация коротких ссылок и связь их с исходными длинными ссылками,
- переадресация на исходный адрес при обращении к коротким ссылкам.
## API для проекта
Сервис обслуживает два эндпоинта:
- /api/id/ — POST-запрос на создание новой короткой ссылки;
- /api/id/<short_id>/ — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Semavova/yacut
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Выполнить миграции:
```python
flask db init
flask db migrate -m "<сообщение>"
flask db upgrade
```
Запустить в терминале командой:
```python
flask run
```
Справка по запросам находится в файле:
```
openapi.yml
```
Файл можно прочитать, вставив содержимое на сайте
```
https://editor.swagger.io/
```
## Технологии:
- Python 3.7
- Flask
- REST API
- SQLAlchemy
- Git

## Автор
[Vladimir Semochkin](https://github.com/Semavova)