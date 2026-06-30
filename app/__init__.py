from flask import Flask

from app.extensions import db, migrate


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    # Importa os modelos
    from app import models

    # Blueprints
    from app.routes.dashboard import dashboard_bp
    from app.routes.veiculos import veiculos_bp
    from app.routes.agendamentos import agendamentos_bp
    from app.routes.manutencoes import manutencoes_bp
    from app.routes.auth import auth_bp
    from app.routes.agenda import agenda_bp
    from app.routes.calendario import calendario_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(veiculos_bp)
    app.register_blueprint(agendamentos_bp)
    app.register_blueprint(manutencoes_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(agenda_bp)
    app.register_blueprint(calendario_bp)
    
    return app