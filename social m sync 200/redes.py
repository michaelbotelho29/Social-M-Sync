from flask import Flask, request, jsonify, render_template_string, url_path_as_url, url_for
import os

app = Flask(__name__)

# Configura uma pasta pública dentro do servidor para expor os uploads como links/URLs
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static_uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

HTML_FILE_NAME = "postar.html"

def carregar_html():
    if os.path.exists(HTML_FILE_NAME):
        with open(HTML_FILE_NAME, "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Erro: Arquivo postar.html não encontrado!</h3>"

@app.route('/')
def index():
    return render_template_string(carregar_html())

@app.route('/publicar', methods=['POST'])
def publicar():
    redes_selecionadas = request.form.getlist('redes')
    legenda = request.form.get('legenda', '')
    
    if 'arquivo' not in request.files:
        return jsonify({"status": "erro", "mensagem": "Nenhum arquivo enviado."}), 400
        
    arquivo = request.files['arquivo']
    
    if not redes_selecionadas:
        return jsonify({"status": "erro", "mensagem": "Nenhuma rede marcada."}), 400

    # 1. Salva o arquivo na pasta pública que o servidor web consegue ler
    caminho_arquivo = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    arquivo.save(caminho_arquivo)

    # 2. CONVERSÃO EM URL: Cria o link web local da imagem automaticamente
    # Isso vai virar algo como: http://127.0.0
    url_da_midia = request.host_url + 'static_uploads/' + arquivo.filename

    postados_com_sucesso = []
    falhas = []

    # 3. Executa suas APIs passando a URL gerada e a legenda por parâmetro de linha de comando
    for script_api in redes_selecionadas:
        if os.path.exists(script_api):
            try:
                # O comando envia a URL criada e a legenda de forma direta para o seu script
                comando = f'python "{script_api}" "{url_da_midia}" "{legenda}"'
                
                status_execucao = os.system(comando)
                
                if status_execucao == 0:
                    postados_com_sucesso.append(script_api)
                else:
                    falhas.append(f"{script_api} (Código do erro: {status_execucao})")
                    
            except Exception as e:
                falhas.append(f"{script_api} (Erro: {str(e)})")
        else:
            falhas.append(f"{script_api} (API não encontrada)")

    return jsonify({
        "status": "sucesso",
        "postado_em": postados_com_sucesso,
        "erros": falhas
    })

# Rota para disponibilizar o arquivo como URL na rede
@app.route('/static_uploads/<filename>')
def serve_file(filename):
    from flask import send_from_directory
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    print("SocialMSync - Gerador de URL de Mídia Ativado!")
    app.run(debug=True)
