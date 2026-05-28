from app.models.book import db, Book
from app.models.equipment import Equipment  # ИЗМЕНЕНИЕ: Импортируем модель оборудования


class BookRepo:
    # ИЗМЕНЕНИЕ: Метод теперь принимает строку поиска и фильтрует данные по названию или месту
    def all(self, search_query=None):
        if not search_query:
            return Book.query.all()

        # Ищем совпадения. Метод .contains() работает аналогично оператору LIKE в SQL
        return Book.query.filter(
            (Book.mer.contains(search_query)) |
            (Book.proved.contains(search_query))
        ).all()

    # ИЗМЕНЕНИЕ: Метод теперь принимает ID оборудования и количество для списания
    def add(self, mer, dater, proved, equipment_id=None, amount_to_spend=0):
        if not mer or not dater or not proved:
            return None

        # Если оборудование выбрано и указано количество больше 0
        if equipment_id and amount_to_spend > 0:
            equipment = db.session.get(Equipment, equipment_id)

            if equipment:
                # Проверяем, хватает ли запасов на складе
                if equipment.quantity < amount_to_spend:
                    return "not_enough_stock"

                # Списываем количество со склада
                equipment.quantity -= amount_to_spend

                # Если всё разобрали, меняем текстовый статус
                if equipment.quantity == 0:
                    equipment.status = "Нет в наличии"
        else:
            amount_to_spend = 0

        # Создаем запись мероприятия с привязанным количеством оборудования
        new_book = Book(
            mer=mer,
            dater=dater,
            proved=proved,
            equipment_id=equipment_id,
            spent_quantity=amount_to_spend
        )
        db.session.add(new_book)
        db.session.commit()
        return new_book

    # ИЗМЕНЕНИЕ: Теперь обновляются только переданные текстовые поля (название, дата, место)
    def update(self, book_id, mer=None, dater=None, proved=None):
        book = db.session.get(Book, book_id)
        if book:
            # Обновляем название, только если оно заполнено в форме
            if mer and mer.strip():
                book.mer = mer

            # Обновляем дату, только если она заполнено в форме
            if dater and dater.strip():
                book.dater = dater

            # Обновляем место проведения, только если оно заполнено в форме
            if proved and proved.strip():
                book.proved = proved

            db.session.commit()
            return True
        return False

    # ИЗМЕНЕНИЕ: Метод теперь возвращает технику на склад перед удалением мероприятия
    def delete(self, book_id):
        book = db.session.get(Book, book_id)
        if book:
            # Если у мероприятия было списанное оборудование — возвращаем его остаток на склад
            if book.equipment_id and book.spent_quantity > 0:
                equipment = db.session.get(Equipment, book.equipment_id)

                if equipment:
                    # Математический возврат количества на склад
                    equipment.quantity += book.spent_quantity

                    # Восстанавливаем статус, если он был "Нет в наличии"
                    if equipment.status == "Нет в наличии" and equipment.quantity > 0:
                        equipment.status = "В наличии"

            db.session.delete(book)
            db.session.commit()
            return True
        return False
