# OBJETIVOS
# criar um campo para inserir um nome para o arquivo gerado. - OK
# analisar a pasta e verificar se não há um arquivo de mesmo nome.



import pyqrcode
#from pyqrcode import QRCode
import png
import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showerror

def cria_qr():
    try:
        base = url.get()
        qr = arquivo.get() + '.png'
        if base != '' and qr != '.png':
            #Gera o QR code
            img = pyqrcode.create(base)
            #Salva o QR code
            img.png(qr, scale=6)
            url.delete(0,tk.END)
            arquivo.delete(0,tk.END)
            #Abre o arquivo gerado
            os.startfile(qr)
        else:
            showerror('Erro!', 'Insira uma url \ne um nome para salvar o QRCode.')
    except:
        showerror('Erro', 'Alguma coisa deu errado, \nTente novamente')

root = tk.Tk()
root.title('Gerador de QR Code')
root.geometry('300x500+500+150')
#root.iconbitmap(' ')

url = ttk.Entry(root, width=49)
url.place(x=0,y=100)
url_label = Label(root, text='Insira a url:')
url_label.place(x=0,y=75)
url.insert(tk.END,'www.google.com')
url.focus()
arquivo = ttk.Entry(root, width=49)
arquivo.place(x=0,y=160)
arquivo.insert(tk.END,'qrCode')
arquivo_label = Label(root, text='Insira um nome para salvar o QRCode:')
arquivo_label.place(x=0,y=135)

button = tk.Button(root,text='Gerar QR Code',
                   relief=tk.RAISED,command=cria_qr)
button.place(x=90,y=200)

root.mainloop()


    
