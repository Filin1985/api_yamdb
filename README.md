# Проект API_YaTube

## Описание проекта\*\*

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории: "Книги", "Фильмы", "Музыка". Список категорий (Category) может быть расширен.

## Авторы проекта\*\*

1. Артем Баландин https://github.com/ArtemBalandin81
2. Марат Ихсанов https://github.com/Filin1985

## Ресурсы API YaMDb

**AUTH**: аутентификация.

**USERS**: пользователи.

**TITLES**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

**CATEGORIES**: категории (типы) произведений ("Фильмы", "Книги", "Музыка").

**GENRES**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.

**REVIEWS**: отзывы на произведения. Отзыв привязан к определённому произведению.

**COMMENTS**: комментарии к отзывам. Комментарий привязан к определённому отзыву.

## Пользовательские роли

**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

**Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.

**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.

**Администратор (admin)** — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

**Администратор Django** — те же права, что и у роли Администратор.

## Алгоритм регистрации пользователей

Пользователь отправляет POST-запрос с параметром email на `/api/v1/auth/email/`.
YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email (функция в разработке).
Пользователь отправляет POST-запрос с параметрами email и confirmation_code на `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).
Эти операции выполняются один раз, при регистрации пользователя. В результате пользователь получает токен и может работать с API, отправляя этот токен с каждым запросом.

**Используемые технологии**

- Django
- Django RestFramework
- JWT Authentification

### Как запустить проект

1. Клонируем репозиторий

```
git clone https://github.com/Filin1985/api_yamdb.git
```

2. Заходим в папку с проектом

```
cd api_yamdb
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

7. Загружаем данные в models для тестирования

```
python3 manage.py loaddatatobase
```

8. Запускаем проект

```
python3 manage.py runserver
```

### Примеры запросов

1. Получить (GET), создать пользователя (POST) - /api/v1/users/
2. Получить (GET), удалить (DELETE) пользователя по username - /api/v1/users/{username}/
3. Получение (GET), удаление (DELETE), изменение отзывов (PUT, PATCH) по id - /api/v1/titles/{title_id}/reviews/

### Ссылка на документацию к проекту

[localhost:8000](http://localhost:8000/redoc)
