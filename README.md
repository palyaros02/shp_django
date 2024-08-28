# Новостной сайт

Автор: Ярослав Паламарчук

Админка: <http://localhost:8000/admin/>

## Запуск проекта

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Обновление документации

```bash
cd docs && make html
```

## Тесты

```bash
python manage.py test
```

----------------

Суперюзер:

- Логин: admin
- Почта: <example@example.com>
- Пароль: admin
