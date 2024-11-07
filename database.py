import pyodbc
from datetime import datetime, timedelta

# print(pyodbc.drivers())

server = 'SERVIDORPROF\SQLEXPRESS'
database = 'sesialimentacao'
usuario = 'likebibi'
senha='four123'

cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};uid={usuario};pwd={senha}')
cursor = cnxn.cursor()

def selectNumberOfClass():
    resposta = cursor.execute(f"select count(*) from usuarios where serie = '3AEM'").fetchall()
    resposta = [tuple(row) for row in resposta]
    return resposta

def insertIntoCardapio(img, dataInicial, dataFinal):
    print(dataInicial)
    cursor.execute(
    "INSERT INTO cardapio (imagem, data_inicial, data_final) VALUES (?, ?, ?)",
    (img, dataInicial, dataFinal)
)
    
def insertIntoGerarAgenda(data, habilitar_cafe_manha, habilitar_almoco, habilitar_cafe_tarde):
    
    data_atual = datetime.now()
    data_variavel_dt = datetime.strptime(data, "%Y-%m-%d")

    if data_atual.date() > data_variavel_dt.date():
        print("A data atual é posterior à data da variável.")
        estado = 2
    elif data_atual.date() < data_variavel_dt.date():
        print("A data atual é anterior à data da variável.")
        estado = 0
    else:
        print("A data atual é igual à data da variável.")
        estado = 1
    
    cursor.execute(
        "insert into GERAR_AGENDA(id_data,habilitar_cafe_manha,habilitar_almoco,habilitar_cafe_tarde) VALUES (?, ?, ?, ?)", 
        (data, habilitar_cafe_manha, habilitar_almoco, habilitar_cafe_tarde)
    )
    cursor.commit()

def selectUser(idUsuario):
    resposta = cursor.execute("select * from usuarios where id_usuario = ?", (idUsuario,)).fetchall()
    resposta = [tuple(row) for row in resposta]
    return resposta

def insertIntoRefeicaoAgendada(user,req):
    print(req)
    datatime = datetime.now()
    primeira_segunda = datatime - timedelta(days=datatime.weekday())
    dias_uteis = [primeira_segunda + timedelta(days=i) for i in range(5)]
    dias_uteis = [dia.strftime('%Y-%m-%d') for dia in dias_uteis]
    id_usuario = user
    
    # Mapear os dias da semana para as chaves
    dias_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']

    # Criar um novo dicionário com as datas substituindo as chaves
    novo_dic = {}
    for i, dia in enumerate(dias_semana):
        novo_dic[dias_uteis[i]] = req[dia]
    
    for dias,periodos in novo_dic.items():
        # print(dias, periodos)


        resposta = cursor.execute("select max(id_agendamento) from REFEICAO_AGENDADA").fetchall()
        resposta = [tuple(row) for row in resposta]
        
        if resposta[0][0] == None:
            id_agendamento = 1
        else:
            id_agendamento = resposta[0][0] + 1

        # print(f"insert into REFEICAO_AGENDADA(id_agendamento,id_data,id_usuario,cafe_manha,almoco,cafe_tarde,log_data_hora) VALUES ({id_agendamento},{dias},{id_usuario}, {periodos[0]}, {periodos[1]}, {periodos[2]}, {datatime})\n")

        # cursor.execute(
        #     "insert into REFEICAO_AGENDADA(id_agendamento,id_data,id_usuario,cafe_manha,almoco,cafe_tarde,log_data_hora) VALUES (?, ?, ?, ?, ?, ?, ?)",
        #     (id_agendamento,dias,id_usuario, periodos[0], periodos[1], periodos[2], datatime)
        # )
        # cursor.commit()


def insertNotificacao(text):
    # Obtendo a data e hora atual
    agora = datetime.now()

    # Formatando para o formato SQL Server
    data_sql = agora.strftime('%Y-%m-%d %H:%M:%S')

    print(data_sql)
    cursor.execute(
        "insert into NOTIFICACOES(id_notificacao,data_hora,texto) values(?, ?, ?)", 
        (2,data_sql,text)
    )
    cursor.commit()

def selectNotificacao():
    # cursor = cnxn.cursor()
    resposta = cursor.execute("select top(1) * from NOTIFICACOES ORDER BY data_hora DESC;").fetchall()
    # cursor.close()
    resposta = [tuple(row) for row in resposta]
    return resposta[0]


# def getImgCardapio(idImg):
#     resposta = cursor.execute("SELECT imagem FROM cardapio WHERE id_imagem = ?", (idImg,)).fetchone()
#     return resposta[0] if resposta and resposta[0] is not None else None


def insertUser(req):
    cursor.execute(
        "insert into usuarios(id_usuario,nome,cpf,email,senha,celular,id_codigo) values VALUES (?,?,?,?,?,?,?)", 
        (req['rm'], req['nome'], req['cpf'], req['email'], req['senha'], req['telefone'],req['tipo_acesso'])
    )
    cursor.commit()

def tryLogin(req):
    return ['2','Sidney Admin','111.111.111-11','sid@gmail.com','(19)99999-9999','123', 'ADMIN']
    return ['2','Sidney Admin','111.111.111-11','sid@gmail.com','(19)99999-9999','123', 'USER']

    resposta = cursor.execute("select * from usuarios where cpf = ?", (req['cpf'])).fetchall()
    resposta = [tuple(row) for row in resposta]
    print(resposta[0])
    if resposta[0][0] == req['senha']:
        return resposta[0]
    else:
        return False

def getRefeicao_agendada():
    return {
        '07:50': {
            'vao comer': [10,10,10,11,6],
            'nao vao comer': [8,9,10,9,13],
            'nao responderam': [12,12,9,11,8],
        },
    }


def getImgCardapio(idImg):
    # Pegar o dia de hoje
    hoje = datetime.now()

    # Calcular o primeiro dia da semana (segunda-feira)
    primeira_segunda = hoje - timedelta(days=hoje.weekday())

    # Criar uma lista com os dias de segunda a sexta
    dias_uteis = [primeira_segunda + timedelta(days=i) for i in range(5)]

    # Converter as datas para o formato string

    # dias_uteis_str = [dia.strftime('%Y-%m-%d') for dia in dias_uteis]

    dias_uteis_str = ['2024-10-14', '2024-04-16', '2024-04-17', '2024-04-18', '2024-04-19']


    resposta = cursor.execute("SELECT imagem FROM cardapio WHERE data_inicial = ?", (dias_uteis_str[0],)).fetchone()
    # cursor.close()
    return resposta[0] if resposta and resposta[0] is not None else None



def selectGerarRefeicao():

    hoje = datetime.now()

    primeira_segunda = hoje - timedelta(days=hoje.weekday())

    dias_uteis = [primeira_segunda + timedelta(days=i) for i in range(5)]

    dias_uteis_str = [dia.strftime('%Y-%m-%d') for dia in dias_uteis]
    print(dias_uteis_str)

    # print("Consulta: ", f"SELECT * FROM GERAR_AGENDA WHERE id_data IN ('{dias_uteis_str[0]}','{dias_uteis_str[1]}','{dias_uteis_str[2]}','{dias_uteis_str[3]}','{dias_uteis_str[4]}')")

    # cursor = cnxn.cursor()
    resposta = cursor.execute("SELECT * FROM GERAR_AGENDA WHERE id_data IN (?,?,?,?,?)", (dias_uteis_str[0],dias_uteis_str[1],dias_uteis_str[2],dias_uteis_str[3],dias_uteis_str[4])).fetchall()
    # cursor.close()

    resposta = [tuple(row) for row in resposta]
    # print(resposta)

    data_atual = hoje.date()
    hora_atual = hoje.time()

    resposta_atualizada = []

    for row in resposta:
        id_data,valor1, valor2, valor3 = row
        
        data_row = datetime.strptime(id_data, '%Y-%m-%d').date()
    
        # Verificar se o dia é anterior ou se é o dia atual antes das 8h
        if data_row < data_atual or (data_row == data_atual and hora_atual > datetime.strptime('08:00', '%H:%M').time()):
            valor1 = False
            valor2 = False
            valor3 = False
        
        resposta_atualizada.append((id_data,valor1, valor2, valor3))

    return resposta_atualizada