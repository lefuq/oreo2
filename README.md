# oreo2

REST Api адресной книги (версия 2).  
Используемый стек технологий: Python 3.9, FastApi

В приложении реализовано 3 сущности: пользователь, телефон, электронный адрес.  
Эндпоинт пользователей (Abonent): localhost:8000/abonents/  
Эндпоинт телефонов (Phone): localhost:8000/phones/  
Эндпоинт электронных адресов (Mail): localhost:8000/mails/  

Для общих эндпоинтов реализованы методы получения данных через HTTP POST, создания данных - HTTP PUT.  
Также, для метода получения реализована сортировка по всем полям моделей через параметр "ordering". Дефолтная пагинация настроена на 10 записей, меняется параметром "opp".  
Для получения конкертного экземпляра сущности после основной ссылки эндпоинта прописать id объекта (прим.: localhost:8000/mails/1/)  
Для эндпоинтов конкретных экземпляров сущностей реализованы методы получения данных через HTTP POST, изменения данных - HTTP PATCH, удаления данных - HTTP DELETE.  
При создании пользователя есть возможность создать привязанные к нему объекты телефона и почтового адреса путем передачи в теле запроса дополнительных данных:
- "phone": {"type": "Городской/Мобильный", "number": "+0 000 000 0000"}
- "mail": {"type": "Рабочая/Личная", "address": "a@bk.com"}  

*примечание: все параметры при создании объектов в теле запроса передаются в "сыром" формате (не через формы):  
{"name": "Иванов Иван",
"photo": "user_profile_photos/blank_photo.jpg",
"sex": "Мужчина",
"birth": "1990-01-01",
"live": "Красноярск, Мира, 1, 1",
"phone": {
    "type": "Городской",
    "number": "+7 391 200 0000"},
"mail": {
    "type": "Рабочая",
    "address":"yolo@swag.com"}
    }*

Для методов создания и изменения реализована запись логов в файл (преднастроенный файл CUlogs.log хранится в adbk/logs/).  
Для методов создания и изменения также настроена валидация (описана в моделях в adbk/models.py).  
Фотографии пользователей хранятся в adbk/user_profile_photos/.  

Первый запуск:
1. Построение образа и запуск: docker-compose up --build;  
2. Запуск миграций и заполнение предподготовленными данными:  
2.1. В новом окне терминала, открытом параллельно работающему с запущенным приложением:  
  -  docker ps (копируем id контейнера oreo2_server);  
  -  docker exec -it [container id] python migration_script.py; <- запуск миграций таблиц в бд  
  -  docker exec -it [container id] python import_script.py; <- запуск импорта данных  
2.2. В docker desktop:  
  -  Переходим в контейнеры/приложения, ищем запущенный oreo2. На контейнере server нажать cli;  
  -  python migration_script.py; <- запуск миграций таблиц в бд  
  -  python import_script.py; <- запуск импорта данных  

Последующие запуски приложения: docker-compose up.