import uuid
from db_config import db  # Importa a instância `db` do banco de dados
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, password):
        self.id = str(uuid.uuid4())  # Gera um ID único e aleatório
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)  # Hasheia a senha com werkzeug

        # Método para verificar a senha
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Dados(db.Model):
    __tablename__ = 'dados'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), db.ForeignKey('users.id'), nullable=False)  # Relação com o usuário
    imagens = db.Column(db.String(500), nullable=True)
    nome_url = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    descricao = db.Column(db.Text(1000), nullable=True)

    # Relaciona com o usuário
    user = db.relationship("User", backref=db.backref("dados", uselist=False))
