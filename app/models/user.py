# models/user.py
from app.app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}  # Защита от дублирования в метаданных

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserRepo:
    def get_by_username(self, username):
        return db.session.scalar(db.select(User).filter_by(username=username))

    def add(self, username, password):
        # Защита от повторной регистрации существующего пользователя
        if self.get_by_username(username):
            return None

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
