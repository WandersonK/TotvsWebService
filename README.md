# TotvsWebService
## Integração Banco Totvs RM com Postgresql

O arquivo de credenciais (credential.py), possui a seguinte estrutura, basta cria-lo na pasta do projeto, e preencher com as informações necessários para conexão.

```
# credential.py

totvs_auth = {
    'server' : '***************',
    'username' : '***************',
    'password' : '***************',
}

db_auth = {
    't_host' : 'localhost',
    't_port' : '5432',
    't_dbname' : 'testes',
    't_name_user' : '***************',
    't_password' : '***************'

    # Schema banco
    'schema' : '***************' # Esse é o schema do seu banco PostgreSQL, na qual será feito o INSERT ou UPDATE
}
```

Pacotes necessários:

* pip install totvserprm
* pip install beautifulsoup4
* pip install psycopg2
* pip install lxml

Na pasta DDL_Banco estão as DDLs para criação das tabelas utilizadas aqui. Caso necessário, altere conforme suas necessidades.

* GCOLIGADA
* PFUNC
* PFUNCAO
* PPESSOA
* PSECAO
