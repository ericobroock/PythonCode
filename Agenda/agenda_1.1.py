import csv
import datetime
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar

# OBJETIVOS:
# Criar um menu de entrada para registrar ou resgatar data
# Criar uma função para procurar a data especificada e printar na tela
# Criar uma função para verificar se existe o arquivo em pasta, para a função
# cria_agenda não ser executada.
# Fazer a entrada de data ser do tipo Data.
# Quando executar o programa, procurar as tarefas do dia.
# Testar o Calendar para mostrar o mês.

def cria_agenda():
    with open('agenda.csv', 'w') as agenda:
        escritor = csv.writer(agenda, delimiter='|', lineterminator= '\n')
        escritor.writerow(['Data', 'Tarefas'])
        escritor.writerow(['15/09/2021', 'Testando'])
        escritor.writerow(['15/07/2020', 'Puta'])
        escritor.writerow(['17/07/2020', 'Bunda'])

def escreve_agenda(data, tarefa):
    with open('agenda.csv', 'a') as agenda:
        escritor = csv.writer(agenda, delimiter='|', lineterminator= '\n')
        escritor.writerow([data, tarefa])

def procurar_data(data):
    with open('agenda.csv', 'r') as agenda:
        leitor = csv.reader(agenda, delimiter='|')
        header = next(leitor) # para não ler o cabeçalho
        for linha in leitor:
            if str(linha[0]) == data:
                print(linha[1])

def tarefa_dia():
    hoje = datetime.datetime.now()
    print(hoje)
    print(type(hoje))
    pesquisa = hoje.strftime('%d/%m/%Y')
    print(type(pesquisa))
    procurar_data(pesquisa)

def tick():
    '''Relógio utilizando recursividade'''
    time_string = datetime.datetime.now()
    hora = time_string.strftime('%H:%M:%S')
    clock.config(text=hora)
    clock.after(200, tick)

def grad_date():
    date.config(text = "Selected Date is: " + cal.get_date())
                
if __name__ == '__main__':
    '''Inicializa o programa'''
    cria_agenda()
    tarefa_dia()
    root = Tk()
    root.geometry("400x400")
    root.title("Agenda")
    mainframe = ttk.Frame(root, padding="10 10 10 10")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(2, weight=3)
    mainframe.rowconfigure(2, weight=3)

    clock = ttk.Label(mainframe)
    clock.grid(column=6, row=1, columnspan=3, sticky=(E))
    tick()

    cal = Calendar(root, selectmode = 'day')
    print(type(cal.get_date()))
    cal.grid(column=1, row=1, columnspan=3, sticky=(E))
     Add Button and Label
    Button(root, text = "Get Date",
       command = grad_date).grid(column=1, row=3, columnspan=3, sticky=(E))
    date = Label(root, text = "")
    date.grid(column=2, row=3, columnspan=3, sticky=(E))
    root.mainloop()
    
  
