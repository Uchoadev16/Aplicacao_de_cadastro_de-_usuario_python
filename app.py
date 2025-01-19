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
#importa biblioteca para imagem
from PIL import ImageTk, Image
import base64

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
    def images_base64(self):
        self.btnovo_base64 = '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ckxJUkXp3+DQEDtIs9Cpp57aDi0m98cQGDbcY489mj/84Q/J+9VEwPeKV7wief9BnvrUpzaf/OQn210D4jElSRWlf4NDQ+wgzUL77rtvW7Q1uT+GwDDgcsst13z3u99thxLje9Zy4okntpX04/sPwuR9tkKazHOTJBmMSQOxkvBd73pXtfliY5Ed23333ds9L+P71kAg9dGPfrR58pOfnLz3INRU+/nPf+58MUmabOnf4NAQO0izzI033tisvvrq8UapggDvZS97WfP9738/ed8a2HqJIrMlWb311luvnW8WjylJqiz9GxwaYgdpljnvvPOapZdeOt4o1VAuY5999pmUwqo//elP20CSyv/xfQc58MADm/vuuy85piSpsvRvcGiIHaRZhCG6I488snn6058eb5Sq2Iz7xz/+cfW6Y8xHo/J+blkLfOc733G+mCRNhfRvcGiIHaRZ5K9//WubtSopmJrjkY98ZHPQQQdVzUQRSH3pS18qWgX6+Mc/vrn66qudLyZJUyH9OxwaYgdpFqHg6eabb97MPffc8Uapjmr3V155ZbVq92y3RCD5lKc8JXmvQVjl+atf/So5piRpEqR/h0ND7CDNImxZtMoqq7T7SSb3RmUETQcffHDzxz/+MTmPEr/97W/bLZxKJu+zevTee+9NjjmZWLXKqtJbbrmlue6665pLLrmkufDCC5tLL720nft26623tuf04IMPmrGbgyhSzHeUxR2/+MUv2nuEBSjUs7vmmmvaBS933nln85e//KX6sLs0stK/w6EhdpBmCR74Z555ZltvK7esxQte8ILmSU96UtLeD/O6VlhhhWpV+W+44YY2wzXXXHMl79UPn5Vir5P1IO09zH/961+3c9o+9alPtds1rbTSSs2yyy7bvOQlL2le/OIXt9fwec97Xvt/mfdGO5/nTW96U7PTTjs1p512WvsZCdBqzm3j3AgIOb8c9KGAb63rxnkQgMb36YpgaZjrwvefRSUE9QRZbBi/6667Nm95y1varcFe+tKXNksssUS7M8Xzn//8ZpFFFmkWXXTRtiQKC15WXHHFNqhnziX7m3Ichv0NpKVxpH+LQ0PsIM0S7Ef52c9+tplvvvniTTIQ2whR9T43o0Z2bP/996+Slfre977XPPe5z03eY5B55pmnnWsWjzcshk2vv/76djeDXXbZpXnlK1/ZBlssjmCOWteAl/l1BLrPfvaz2+CMQO6UU05pfvOb31QJYo8//vi23AiBRY5lllmmOeyww9rPGY9ZgvpwJefRs+mmmxaVJiHzyLXk+8M5rLXWWm1wzNxDrjvf6S6/K36GlcLPeMYz2kBtnXXWaY444og2sJuMlcPSjJbeQ6EhdpBmCbIcO++8c1HB1I985CPthPynPe1pyf/WD9mxlVdeuc0kxPPJRcapZBUoGQ8exPF4pcjOMMxIkElWhQcz1zQ3YzcejsHiCrIzBMAEemRghslOHXPMMc3888+fvNcgDAdvv/32VTZ/J4hiDiGBZ3yfLgiEPvOZzzR/+tOfkmNPhGvG8OKXv/zlNsAlE8k/RJgvWbIaN+I4z3rWs5rVVlut+fjHP94WFB4mcyeNlPSeCQ2xgzRL8EB885vf3G6YndwXfVDT6/Of/3w7l4YHam52jOzDxz72sXZIJ55TDoKTJz7xicnxB1l33XXbjdHj8UoQmHzhC19o1lhjjWbeeedtr02NB3vEMQnKyODsueee7TBdPJeuTj/99GaxxRZL3mMQPtsWW2zR/O53v0uOmevoo49u9waN79EVAT0LMHKGBAnA3/Oe97SBLZnKGsFyRJDIdSJbtsEGG7TbbZGBjucizTrp/RIaYgdplvjZz37WzlXqMiQz1jOf+cw2Q8OcH/a0JAiJPzMIc24Y0st5mI7FcB1zdnIfqAQ1O+yww9CLCJiM/+1vf7t561vf2g5v5Z7HMMi6sXsA2biSzMvll1/eXrt43EG4duuvv36bmYvHzMHiBbJHpUErw7dkt7qsyuV7wrw7CvwytDkVq4Z7+EcKw7DHHXdcm4WO5ybNKuk9EhpiB2mWOOOMM9oHW3JPDMAkdFaXMexz/vnnt/+dG4yQPWCYsXT+EVkRHq65gSTzxcjKsRIuHrMrsmEnnXRSO8zF0F3uOdTA+zJHiRWZuQHZzTff3A6nxmN2seaaa7ZDffGYXRHEMq+K4bx47C743FtvvXWnuWLMDbvooouajTfeuB3OLg3+hkFAxveU77rzyDSrpfdHaIgdpFmCOU4lWS2G5MhucAyyJNtuu21R0djXvva1bVX+LhmO6Kyzzip6oLMTAJPheVDHY3ZBIEIwt9RSS2UHoLUx3LvJJps01157bdY1JCigXzxeFwxrU5uuNKPJPCqGiUszVMz3O+ecczr9/liNylZZZBLnRMDcw/eEgIzh4WGH5qUZK703QkPsIM0SZFZy54uBeTe9oSqyYzxkmMsUf24QJk+TMXjggQeScxvk8MMPzy6tAYbnfvSjH2UFLz0MbX74wx9uyxyUTjyviQCDYPoDH/hAm+2K5zsRAil+h/F4Xbzuda9r59uVLCBg7hRDdgsvvHBRlor5gXvttVdbqy0eO6J8CvMZ51TmMiIge81rXtPOW+sSSEojJ70vQkPsIM0CDNNRqiD3QcUDkfk3Y4dcCKa222677MCOB/Kqq67aXHHFFVnBEcNyTN7PfaDzWddee+22rEE85iCs2vvQhz7ULLjggtnvO9kISg899NCsieIsAsj9fYFaaQSzJcHYTTfdVLRgpIdghoxsv/cm0GHPUQoZT4eAeSyGLMkKUki232eQRlJ6T4SG2EGaBRjaIsOT3A8DLLTQQm2dKub+9I5FpoV/8ZPxyA3umMtDGYCcCfWlc55YQUcx1dwaZwRin/vc59riuNMtEOt59atfnbW68Kijjmrnz8XjDEIx1IsvvjgreO6hph3BbO53BAScTNrvN9ePyfpkxPhu8LuOx5gOuH+OPfZYhys1+6T3Q2iIHaRZgAnoJcVeWQVJVflYfJRM2dvf/va2CGbs0w/BDSvrKJQZz3EiPHApOBuPNQiBHyU5+j3QI4KOc889t3nVq15VLRDjOMxjovwBc+1KgpOI606w0vUh/61vfatdFRuPMwhz5bgeuYsGCICHyYpRJuKOO+7oG2yS8Xzve9/bFhaucU17RV353jAcXGOOINmxd77znW2WMJ6/NNLS+yE0xA7SLLDbbru1KxqT+2GA17/+9e2cofEeikyYLsmOUW+KFXZd59IQdJRU3qfPD3/4w6ysDvW82PKmZH7aWFwT5tVts8027VZM7ADAQgLmUO2xxx7txPRhh9Uod9FllSFKM6PU6OL33PV31UMplJLgD+xi8PWvf33g741tiWpkLwm8GM6msDG/H977a1/7Wrtwg8UrwwZ7ZMeYZxnPXxpp6b0QGmIHacRRTmKjjTaKN8ZArIBjrtbdd9+dHBN33XVXW9m8pBAre1ayAfN4Qd5YzIui8n/JrgFsLcR7xGNOhKHT/fbbr61WX/rwJcCiwOruu+/eBkAcc2xQwdwhsorUXNtqq63aLEzpexEId81acR5kueIxBiHYOfHEE7Pmp7H/JPXYSjJLfOcYWh40aZ8gm30kS96jh0wxG88TbJKFixu289+sJGWYkfphpe9FsMg/hnJ2D5BmvPReCA2xgzTimATNqrjkXhiAjADzuyaqDUYQwIOM4CM3O8FDl0r2g2oxUVqCgI9VcvEYg2y22WZZNbLYson9JXN3GOihH/0JXghU+03a5qFPcVLOsXS+ExlG9o7ssjqV9yOgyA38CEzJQI2dM9gP3wkymWyGHo81CN8hVr9SKywOi4913333tdt6lXwnesiGsVKTrC+fbaJ/FNBOEMWm4gwzx+N09cY3vrFoIYk0Y6X3QWiIHaQR981vfrOoFAV1vQi2+j2IyRxsvvnmRXWkGAKiDlW/oIWq89SOKgmQGB7sEqiAhy4ZGQLQeJyumNfG8BbBwkQP97EIOBi+IsOTG8yCYWeGVAn84rHH84Y3vCH7OjLp/5BDDuk8746sGOdUEmASXPJe/arXc11ZPVmyMriHjNiOO+7YDvH2++6NxRw4FgqUzoFj1wZq7HX5XkgjIb0PQkPsII04NljO3eAbbJ3EUFu/BxYBxVe+8pW2uGrsPwhZFybY9xu+ufDCC9vhtZJghRWfg+Yd9bCgoDQoAg94AjGCv5wHLsNjTEIvyfIQjFAqhIC13++ohyApt1gv58UWWIMymOC7wFwxCp6WXEeCbrbs6vdZqHfH5uUlw9YgSKTm2kTzICfCz5LxLCk8DK4HgXfOcK80o6X3QWiIHaQRxhAj85dyVz2CGkldJoizXRAP+twJ6czBYWUlGYPxHsDM2aGsBkFb7DsIc7F6uwYMwvtQU6zkGoE5c0zKn2g4tx8+NxP7CWDicbtgXhxbVfUb1uuhgG3uDgwEEbvsskvfgLmHwHLTTTctyoqxYOK8887rO/+Na8XPsC1Vyfwtvp9kBxmO7hqkj0XWj8LJJVlgMNzb5TpKIyG9B0JD7CCNMGpRUYKiZHiFQqEEWvGYEVkDNtEuyRqw4m6ihxTBDUFSSX0sCoYyhBqPOR4m0xMUlgx7ERQw3Hr11VdnZVrGYjI6pTTisbtYcsklm7PPPrtvENPDXK6S3xEV/7vUhSPzs8gii2RfR67hFltsMfC7xvfhgAMOaLO8ue8B9mWlxEtu9rKH86PYccmCFRAMd7mO0khI74HQEDtII4wHPYU7SzIJlGPoWseKh8xaa62VnTXgvMg2EBDFYzIkRY2mkowV+2d2yVSRIfniF7/YrkyMx+iCDBxbNY0XTHbFvLk3velNybG7oPTEN77xjU7DX3wXKBsRjzEIw6i/+93vkuONxfuzQXfJ74r5jATz42VHx+IfFmS2Skq0YP31129Ll5QEYiCIYzeK0nmFZKgHBZzSyEjvgdAQO0gjjIccdY6S+2AA5hYxnDPoAdnDA465Y1Rcj8cahPlWzB2LQ208fFmdmDv8SdaEAKnLUBQTs5m4XzK0xhAec7bIinV5r4lQOmTDDTdMjt8FQSTBZL9FFj0EfSVz+wiIGaKLxxuLwrwEerkZK4YnycAOCvZw5plnFtW1AwHcV7/61c7/uBgPASc7M5QUTwalTLp8TmkkpPdAaIgdpBHFg4eNuUsm71OUlGAoHrOfYeYMUXojPvCp/F9S7JU5ZszDiuc3HuaVUSk+d5UhmES+//77t6sn43FzMDl+k002SY7fBXXAKLvQJRjrBbe5WVIyl+yvGI/XQ1b0/e9/f/Y15DzICLJ4okvQv/feexdnpdhEPPf7HBFwM9RbMocRlGjpuvJVmvHSeyA0xA7SiKJwJg/J3BV0oGhn7r/imQhPdowaU7mr6RjeYjXi2KDi05/+dFFtJx68l1xySXJ+Edk8JoQzTJZ7viBQpMxCbnX6iGCO4qPx+F2QjeKadxmmpM4VleZzh5KpkcWq2ng8cA3POeecdtus3IxVb7uqLuVHyJqWlpbIWYTQD/PyWFBS8p0Ec+8mKqAsjZz0HggNsYM0othgmw2lczMW2GeffTplWyKyDwxrlTw02Y+Qc+7N6SGQLJksTWDDceK5RQRRxxxzTPHDlVIMw8xB6iFbwmePx++iN2esS0DYC85zr+lKK63UDlnH44E5UFSXLyk1wdBs1+tHIMlihdyAD2SyGKLs8j79EPCy+XnpMCUrbp0zplkjvQdCQ+wgjShKRvCwTu6BAXhYkwEoeXgRFFCPiVV18biDsNqtN6+HIaGVV145e0iNLAgFPbusWuNnGPoqCSTwwQ9+sJ1zFo+bi4CErE88fhc5qyl7E9AprhqP08+yyy7bls+Ix+P70dvEPXdeH0PnZNS6BJG4+OKL2yHZeJwu2Hrr0ksvTY6Zi+FkdqTIvX497H3Z5XspjYT0HggNsYM0ohi+KillwLAdex7G43XFFkSsrMsNpJhk/ba3va0NTshssc1S/JlBGPpieLPLRG0yUszVKlkBiJNPPrkoexgxpFpa2oJ+V155ZacFBARsJdv6ENAzHBuPR6V8hv9y53ExTLrDDjtkBSYsUiiZ+4iumdJBhi1tQVmNLt9LaSSk90BoiB2kEcWDsqRGV68QazxeVwQGTKDPnejMEBSr/Qhyzj///KJMCFX0WXXXJeNyyy23NK997WuLhnEJ4C6//PKi7GHEtSrZyxFMgGdouMt58DNsjZUboJOxpIZYPB7ZJva7zM2KMaePTFuXc+6hRlfJwhDOjfsgJ/CbCEOla665ZvacO5CxzdkRQprx0vsgNMQO0ohi4nVuoEFAVGPVF/OTCBRy546x/Q4TndlXMjeDA4q9DtpSp+fGG29sq7mXTN5//vOf33eFYVdMTKcMR0nWh98tmb2c3xULFgh4c+ZeUbWf4eN4LOpm5WbF+JwHH3xw3/0nx0MmLTfoQ2+z+657a/ZDLTwWKpR8X7iGw/wDR5px0vsgNMQO0ggiE0CgkXz/B2Dl5UEHHdRpL8J+yHoce+yxbYX9+B6DMEeJrZhy53IxLMqkcIZJ4/mMh7IWJXW3QEaI4dR4zFwEUltvvXXRUCk1uvbbb7+s0hpMxGdoMyewIUBmDuHY41CzjMAkZyi6V8qi616aPWST2E8yJ4Ds4ftHbbAaw8ms9i2powdKitQYKpVmjPQ+CA2xgzSCqLZeUlWecg1U3u9SKmEQ6oYxByx3E2yyaWQ0crN6zOVhFWjX4IS5VmS44nG6eP3rX99p385Brrjiina1Yk5w1MNw42mnnZb1uyKbR6Cbk7EkCGKz+V4AxRAww4a5c6f4PlKnK3feFD+/2WabJcfrgtIfNb7P/ONiyy23zP7MPRR8rTFUKs0Y6X0QGmIHaQQdddRRRfPF2DqJlWuxGn4JHoDHHXdcG+DlZjX4+dw+zFHLedjzOUu2BwJzh7pm4CbChHomdZNtyf2soDDvT37yk6wsE+fMMHRugPyxj33s/1Zs8p5kuHKH6yirQQCbM1cMrAKlXEo8Xhc5pT/6Ydi9dFsx5pgdccQRVe4pacZI74XQEDtII4jyDrmZJQICSix0rf00CMcgE0MNrZxMTCkCKzJNXSdJ87OlmTGq9g8bjFEAlH0fS4rygmxR7jkwd4qSHLmT4RkOJbjG0UcfnT1cR0DOpP0uJTgizrl0hwIWRrAgZNjMGAFd7oKUnkUXXbQtPxKPKY209F4IDbGDNGKYHF1S0Z1syTbbbFO1SjgPQaqslwyZ5lpxxRWztrxh3hPlM0qyUrxX3L4pF6s+ef+SbAtZKco9dM0C9pBFO+SQQ7KH2/baa682KGLRA0PPOSsK+XwUPC2tgM85k1XLzcSBfVnJzg4zZ4xVlGzzlfuPG/DdYjeLm266KTmuNNLS+yE0xA7SiGEuFPOQku/+AKz4Yjil9KE5EUpI8EAqCTpybLvttllbOBG4MRG/5LyYr8VE9NIM4v33398GzCUT90EtOILJkveninzuSlXKQxDkU7suZ7NuAij2HSULGc8jB1X+qUMXjz8IQScLUkq/0/xjgiLGpaVHqNbPatlhF8RIM056P4SG2EEaMTwwS+ZCkUWg2GvJUFI/zJXhgVa6jUxXbG2U89Ajs1VaZ4wJ92eccUbRXCSyWb2Vpl2DmrEIHgk8SyeEM+SWuzPD9ttv3wavzDfLGVblM1KEt8v+k/2U1hkjGGQ4t2SxBcPd1FJjSDonE9jD75ZVlOxS4HwxzTrpPREaYgdphJApOeyww7LrP4EJ4dRSKsm2DMLcJmqAlQQ+XV144YWd54uBshIMP5Vmp3baaad2Ync8bj8MuXGe7BlaMuwGAu1TTz01a+L+WBdddFG7hVE8bj+U32BYle9I10wimSxKjXSt+9YPKyJLg/nllluu/czxmIPw/aDiPvdSSdBM8MjczZw6cNLISO+J0BA7SCOEsg4MKZUEGOuvv347PyYeswYCvCOPPLJZYIEFkvetgQnlPPTj+/ZDFu2jH/1o8V6DDBVS0b7rvC2yaKzgpLRETnZpLAIcam7ddtttyfG7YlEFqyHjsfvhPcmK5QT57KBA0Nj1+vTDkHDpUCFB0c4779wOs3b5hwY/w56jzJPje1UaNDMf8IILLqieaZZmhPSeCA2xgzRCyGyttdZaRfNrqIzetUZXCYa5OLeSIZ9B1lhjjeaOO+5I3rMfHrpke1hRWfLAJctHvTGGdvtVeOd9GFKkaCjZQQKxkkwLfdjuidpiJcOjPZxL7gIPrm/OdeLnmLTPHL4uAdAgfF6uXUk9NlD5n1ppZKn6ZemY6H/ttde2w7L0Kfk9gfNk1Sr7Wcb3kGaF9L4IDbGDNEIYAltyySU7DyWNRZZnmIf8IGRIKIvAXoelD7mJ7LrrrlnzxXquueaadoJ56fApGUgCMubEkVUcO0zK/8/Dn5IOBxxwQBtIEYiWfnaCOIZGCTqHCXAIRiipEY/fDxuw5wTR7Gxw9dVXZw0bD8KWSOw6EN+rC645mbX999+/ueqqq5LvCsE02xUx73Dttdduh0RLf09gOJfvVs3PL80o6X0RGmIHaUTwkGVydu5G0OAhx8NzmIf8IBybgqHUMivJ3E2EQIoit/0yHhNh6GrPPffM3nppLGqoMSGeieKUjaCUAisW995772aLLbZoJ3GTZSkJkMdaddVVm0suuaTKsBdD2TkBKJmursFJb5um0hWME6FWV+6+mmNx/RkmZ89Wfudsk8RCCoaqCfRWW221dhELJV5K3wOsVD300EP7ZkulkZfeG6EhdpBGBP/aJxgomQNFdfEaey0OwjAQw0W5RUP74QF6+umnJ+/VBQEim2cvs8wyyXFzEKwQYHLtCYZ5IPNQJ+DpOrTXD8EcgXatB/ynPvWpoQLQifBZCWrICtUO7H/72982m2++edGqyh6CLIYQKXlBEVdWe3IdCKhpHyYIA79zso5TcS9J01p6f4SG2EEaETys2DamZPI+E7TJEsVjToYbbrihHQqqEaRglVVWaWurxffpijlU7B1YM1tXEwEemZya8/kIXksryvdDpX0yg3EYsAYyglTTX2SRRYYOmiYD3x/KYNTKXkozWnqPhIbYQRoR/GucIbHc4TAebOw9OJnzxcbiQcXcsZIM3ngYHhxmFSgZHFa9lc61m0ysXqSsRGmB14kQvJbUouuH7BLbFlFtvmTIeBA+/80339xW4y/Zd3Wyrbzyys1ZZ53VBqI1f1fSjJTeI6EhdpBGBA/YkuX/PNio4zSVDxBKMyy//PLFq+N6yEaQNRq2qCiV1hniJVs0XbIuDMcx54whv9qZFuq+saAgvucwmDdHMDLM1kODMCGezBMrK6fL7wmUOaEIMN/DqbyPpGkrvU9CQ+wgjQj2gCyp47X00ku3maF4vMnEA+vjH/94u0ovnk8OPi9Zthq1rAgQ2ZuTjN2cfNDz3qycZIUopUpqB2IgqFl22WWT9y5FRnGfffbJLoJbgsCZ+XMMidYa6i5FNpDAkHIjtebzSSMhvV9CQ+wgjQgmDpcUE6XYK/O44vEmG8VH3/CGNww1V4sSAkzArxGwMLR23XXXtcNgpdXeh8W1IMvC9j9kryZjuK+Ha5+zorIf9visUWm/K4JvFiGQ3av1GXKRRWVBAYV8a/xjQBop6T0TGmIHaUQwZyV3zhM/T4HLqZq8PxaZBLZuGmZokL0lCepqDQ2xhyDzs6i+zkq73Os5DALAddZZp91blPpktT7TRIZdmdhDJpEh3qkOSMjCnXDCCe3WUiWLVkqRDWN+4Uc+8pH2uzJVcy2lGSW9d0JD7CCNAB5MPCCS7/sAzBdj8v6cGGIh2PjRj37UFk0tyW4w34zVo6wijcceBkN4ZKUOP/zwtuTHMJm7LghEyYZ98pOfbKu/T9UEcIYVh11EwbmzqwIZxak457F4P1bCsgMCgSXlKuL51UbA/O53v7vduYEtkyzqKk0gvX9CQ+wgjQCG6qhsn3zfB2DSNfNv5tS/7smmfOITn2jrcsVzG4T6UAceeGDVkg89POiZjM2iCIqCMgxHFmnYBQcggCG7wnw5qv8zJMlQF0HYVA3z4fjjjy+aYzj2c7Bg5KSTTpryrNhYDFHffvvt7Xmst9567XeJ61uabR2L3zdD/+wzSQaZXSpYuUsGNZ6HpDHS+yk0xA7SCGBDZoptrrTSSlm23HLLKZ3rMx42geY84rkNQkaGrAgTuuMxa+kFZZwjQdmGG27YLLfccu0m2ARnXSeQUwyUYc/FF1+8HVZjXhq1vigDQaX6OXH9r7jiimaDDTZIrmtXTFzfd9992yziVGfFxsP34JZbbmlrkW233XbtOVKxf9555+0cRPNz/DxlP8iKvu1tb2szllwrMmEGYVJH6f0VGmIHaQTcf//97WrAW2+9NQtzk+ZUVqyHzAYbSsdzG4QMBcOrUxEIECwxJMY1vvzyy9ssDCU1KJbLptsUsWW4lUCLuXv8/2uuuWYbvFF7i+2H2CLpnHPOaVdI8nkpATEV5z4R3p99LuN17YprQYAyJwLJiXA9ydLdfffd7dAp5SaYz7bttts2G2+8cZs5W3311dtCwSuuuGI755D/XnfddZuNNtqorelG0M2m7gyh8x0jGHc4UsoUY6+kIXaQpI542PNg5oFPAHzPPfe0D2xWo1IP7LLLLmuDNeZ+sbCATA1z2gjkCBwJfKdT8DLKuM5ky8g8MpTN74HCyARpDD9feumlbcDFf5OhJDAluOTnCVQNwKQhxNgraYgdJGlIBGkgAEDvv+dk5kspf0/SFImxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omxV9IQO0iSJKmeGHslDbGDJEmS6omx1zgNaSdJkiQNL8ZcBmOSJElTKMZcEwZjBmSSJEl1xVirp2matNFgTJIkqa4Yaz2sDcP6BGMGZJIkSXXEGMtgTJIkaYrE+GpMIPZ/wZgBmSRJ0iSJsdVEwZgBmSRJUmUxpgqBWBt//c9/jPPDBmSSJEkFYiw1TiDWxl9JwzidDMgkSZIyxBgqJxjjFTsZkEmSJHUQ46YBgRiv8VsHBWQGZZIkSf8rxkodAjFeE/8vBmSSJEndxBipYyDGq///akAmSZI0sRgXjWPQa/BPdAnIEE9OkiRpVMU4aBxdX91/0qBMkiQpjX3GkfPK++muARniiUuSJM1kMdaZQO4rv4cBmSRJmk1ifDOB0ld5z5ygDPGDSZIkTWcxlpnAsK/hj2BQJkmSRkWMWwao8apzlNyADPHDS5IkzSkxThmg5qvu0UqCMsQLIkmSNNliPNLBZLwm56ilQRnihZIkSaolxh0dTeZrco/+0Ct+oM7iBZQkScoV44sMU/Gamnd56BU/YJZ4YSVJksYTY4hMU/2a+nccNijriRdekiTNTjFGKDSnXnPunR96xQtRLP5iJEnSaIoxwBCmw2t6nMVDr3iBhhZ/eZIkaWaJz/YKpttr+p3RQ6944aqJv2RJkjQ9xGd2JdP9Nf3P8KFXvLCTIn4pJElSXfHZO0lm0mtmne2YV7zoUyJ+oSRJ0n/F5+YUmsmvmX32Y17xlzLtxC+sJEnTVXyGTTOj9hq9TzTmFX95kiRp5hn11/8DBumk94cboz4AAAAASUVORK5CYII='
class aplicacao(funcs, relatorios):
    #construtor
    def __init__(self):
        #atributos
        self.root = root
        self.images_base64()
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
        
        #chamando a imagem com o objeto PhotoImage em base64
        self.imgNovo = PhotoImage(data=base64.b64decode(self.btnovo_base64))
        #posicionando a imagem no local
        self.imgNovo = self.imgNovo.subsample(9,9)
        
        self.bt_novo = ttk.Button(self.frame_1, image=self.imgNovo, command=self.add_clientes)
        self.bt_novo.place(relx=0.58, rely=0.1,  relwidth=0.1, relheight=0.15)
        
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
        
        def Quit(): self.root.destroy()
        
        #imprindo em modo cascata o menu de opções
        menubar.add_cascade(label = "Opções", menu = filemenu)
        menubar.add_cascade(label = "Relatorios", menu = filemenu2)
        #adcionando comandos para os menus
        filemenu.add_command(label="Sair", command= Quit)
        filemenu.add_command(label="Limpa Cliente", command=self.limpar_tela)
        
        filemenu2.add_command(label="Ficha do cliente", command=self.geraRelatCliente)
 
aplicacao()