# Projeto em desenvolvimento
from credential import totvs_auth, db_auth
import os
from lxml import etree, objectify
from xml.dom import minidom
from totvserprm.retrieve import ConsultSQL
from datetime import *
import platform
import psycopg, sys

# import requests
# import xmltodict
# import dicttoxml
# from xml.etree import ElementTree as elements

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
codsentenca='WEBSERVICE',
parameters={}
)

# Dicionário de chaves únicas nas tabelas para acesso
key_tables = {"pfunc":"id",
              "ppessoa":"codigo",
              "pfuncao":"id",
              "gcoligada":"codcoligada",
              "pcodinstrucao":"codcliente",
              "psecao":"id"}


# Recebendo informações da tabela e opção de operação (insert ou update)
table = 'ppessoa' #input("Favor informar a tabela: ")
option = 'i' #input("Qual operação deseja? ")

# Definindo local para salvar o log
if platform.system() == 'Windows':
    dir_save = os.environ['HOMEPATH'] + '\\Documents\\TotvsWebService\\logrm\\'  # Windows
    arquivo_save = dir_save + 'saida.xml'  # Windows
elif platform.system() == 'Linux':    
    dir_save = os.environ['HOME'] + '/Documentos/Scripts_Python/TotvsWebService/logrm/'  # Linux
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
    if option == 'i':
        push_dbpostgres_insert(pretty)
    elif option == 'u':
        push_dbpostgres_update(pretty)

def leitura_xml():
    tree = ET.parse(arquivo_save)
    root = tree.getroot()

def leitura_xmlsoup():
    infile = open(arquivo_save, "r", encoding="utf-8")
    contents = infile.read()
    soup = BeautifulSoup(contents, 'xml')
    
    my_date = (datetime.now() - timedelta(30)).strftime('%Y-%m-%dT%H:%M:%S')

def push_dbpostgres_insert(pretty):
    
    soup = BeautifulSoup(pretty, 'xml')
    
    resultado_total = soup.find_all('resultado')
    
    my_date = (datetime.now() - timedelta(30)).strftime('%Y-%m-%dT%H:%M:%S')  # 30 dias
# ========================== 1.0 ======================================     
    for i1 in range(0, len(resultado_total)):
        conjunto_tags = []
        conjunto_dados = []
        resultado_colaborador = resultado_total[i1].contents
        
        for i2 in range(0, len(resultado_colaborador)):
            
            if resultado_colaborador[i2] != '\n':
                tag = resultado_colaborador[i2].name
                
                if resultado_colaborador[i2].get_text(tag) != '' and tag != 'salario':
                    
                    dado = resultado_colaborador[i2].contents
                    conjunto_tags.append(tag)
        
                    for i3 in range(0, len(dado)):
                        conjunto_dados.append(dado[i3])
                        # print(tag, ":", dado[i3])

        conjunto_tags = str(tuple(conjunto_tags)).replace("'","")
        # print(i1)
        # print(conjunto_tags)
        # print()
        conjunto_dados = str(tuple(conjunto_dados)).replace('"','$$')
        # print(conjunto_dados)
        # print()
        # input()
        try:
            t_host = db_auth.get('t_host')
            t_port = db_auth.get('t_port')
            t_dbname = db_auth.get('t_dbname')
            t_name_user = db_auth.get('t_name_user')
            t_password = db_auth.get('t_password')
            
            con = psycopg.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_name_user, password=t_password)
            cur = con.cursor()
            # cur.execute(f"INSERT INTO {db_auth.get('schema')}.rm_{table}{conjunto_tags} VALUES {conjunto_dados}")
            cur.execute(f"INSERT INTO public.rm_{table}{conjunto_tags} VALUES {conjunto_dados}")
            con.commit()
        except psycopg.DatabaseError as e:
            if con:
                con.rollback()
            print('Error %s' % e)
            sys.exit(1)
        finally:
            if con:
                con.close()
# ========================== FIM 1.0 ================================================

# ========================== 2.0 em Desenvolvimento ====================================== 
    for i1 in range(0, len(resultado_total)):
        conjunto_tags = []
        conjunto_dados = []
        resultado_colaborador = resultado_total[i1].contents
        # print(resultado_colaborador)
        
        for i2 in range(0, len(resultado_colaborador)):
            
            for string in resultado_colaborador[i2].stripped_strings:
                print(repr(string))
            print(repr(i2))
            
            if resultado_colaborador[i2] != '\n':
                tag = resultado_colaborador[i2].name
                
                if resultado_colaborador[i2].get_text(tag) != '' and tag != 'salario':
                    
                    dado = resultado_colaborador[i2].contents
                    conjunto_tags.append(tag)
        
                    for i3 in range(0, len(dado)):
                        conjunto_dados.append(dado[i3])
                        # print(tag, ":", dado)

        conjunto_tags = str(tuple(conjunto_tags)).replace("'","")
        # print(i1)
        # print(conjunto_tags)
        # print()
        conjunto_dados = str(tuple(conjunto_dados)).replace('"','$$')
        # print(conjunto_dados)
        # print()
        # input()
        try:
            t_host = db_auth.get('t_host')
            t_port = db_auth.get('t_port')
            t_dbname = db_auth.get('t_dbname')
            t_name_user = db_auth.get('t_name_user')
            t_password = db_auth.get('t_password')
            
            con = psycopg.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_name_user, password=t_password)
            cur = con.cursor()
            cur.execute(f"INSERT INTO public.rm_{table}{conjunto_tags} VALUES {conjunto_dados}")
            con.commit()
        except psycopg.DatabaseError as e:
            if con:
                con.rollback()
            print('Error %s' % e)
            sys.exit(1)
        finally:
            if con:
                con.close()
# ========================== FIM 2.0 ======================================


def push_dbpostgres_update(pretty): # Em desenvolvimento
    
    soup = BeautifulSoup(pretty, 'xml')
    
    resultado_total = soup.find_all('resultado')
    
    my_date = (datetime.now() - timedelta(30)).strftime('%Y-%m-%dT%H:%M:%S')  # 30 dias
     
    for i1 in range(0, len(resultado_total)):
        conjunto_tags = []
        conjunto_dados = []
        va = []
        resultado_colaborador = resultado_total[i1].contents
        
        for i4 in range(0, len(resultado_colaborador)):
            if resultado_colaborador[i4].name == key_tables[table]:
                tag_coluna = key_tables[table] + ' ='
                coluna_key = resultado_colaborador[i4].get_text(resultado_colaborador[i4].name)
                print(coluna_key)
                break
                # print("tag:", tag_coluna, "dado:", coluna_key)
                    
            # print("2# tag:", key_tables[table], "dado", coluna_key)#, "dado:", coluna_key)
        
        for i2 in range(0, len(resultado_colaborador)):
            
            if resultado_colaborador[i2] != '\n':
                tag = resultado_colaborador[i2].name
                
                if resultado_colaborador[i2].get_text(tag) != '' and tag != 'salario':
                    
                    
                    dado = resultado_colaborador[i2].contents
                    # print(dado)
                    conjunto_tags.append(tag)
        
        
                    # for i4 in range(0, len(resultado_colaborador)):
                    #     if resultado_colaborador[i4].name == key_tables[table]:
                    #         # tag_coluna = key_tables[table] + ' ='
                    #         coluna_key = resultado_colaborador[i4].get_text(resultado_colaborador[i4].name)
                    #         # print(coluna_key)
                    #         break
                    #         # print("tag:", tag_coluna, "dado:", coluna_key)
                                
                    #     # print("2# tag:", key_tables[table], "dado", coluna_key)#, "dado:", coluna_key)
                        
                    for i3 in range(0, len(dado)):
                        # print(dado[i3])
                        conjunto_dados.append(dado[i3])
                        string_tratada = '$$' + dado[i3] + '$$'
                        # print(tag, ":::", dado[i3] )
                        
                        # va.append(tag + '=' + "'" + str(dado[i3]).replace('"','"') + "'")
                        # va.append(tag + '=' + string_tratada)
                        # va.append(tag + '=' + dado[i3])
                        # if tag == 'codcliente' or tag == 'codigo' or tag == 'id' or tag == 'codcoligada':
                    
                    # print("2# tag:", key_tables[table], "dado", coluna_key)#, "dado:", coluna_key)
                        try:
                            t_host = db_auth.get('t_host')
                            t_port = db_auth.get('t_port')
                            t_dbname = db_auth.get('t_dbname')
                            t_name_user = db_auth.get('t_name_user')
                            t_password = db_auth.get('t_password')
                            
                            con = psycopg.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_name_user, password=t_password)
                            cur = con.cursor()
                            # cur.execute(f'UPDATE public.rm_ppessoa SET {va} where {tagwhere} CAST ({abc1234} AS text)')# WHERE <condition>')
                            cur.execute(f'UPDATE public.rm_{table} SET {tag} = $${dado[i3]}$$ where {tag_coluna} \'{coluna_key}\'')#CAST (31 AS text)') #CAST ({abc1234} AS text)')# WHERE <condition>')
                            # cur.execute(f"INSERT INTO public.rm_psecao{conjunto_tags} VALUES {conjunto_dados}")
                            con.commit()
                        except psycopg.DatabaseError as e:
                            if con:
                                con.rollback()
                            print('Error %s' % e)
                            sys.exit(1)
                        finally:
                            if con:
                                con.close()
                        
                        
                        
                        
                        
                        # if tag == 'codigo':
                        #     tagwhere = tag + ' = '
                        #     abc1234 = '31'
                        
        # va = str(tuple(va)).replace(")","").replace("(","")#.replace('"','')
        # conjunto_tags = str(tuple(conjunto_tags)).replace("'","")
        # conjunto_dados = str(tuple(conjunto_dados)).replace('"','$$')
        
        # try:
            # t_host = db_auth.get('t_host')
            # t_port = db_auth.get('t_port')
            # t_dbname = db_auth.get('t_dbname')
            # t_name_user = db_auth.get('t_name_user')
            # t_password = db_auth.get('t_password')
        #     con = psycopg.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_name_user, password=t_password)
        #     cur = con.cursor()
        #     # cur.execute(f'UPDATE public.rm_ppessoa SET {va} where {tagwhere} CAST ({abc1234} AS text)')# WHERE <condition>')
        #     cur.execute(f'UPDATE public.rm_ppessoa SET naturalidade = {string_tratada} where {tagwhere} {abc1234}') #CAST ({abc1234} AS text)')# WHERE <condition>')
        #     # cur.execute(f"INSERT INTO public.rm_psecao{conjunto_tags} VALUES {conjunto_dados}")
        #     con.commit()
        # except psycopg.DatabaseError as e:
        #     if con:
        #         con.rollback()
        #     print('Error %s' % e)
        #     sys.exit(1)
        # finally:
        #     if con:
        #         con.close()
                
                
                

pretty_print(resultadoF)


# leitura_xml()


# leitura_xmlsoup()