import sys
from pathlib import Path
import pytest
from flask import Flask

# Корректно выставляем корень проекта в пути поиска модулей
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.app import db  # Импортируем db напрямую из нашей центральной точки
from app.controllers.books_controller import bp as books_bp
from app.controllers.auth_controller import bp as auth_bp
from app.controllers.equipment_controller import bp as equipment_bp  # ДОБАВЛЕНО ИМПОРТ


@pytest.fixture()
def app():
    # Строим абсолютный путь к шаблонам
    templates_dir = str(ROOT / "app" / "views")
    flask_app = Flask(__name__, template_folder=templates_dir)

    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # База в оперативной памяти
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "LOGIN_DISABLED": True,  # Отключает проверку авторизации для упрощения тестов
        "SECRET_KEY": "test_secret_key"
    })

    db.init_app(flask_app)

    # Регистрируем ВСЕ блюпринты приложения
    flask_app.register_blueprint(books_bp)
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(equipment_bp)  # ДОБАВЛЕНО РЕГИСТРАЦИЮ

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    # Теперь app корректно подхватывает фикстуру выше
    return app.test_client()
