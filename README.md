# Тестовое задание

Запуск: `docker-compose up --build`

Сразу применятся миграции, а также создастся суперпользователь (админ)

Swagger доступен по http://localhost:8000/api/swagger/

Админка доступна по http://localhost:8000/admin/

Доступ: username `admin`, пароль `admin`

Пользователь через админку создавался бы по http://localhost:8000/admin/src/user/add/. Я вручную после поднятия сервиса создавал с username `test`, пароль `Test123!`

В swagger-е потом ходил на `/api/token/`, после чего указывал `access_token` в кнопке `Authorize`.

Награду, которую пользователь может получить 1 раз в день, я установил равной `500`.

## Выполненные требования

✅ Стек технологий

- ✅ Django REST Framework
- ✅ PostgreSQL
- ✅ Celery
- ✅ Redis (как брокер для Celery)
- ✅ JWT
- ✅ CORS и CSRF (по стандартам безопасности)

✅ Функциональность

✅ Аутентификация

✅ Настроить авторизацию по JWT

- ✅ Эндпоинты:
    - ✅ POST /api/token/ — получение access/refresh
    - ✅ POST /api/token/refresh/ — обновление
    - ✅ POST /api/token/verify/ — валидация токена
- ✅ Настроить CORS для доступа с фронта (можно указать localhost:3000)
- ✅ Настроить CSRF для админки (по желанию)

✅ Пользовательская модель. Расширить AbstractUser

- ✅ Добавить поле coins: IntegerField (по умолчанию 0)

✅ Админка. Возможность создавать пользователя

- ✅ Возможность создавать награду (см. ниже)

✅ API: Получение информации о себе. GET /api/profile/

- ✅ Только для авторизованных пользователей
- ✅ Ответ: username, email, coins

✅ Модель ScheduledReward. Поля:

- ✅ user (ForeignKey)
- ✅ amount (целое число)
- ✅ execute_at (дата/время)

✅ Celery: обработка ScheduledReward

✅ Настроить Celery и Redis

- ✅ При создании объекта ScheduledReward → планируется задача
- ✅ В execute_at:
    - ✅ начисляется coins пользователю
    - ✅ создаётся запись в RewardLog

✅ Модель RewardLog. Поля:

- ✅ user
- ✅ amount
- ✅ given_at

✅ API: Список наград. GET /api/rewards/

- ✅ Возвращает список всех выданных наград пользователю

✅ (Дополнительно) POST /api/rewards/request/

✅ Пользователь может сам запросить награду

- ✅ Ограничение: только 1 раз в сутки
- ✅ При успешном запросе создаётся ScheduledReward, которая выполнится через 5 минут

✅ Требования к выполнению

- ✅ Docker (или docker-compose)
- ✅ Команда запуска + миграции описаны в README
- ✅ Swagger
