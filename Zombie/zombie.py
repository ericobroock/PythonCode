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
roll_dice=[]

##begin=input('Digite s para rodar os dados')
##if begin == 's':
##    for i in range(3):
##        roll = randint(1,len(dice_can)-1)
##        face_rand = random.choice(dice_can[roll])
##        print(face_rand)
##        if face_rand == 'brain':
##            point += 1
##        elif face_rand == 'shot':
##            death -= 1
##        else:
##            print(dice_can[roll])
##            roll_dice.append(dice_can[roll])
##        dice_can.pop(roll)
##        print(roll)
##    print (dice_can)
##    print (len(dice_can))
##    print('Tem tantos pontos ', point)
##    print('Tem de vida ', death)
##    print(roll_dice)
##    print(len(roll_dice))
#segunda_rodada=input("Digite s para rerolar os dados")
def Rodadas():
    global point, death
    while len(roll_dice) <= 2:
        roll = randint(1,len(dice_can)-1)
        roll_dice.append(dice_can[roll])
        print('roll_dice tem ', len(roll_dice), 'dados')
        print(roll_dice)
        dice_can.pop(roll)
    for i in roll_dice:
        i=0
        face_rand = random.choice(roll_dice[i])
        print(face_rand)
        if face_rand == 'brain':
            point += 1
        elif face_rand == 'shot':
            death -= 1
        else:
            continue
        roll_dice.pop()
        i += 1
    print(roll_dice)
    print(len(roll_dice))
    print('dice_can tem ', len(dice_can), 'dados')
    print('Tem tantos pontos ', point)
    print('Tem de vida ', death)

if __name__ == '__main__':
    while True:
        if death > 0:
            begin=input('Digite sim para rodar os dados')
            if begin == 'sim':
                Rodadas()
        else:
            break
    print("Você morreu")

               
