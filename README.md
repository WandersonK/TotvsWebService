# TotvsWebService
Integração Banco Totvs RM com Postgresql

O arquivo de credenciais (credential.py), possui a seguinte estrutura, basta cria-lo na pasta do projeto, e preencher com as informações necessários para conexão.

```
# credential.py

totvs_auth = {
    'server' : '***************',
    'username' : '***************',
    'password' : '***************',
    'schema' : '***************'
}

db_auth = {
    't_host' : 'localhost',
    't_port' : '5432',
    't_dbname' : 'testes',
    't_name_user' : '***************',
    't_password' : '***************'
}
```
