from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, render_template, request, redirect, jsonify, session
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets, string, os, json, requests
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

def get_user_email(username):
    file_path = USERS_DIR / username / "UserInfo.txt"

    if not file_path.exists():
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    return dados.get("email")

# cadastro
# Início
BASE_DIR = Path(__file__).resolve().parent
USERS_DIR = BASE_DIR / "registros"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/entrarCadastro")
def pagina_cadastro():
    return render_template("cadastro.html")

@app.route("/entrarLogin")
def pagina_login():
    return render_template("login.html")

@app.route('/check-username')
def check_username():
    username = request.args.get('username', '').strip()

    if not username:
        return jsonify({"error": "username não informado"}), 400

    caminho = USERS_DIR / username
    existe = caminho.is_dir()

    return jsonify({"exists": existe})

@app.route('/check-email')
def check_email():
    userEmail = request.args.get('userEmail', '').strip()
    otp = ''.join(secrets.choice(string.digits) for _ in range(6))

    if not userEmail:
        return jsonify({"error": "e-mail não informado"}), 400
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Confirme sua identidade"
    msg["From"] = GMAIL_USER
    msg["To"] = userEmail

    texto = f"Seu código de verificação é: {otp}"
    html = f"""
    <html>
      <body>
        <p>Seu código de verificação é: <strong>{otp}</strong></p>
      </body>
    </html>
    """

    msg.attach(MIMEText(texto, "plain"))
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
    session['otp'] = otp

    return "OK"

@app.route('/check-emailConfirmation')
def check_confirmation():    
    confirmation = request.args.get('confirmation', '').strip()
    session['confirmation'] = confirmation
    if not confirmation:
        return jsonify({"error": "sem código de verificação"}), 400
    verify = confirmation == session.get('otp')

    return jsonify({"verify": verify})

@app.route('/cadastrar', methods=['POST'])
def cadastro():
    if session.get('confirmation') == session.get('otp'):
        userName = request.form.get("userName", "").strip()
        userCPF = request.form.get("userCPF", "").strip()
        userEmail = request.form.get("userEmail", "").strip()
        userNumber = request.form.get("userNumber", "").strip()
        USERNAME = request.form.get("username", "").strip()
        PASSWORD = request.form.get("userPassword1", "").strip()

        user_dir = USERS_DIR / USERNAME
        if user_dir.exists():
            return jsonify({"error": "usuário já existe"}), 400
        user_dir.mkdir(parents=True)

        cadastro = {
            "nome": userName,
            "CPF": userCPF,
            "email": userEmail,
            "Number": userNumber,
        }

        with open(user_dir / "UserInfo.txt", 'w', encoding='utf-8') as f:
            json.dump(cadastro, f, ensure_ascii=False, indent=2)

        with open(user_dir / "Senha.txt", 'w', encoding='utf-8') as f:
            f.write(PASSWORD)
        return render_template("AllDone.html")
    else:
        return render_template('cadastro.html')
# Fim

@app.route('/check-loginUsername')
def check_logUsername():
    username = request.args.get("logUsername", "").strip()
    session['username'] = username
    caminho = USERS_DIR / username
    existe = caminho.is_dir()
    if existe:
        with open(caminho / "Senha.txt") as i:
            session['password'] = i.read()
    return jsonify({"existe": existe})

@app.route('/check-loginPassword')
def check_logPassword():
    password = request.args.get("logPassword", "").strip()

    if password == session.get('password'):
        otp = ''.join(secrets.choice(string.digits) for _ in range(6))
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Confirme sua identidade"
        msg["From"] = GMAIL_USER
        msg["To"] = get_user_email(session.get("username"))
         
        texto = f"Seu código de verificação é: {otp}"
        html = f"""
        <html>
            <body>
            <p>Seu código de verificação é: <strong>{otp}</strong></p>
          </body>
        </html>
        """
         
        msg.attach(MIMEText(texto, "plain"))
        msg.attach(MIMEText(html, "html"))
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        session['otp2'] = otp
        return ({"verify": True,
             "email": get_user_email(session.get('username'))})
    else:
        return ({"verify": False})


@app.route('/entrar', methods={'POST'})
def entrar_conta():
    otp = request.form.get("emailConfirmation", "").strip()
    if otp == session.get('otp2'):
        return render_template("home.html")
    else:
        return render_template("login.html")

@app.route("/EntrarLogarContas")
def logar_contas():
    username = session.get('username')

    if not username:
        return jsonify({"error": "usuário não autenticado"}), 401

    redes_dir = USERS_DIR / username / "Redes"

    if not redes_dir.exists():
        redes_dir.mkdir(parents=True)
    return render_template("loginContas.html")

@app.route("/EntrarFazerPostagem")
def fazerPost():
    return render_template("postar.html")

@app.route('/logarInstagram', methods=['POST'])
def logar_instagram():
    dados = request.json

    instagram_username = dados.get('InstagramUsername', '').strip()
    instagram_password = dados.get('InstagramPassword', '').strip()

    if not instagram_username or not instagram_password:
        return jsonify({"error": "usuário e senha são obrigatórios"}), 400

    username = session['username']
    user_dir = USERS_DIR / username / "Redes"
    with open(user_dir / "InstagramData.txt", 'w', encoding='utf-8') as f:
        f.write[
            "InstagramUser": instagram_username,
            "InstagramPassword": instagram_password
        ]

    return jsonify({"ok": True}) 

@app.route('/logarFacebook', methods=['POST'])
def logar_facebook():
    username = session.get('username')
    if not username:
        return jsonify({"error": "usuário não autenticado"}), 401

    dados = request.json
    facebook_username = dados.get('facebookUsername', '').strip()
    facebook_password = dados.get('facebookPassword', '').strip()

    if not facebook_username or not facebook_password:
        return jsonify({"error": "usuário e senha do Facebook são obrigatórios"}), 400

    username = session['username']
    user_dir = USERS_DIR / username / "Redes"
    with open(user_dir / "FacebookData.txt", 'w', encoding='utf-8') as f:
        f.write[
            "FacebookUser": facebook_username,
            "FacebookPassword": facebook_password
        ]
    return jsonify({"ok": True})


@app.route('/logarLinkedIn', methods=['POST'])
def logar_linkedin():
    username = session.get('username')
    if not username:
        return jsonify({"error": "usuário não autenticado"}), 401

    dados = request.json
    linkedin_username = dados.get('linkedInUsername', '').strip()
    linkedin_password = dados.get('linkedInPassword', '').strip()

    if not linkedin_username or not linkedin_password:
        return jsonify({"error": "usuário e senha do LinkedIn são obrigatórios"}), 400

    username = session['username']
    user_dir = USERS_DIR / username / "Redes"
    with open(user_dir / "LinkedInData.txt", 'w', encoding='utf-8') as f:
        f.write[
            "LinkedInUser": linkedin_username,
            "LinkedInPassword": linkedin_password
        ]
    return jsonify({"ok": True})

@app.route("/FazerPostagem", methods=['POST'])
def postar():
    Legenda = request.form.get("postLegenda", "").strip()
    img = request.form.get("postInage", "").strip()
    InstagramCheck = request.form.get("Instagram", "").strip()
    FacebookCheck = request.form.get("Facebook", "").strip()
    LinkedInCheck = request.form.get("LinkedIn", "").strip()
    API_KEY = os.environ.get("Ay_API_KEY")
    URL_API = "https://app.ayrshare.com/api/post"
    if InstagramCheck == "on":
        dados_do_post = {
            "post": Legenda,
            "platforms": ["instagram"],
            "mediaUrls": img
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        print("Enviando postagem para o Instagram...")

        resposta = requests.post(URL_API, json=dados_do_post, headers=headers)

        if resposta.status_code == 200:
            print(f"O post de: {session.get("username")}O post já está disponível no Instagram.")
            print(resposta.json())
        else:
            print(f"Ops, algo deu errado. Código do erro: {resposta.status_code}")
            print(f"Detalhes do erro: {resposta.text}")
    if FacebookCheck == "on":
        dados_do_post = {
            "post": Legenda,
            "platforms": ["facebook"],
            "mediaUrls": img
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        print("Enviando postagem para o Facebook...")
        resposta = requests.post(URL_API, json=dados_do_post, headers=headers)

        if resposta.status_code == 200:
            print(f"O post de: {session.get("username")}O post já está disponível no Instagram.")
            print(resposta.json())
        else:
            print(f"Ops, algo deu errado. Código do erro: {resposta.status_code}")
            print(f"Detalhes do erro: {resposta.text}")
    if LinkedInCheck == "on":
        dados_do_post = {
            "post": (
                Legenda
            ),
            "platforms": ["linkedin"],
            "mediaUrls": [
                img
            ],
        }
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

        resposta = requests.post(URL_API, json=dados_do_post, headers=headers)

        if resposta.status_code == 200:
            print(f"O post de: {session.get("username")}O post já está disponível no Instagram.")
            print(resposta.json())
        else:
            print(f"Erro encontrado. Código: {resposta.status_code}")
            print(f"Detalhes: {resposta.text}")
    return render_template("postar.html")

if __name__ == "__main__":
    app.run(debug=True)
