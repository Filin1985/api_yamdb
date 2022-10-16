# Проект API_YaTube

##Описание проекта\*\*

Данный проект позволяет делать API запросы к постам, их комментариям и группам.

**Используемые технологии**

- Django
- Django RestFramework

### Как запустить проект

1. Клонируем репозиторий

```
git clone https://github.com/Filin1985/api_final_yatube.git
```

2. Заходим в папку с проектом

```
cd yatube_api
```

3. Устанавливаем виртуальное окружение

```
python3 -m venv venv
```

4. Активируем виртуальное окружение

```
source venv/bin/activate
```

5. Устанавливаем зависимости из файла requirements.txt

```
pip install -r requirements.txt
```

6. Выполняем миграции

```
python3 manage.py migrate
```

7. Запускаем проект

```
python3 manage.py runserver
```

### Примеры запросов

1. Получить (GET), создать все публикации (POST) - /api/v1/posts/
2. Получить (GET), удалить (DELETE) по id - /api/v1/posts/{id}/
3. изменить публикацию (PUT, PATCH) по id - /api/v1/posts/{id}/
