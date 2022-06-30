import csv
import datetime

'''with open('brasil-covid.csv', 'r') as arquivo_csv:
    leitor = csv.reader(arquivo_csv)
    header = next(leitor) # para não ler o cabeçalho
    for linha in leitor:
        if float(linha[2]) > 1:
            print(linha)
'''

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
        escritor.writerow(['15/07/2021', 'Testando'])
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
                
if __name__ == '__main__':
    cria_agenda()
    tarefa_dia()
    while True:
        menu = int(input('Digite 1 para inserir tarefas \nDigite 2 para pesquisar: \n'))
        if menu == 1:
            data = input('Escreva a data em que vai registrar a tarefa: \n')
            #dt = datetime.datetime.strptime(data, '%d/%m/%Y')
            #print(dt)
            if len(data) == 10:
                tarefa = input('Descreva a tarefa: \n')
                escreve_agenda(data, tarefa)
            else:
                print("Escreva a data no formado dd/mm/aaaa.")
        elif menu == 2:
            data = input('Escreva a data que deseja pesquisar: \n')
            procurar_data(data)
        else:
            break
    
