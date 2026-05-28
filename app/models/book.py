# app/models/book.py
from app.app import db  # Импортируем строго ОДИН глобальный db
from sqlalchemy.orm import relationship  # ДОБАВЛЕНО: Импорт для создания связей

class Book(db.Model):
    __tablename__ = 'books'
    __table_args__ = {'extend_existing': True}  # Защита от дублирования в метаданных

    id = db.Column(db.Integer, primary_key=True)

    mer = db.Column(db.String(100), nullable=False)
    dater = db.Column(db.String(100), nullable=False)
    proved = db.Column(db.String(50), nullable=False)

    # Внешний ключ для связи с таблицей оборудования
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=True)

    # Поле для хранения количества списанного оборудования
    spent_quantity = db.Column(db.Integer, default=0, nullable=False)

    # ДОБАВЛЕНО: Связь с моделью Equipment.
    # backref="books" автоматически создаст скрытое свойство .books внутри модели Equipment
    equipment = relationship("Equipment", backref="books")

    def __repr__(self):
        return f'<Book {self.mer}>'
