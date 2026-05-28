from flask import Blueprint, request, render_template, redirect, url_for, flash  # ИЗМЕНЕНИЕ: Добавлен flash
from app.models.repo import BookRepo
from app.models.equipment import Equipment  # ИЗМЕНЕНИЕ: Импортируем модель оборудования для селекта
from app.app import db  # ИЗМЕНЕНИЕ: Импортируем db для выполнения SQL-запросов
from flask_login import login_required

bp = Blueprint("books", __name__, url_prefix="/books")
repo = BookRepo()


@bp.get("/")
@login_required
def list_books():
    # ИЗМЕНЕНИЕ: Перехватываем поисковую строку из URL параметров
    search_query = request.args.get("search", "").strip()

    # ИЗМЕНЕНИЕ: Передаем запрос в репозиторий для фильтрации результатов
    books = repo.all(search_query=search_query)

    # ИЗМЕНЕНИЕ: Передаем на фронтенд только то оборудование, которое есть в наличии (> 0)
    available_equipment = db.session.scalars(
        db.select(Equipment).filter(Equipment.quantity > 0)
    ).all()

    # ИЗМЕНЕНИЕ: Добавлен аргумент search_query=search_query для сохранения текста в инпуте фронтенда
    return render_template(
        "books/list.html",
        books=books,
        equipment_list=available_equipment,
        search_query=search_query
    )


@bp.post("/")
@login_required
def create_book():
    mer = request.form.get("mer")
    dater = request.form.get("dater")
    proved = request.form.get("proved")

    # ИЗМЕНЕНИЕ: Принимаем ID оборудования и количество из формы
    equipment_id = request.form.get("equipment_id")
    amount = request.form.get("amount", 0)

    # Конвертируем в нужные типы данных
    eq_id = int(equipment_id) if equipment_id else None
    amount_to_spend = int(amount) if amount else 0

    # Передаем параметры в репозиторий и проверяем результат
    result = repo.add(mer, dater, proved, eq_id, amount_to_spend)

    if result == "not_enough_stock":
        flash("Ошибка: На складе нет такого количества выбранного оборудования!", "danger")
    elif result:
        flash("Мероприятие успешно добавлено, оборудование списано!", "success")

    return redirect(url_for("books.list_books"))


@bp.post("/update_book")
@login_required
def update_book():
    book_id_raw = request.form.get("id")
    mer = request.form.get("new_mer")
    dater = request.form.get("new_dater")
    proved = request.form.get("new_proved")

    # Проверяем, что ID вообще передали, и конвертируем его в int
    if book_id_raw and book_id_raw.strip():
        book_id = int(book_id_raw)

        # Вызываем обновленный метод репозитория
        result = repo.update(book_id, mer, dater, proved)

        if result:
            flash(f"Мероприятие №{book_id} успешно изменено!", "success")
        else:
            flash(f"Ошибка: Мероприятие с ID {book_id} не найдено.", "danger")
    else:
        flash("Ошибка: Не указан ID записи для изменения!", "danger")

    return redirect(url_for("books.list_books"))


@bp.post("/<int:book_id>/delete")
@login_required  # ИЗМЕНЕНИЕ: Добавлена защита авторизацией
def delete_book(book_id):
    # ИЗМЕНЕНИЕ: Вызов нашего нового метода repo.delete автоматически вернет технику на склад
    result = repo.delete(book_id)

    if result:
        flash("Мероприятие удалено, оборудование возвращено на склад!", "success")
    else:
        flash("Ошибка при удалении мероприятия.", "danger")

    return redirect(url_for("books.list_books"))
