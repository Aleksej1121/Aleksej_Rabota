# app/models/equipment.py
from app.app import db

class Equipment(db.Model):
    __tablename__ = 'equipment'
    __table_args__ = {'extend_existing': True}  # Защита от дублирования в метаданных

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Название
    type = db.Column(db.String(50), nullable=False)  # Тип
    description = db.Column(db.Text, nullable=True)  # Описание
    status = db.Column(db.String(50), nullable=False)  # Состояние

    # Количество оборудования на складе
    quantity = db.Column(db.Integer, default=0, nullable=False)  # Количество


class EquipmentRepo:
    """Репозиторий для выполнения CRUD-операций с оборудованием"""

    def all(self):
        return db.session.scalars(db.select(Equipment)).all()

    def add(self, name, type, description, status, quantity=0):
        if not name or not type or not status:
            return None
        equipment = Equipment(
            name=name,
            type=type,
            description=description,
            status=status,
            quantity=quantity
        )
        db.session.add(equipment)
        db.session.commit()
        return equipment

    def update(self, eq_id, new_name=None, new_type=None, new_description=None, new_status=None, new_quantity=None):
        equipment = db.session.get(Equipment, eq_id)
        if not equipment:
            return False
        if new_name: equipment.name = new_name
        if new_type: equipment.type = new_type
        if new_description: equipment.description = new_description
        if new_status: equipment.status = new_status

        if new_quantity is not None:
            equipment.quantity = new_quantity

        db.session.commit()
        return True

    def delete(self, eq_id):
        equipment = db.session.get(Equipment, eq_id)
        if not equipment:
            return False
        db.session.delete(equipment)
        db.session.commit()
        return True
