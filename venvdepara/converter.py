import os

import pandas as pd
import sqlalchemy
import configparser
import psycopg2 # para o PostgreSQL


config = configparser.ConfigParser()
config.read("config.ini");
#'postgresql+psycopg2://NotaCasteloBranco:es74079@localhost/NotaCasteloBranco'    Exemplo
class Converter():
    def criar_tabela(self, banco, usuario, senha, planilha, tabela):

        drive = config['default']["drive"]
        host = config['default']["host"]

        if banco == "":
            banco=config['default']["banco"]
        if usuario == "":
            usuario = config['default']["usuario"]
        if senha == "":
            senha = config['default']["senha"]

        self.usuario = usuario
        self.senha = senha
        self.banco = banco
        self.tabela = tabela

        credencial_banco = drive +'://'+ self.usuario +':'+ self.senha +'@'+host +'/'+ self.banco

        self.planilha = planilha

        #sheet = "C:\\Users\\richielly.carvalho\\Desktop\\NotaCasteloBranco\\ArquivosConcorrentes\\Notas Fiscais Canceladas.csv"

        engine = sqlalchemy.create_engine(credencial_banco)

        pastas = os.listdir(config['default']["path"])
        schemas_name = []
        for schema_name in pastas:
            if not schema_name.endswith('.zip'):
                schemas_name.append(schema_name)
    
        for schema in schemas_name:
            if not engine.dialect.has_schema(engine, schema):
                engine.execute(sqlalchemy.schema.CreateSchema(schema))

        nome_schema = 'Licitacao'
        df = pd.read_csv(config['default']["path"]+nome_schema+'/csv/'+self.planilha, encoding='UTF-8',sep=';')
            
        try:
            df.to_sql(
            name=self.tabela,
            con=engine,
            schema=nome_schema,
            index=False,
             # if_exists ='append' Utilizar se quiser incluir dados replicados no banco existente
        )
        except ValueError as error:
            return error
        except Exception as error2:
            return error2
