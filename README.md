# Aleksej_Rabota

![alt text](https://private-user-images.githubusercontent.com/288481176/599173144-62fa6d04-f0ed-4070-ac05-03f39893930b.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Nzk5MzcwMjksIm5iZiI6MTc3OTkzNjcyOSwicGF0aCI6Ii8yODg0ODExNzYvNTk5MTczMTQ0LTYyZmE2ZDA0LWYwZWQtNDA3MC1hYzA1LTAzZjM5ODkzOTMwYi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNTI4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDUyOFQwMjUyMDlaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT03YmE5NjViY2E2YjA1MmQwNzJmNWYxZjE2MjI0ZGFlZTIwYzEyZmY5NWRjOTk4N2UxN2NiNWVhMjIyYTA5YzgyJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.Q3tNLKU2oVBFHSTwSBhXe8HFVLxqZUbX1mMDjOi3-9Y)

                                                  Мои достижения без пар

Репозиторий, содержащий приложение об учёте мороприятий и оборудования, созданное на Flask



**Приложение позволяет:**
- Просматривать полную информацию о мероприятиях и оборудовании
- Фильтровать и сортировать мероприятия и оборудование
- Искать нужные мероприятия
- Добавлять, изменять и удалять мероприятия (только для авторизованных пользователей)
- Добавлять, изменять и удалять оборудование (только для авторизованных пользователей)



**Особенности:**
- База данных создана на SQLlite
- При регистрации, пароль хэшируется и недоступен для просмотра, так как его нельзя расшифровать
- Удобная страница создания мероприятий. Позволяет вводить название, дату и место проведение мероприятий.
- Имеется подсчёт количества оборудования.
- Фильтрация происходит по названию и месту проведения.
- Быстрый поиск мероприятий по названию.
- Полный набор тестов на pytest для проверки функционала. Тесты проходят в базе данных SQLite, которая повторяет основную базу данных, но никак не связана с нею и удаляется после окончания тестирования

**Структура проекта:**
- controllers/ (Обработка запросов и взаимодействие между моделью и представлением)
- models/ (Данные и логика приложения)
- views/ (Визуальное отображение данных)
- static/ (Дизайн элементов для views)

**Установка**
1. Перейдите в любой удобный каталог (cd C:\Users\USER\Documents), клонируйте репозиторий и перейдите к нему и установите библиотеки
- `pip install flask pytest flask-sqlalchemy pymysql cryptography flask-login werkzeug`

2. Запустите приложение
- `run.py`
- При первом запуске программы app.py автоматически создаст базу данных и внесет пользователя с именем nim и паролем lol

3. Перейдите по ссылке (http://127.0.0.1:5000)

**Тестирование**
1. Перейдите в корень проекта
2. Запустите тесты
- `pytest -v`
Тесты используют SQLite.
