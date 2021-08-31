# Rolador de dados
from random import randint

qt = int(input('Digite quantos dados irá rolar: '))
dado = int(input('Quantos lados esses dados têm? '))
bonus = int(input('Quanto de bonus terá a rolagem? '))
resultado=[]

for i in range(qt):
    
    rolagem = randint(1, dado)
    resultado.append(rolagem)
    
print('--> Dado d'+str(dado), end=': ')
print(*resultado, sep=' + ', end='')

soma = 0
for i in range(len(resultado)):
    soma += resultado[i]
soma += bonus
print(' + ('+str(bonus)+') =',soma)

