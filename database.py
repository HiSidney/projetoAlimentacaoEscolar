import pyodbc
from datetime import datetime

print(pyodbc.drivers())

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

def insertIntoDesperdicio(waste,date):
    cursor.execute(f"insert into desperdicio values({waste}, '{date}')")
    cursor.commit()

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
        "insert into gerar_agenda(estado,data,habilitar_cafe_manha,habilitar_almoco,habilitar_cafe_tarde) VALUES (?, ?, ?, ?, ?)", 
        (estado, data, habilitar_cafe_manha, habilitar_almoco, habilitar_cafe_tarde)
    )
    cursor.commit()


def insertIntoRefeicaoAgendada(req):

    id_usuario = 2
    # print(req)
    id_agenda = [6,7,8,9,10]

    for id in id_agenda:
        for dia, periodos in req.items():
            # print(f"{dia}: {periodos[0]}")
            # print(f"{dia}: {periodos[1]}")
            # print(f"{dia}: {periodos[2]}")

            print(f"insert into refeicao_agendada(id_agenda,id_usuario,cafe_manha,almoco,cafe_tarde) VALUES ({id},{id_usuario}, {periodos[0]}, {periodos[1]}, {periodos[2]})\n")

            cursor.execute(
                "insert into refeicao_agendada(id_agenda,id_usuario,cafe_manha,almoco,cafe_tarde) VALUES (?, ?, ?, ?, ?)", 
                (id, id_usuario, periodos[0], periodos[1], periodos[2])
            )
            cursor.commit()


def getImgCardapio(idImg):
    resposta = cursor.execute("SELECT imagem FROM cardapio WHERE id_imagem = ?", (idImg,)).fetchone()
    return resposta[0] if resposta and resposta[0] is not None else None