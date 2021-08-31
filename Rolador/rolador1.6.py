# Rolador de dados
# objetivo:
# - Inserir ícone embutido em .exe

from random import randint
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime
import os
import base64
from d20icon import icon


class rolador:

    def __init__(self, root):
        '''Contrutor'''
        root.title("Rolador de dados")
        #root.geometry("600x150")
        #root.iconbitmap(tempFile)
        mainframe = ttk.Frame(root, padding="10 10 10 10")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(2, weight=3)
        mainframe.rowconfigure(2, weight=3)
        #self.y = StringVar()
        #self.x = StringVar()
        self.saidas(mainframe)
        self.buttons(mainframe, self.res)
        self.entradas(mainframe)
        self.menus()

        # Construtor do relógio
        self.clock = ttk.Label(mainframe)
        self.clock.grid(column=6, row=1, columnspan=3, sticky=(E))
        self.tick()
        
        #pass

    def tick(self):
        '''Relógio utilizando recursividade'''
        self.time_string = datetime.datetime.now()
        hora = self.time_string.strftime('%H:%M:%S')
        self.clock.config(text=hora)
        self.clock.after(200, self.tick)        

    def menus(self):
        '''Barra de menu superior'''
        menubar = Menu(root)
        hist = Menu(menubar,tearoff = 0)
        hist.add_command(label='Histórico', command=self.historico)
        hist.add_command(label='Limpar histórico', command=self.apaga_historico)
        menubar.add_cascade(label='Histórico', menu=hist, font=('verdana',10,'bold'))
        about = Menu(menubar,tearoff = 0)
        about.add_command(label='Versão', command=self.sobre)
        menubar.add_cascade(label='Sobre', menu=about, font=('verdana',10,'bold'))
        root.config(menu=menubar)

    def sobre(self):
        '''Controlador de versão'''
        root = Tk()
        root.geometry('160x90')
        root.title('Sobre')
        #root.iconbitmap(tempFile)
        texto = ttk.Label(root, text='Feito pelo Erico. V1.6')
        texto.place(x=20, y=20)
        def OK():
            root.destroy()
        ok = ttk.Button(root,text='OK',command=OK)
        ok.place(x=40,y=50)
        root.resizable(width=False, height=False)
        
    def buttons(self, mainframe, res):
        '''Todos os botões do programa'''
        d4 = ttk.Button(mainframe, width=5, text="d4", command=lambda:self.rolagens(4, res))
        d4.grid(column=1, row=3, sticky=(N,S), pady=5)
        d6 = ttk.Button(mainframe, width=5, text="d6", command=lambda:self.rolagens(6, res))
        d6.grid(column=2, row=3, sticky=(N,S), pady=5)
        d8 = ttk.Button(mainframe, width=5, text="d8", command=lambda:self.rolagens(8, res))
        d8.grid(column=3, row=3, sticky=(N,S), pady=5)
        d10 = ttk.Button(mainframe, width=5, text="d10", command=lambda:self.rolagens(10, res))
        d10.grid(column=4, row=3, sticky=(N,S), pady=5)
        d12 = ttk.Button(mainframe, width=5, text="d12", command=lambda:self.rolagens(12, res))
        d12.grid(column=5, row=3, sticky=(N,S), pady=5)
        #d20_photo = PhotoImage(file = 'C:\Python\Algoritmos\d20.png')
        #photo = d20_photo.subsample(3, 3)
        d20 = ttk.Button(mainframe, width=5, text="d20", command=lambda:self.rolagens(20, res))
        d20.grid(column=6, row=3, sticky=(N,S), pady=5)
        d100 = ttk.Button(mainframe, width=5, text="d100", command=lambda:self.rolagens(100, res))
        d100.grid(column=7, row=3, sticky=(N,S), pady=5)
   
    def entradas(self, mainframe):
        ''' Entradas de valores manuais'''
        qt_dados = LabelFrame(mainframe, text='Quantos dados?')
        qt_dados.grid(column=1, row=1,columnspan=3, sticky=(W))
        self.entrada_qt = StringVar()
        quantos_dados = ttk.Entry(qt_dados, width=15, textvariable=self.entrada_qt)
        quantos_dados.grid(column=1, row=1, sticky=(W, E))

        qt_bonus = LabelFrame(mainframe, text='Bônus?')
        qt_bonus.grid(column=1, row=2, columnspan=3, sticky=(W))
        self.entrada_bonus = StringVar()
        quantos_bonus = ttk.Entry(qt_bonus, width=15, textvariable=self.entrada_bonus)
        quantos_bonus.grid(column=1, row=1, sticky=(W, E))
        quantos_bonus.focus()
              
    def rolagens(self, dado, res, *args):
        '''Comanda as rolagens e os resultados em tela e log'''
        self.label.destroy()
        try:
            qt = int(self.entrada_qt.get())
            if qt < 1:
                qt = 1
        except ValueError:
            qt = 1
        try:
            bonus = int(self.entrada_bonus.get())
        except ValueError:
            bonus = 0
        #dado = int(input('Quantos lados esses dados têm? '))
        #bonus = int(input('Quanto de bonus terá a rolagem? '))
        #
        resultado=[]

        for i in range(qt):
            
            rolagem = randint(1, dado)
            resultado.append(rolagem)
            
        print('-> '+str(qt)+' Dado d'+str(dado), end=': ')
        print(*resultado, sep=' + ', end='\n')
        #self.y = StringVar()
        soma = 0
        for i in range(len(resultado)):
            soma += resultado[i]
        if qt == 1:
            p = ' Dado'
        else:
            p = ' Dados'
        self.x = str(' -> '+str(qt)+p+' d'+str(dado)+': ')
        self.y = self.x + (' + '.join(map(str,resultado)))
        if bonus > 0:
            soma += bonus
            self.z = self.y + (' + (')+str(bonus)+') = '+str(soma)
        else:
            self.z = self.y + (' = '+str(soma))
        
        print('teste x ',self.x)
        print('teste y ',self.y)
        print(self.z)
        self.label = Label(res, text=self.z, wraplength=260)
        self.label.grid(column=1, row=1, sticky=(W,E))
        
        # Plota o resultado no arquivo de histórico
        date = (self.time_string.strftime('%d/%m/%y - %H:%M:%S'))
        file = open('historico-de-rolagens.txt', 'a')
        file.write(str(date) + str(self.z) + '\n')
        file.close()

    def saidas(self, mainframe):
        '''Saída de resultados'''
        self.res = LabelFrame(mainframe, text='Resultado:')
        self.res.grid(column=1, row=4,columnspan=7, sticky=(W,E))
        self.label = ttk.Label(self.res, text=' ', wraplength=200)
        self.label.grid(column=1, row=1, sticky=(W,E))
    
    def historico(self):
        '''Carrega o histórico e mostra na tela'''
        root = Tk()
        #root.geometry('160x90')
        root.title('Histórico de Rolagens')
        #root.iconbitmap(tempFile)
        f = open('historico-de-rolagens.txt')
        self.text = Text(root, width = 80, height = 15, wrap = "none")
        ys = ttk.Scrollbar(root, orient = 'vertical', command = self.text.yview)
        xs = ttk.Scrollbar(root, orient = 'horizontal', command = self.text.xview)
        self.text['yscrollcommand'] = ys.set
        self.text['xscrollcommand'] = xs.set
        self.text.pack(fill=BOTH)
        self.text.place(x=0, y=0)
        self.text.insert(1.0, f.read())
        self.text.grid(column = 0, row = 0, sticky = 'nwes')
        xs.grid(column = 0, row = 1, sticky = 'we')
        ys.grid(column = 1, row = 0, sticky = 'ns')
        root.grid_columnconfigure(0, weight = 1)
        root.grid_rowconfigure(0, weight = 1)
        self.text.config(state=DISABLED)
        f.close()

    def apaga_historico(self):
        message = messagebox.askquestion('Limpar o histórico?',
                                     'Esta operação não poderá ser revertida.')
        if message == 'yes':
            file = open('historico-de-rolagens.txt', 'w')
            file.close()
            
# Formaliza o ícone de string64 para imagem
icondata= base64.b64decode(icon)
## The temp file is icon.ico
tempFile= "icon.ico"
iconfile= open(tempFile,"wb")
## Extract the icon
iconfile.write(icondata)
iconfile.close()
        
root = Tk()
root.wm_iconbitmap(default=tempFile)
rolador(root)
#Bloqueia o tamanho da tela
root.resizable(width=False, height=False)
# Delete the tempfile
os.remove(tempFile)

root.mainloop()
