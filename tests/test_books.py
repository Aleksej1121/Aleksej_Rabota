# tests/test_books.py
import pytest
from app.models.book import Book
from app.models.equipment import Equipment
from app.app import db
@pytest.fixture()

def setup_data(app):
    """Фикстура для наполнения тестовой БД базовыми данными"""
    with app.app_context():
        eq1 = Equipment(name="Проектор", type="Техника", status="В наличии", quantity=10)
        eq2 = Equipment(name="Стул", type="Мебель", status="В наличии", quantity=5)
        db.session.add_all([eq1, eq2])
        b1 = Book(mer="Выпускной", dater="25.05.2026", proved="Актовый зал")
        db.session.add(b1)
        db.session.commit()

def test_list_books_page(client, setup_data):
    """Проверка, что страница открывается и отображает существующие записи"""
    response = client.get("/books/")
    assert response.status_code == 200
    assert "ШКОЛЬНЫЕ МЕРОПРИЯТИЯ" in response.data.decode("utf-8")
    assert "Выпускной" in response.data.decode("utf-8")

def test_search_books(client, setup_data):
    """Проверка работы поискового фильтра"""
    response = client.get("/books/?search=Выпускной")
    assert "Выпускной" in response.data.decode("utf-8")
    response_empty = client.get("/books/?search=Несуществующее")
    assert "Выпускной" not in response_empty.data.decode("utf-8")

def test_create_book_without_equipment(client):
    """Добавление мероприятия без привязки оборудования"""
    data = {"mer": "Олимпиада", "dater": "12.10.2026", "proved": "Кабинет 12"}
    response = client.post("/books/", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert "Олимпиада" in response.data.decode("utf-8")

def test_create_book_with_equipment_success(client, setup_data, app):
    """Успешное списание оборудования при создании мероприятия"""
    data = {
        "mer": "Концерт",
        "dater": "30.12.2026",
        "proved": "Сцена",
        "equipment_id": "1",  # ID Проектора
        "amount": "4"  # Списываем 4 штуки из 10
    }
    response = client.post("/books/", data=data, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        equipment = db.session.get(Equipment, 1)
        assert equipment.quantity == 6

def test_create_book_not_enough_stock(client, setup_data, app):
    """Попытка списать больше оборудования, чем есть на складе"""
    data = {
        "mer": "Собрание",
        "dater": "01.09.2026",
        "proved": "Зал",
        "equipment_id": "2",  # ID Стула (всего 5 штук)
        "amount": "10"  # Запрашиваем 10
    }
    response = client.post("/books/", data=data, follow_redirects=True)
    assert "Ошибка" in response.data.decode("utf-8")

def test_update_book_partial(client, setup_data, app):
    """Частичное обновление только указанных столбцов мероприятия"""
    data = {
        "id": "1",
        "new_mer": "Супер Выпускной",
        "new_dater": "",  # оставляем пустым
        "new_proved": ""  # оставляем пустым
    }
    client.post("/books/update_book", data=data)
    with app.app_context():
        book = db.session.get(Book, 1)
        assert book.mer == "Супер Выпускной"
        assert book.dater == "25.05.2026"  # Убеждаемся, что дата не затёрлась пустым полем

def test_delete_book_and_return_equipment(client, setup_data, app):
    """Удаление мероприятия и автоматический возврат техники на склад"""
    client.post("/books/", data={"mer": "КВН", "dater": "10.11", "proved": "Зал", "equipment_id": "2", "amount": "3"})
    with app.app_context():
        assert db.session.get(Equipment, 2).quantity == 2  # Осталось 5 - 3 = 2
    client.post("/books/2/delete")
    with app.app_context():
        assert db.session.get(Equipment, 2).quantity == 5


def test_create_book_negative_amount_error(client, setup_data, app):
    """Попытка списать отрицательное количество оборудования (-5 штук)"""
    data = {
        "mer": "Спортивный хакатон",
        "dater": "15.06.2026",
        "proved": "Спортзал",
        "equipment_id": "1",  # ID Проектора
        "amount": "-5"  # Отрицательное число
    }
    # Отправляем запрос
    response = client.post("/books/", data=data, follow_redirects=True)

    # Проверяем, что количество на складе НЕ увеличилось и осталось равным 10
    with app.app_context():
        equipment = db.session.get(Equipment, 1)
        assert equipment.quantity == 10


def test_equipment_status_changes_to_out_of_stock(client, setup_data, app):
    """Проверка автоматической смены статуса оборудования на 'Нет в наличии' при нулевом остатке"""
    data = {
        "mer": "Большой концерт",
        "dater": "20.06.2026",
        "proved": "Актовый зал",
        "equipment_id": "2",  # ID Стула
        "amount": "5"  # Забираем все 5 штук из 5 доступных
    }
    client.post("/books/", data=data, follow_redirects=True)

    # Проверяем, изменился ли статус в базе данных
    with app.app_context():
        equipment = db.session.get(Equipment, 2)
        assert equipment.quantity == 0
        assert equipment.status == "Нет в наличии"


def test_update_book_missing_id_flash_message(client):
    """Попытка отправить форму изменения мероприятия без указания ID записи"""
    data = {
        "id": "   ",  # Передаем пробелы вместо реального ID
        "new_mer": "Новое название",
        "new_dater": "11.11.2026",
        "new_proved": "Класс"
    }
    response = client.post("/books/update_book", data=data, follow_redirects=True)

    assert response.status_code == 200
    # Проверяем, что сработало наше flash-уведомление из books_controller.py
    assert "Не указан ID записи для изменения!" in response.data.decode("utf-8")
