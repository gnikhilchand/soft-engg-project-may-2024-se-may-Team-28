from flasgger import Swagger
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)

    from app.models import user, course, feedback, problem_solving
    from app.routes.courses import courses_bp
    from app.routes.assignment import assignments_bp
    from app.routes.summary import summary_bp
    # from app.routes.notes import notes_bp
    from app.routes.questions import questions_bp
    from app.routes.miduser import mid_user_bp
    from app.routes.superuser import superuser_bp
    from app.routes.user import user_bp
    from app.routes.code_evalution import code_bp
    from app.routes.inforoutes import info

    app.register_blueprint(summary_bp)
    # app.register_blueprint(notes_bp, url_prefix='/api')
    app.register_blueprint(questions_bp)

    app.register_blueprint(courses_bp)
    app.register_blueprint(assignments_bp, url_prefix='/assignments')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(mid_user_bp, url_prefix='/mid_user')
    app.register_blueprint(superuser_bp, url_prefix='/superuser')
    app.register_blueprint(code_bp, url_prefix='/api')
    app.register_blueprint(info)

    from app.routes import auth
    app.register_blueprint(auth.bp)

    return app