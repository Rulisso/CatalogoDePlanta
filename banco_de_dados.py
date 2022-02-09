import MySQLdb
dict = {"1": "a", "2": "b", "3": "c", "4": "d", "5": "e", "6": "f", "7": "g", "8": "h", "9": "i", "0": "j"}

hosp = str("bcl37brbi9oxlnsvxfnc-mysql.services.clever-cloud.com")
eu = str("ujwnfer3ugf9hroz")
senha = str("GDF98FJhTFGnrLa24E0k")
banco = str("bcl37brbi9oxlnsvxfnc")


def carrega_id(chat_id, chat_name):
    conexao = MySQLdb.connect(host=hosp, user=eu, password=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("select * from dados")
    lista = []
    linhas = cursor.fetchall()
    for linha in linhas:
        id = linha[0]
        lista.append(id)
    conferir_id(chat_id, lista, chat_name)
    cursor.close()


def conferir_id(chat_id, lista, chat_name):
    if not pega_dados(chat_id) in lista:
        adicionar_usuario(chat_id, chat_name)
    else:
        pass


def pega_dados(chat_id):
    nome_id = chat_id
    for i in chat_id:
        nome_id = nome_id.replace(i, dict[i])
    return nome_id


def adicionar_usuario(chat_id,chat_name):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("insert into dados VALUES('{}','{}')".format(pega_dados(chat_id), chat_name))
    conexao.close()


def adicionar_foto(chat_id, file_id, nome_da_planta):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("insert into {}_foto(foto,nome_da_planta) VALUES('{}','{}')".format(pega_dados(chat_id), file_id, nome_da_planta))
    conexao.close()


def adicionar_table_foto(chat_id):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("create table if not exists {}_foto (id int primary key auto_increment, foto text, nome_da_planta text)".format(pega_dados(chat_id)))
    conexao.close()


def adicionar_table_planta(chat_id):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("create table if not exists {}_plantas (id int primary key auto_increment, nome_da_planta varchar(100), brilho varchar(10), agua varchar(10), sol varchar(10), tem_flor enum('sim','nao'), obs text,data dateTime)".format(pega_dados(chat_id)))
    conexao.close()


def adicionar_info_plantas(chat_id, nome_da_planta, data):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("insert into {}_plantas(nome_da_planta, data) VALUES('{}','{}')".format(pega_dados(chat_id), nome_da_planta, data))
    conexao.close()


def adicionar_brilho_plantas(chat_id, brilho, nome_da_planta):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("UPDATE {}_plantas set brilho='{}' where nome_da_planta='{}' and brilho is null".format(pega_dados(chat_id), brilho, nome_da_planta))
    conexao.close()


def adicionar_agua_plantas(chat_id, agua, nome_da_planta):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("UPDATE {}_plantas set agua='{}' where nome_da_planta='{}' and agua is null".format(pega_dados(chat_id), agua, nome_da_planta))
    conexao.close()


def adicionar_sol_plantas(chat_id, sol, nome_da_planta):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("UPDATE {}_plantas set sol='{}' where nome_da_planta='{}' and sol is null".format(pega_dados(chat_id), sol, nome_da_planta))
    conexao.close()


def adicionar_flor_plantas(chat_id, flor, nome_da_planta):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("UPDATE {}_plantas set tem_flor='{}' where nome_da_planta='{}' and tem_flor is null".format(pega_dados(chat_id), flor, nome_da_planta))
    conexao.close()


def adicionar_Obs_plantas(chat_id, obs, nome_da_planta):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("UPDATE {}_plantas set obs='{}' where nome_da_planta='{}' and obs is null".format(pega_dados(chat_id), obs, nome_da_planta))
    conexao.close()


def adicionar_Mais_Obs_plantas(chat_id, obs, nome_da_planta):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("UPDATE {}_plantas set obs='{}' where nome_da_planta='{}'".format(pega_dados(chat_id), obs, nome_da_planta))
    conexao.close()


def verifica_obs(chat_id, nome):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("select obs from {}_plantas where nome_da_planta = '{}'".format(pega_dados(chat_id), nome))
    lista = []
    linhas = cursor.fetchall()
    for linha in linhas:
        obs = linha[0]
        lista.append(obs)
    cursor.close()
    return lista




def verifica_info_planta(chat_id, nome):
    print(nome)
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("select * from {}_plantas".format(pega_dados(chat_id)))
    lista = []
    lista1 = []
    lista2 = []
    lista3 = []
    lista4 = []
    lista5 = []
    lista6 = []
    lista7 = []
    cont = 0
    linhas = cursor.fetchall()
    for linha in linhas:
        if nome in linha:
            nome_ = linha[1]
            brilho = linha[2]
            agua = linha[3]
            sol = linha[4]
            flor = linha[5]
            obs = linha[6]
            data = linha[7]

            lista1.append(nome_)
            lista2.append(brilho)
            lista3.append(agua)
            lista4.append(sol)
            lista5.append(flor)
            lista6.append(obs)
            lista7.append(str(data))

            lista.append(lista1)
            lista.append(lista2)
            lista.append(lista3)
            lista.append(lista4)
            lista.append(lista5)
            lista.append(lista6)
            lista.append(lista7)
            cont +=1
            if cont <= 1:
                break
    cursor.close()
    return lista


def adicionar_table_audio(chat_id):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("create table if not exists {}_audio (id int primary key auto_increment, audio text)".format(pega_dados(chat_id)))
    conexao.close()


def adicionar_audio(chat_id, file_id):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("insert into {}_audio(audio) VALUES('{}')".format(pega_dados(chat_id), file_id))
    conexao.close()


def carrega_foto(chat_id):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("select * from {}_foto".format(pega_dados(chat_id)))
    lista = []
    linhas = cursor.fetchall()
    for linha in linhas:
        file_id = linha[1]
        lista.append(file_id)
    cursor.close()
    return lista


def carrega_foto_id(chat_id):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("select * from {}_foto".format(pega_dados(chat_id)))
    lista = []
    linhas = cursor.fetchall()
    for linha in linhas:
        file_id = linha[0]
        lista.append(file_id)
    cursor.close()
    return lista


def carrega_foto_pelo_id(chat_id, id, nome):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("select * from {}_foto where id = '{}' and nome_da_planta = '{}'".format(pega_dados(chat_id), id, nome))
    lista = []
    linhas = cursor.fetchall()
    for linha in linhas:
        file_id = linha[1]
        lista.append(file_id)
    cursor.close()
    return lista


def carrega_foto_nome(chat_id):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("select * from {}_foto".format(pega_dados(chat_id)))
    lista = []
    linhas = cursor.fetchall()
    for linha in linhas:
        file_id = linha[2]
        lista.append(file_id)
    cursor.close()
    return lista



def carrega_audio(chat_id):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("select * from {}_audio".format(pega_dados(chat_id)))
    lista = []
    linhas = cursor.fetchall()
    for linha in linhas:
        file_id = linha[1]
        lista.append(file_id)
    cursor.close()
    return lista


def carrega_audio_id(chat_id):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("select * from {}_audio".format(pega_dados(chat_id)))
    lista = []
    linhas = cursor.fetchall()
    for linha in linhas:
        file_id = linha[0]
        lista.append(file_id)
    cursor.close()
    return lista


def verifica_foto(chat_id, nome):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("select foto from {}_foto where nome_da_planta = '{}'".format(pega_dados(chat_id), nome))
    lista = []
    linhas = cursor.fetchall()
    for linha in linhas:
        a = linha[0]
        lista.append(a)
    cursor.close()
    return lista


def verifica_nome(chat_id):
    conexao = MySQLdb.connect(host=hosp, user=eu, passwd=senha, db=banco)
    cursor = conexao.cursor()
    cursor.execute("select nome_da_planta from {}_foto where nome_da_planta is not null".format(pega_dados(chat_id)))
    lista = []
    linhas = cursor.fetchall()
    for linha in linhas:
        nome = linha[0]
        lista.append(nome)
    cursor.close()
    return lista
