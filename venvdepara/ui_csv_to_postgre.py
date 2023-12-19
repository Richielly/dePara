import os
import converter
from glob import glob
from time import sleep as t
import shutil
import logging

import PySimpleGUI as sg

arquivos_csv = []

sg.theme('BluePurple')

criar = converter.Converter()

# origem = r"C:\csv_to_postgre\\"

# destino = r"C:\csv_to_postgre\convertido\\"
# old = r"C:\csv_to_postgre\old\\"

def start():

    ativo = True
    tempo = 10
    evento, valores = janela.read()
    origem  = str(valores["diretorio_origem"]).replace('/','\\')+'\\'
    destino = str(valores["diretorio_destino"]).replace('/', '\\') + '\\'
    nao_convertido = str(valores["diretorio_nao_convertido"]).replace('/', '\\') + '\\'


    while ativo:

        if evento == sg.WIN_CLOSED or evento == "Cancelar":
            break
        if evento == "Iniciar":
            banco = valores["banco"]
            usuario = valores["usuario"]
            senha = valores["senha"]
            janela["texto_log"].update(f"processamento do arquivo {banco}. ")

            # os.chdir("C:\csv_to_postgre\\")
            os.chdir(origem)
            logging.basicConfig(filename='conversao.log', encoding='utf-8', level=logging.DEBUG)

            if ('Todos' == 'Todos'):
                for arq in glob('*.csv'):
                    arquivos_csv.append(arq)

                for tabela in arquivos_csv:

                    mensagem = criar.criar_tabela(banco, usuario, senha, tabela, tabela.split('.')[0])

                    if mensagem == None:
                        logging.info(f"Tabela {tabela.split('.')[0]} gerada com sucesso.")
                        sg.Print(f"Tabela {tabela.split('.')[0]} gerada com sucesso.")
                        sg.Print(shutil.move(f"{origem}{tabela}", destino))

                    else:
                        sg.Print(mensagem)
                        logging.error(mensagem)
                        shutil.move(f"{origem}{tabela}", nao_convertido)

        sg.Print(f"\nNenhum arquivo mais para processar no diretório [{origem}].")

        sg.Print(f"Sistema irá fechar em {tempo} segundos.")
        t(tempo)
        ativo = False
    # sg.PrintClose
    janela.close()

layout = [
    [sg.Text("Conversor csv para Postgre")],
    [sg.Text("Banco:  "), sg.InputText(key="banco")],
    [sg.Text("Usuario:"), sg.InputText(key="usuario")],
    [sg.Text("Senha:  "), sg.InputText(key="senha")],
    [sg.Text("Origem", size=(6, 1)), sg.InputText(), sg.FolderBrowse(key="diretorio_origem")],
    [sg.Text('Destino', size=(6, 1)), sg.InputText(), sg.FolderBrowse(key="diretorio_destino")],
    [sg.Text('Não convertido', size=(11, 1)), sg.InputText(), sg.FolderBrowse(key="diretorio_nao_convertido")],
    [sg.Button("Iniciar"), sg.Button("Cancelar")],
    [sg.Text("", key="texto_local_planilhas")],
    [sg.Text("", key="texto_log")],
    # [sg.Output(size=(80,20))],
]

janela = sg.Window("Conversor csv", layout)
# progress_bar = janela['progressbar']

start()