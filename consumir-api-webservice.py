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
# resultadoF = consultsql.get(
# codcoligada=1,
# codsistema='P',
# codsentenca='WS_ppessoa',
# parameters={}
# )

# Dicionário de chaves únicas nas tabelas para acesso
key_tables = {"pfunc":"id",
              "ppessoa":"codigo",
              "pfuncao":"id",
              "gcoligada":"codcoligada",
              "psecao":"id"}

# Recebendo informações da tabela e opção de operação (insert)
# table = 'ppessoa' #input("Favor informar a tabela: ")
# option = 'i' #input("Qual operação deseja? ")

# Definindo local para salvar o log
if platform.system() == 'Windows':
    dir_save = os.environ['HOMEPATH'] + '\\logrm\\'  # Windows
    arquivo_save = dir_save + 'saida.xml'  # Windows
elif platform.system() == 'Linux':    
    # dir_save = os.environ['HOME'] + '/logrm/'  # Linux
    dir_save = '/var/log/logrm/' # Linux
    arquivo_save = dir_save + 'saida.xml'  # Linux

# Criando a pasta de log caso ela não exita
if not os.path.isdir(dir_save):
    os.makedirs(dir_save)

# Salva a data e hora para afim de criar o arquivo de log específico
# date_var = datetime.now().strftime('%Y-%m-%d_T%H-%M-%S')

# Esta função cria um arquivo e salva o log na pasta específicada
def salvar_saida(pretty, key_table_idx):
    # Salva a data e hora para afim de criar o arquivo de log específico
    date_var = datetime.now().strftime('%Y-%m-%d_T%H-%M-%S')
    
    arquivo_log = open(dir_save + date_var + '_log_' + key_table_idx + '.xml', 'w+', encoding="utf-8")  # O 'w' indica write (escrita)
    arquivo_log.write(pretty)
    arquivo_log.close()
    
    """
    arquivo = open(arquivo_save, 'w+', encoding='utf-8')
    arquivo.write(pretty)
    arquivo.close()
    """

def pretty_print(elem, key_table_idx):
    xml = etree.tostring(elem)
    pretty = minidom.parseString(xml).toprettyxml(indent='   ')
    """Descomentar a chamada da função de salvar_saida caso necessário salvar"""
    salvar_saida(pretty, key_table_idx)
    push_dbpostgres_insert(pretty, key_table_idx)

def push_dbpostgres_insert(pretty, key_table_idx):
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
    
    cur.execute(f"SELECT {key_tables[key_table_idx]} FROM {db_auth.get('schema')}.rm_{key_table_idx};")
    res_tabela = cur.fetchall()
    
    for i1 in range(0, len(resultado_total)):
        
        conjunto_tags = []
        conjunto_dados = []
        resultado_colaborador = resultado_total[i1].contents
        
        for i2 in range(0, len(resultado_colaborador)):

            if resultado_colaborador[i2].name == key_tables[key_table_idx]:
                tag_coluna = key_tables[key_table_idx] + ' ='
                coluna_key = int(resultado_colaborador[i2].get_text(resultado_colaborador[i2].name))
                
                cur.execute(f"SELECT recmodifiedon FROM {db_auth.get('schema')}.rm_{key_table_idx} WHERE {tag_coluna} {coluna_key};")
                recmodifiedon_list = cur.fetchall()
                
                break
            
        for i3 in range(0, len(resultado_colaborador)):
            
            if resultado_colaborador[i3].name == 'recmodifiedon' and recmodifiedon_list != []:
                recmodifiedon_tuple = recmodifiedon_list[0]
                data_tabela = recmodifiedon_tuple[0]
                
                data_xml = resultado_colaborador[i3].get_text(resultado_colaborador[i3].name)
                
                boll_recmodifiedon = data_xml > data_tabela.strftime('%Y-%m-%dT%H:%M:%S')
                
                break
            else:
                boll_recmodifiedon = False
                
        for i4 in range(0, len(resultado_colaborador)):
            
            if resultado_colaborador[i4] != '\n':
                tag = resultado_colaborador[i4].name
                
                if resultado_colaborador[i4].get_text(tag) != '' and tag != 'salario':
                    dado = resultado_colaborador[i4].contents
                    conjunto_tags.append(tag)

                    for i5 in range(0, len(dado)):
                        conjunto_dados.append(dado[i5])
                        
                        if (coluna_key,) in res_tabela and boll_recmodifiedon:
                            cur.execute(f"UPDATE {db_auth.get('schema')}.rm_{key_table_idx} SET {tag} = $${dado[i5]}$$ WHERE {tag_coluna} '{coluna_key}'")
                            con.commit()

        conjunto_tags = str(tuple(conjunto_tags)).replace("'","")
        conjunto_dados = str(tuple(conjunto_dados)).replace('"','$$')
        
        if (coluna_key,) not in res_tabela:
            cur.execute(f"INSERT INTO {db_auth.get('schema')}.rm_{key_table_idx}{conjunto_tags} VALUES {conjunto_dados}")
            con.commit()
            
    con.close()

for key_table_idx in key_tables.keys():
    
    resultadoF = consultsql.get(
    codcoligada=1,
    codsistema='P',
    codsentenca='WS_' + key_table_idx,
    parameters={}
    )
    
    pretty_print(resultadoF, key_table_idx)
