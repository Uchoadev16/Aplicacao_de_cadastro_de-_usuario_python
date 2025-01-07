#importando o tkinter
from tkinter import *
from tkinter import ttk
import sqlite3

#criação visual para documentos PDF
from reportlab.pdfgen import canvas
#tamanho padrão da pagina criada
from reportlab.lib.pagesizes import letter, A4
#permite trabalhar com fontes
from reportlab.pdfbase import pdfmetrics
#Esta classe permite registrar e usar fontes TrueType 
from reportlab.pdfbase.ttfonts import TTFont
#criação do arquivo pdf
from reportlab.platypus import SimpleDocTemplate, Image 
#permite abri URLs em um navegador
import webbrowser

#instanciando o objeto tk para criar a tela
root = Tk()

class relatorios():
    def printCliente(self):
        #abrindo um arquivo em um navegador padrão
        webbrowser.open("cliente.pdf")
    def geraRelatCliente(self):
        #estilizando o pdf
        self.c = canvas.Canvas("cliente.pdf")

        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.fone = self.fone_entry.get()
        self.cidade = self.cidade_entry.get() 
        
        #setando as fontes
        self.c.setFont("Helvetica-Bold", 24)
        #a sua localização e o que terá escrito nela
        self.c.drawString(200, 790, 'Ficha do Cliente')
        
        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Codigo:')
        self.c.drawString(50, 670, 'Nome:')
        self.c.drawString(50, 630, 'Telefone:')
        self.c.drawString(50, 600, 'Cidade:')
        
        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigo)
        self.c.drawString(150, 670, self.nome)
        self.c.drawString(150, 630, self.fone)
        self.c.drawString(150, 600, self.cidade)
        
        #crinado uma linha 
        self.c.rect(20, 720, 550, 200, fill=False, stroke=True)
        #abrindo a pagina
        self.c.showPage()
        #salvando o arquivo
        self.c.save()
        #abrindo o pdf no navegador
        self.printCliente()
class funcs():
    def limpar_tela(self):
        #limpando os dados das Entrys
        self.codigo_entry.delete(0 ,END)
        self.nome_entry.delete(0 ,END)
        self.fone_entry.delete(0 ,END)
        self.cidade_entry.delete(0 ,END)  
    def connect_bd(self):
        #se conectando com o banco de dados SQLite
        self.conn = sqlite3.connect("clientes.bd")
        #criando atributo para executar os comandos SQL
        self.cursor = self.conn.cursor(); print('banco de dados criado com sucesso!')       
    def desconecta_bd(self):
        #desconectando com o banco de dados
        self.conn.close()      
    def monTabelas(self):
        #se conectando ao banco de dados
        self.connect_bd(); print("conectando ao banco de dados")
        #escrevendo o codigo SQL
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_cliente CHAR(40) NOT NULL,
                telefone CHAR(20),
                cidade VARCHAR(40)
            );
        """)
        #executando o codigo
        self.conn.commit()
        #se desconectando do banco de dados
        self.desconecta_bd()   
    def variavies(self):
        #colocando os valores de cada entry dentro dos entrys
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.fone = self.fone_entry.get()
        self.cidade = self.cidade_entry.get()     
    def add_clientes(self):
        
        #fazendo a inserção de dados no banco
        self.variavies()
        self.connect_bd()
        self.cursor.execute("""INSERT INTO clientes (nome_cliente, telefone, cidade) VALUES(?,?,?)""", (self.nome, self.fone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()      
    def select_lista(self):
        
        #deletando todas as linhas do treeView
        self.listaCli.delete(*self.listaCli.get_children())
        self.connect_bd()
        #vazendo o select
        lista = self.cursor.execute("""SELECT cod, nome_cliente, telefone, cidade FROM clientes ORDER BY nome_cliente ASC;""")
        #imprindo os dados no treeView
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()              
    def OnDoubleClick(self, event):
        
        self.limpar_tela()
        #fazendo o select de todos os dados que estao no item do treeView
        self.listaCli.selection()
        #fazendo a inserção dos dados nas Entrys
        for n in self.listaCli.selection():
            #retonando todos os valores do item na linha pelo loop
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            #inserindo os dados
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.fone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
    def delete_cliente(self):
        #fazendo o delete do item 
        self.variavies()
        self.connect_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_lista()
    def altera_clientes(self):
        #alterando o item
        self.variavies()
        self.connect_bd()
        self.cursor.execute("""UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ? WHERE cod = ? """, (self.nome, self.fone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_lista()  
    def busca_cliente(self):
        self.connect_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """SELECT * FROM clientes WHERE  nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpar_tela()
        self.desconecta_bd()
class aplicacao(funcs, relatorios):
    #construtor
    def __init__(self):
        #atributos
        self.root = root
        self.tela()
        self.frames_de_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.monTabelas()
        self.select_lista()
        self.Menus()
        #função para deixa a tela em lupim 
        root.mainloop() 
    def tela(self):
        #title definir o titulo da tela
        self.root.title("cadastro de clientes")
        #configure para definir a cor da fundo
        self.root.configure(background="#2D2D2D")
        #geometry para definir o tamanho da tela 
        self.root.geometry("700x500")
        #resizable para saber que a tela é responsiva verticalmente ou horizontalmente
        self.root.resizable(True, True)
        #maxsize para definir o tamanho maximo da tela 
        self.root.maxsize(width=900, height=700)
        #minsize para definir o tamanho minimo da tela
        self.root.minsize(width=500, height=400) 
    def frames_de_tela(self):
        #criando um frame dentro da tela root
            #bd = borda, bg = background da borda, highlightbackground = cor da borda, highlightthickness = largura da borda 
        self.frame_1 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=3 )
        #deixando o frame responsivel
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        
        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    def widgets_frame1(self):
        
        #criando o botão
            #text = colocar o nome do botão
        self.bt_limpar = Button(self.frame_1, text='Limpar', bd=3, bg='#107db2', fg='white', font=('verdana', 8, 'bold'), command=self.limpar_tela)
        #posicionando
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)
        
        self.bt_busca = Button(self.frame_1, text='Buscar', bd=3, bg='#107db2', fg='white', font=('verdana', 8, 'bold'), command=self.busca_cliente)
        self.bt_busca.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        
        self.bt_novo = Button(self.frame_1, text='Novo', bd=3, bg='#107db2', fg='white', font=('verdana', 8, 'bold'), command=self.add_clientes)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        
        self.bt_alterar = Button(self.frame_1, text='Alterar', bd=3, bg='#107db2', fg='white', font=('verdana', 8, 'bold'), command=self.altera_clientes)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        
        self.bt_apagar = Button(self.frame_1, text='Apagar', bd=3, bg='#107db2', fg='white', font=('verdana', 8, 'bold'), command=self.delete_cliente) 
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)
        
        #labels e botões
        #codigo
            #criando um label
        self.lb_codigo = Label(self.frame_1, text="Codigo", bg='#dfe3ee', fg='#107db2')
            #posicionando
        self.lb_codigo.place(relx=0.05, rely=0.05)
            #criando a entry para colocar dados
        self.codigo_entry = Entry(self.frame_1)
            #posicionando
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)
        
        #Nome
        self.lb_nome = Label(self.frame_1, text="Nome", bg='#dfe3ee', fg='#107db2')
        self.lb_nome.place(relx=0.05, rely=0.35)
    
        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.8)
        
        #telefone
        self.lb_fone = Label(self.frame_1, text="Telefone", bg='#dfe3ee', fg='#107db2')
        self.lb_fone.place(relx=0.05, rely=0.65)
    
        self.fone_entry = Entry(self.frame_1)
        self.fone_entry.place(relx=0.05, rely=0.75, relwidth=0.4)
        
        #
        self.lb_cidade = Label(self.frame_1, text="Cidade", bg='#dfe3ee', fg='#107db2')
        self.lb_cidade.place(relx=0.5, rely=0.65)
    
        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.5, rely=0.75, relwidth=0.4)   
    def lista_frame2(self):
        
        #criando uma tabela
        self.listaCli = ttk.Treeview(self.frame_2, height=3, column=("col1","col2","col3","col4"))
        #escrevendo no cabeçalho da tabela
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Codigo")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade") 
        
        #tamanho da coluna da tabela
        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)
        #posicionando a tabela
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
        #criando uma barra de rolagem
        self.scrolLista = Scrollbar(self.frame_2, orient='vertical')
        #ondem essa barra de rolagem vai mecher
        self.listaCli.configure(yscrollcommand=self.scrolLista.set)
        #posicionando a barra de rolagem
        self.scrolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)
    def Menus(self):
        #instanciando o objeto menu
        menubar = Menu(self.root)
        #configurando na janela principal que a tela tera um menubar
        self.root.config(menu=menubar)
        #criando opções para o menubar
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        #imprindo em modo cascata o menu de opções
        menubar.add_cascade(label = "Opções", menu = filemenu)
        menubar.add_cascade(label = "Relatorios", menu = filemenu2)
        #adcionando comandos para os menus
        filemenu.add_command(label="Sair", command= quit)
        filemenu.add_command(label="Limpa Cliente", command=self.limpar_tela)
        
        filemenu2.add_command(label="Ficha do cliente", command=self.geraRelatCliente)
 
    
aplicacao()