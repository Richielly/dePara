import tkinter as tk
import converter
import configparser
import os
from glob import glob

config = configparser.ConfigParser()
config.read("config.ini");
OPTIONS = ['Todos']
class Application:
    def __init__(self, master=None):

        if not os.path.exists('C:\csv_to_postgre'):
            os.makedirs('C:\csv_to_postgre')

        diretorio = os.chdir(config['default']["path"])

        for arq in glob('*.csv'):
            OPTIONS.append(arq)

        self.opcoes = tk.StringVar(master)
        #root["bg"] = "gray"

        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = tk.Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = tk.Frame(master)
        self.segundoContainer["pady"] = 10
        self.segundoContainer.pack()

        self.terceiroContainer = tk.Frame(master)
        self.terceiroContainer["pady"] = 10
        self.terceiroContainer.pack()

        self.quartoContainer = tk.Frame(master)
        self.quartoContainer["pady"] = 10
        self.quartoContainer.pack()

        self.quintoContainer = tk.Frame(master)
        self.quintoContainer["pady"] = 10
        self.quintoContainer.pack()

        self.sextoContainer = tk.Frame(master)
        self.sextoContainer["pady"] = 10
        self.sextoContainer.pack()

        self.setimoContainer = tk.Frame(master)
        self.setimoContainer["pady"] = 10
        self.setimoContainer.pack()

        self.oitavoContainer = tk.Frame(master)
        self.oitavoContainer["pady"] = 10
        self.oitavoContainer.pack()

        self.titulo = tk.Label(self.primeiroContainer, text="Criar Tabelas no banco Postgre a partir de uma planilha CSV.")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.bancoLabel = tk.Label(self.segundoContainer, text="Banco   ", font=self.fontePadrao)
        self.bancoLabel.pack(side=tk.LEFT)

        self.banco = tk.Entry(self.segundoContainer)
        self.banco["width"] = 50
        self.banco["font"] = self.fontePadrao
        self.banco.pack(side=tk.LEFT)

        self.usuarioLabel = tk.Label(self.terceiroContainer,text="Usuário ", font=self.fontePadrao)
        self.usuarioLabel.pack(side=tk.LEFT)

        self.usuario = tk.Entry(self.terceiroContainer)
        self.usuario["width"] = 50
        self.usuario["font"] = self.fontePadrao
        self.usuario.pack(side=tk.LEFT)

        self.senhaLabel = tk.Label(self.quartoContainer, text="Senha   ", font=self.fontePadrao)
        self.senhaLabel.pack(side=tk.LEFT)

        self.senha = tk.Entry(self.quartoContainer)
        self.senha["width"] = 50
        self.senha["font"] = self.fontePadrao
        self.senha["show"] = "*"
        self.senha.pack(side=tk.LEFT)

        self.planilhaLabel = tk.Label(self.quintoContainer, text="Planilha ", font=self.fontePadrao)
        self.planilhaLabel.pack(side=tk.LEFT)

        if len(OPTIONS)>0:
            self.planilha = self.opcoes.set('***** Planilha *****')
            self.planilha = tk.OptionMenu(self.quintoContainer,self.opcoes, *OPTIONS)
            self.planilha["width"] = 45
            self.planilha["font"] = self.fontePadrao
            self.planilha.pack()
        else:
            self.diretorio = tk.Label(self.quintoContainer, text='Local das planilhas esta vazio. ', font=self.fontePadrao)
            self.diretorio["width"] = 45
            self.diretorio.pack()

        self.tabelaLabel = tk.Label(self.sextoContainer, text="Tabela   ", font=self.fontePadrao)
        self.tabelaLabel.pack(side=tk.LEFT)

        self.tabela = tk.Entry(self.sextoContainer)
        self.tabela["width"] = 50
        self.tabela["font"] = self.fontePadrao
        self.tabela.pack(side=tk.LEFT)

        self.gerar = tk.Button(self.setimoContainer)
        self.gerar["text"] = "Gerar Tabela"
        self.gerar["font"] = ("Calibri", "12")
        self.gerar["width"] = 20
        self.gerar["command"] = self.criar_tabela
        self.gerar.pack()

        self.mensagem = tk.Label(self.setimoContainer, text="", font=self.fontePadrao)
        self.mensagem ["width"] = 200
        self.mensagem.pack()

        self.diretorio = tk.Label(self.oitavoContainer, text='Local das planilhas: '+config['default']["path"], font=self.fontePadrao)
        self.diretorio["width"] = 200
        self.diretorio.pack()

    #Método verificar senha
    def verificaSenha(self):
        usuario = self.nome.get()
        senha = self.senha.get()
        if usuario == "NotaCasteloBranco" and senha == "es74079":
            self.mensagem["text"] = "Conexão ao banco feita com sucesso"
        else:
            self.mensagem["text"] = "Erro ao tentar conexão com o banco"

    def create_all_tables(self):

        criar = converter.Converter()


        for planilha in planilhas:
            pass
            # mensagem = criar.criar_tabela(self.banco.get(), self.usuario.get(), self.senha.get(), self.opcoes.get(), self.tabela.get())

    def criar_tabela(self):

        config = configparser.ConfigParser()
        config.read("config.ini");

        if len(OPTIONS) == 0:
            self.mensagem["text"] = 'A pasta de planilhas esta vazia.'

        if self.tabela.get() == '' and self.opcoes.get() != 'Todos':
            self.mensagem["text"] = "Informe o nome da tabela que será gerada no banco de dados."

        elif self.opcoes.get() == '':
             self.mensagem["text"] = "Informe a planilha que será utilizada para gerar a tabela no banco de dados."
        else:
            criar = converter.Converter()
            
            if (self.opcoes.get()=='Todos'):
                arquivos_csv = []
                for arq in glob('*.csv'):
                    arquivos_csv.append(arq)

                for tabela in arquivos_csv:
                    self.mensagem["text"] = "Tabela " + tabela.split('.')[0] + " em processamento ..."
                    mensagem = criar.criar_tabela(self.banco.get(), self.usuario.get(), self.senha.get(), tabela, tabela.split('.')[0])

            else:
                mensagem = criar.criar_tabela(self.banco.get(), self.usuario.get(), self.senha.get(), self.opcoes.get(),
                                              self.tabela.get())

            if mensagem == None:
                self.mensagem["text"] = "Tabela gerada com sucesso."
            else:
                self.mensagem["text"] = mensagem

root = tk.Tk()
root.geometry('900x400')
root.title("CSV To Postgre")
root.iconbitmap('equiplano-logo-vertical.ico')
Application(root)
root.mainloop()

#pyinstaller --onefile -n csv_to_postgre --noconsole main.py
