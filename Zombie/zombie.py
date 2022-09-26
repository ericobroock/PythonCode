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

def Rodadas():
    global point, death
    # Pega 3 dados da lata.
    while len(roll_dice) <= 2:
        roll = randint(0,len(dice_can)-1)
        print('Pega o dado número ', roll)
        roll_dice.append(dice_can[roll])
        print(dice_can[roll])
        dice_can.pop(roll)
    print('A mão possui', len(roll_dice), 'dados')
    print(roll_dice)
    out_dice=[]
    giro = 1
    # Roda os 3 dados
    for i in roll_dice:
        print(str(giro) + 'º dado jogado')
        giro += 1
        face_rand = random.choice(i)
        print('A rolagem do dado foi', face_rand)
        if face_rand == 'brain':
            point += 1
            out_dice.append(i)
        elif face_rand == 'shot':
            death -= 1
            out_dice.append(i)
        else:
            continue
    # Verifica se os dados foram contabilizados, brain ou shot,
    # e remove da mão.
    for i in out_dice:
        roll_dice.remove(i)
    print('Dados que saem da jogada ', out_dice)
    print('Dados remanescentes na mão, ' + str(len(roll_dice))+': ', roll_dice)
    print('\nA lata ainda tem ', len(dice_can), 'dados')
    print('Você já tem ', point, 'pontos!')
    print('Vida restante: ', death)

if __name__ == '__main__':
    print("Bem vindo ao ZOMBIE DICE!!!\n")
    while True:
        if death > 0:
            begin=input('Digite sim para rodar os dados: ')
            if begin == 'sim':
                Rodadas()
        else:
            break
    print("Você morreu")

               
