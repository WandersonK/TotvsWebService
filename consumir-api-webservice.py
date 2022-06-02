# Projeto em desenvolvimento
from credential import totvs_auth, db_auth
import os
from lxml import etree
from xml.dom import minidom
from totvserprm.retrieve import ConsultSQL
from datetime import *
import platform
import psycopg
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# Recebendo as informações de acesso ao servidor
server = totvs_auth.get('server')
# server = input("Insita a url do seu Webservice: ")
username = totvs_auth.get('username')
# username = input("Insira o username do RM: ")
password = totvs_auth.get('password')
# password = input("Insira a senha do RM: ")

# Realizando a consulta via Webservice na Totvs
consultsql = ConsultSQL(server, username, password)
resultadoF = consultsql.get(
codcoligada=1,
codsistema='P',
codsentenca='WS_ppessoa',
parameters={}
)

# Dicionário de chaves únicas nas tabelas para acesso
key_tables = {"pfunc":"id",
              "ppessoa":"codigo",
              "pfuncao":"id",
              "gcoligada":"codcoligada",
              "pcodinstrucao":"codcliente",
              "psecao":"id"}

# Recebendo informações da tabela e opção de operação (insert)
table = 'ppessoa' #input("Favor informar a tabela: ")
# option = 'i' #input("Qual operação deseja? ")

# Definindo local para salvar o log
if platform.system() == 'Windows':
    dir_save = '.\\logrm\\'  # Windows
    arquivo_save = dir_save + 'saida.xml'  # Windows
elif platform.system() == 'Linux':    
    dir_save = './logrm/'  # Linux
    arquivo_save = dir_save + 'saida.xml'  # Linux

# Criando a pasta de log caso ela não exita
if not os.path.isdir(dir_save):
    os.makedirs(dir_save)

# Salva a data e hora para afim de criar o arquivo de log específico
date_var = datetime.now().strftime('%Y-%m-%d_T%H-%M-%S')

# Esta função cria um arquivo e salva o log na pasta específicada
def salvar_saida(pretty):
    arquivo_log = open(dir_save + 'log_' + date_var + '.xml', 'w+', encoding="utf-8")  # O 'w' indica write (escrita)
    arquivo_log.write(pretty)
    arquivo_log.close()
    
    """
    arquivo = open(arquivo_save, 'w+', encoding='utf-8')
    arquivo.write(pretty)
    arquivo.close()
    """

def pretty_print(elem):
    xml = etree.tostring(elem)
    pretty = minidom.parseString(xml).toprettyxml(indent='   ')
    """Descomentar a chamada da função de salvar_saida caso necessário salvar"""
    # salvar_saida(pretty)
    push_dbpostgres_insert(pretty)

def push_dbpostgres_insert(pretty):
    soup = BeautifulSoup(pretty, 'xml')
    
    resultado_total = soup.find_all('resultado')
    
    my_date = (datetime.now() - timedelta(30)).strftime('%Y-%m-%dT%H:%M:%S')  # 30 dias
    
    t_host = db_auth.get('t_host')
    t_port = db_auth.get('t_port')
    t_dbname = db_auth.get('t_dbname')
    t_name_user = db_auth.get('t_name_user')
    t_password = db_auth.get('t_password')
    
    con = psycopg.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_name_user, password=t_password)
    cur = con.cursor()
    
    cur.execute(f"SELECT {key_tables[table]} FROM {totvs_auth.get('schema')}.rm_{table};")
    res_tabela = cur.fetchall()

    for i1 in range(0, len(resultado_total)):
        
        conjunto_tags = []
        conjunto_dados = []
        resultado_colaborador = resultado_total[i1].contents
        
        for i4 in range(0, len(resultado_colaborador)):

            if resultado_colaborador[i4].name == key_tables[table]:
                tag_coluna = key_tables[table] + ' ='
                coluna_key = int(resultado_colaborador[i4].get_text(resultado_colaborador[i4].name))
                print(coluna_key)
                break
        
        for i2 in range(0, len(resultado_colaborador)):
            
            if resultado_colaborador[i2] != '\n':
                tag = resultado_colaborador[i2].name
                
                if resultado_colaborador[i2].get_text(tag) != '' and tag != 'salario':
                    dado = resultado_colaborador[i2].contents
                    conjunto_tags.append(tag)
        
                    for i3 in range(0, len(dado)):
                        conjunto_dados.append(dado[i3])
                        
                        if (coluna_key,) in res_tabela:
                            cur.execute(f"UPDATE {totvs_auth.get('schema')}.rm_{table} SET {tag} = $${dado[i3]}$$ WHERE {tag_coluna} '{coluna_key}'")
                            con.commit()

        conjunto_tags = str(tuple(conjunto_tags)).replace("'","")
        conjunto_dados = str(tuple(conjunto_dados)).replace('"','$$')
        
        if (coluna_key,) not in res_tabela:
            cur.execute(f"INSERT INTO {totvs_auth.get('schema')}.rm_{table}{conjunto_tags} VALUES {conjunto_dados}")
            con.commit()
            
    con.close()

pretty_print(resultadoF)
