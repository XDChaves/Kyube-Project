import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from db_config import db
from flask_mail import Mail

# Load environment variables
load_dotenv()

mail = Mail()

def create_app():
    app = Flask(__name__)

    # Defina sua chave secreta
    app.secret_key = os.getenv('s_key')

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuração do servidor de e-mail (exemplo usando Gmail)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Usuário de e-mail
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Senha ou App Password

    # Inicializa o Flask-Mail e SQLAlchemy com o app
    mail.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)  #Inicializa o Flask-Migrate com o app e o banco de dados

    # Configuração para upload de imagem de perfil
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Garante que a pasta de upload exista
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Erro ao criar as tabelas: {e}")

    # Import views (after app creation)
    from view import view

    # Register routes from view module
    for route, view_func in view:
        app.add_url_rule(route, view_func.__name__, view_func, methods=["POST", "GET"])
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
