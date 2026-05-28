from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy  # ИЗМЕНЕНИЕ: Импортируем сам класс SQLAlchemy

app = Flask(__name__, template_folder='views')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SECRET_KEY'] = '12344321'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ИЗМЕНЕНИЕ: Создаем единственный глобальный экземпляр db прямо здесь
db = SQLAlchemy(app)

# ИЗМЕНЕНИЕ: Теперь импортируем ВСЕ модели строго ПОСЛЕ создания db
from app.models.book import Book
from app.models.user import User
from app.models.equipment import Equipment

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Регистрация блюпринтов
from app.controllers.books_controller import bp as books_bp

app.register_blueprint(books_bp)

from app.controllers.equipment_controller import bp as equipment_bp

app.register_blueprint(equipment_bp)

from app.controllers.auth_controller import bp as auth_bp

app.register_blueprint(auth_bp)

# Автоматическая инициализация таблиц и создание пользователя в SQLite
with app.app_context():
    db.create_all()  # Теперь гарантированно создадутся все таблицы без циклической ошибки

    from app.models.user import UserRepo

    repo = UserRepo()
    if not repo.get_by_username('nim'):
        repo.add('nim', 'lol')
        print("Пользователь nim создан!")


@app.route('/')
def index():
    return redirect(url_for('books.list_books'))

#nim lol
