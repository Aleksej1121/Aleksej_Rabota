from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.equipment import EquipmentRepo  # Импортируем из нового файла моделей

# ИЗМЕНЕНИЕ: Перенесли префикс '/equipment' сюда, чтобы роуты работали корректно без дублирования
bp = Blueprint('equipment', __name__, url_prefix='/equipment')
repo = EquipmentRepo()


# ИЗМЕНЕНИЕ: Путь сокращен до '/', так как префикс уже задан выше
@bp.route('/')
@login_required
def list_equipment():
    items = repo.all()
    return render_template('equipment/list.html', items=items)


# ИЗМЕНЕНИЕ: Путь сокращен до '/create'
@bp.post('/create')
@login_required
def create_equipment():
    name = request.form.get('name')
    eq_type = request.form.get('type')
    description = request.form.get('description')
    status = request.form.get('status')

    # ИЗМЕНЕНИЕ: Получаем количество из новой формы добавления
    quantity_raw = request.form.get('quantity', 0)
    quantity = int(quantity_raw) if quantity_raw else 0

    # ИЗМЕНЕНИЕ: Передаем параметр quantity в репозиторий
    if repo.add(name, eq_type, description, status, quantity):
        flash("Оборудование успешно добавлено!", "success")
    else:
        flash("Ошибка: заполните обязательные поля!", "danger")
    return redirect(url_for('equipment.list_equipment'))


# ИЗМЕНЕНИЕ: Путь сокращен до '/update'
@bp.post('/update')
@login_required
def update_equipment():
    eq_id = request.form.get('id')
    new_name = request.form.get('new_name')
    new_type = request.form.get('new_type')
    new_description = request.form.get('new_description')
    new_status = request.form.get('new_status')

    # ИЗМЕНЕНИЕ: Получаем новое количество из формы редактирования
    new_qty_raw = request.form.get('new_quantity')
    new_quantity = int(new_qty_raw) if new_qty_raw else None

    # ИЗМЕНЕНИЕ: Передаем параметр new_quantity в репозиторий
    if repo.update(eq_id, new_name, new_type, new_description, new_status, new_quantity):
        flash("Данные оборудования обновлены!", "success")
    else:
        flash("Ошибка: оборудование с таким ID не найдено", "danger")
    return redirect(url_for('equipment.list_equipment'))


# ИЗМЕНЕНИЕ: Путь сокращен до '/<int:eq_id>/delete'
@bp.post('/<int:eq_id>/delete')
@login_required
def delete_equipment(eq_id):
    if repo.delete(eq_id):
        flash("Оборудование удалено из базы данных", "success")
    else:
        flash("Ошибка при удалении", "danger")
    return redirect(url_for('equipment.list_equipment'))
