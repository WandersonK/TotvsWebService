# Projeto em desenvolvimento
from credential import totvs_auth, db_auth
from os import environ, path, makedirs, remove, walk
from lxml import etree
from totvserprm.retrieve import ConsultSQL
from datetime import datetime, date, timedelta
from platform import system
from psycopg2 import connect
from bs4 import BeautifulSoup

# Salva a data para de criar o arquivo de log específico ('%Y-%m-%d_H%H-%M-%S')
data_execucao = datetime.now().strftime('%Y%m%d')

# Recebendo as informações de acesso ao servidor
server = totvs_auth.get('server')
# server = input("Insita a url do seu Webservice: ")
username = totvs_auth.get('username')
# username = input("Insira o username do RM: ")
password = totvs_auth.get('password')
# password = input("Insira a senha do RM: ")

# Instanciando a comunicação com a base Totvs
consultsql = ConsultSQL(server, username, password)

# Dicionário de chaves únicas nas tabelas para acesso
key_tables = {"pfunc": "id",
              "ppessoa": "codigo",
              "pfuncao": "id",
              "gcoligada": "codcoligada",
              "psecao": "id"
              }

# Definindo local para salvar o log
if system() == 'Windows':
    dir_save = environ['HOMEPATH'] + '\\logrm\\'  # Windows
elif system() == 'Linux':
    # dir_save = environ['HOME'] + '/logrm/'  # Linux
    dir_save = '/var/log/logrm/' # Linux

# Criando a pasta de log caso ela não exita
if not path.isdir(dir_save):
    makedirs(dir_save)


def push_dbpostgres_insert(conteudo_xml, key_table_idx):
    # Data para Log
    data_log = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
    
    try:
        soup = BeautifulSoup(conteudo_xml, 'xml')
        resultado_total = soup.find_all('resultado')

        t_host = db_auth.get('t_host')
        t_port = db_auth.get('t_port')
        t_dbname = db_auth.get('t_dbname')
        t_name_user = db_auth.get('t_name_user')
        t_password = db_auth.get('t_password')

        con = connect(host=t_host, port=t_port, dbname=t_dbname, user=t_name_user, password=t_password)
        cur = con.cursor()

        cur.execute(f"SELECT {key_tables[key_table_idx]} FROM {db_auth.get('schema')}.rm_{key_table_idx};")
        res_tabela = cur.fetchall()

        for i1 in range(0, len(resultado_total)):

            conjunto_tags = []
            conjunto_dados = []
            resultado_individual = resultado_total[i1].contents # O .contents retorna o conteúdo dentro da tag <resultado> do xml (não armazena a tag <resultado>), esse resultado é passado em uma lista
            
            for i2 in range(0, len(resultado_individual)):
                
                if resultado_individual[i2].name == key_tables[key_table_idx]: # O .name se refere ao nome da tag
                    
                    tag_coluna = key_tables[key_table_idx] + ' ='
                    coluna_key = int(resultado_individual[i2].get_text(resultado_individual[i2].name)) # Coletando o conteúdo da tag atual em resultado_individual[i2]

                    cur.execute(f"SELECT recmodifiedon FROM {db_auth.get('schema')}.rm_{key_table_idx} WHERE {tag_coluna} {coluna_key};")
                    recmodifiedon_list = cur.fetchall()

                    break

            for i3 in range(0, len(resultado_individual)):

                if resultado_individual[i3].name == 'recmodifiedon' and recmodifiedon_list != []:
                    recmodifiedon_tuple = recmodifiedon_list[0]
                    data_tabela = recmodifiedon_tuple[0]

                    data_xml = resultado_individual[i3].get_text(resultado_individual[i3].name)

                    boll_recmodifiedon = data_xml > data_tabela.strftime('%Y-%m-%dT%H:%M:%S')

                    break
                else:
                    boll_recmodifiedon = False

            for i4 in range(0, len(resultado_individual)):

                if resultado_individual[i4] != '\n':
                    tag = resultado_individual[i4].name

                    if resultado_individual[i4].get_text(tag) != '' and tag != 'salario':
                        dado = resultado_individual[i4].contents
                        conjunto_tags.append(tag)

                        for i5 in range(0, len(dado)):
                            conjunto_dados.append(dado[i5])

                            if (coluna_key,) in res_tabela and boll_recmodifiedon:
                                cur.execute(f"UPDATE {db_auth.get('schema')}.rm_{key_table_idx} SET {tag} = $${dado[i5]}$$ WHERE {tag_coluna} '{coluna_key}'")
                                con.commit()

            conjunto_tags = str(tuple(conjunto_tags)).replace("'", "")
            conjunto_dados = str(tuple(conjunto_dados)).replace('"', '$$')

            if (coluna_key,) not in res_tabela:
                cur.execute(f"INSERT INTO {db_auth.get('schema')}.rm_{key_table_idx}{conjunto_tags} VALUES {conjunto_dados}")
                con.commit()

        con.close()
    
    except Exception as erro_rotina:
        # Log em caso de erro
        mensagem = f'\n[{data_log}] (-> Falha) Ocorreu o seguinte erro na rotina: {erro_rotina}\n     {erro_rotina.with_traceback}'
        arquivo_log = f'{dir_save}/rotina_webservicetotvs_{data_execucao}_stderr.log'
        gravar_log(arquivo_log, mensagem)
        
    else:
        # Log em caso de êxito
        mensagem = f'\n[{data_log}] (-> Êxito) A rotina foi executada sem erros.'
        arquivo_log = f'{dir_save}/rotina_webservicetotvs_{data_execucao}.log'
        gravar_log(arquivo_log, mensagem)


# Esta função faz um pré tratamento dos dados para o banco
def gravar_log(arquivo_log, mensagem):
    
    # Cria o arquivo na pasta especificada e salva o log
    log_instancia = open(arquivo_log, 'a', encoding='utf-8')  # O 'a' indica append, insere linha seguida, sem sobrepor o existente
    log_instancia.write(mensagem)
    log_instancia.close()
    

def excluir_log_antigo():
    tempo_delete_arq_log= date.today() - timedelta(60)  # Definir quantos dias para excluir os arquivos de log, atual 60 dias
    
    for dir_completo, dir_name, file_names_list in walk(dir_save):
        for file_name in file_names_list:
            
            path_arquivo = path.join(dir_completo, file_name)
            vida_arquivo = date.fromtimestamp(path.getmtime(path_arquivo))
    
            if path.isfile(path_arquivo) and vida_arquivo < tempo_delete_arq_log:
                remove(path_arquivo)


for key_table_idx in key_tables.keys():
    # Aqui faz a consulta via Webservice na base Totvs
    resultadoF = consultsql.get(
        codcoligada=1,
        codsistema='P',
        codsentenca='WS_' + key_table_idx,
        parameters={}
    )
    
    # Aqui faz a conversão do lxml para bytes e para str utf-8
    xml = etree.tostring(resultadoF, encoding="utf-8").decode("utf-8")
    
    # Aqui chama a função para salvar os dados no banco de dados
    # push_dbpostgres_insert(xml, key_table_idx)

excluir_log_antigo()
