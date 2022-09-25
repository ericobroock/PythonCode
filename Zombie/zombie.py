''' Projeto Zombie Dice
Tem 6 dados verdes, 4 amarelos e 3 vermelhos
Os dados saem da caixa aleatóriamente, sempre 3.
'''

import random
from random import randint

dado_vermelho=('brain', 'run', 'run', 'shot', 'shot', 'shot')
dado_amarelo=('brain', 'brain', 'run', 'run', 'shot', 'shot')
dado_verde=('brain', 'brain', 'brain', 'run', 'run', 'shot')

dice_can=[dado_vermelho, dado_vermelho, dado_vermelho,
          dado_amarelo, dado_amarelo, dado_amarelo, dado_amarelo,
          dado_verde, dado_verde, dado_verde, dado_verde, dado_verde, dado_verde]

point=0
death=3
reroll_dice=[]

begin=input('Digite s para rodar os dados')
if begin == 's':
    for i in range(3):
        roll = randint(1,len(dice_can)-1)
        face_rand = random.choice(dice_can[roll])
        print(face_rand)
        if face_rand == 'brain':
            point += 1
        elif face_rand == 'shot':
            death -= 1
        else:
            print(dice_can[roll])
            reroll_dice.append(dice_can[roll])
        dice_can.pop(roll)
        print(roll)
    print (dice_can)
    print (len(dice_can))
    print('Tem tantos pontos ', point)
    print('Tem de vida ', death)
    print(reroll_dice)
    print(len(reroll_dice))
segunda_rodada=input("Digite s para rerolar os dados")
if segunda_rodada == 's':
    while len(reroll_dice) <= 2:
        roll = randint(1,len(dice_can)-1)
        reroll_dice.append(dice_can[roll])
        dice_can.pop(roll)
    for i in reroll_dice:
        face_rand = random.choice(dice_can[roll])
        print(face_rand)
        if face_rand == 'brain':
            point += 1
        elif face_rand == 'shot':
            death -= 1
        else:
            print(dice_can[roll])
            continue
        reroll_dice.pop(roll)
    print(reroll_dice)
    print(len(reroll_dice))
    print(dice_can)

#if "__name__" == "__main__":
    

               
