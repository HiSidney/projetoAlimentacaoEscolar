from flask import Flask,render_template,render_template_string,request,jsonify,send_file
app = Flask(__name__)

import pandas as pd
import database
import pyodbc
import io


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        req = request.get_json()
        database.insertIntoRefeicaoAgendada(req)

        return 'sucesso'
    #info = database.selectNumberOfClass()
    return render_template('home.html')

@app.route('/imagem/<int:id>')
def get_image(id):
    img_data = database.getImgCardapio(id) # Obter os dados da imagem do banco
    if img_data:
        return send_file(io.BytesIO(img_data), mimetype='image/jpeg')
    return "Imagem não encontrada", 404

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html')

@app.route('/atualizacaoCardapio', methods=['GET', 'POST'])
def atualizacaoCardapio():
    if request.method == 'POST':

        req = request.get_json()
        print(req)
        database.insertIntoGerarAgenda(req['date'], req['manha'], req['almoco'], req['tarde'])

        return 'Sucesso'
    
    return render_template('atualizacaoCardapio.html')

@app.route('/uploudImgCardapio', methods=['POST'])
def uploudImgCardapio():
    print("Requisição recebida")
 # Verifica se o arquivo está presente na requisição
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    # Verifica se algum arquivo foi selecionado
    if file.filename == '':
        return 'No selected file', 400

    # Lê o arquivo como binário
    file_content = file.read()  # Conteúdo do arquivo

    # Obtém as datas do request
    data_inicial = request.form.get('date1')
    data_final = request.form.get('date2')

    # Conexão com o SQL Server
    server = 'SERVIDORPROF\SQLEXPRESS'
    database = 'sesialimentacao'
    usuario = 'likebibi'
    senha='four123'
    cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};uid={usuario};pwd={senha}')
    cursor = cnxn.cursor()

    # Insere o arquivo e as datas no banco
    cursor.execute(
        "INSERT INTO cardapio (imagem, data_inicial, data_final) VALUES (?, ?, ?)",
        (file_content, data_inicial, data_final)  # Altere id_imagem conforme necessário
    )
    cnxn.commit()
    cursor.close()
    cnxn.close()

    return 'Arquivo e dados enviados com sucesso', 200

@app.route('/calendario')
def calendario():
    return render_template('calendario.html')

@app.route('/registrarDesperdicio', methods=['POST', 'GET'])
def registrarDesperdicio():
    if request.method == 'POST':
        req = request.get_json()
        database.insertIntoDesperdicio(req['waste'], req['date'])
        return jsonify({'value':True})
    return render_template("registrarDesperdicio.html")

@app.route('/registro_de_alunos-00')
def registro_de_alunos():
    return render_template('listAlunos.html')

@app.route('/salvarChatBot', methods=['GET', 'POST'])
def salvarChatBot():
    if request.method == 'POST':
        req = request.get_json()
        print(req)

        return jsonify({'value':True})
    
    return jsonify({'value':True})

app.run(debug=True, host='0.0.0.0')