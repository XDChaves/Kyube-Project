import os
from flask import request, render_template, jsonify, redirect, url_for, current_app, session, flash
from flask_mail import Message
from datetime import datetime, timedelta, timezone
import uuid
from sqlalchemy import inspect
from models import User, Dados
from db_config import db
from app import mail, load_dotenv
from functools import wraps
from werkzeug.utils import secure_filename

load_dotenv()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Função para verificar extensão permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cadastrar():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email já cadastrado.'}), 409

        # Gera um token de confirmação
        confirmation_token = str(uuid.uuid4())

        # Armazena os dados temporariamente na sessão, incluindo a senha sem hash
        session['temp_user'] = {
            'name': name,
            'email': email,
            'password': password,  # Senha será hasheada no models.py ao criar User
            'confirmation_token': confirmation_token,
            'token_expiration': (datetime.now(tz=timezone.utc) + timedelta(hours=1)).isoformat()  # Usa timezone-aware now
        }

        # Envia o e-mail de confirmação
        send_confirmation_email(email, confirmation_token)

        flash('Um link de confirmação foi enviado para o seu e-mail.')
        return render_template('index.html')
def send_confirmation_email(email, token):
    confirm_url = url_for('confirm_email', token=token, _external=True)
    name = request.form.get('name')

    # Calcula a hora de expiração
    expiration_time = (datetime.now(tz=timezone.utc) + timedelta(hours=1)).strftime('%H:%M UTC')

    msg = Message(
        subject='Confirmação de Cadastro - kyube',
        sender=(f"Kyube", current_app.config['MAIL_USERNAME']),
        recipients=[email]
    )
    
    # Corpo do e-mail em HTML
    msg.html = (
        f"<p>Olá, {name}! </p>"
        f"<p>Obrigado por se cadastrar no <strong>KYUBE</strong>! Para concluir seu cadastro, "
        f"por favor clique em 'Confirmar Cadastro' logo abaixo para verificar seu endereço de e-mail:</p>"
        f"<p><a href='{confirm_url}'>Confirmar Cadastro</a></p>"
        f"<p><em>Este link expira em 1 hora.</em></p>"
        f"<p>Se você não realizou este cadastro, por favor ignore este e-mail.</p>"
        f"<p>Atenciosamente,<br>"
        f"kyube</p>"
    )
    
    mail.send(msg)
def confirm_email(token):
    temp_user = session.get('temp_user')

    if temp_user and temp_user['confirmation_token'] == token:
        # Verifica se o token está expirado
        token_expiration = datetime.fromisoformat(temp_user['token_expiration']).replace(tzinfo=timezone.utc)
        if token_expiration >= datetime.now(tz=timezone.utc):  #Usa timezone-aware now

            # Cria o usuário com o hashing automático no modelo User
            new_user = User(
                name=temp_user['name'],
                email=temp_user['email'],
                password=temp_user['password']  # Hasheamento ocorre no __init__ do User
            )
            db.session.add(new_user)
            db.session.commit()
            
            # Limpa os dados temporários da sessão
            session.pop('temp_user', None)
            return redirect(url_for('perfil'))

    return jsonify({'error': 'Token inválido ou expirado.'}), 400
def verificar_email():
    email = request.args.get("email")
    # Verifica se o email já está cadastrado
    if User.query.filter_by(email=email).first():
        return jsonify({"exists": True}), 200
    return jsonify({"exists": False}), 200

def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Todos os campo são obrigatórios')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('create'))
        else:
            flash('Email ou senha inválidos')
            return redirect(url_for('login'))

    return render_template('index.html')
def logout():
    # Remove o user_id e o user_name da sessão para deslogar o usuário
    session.pop('user_id', None)
    session.pop('user_name', None)  # Remove o nome do usuário da sessão
    return redirect(url_for('index'))
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # Verifica se o usuário não está logado
            flash("Você precisa estar logado para acessar a página.")  # Define a mensagem
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@login_required
def upload_profile_image():
    if 'profile_image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem selecionada para upload.'}), 400
    
    file = request.files['profile_image']
    if file and allowed_file(file.filename):
        # Obtém o nome do usuário logado da sessão
        user_name = session.get('user_name')
        extension = 'jpg'  # Extensão padrão para o arquivo de imagem
        filename = secure_filename(f"{user_name}.{extension}") # Salva com um nome seguro

        # Define o caminho completo do upload
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        # Verifica se já existe um arquivo e o substitui
        if os.path.exists(filepath):
            os.remove(filepath)  # Remove o arquivo antigo, caso exista
        file.save(filepath)
    
        # Atualiza o banco de dados com o caminho do novo arquivo
        user_id = session.get('user_id')
        user_data = Dados.query.filter_by(user_id=user_id).first()
        
        if user_data:
            user_data.imagens = filename  # Salva apenas o nome do arquivo
        else:
            user_data = Dados(user_id=user_id, imagens=filename, nome_url='', url='', descricao='')
            db.session.add(user_data)
        db.session.commit()
        
        # Retorna a URL da imagem para o frontend
        return jsonify({'success': True, 'image_url': url_for('static', filename=f'uploads/{filename}')})
    else:
        return jsonify({'error': 'Tipo de arquivo não permitido.'}), 400

def index():
    user_name = session.get('user_name')
    user_id = session.get('user_id')

    # Verifica se o usuário possui uma imagem de perfil salva
    user_data = Dados.query.filter_by(user_id=user_id).first()
    user_image = url_for('static', filename='uploads/padraoperfilfoto.png')  # Imagem padrão
    
    if user_data and user_data.imagens:
        user_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user_data.imagens)
        if os.path.exists(user_image_path):
            user_image = url_for('static', filename=f'uploads/{user_data.imagens}')

    return render_template("index.html", user_name=user_name, user_image=user_image)

@login_required
def create():
    user_name = session.get('user_name')
    user_id = session.get('user_id')

    # Verifica se o usuário possui uma imagem de perfil salva
    user_data = Dados.query.filter_by(user_id=user_id).first()
    user_image = url_for('static', filename='uploads/padraoperfilfoto.png')  # Imagem padrão

    if user_data and user_data.imagens:
        user_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(user_data.imagens))
        if os.path.exists(user_image_path):
            user_image = url_for('static', filename=f'uploads/{os.path.basename(user_data.imagens)}')

    return render_template("create.html", user_name=user_name, user_image=user_image)

def salvar_url():
    user_id = session.get('user_id')
    nome_url = request.form.get('nome_url')
    url = request.form.get('url')
    descricao = request.form.get('descrição')

    novo_dado = Dados(
        nome_url=nome_url,
        url=url,
        descricao=descricao,
        user_id=user_id
    )

    db.session.add(novo_dado)
    db.session.commit()

    return redirect(url_for('create'))

@login_required
def perfil():
    user_name = session.get('user_name')
    user_id = session.get('user_id')

    # Buscando dados do usuário, incluindo URLs
    dados_usuario = Dados.query.filter_by(user_id=user_id).all()

    # Verifica se o usuário possui uma imagem de perfil salva
    user_data = Dados.query.filter_by(user_id=user_id).first()
    user_image = url_for('static', filename='uploads/padraoperfilfoto.png')  #Imagem padrão

    if user_data and user_data.imagens:
        user_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user_data.imagens)
        if os.path.exists(user_image_path):
            user_image = url_for('static', filename=f'uploads/{user_data.imagens}')

    # Passando os dados do usuário e URLs para o template
    return render_template("perfil.html", user_name=user_name, user_image=user_image, dados=dados_usuario)


# Função para buscar os dados do usuário
def buscar_dados_usuario(user_id):
    return Dados.query.filter_by(user_id=user_id).all()

def deletar_url(id):
    dado = Dados.query.get(id)
    if dado:
        db.session.delete(dado)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Item deletado com sucesso!'})
    return jsonify({'success': False, 'message': 'Item não encontrado.'})

view = [
    ("/", index),
    ("/cadastrar", cadastrar),  # Rota para cadastrar o usuário
    ("/confirm_email/<token>", confirm_email),  # Rota para confirmação de e-mail
    ("/verificar_email", verificar_email),  # Rota para verificação de e-mail assíncrona
    ("/logar", login),  # Adiciona a rota de login ao view
    ("/perfil", perfil),
    ("/create", create),
    ("/logout", logout),  # Adiciona a rota de logout
    ("/upload_profile_image", upload_profile_image),
    ("/salvar_url", salvar_url),
    ("/deletar_url/<int:id>", deletar_url)
]