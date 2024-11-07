from flask import Flask,render_template,render_template_string,request,jsonify,send_file,make_response,redirect
app = Flask(__name__)

import database
import pyodbc
import io
from datetime import datetime, timedelta


@app.route('/', methods=['GET', 'POST'])
def home():

    redirect_response = identificarUser('USER')
    if redirect_response:
        return redirect_response
    
    if request.method == 'POST':

        req = request.get_json()
        cookies = request.cookies
        user = cookies.get('idUsuario')
        database.insertIntoRefeicaoAgendada(user,req)

        return 'sucesso'
    #info = database.selectNumberOfClass()
    return render_template('home2.html')

@app.route('/imagem/<int:id>')
def get_image(id):
    img_data = database.getImgCardapio(id) # Obter os dados da imagem do banco
    if img_data:
        return send_file(io.BytesIO(img_data), mimetype='image/jpeg')
    return "Imagem não encontrada", 404

@app.route('/login', methods=['GET','POST'])
def login():
    
    redirect_response = identificarUser(None)
    if redirect_response:
        return redirect_response
    
    if request.method == 'POST':
        req = request.get_json()
        resposta = database.tryLogin(req)
        if resposta != False:
            if resposta[2] == req['cpf'] and resposta[5] == req['senha']:

                res = make_response(jsonify({'value': True, 'tipoAcesso': resposta[6]}))

                expires = datetime.now() + timedelta(days=1)
                res.set_cookie("idUsuario",resposta[0], expires=expires)
                res.set_cookie("nome",resposta[1], expires=expires)
                res.set_cookie("cpf",resposta[2], expires=expires)
                res.set_cookie("email",resposta[3], expires=expires)
                res.set_cookie("celular",resposta[4], expires=expires)
                res.set_cookie("tipoAcesso",resposta[6], expires=expires)

                print('acesso permitido')
                
                return res
            
            print('acesso negado 1')
            return jsonify({'value': False})
                
        else:
            print('acesso negado 2')
            return jsonify({'value': False})
        
    return render_template('login.html')

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    
    redirect_response = identificarUser(None)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        req = request.get_json()
        database.insertUser(req)

        return jsonify({'value': True})

    return render_template('cadastro.html')



@app.route('/identificar_user')
def identificar_user():
    cooki = request.cookies
    tipoAcesso = cooki.get('tipoAcesso')
    print(tipoAcesso)
    return cooki


def identificarUser(user):
    cooki = request.cookies
    tipoAcesso = cooki.get('tipoAcesso')
    print(tipoAcesso, user)
    
    print(user == tipoAcesso)
    if user == tipoAcesso:
        return None
    elif user != tipoAcesso and tipoAcesso == 'ADMIN':
        return redirect('/relatorio')
    elif user != tipoAcesso and tipoAcesso != 'ADMIN' and tipoAcesso:
        return redirect('/')
    else:
        return redirect('/login')
    

@app.route('/encerrar_sessao')
def encerrar_sessao():
    print('encerar')
    resposta = make_response(redirect('/'))
    resposta.set_cookie("idUsuario", '', expires=0)
    resposta.set_cookie("nome", '', expires=0)
    resposta.set_cookie("cpf", '', expires=0)
    resposta.set_cookie("email", '', expires=0)
    resposta.set_cookie("celular", '', expires=0)
    resposta.set_cookie("tipoAcesso", '', expires=0)
    return resposta

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/getInfoAboutUser')
def getInfoAboutUser():
    cookies = request.cookies
    idUsuario = cookies.get('idUsuario')
    info = database.selectUser(idUsuario)
    return info

@app.route('/relatorio')
def relatorio():
    
    redirect_response = identificarUser('ADMIN')
    if redirect_response:
        return redirect_response

    return render_template('relatorio.html')

@app.route('/getRelatorio')
def getRelatorio():
    relatorios = database.getRefeicao_agendada()
    return relatorios


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

@app.route('/registro_de_alunos-00')
def registro_de_alunos():
    return render_template('listAlunos.html')

# @app.route('/salvarChatBot', methods=['GET', 'POST'])
# def salvarChatBot():
#     if request.method == 'POST':
#         req = request.get_json()
#         print(req)

#         return jsonify({'value':True})
    
#     return jsonify({'value':True})

@app.route('/rotaSelectGerarRefeicao')
def rotaSelectGerarRefeicao():
    # verificar de o user já salvou uma vez

    info = database.selectGerarRefeicao()
    if info:
        return info
    else:
        return []
    
@app.route('/salvar-notificacao', methods=['GET', 'POST'])
def salvarNotificacao():
    if request.method == 'POST':
        req = request.get_json()
        database.insertNotificacao(req['text'])
        return jsonify({'value':True})

    return jsonify({'value':False})

@app.route('/pega-notificacao')
def pegaNotificacao():
    notificacao = database.selectNotificacao()

    return jsonify({'notificacao':notificacao, 'nomeUser':'Sidney'})


app.run(debug=True)