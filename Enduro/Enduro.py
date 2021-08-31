#===============================================================================
# Imports
#===============================================================================

import pyxel
from random import randint

#===============================================================================
# Variáveis e Constantes
#===============================================================================

largura_tela = 88
altura_tela = 256
velocidade_max = 10
velocidade_min = 1
score_car = 5
record = 0

#===============================================================================
# Classe que roda o Game
#===============================================================================

class Game:

    #===========================================================================
    # Inicializa o Pyxel
    #===========================================================================

    def __init__(self):

        self.reiniciar()
        
        # Título do programa
        pyxel.init(largura_tela, altura_tela, caption="Enduro", fps=35)

        # Load
        pyxel.load("assets/carro.pyxres")
        
        # fazendo o mouse aparecer na tela
        pyxel.mouse(True)

        # Aplica trilha sonora
        if ativo == False:
            self.som_abertura()

        pyxel.run(self.update, self.draw)

    #===========================================================================
    # Define sons
    #===========================================================================    

    def som_abertura(self):
        
        # Som de abertura e reinício
        ch = 0 # São possíveis de 0 a 3 canais
        snd = 1 # Som registrado no editor
        
        pyxel.play(ch,snd,loop=False)

    def som_batida(self):
        global bateu
        
        pyxel.play(1, 5, loop=False)
        bateu = False

    def som_vel(self):

        if not morto:
            snd = velocidade + 9
            pyxel.play(2, snd, loop=False)
        
    #===========================================================================
    # Funções para o comando Update
    #===========================================================================

    def reiniciar(self):
        global score, morto, ativo, p_x, p_y, velocidade, bateu, carros, bordas, record
        
        # Valores de variáveis originais ou personlizados para reinicio.
        score = 0
        morto = False  
        ativo = False
        p_x = 8 + 24
        p_y = altura_tela - 42
        velocidade = 1
        bateu = True
                
        # Carros obstáculos
        dist_carros = 64 + 30
        ca1 = 8 + 24 * randint(0,2), -32
        ca2 = 8 + 24 * randint(0,2), -32
        ca3 = 8 + 24 * randint(0,2), -32 - (1 * dist_carros)
        ca4 = 8 + 24 * randint(0,2), -32 - (1 * dist_carros)
        ca5 = 8 + 24 * randint(0,2), -32 - (2 * dist_carros)
        ca6 = 8 + 24 * randint(0,2), -32 - (2 * dist_carros)

        carros = [ca1, ca2, ca3, ca4, ca5, ca6]

        # Bordas para sensação de movimento
        bordas = []
        for y in range (altura_tela):
            if y % 8 == 0:
                bordas.append(y)

        # Lendo o recorde salvo no arquivo
        records = open('assets/records.pyxres', 'r')
        points = records.readlines()
        for i in points:
            if int(i) >= record:
                record = int(i)
        records.close()

    def movimento(self):

        global p_x, velocidade

        #variável de controles
        esquerda = pyxel.btnp(pyxel.KEY_LEFT)
       
        if esquerda and not morto and p_x > 8:
            p_x -= 24

        direita = pyxel.btnp(pyxel.KEY_RIGHT)
       
        if direita and not morto and p_x < 56:
            p_x += 24

        acelera = pyxel.btnp(pyxel.KEY_UP)

        if acelera and not morto and velocidade < velocidade_max:
            velocidade += 1

        freia = pyxel.btnp(pyxel.KEY_DOWN)

        if freia and not morto and velocidade > velocidade_min:
            velocidade -= 1

       
    def carros(self):
        i = 0
        if not morto:
            for x, y in carros:
                if y < altura_tela:
                    b = 1 * velocidade
                    c = 0
                else:
                    b = -altura_tela -32
                    c = 8 + 24 * randint(0,2) - x
                
                carros[i] = x + c, y + b
                i = i + 1

    def score(self):
        global score

        #Percorre as coodenadas x e y de cada cano
        for x, y in carros:
            #verifica se as posições coincidem e não está morto
            if p_y + 42 <= y and not morto:
                score = score + score_car * velocidade

    def record(self):
        global record

        # Sobreescreve com o novo record com o valor de score        
        if morto and score > record:
            file = open('assets/records.pyxres', 'w')
            file.write(str(score))
            file.close()

        limpa_record = pyxel.btnp(pyxel.KEY_SPACE)
        if limpa_record:
            record = 0
            file = open('assets/records.pyxres', 'w')
            file.write(str(record))
            file.close()
            
    def colisoes(self):
        global morto

        # Condição de colisão com os carros
        for x, y in carros:
            colide_x = p_x + 24 > x and p_x < x + 24
            colide_y = p_y < y + 29 and p_y + 29 > y

            # A variável bateu é usada para o som ser executado uma vez
            if colide_x and colide_y and bateu:
                morto = True
                self.som_batida()
                    
    def bordas(self):
        global bordas
        i = 0
        if not morto:
            for y in bordas:
                if y < altura_tela:
                    y = 1 + ( 1 * velocidade )
                else:
                    y = -altura_tela
                            
                bordas[i] += y
                i += 1
     
    #===========================================================================
    # Funções para o comando Draw
    #===========================================================================

    def desenha_instrucoes(self):
        cor = 15
        y = altura_tela / 3
        y1 = altura_tela / 3 + 16
        y2 = altura_tela / 3 + 24
        y3 = altura_tela / 3 + 40
        y4 = altura_tela / 3 + 48

        if morto:
            pyxel.rect(7, y - 1, largura_tela - 14, 7, 0)
            pyxel.rect(7, y1 - 1, largura_tela - 14, 15, 0)
            msg = 'You Crashed!'
            msg1 = 'Press R'
            msg2 = 'to restart.'
            msg3 = ''
            msg4 = ''            
        elif ativo:
            msg = ''
            msg1 = ''
            msg2 = ''
            msg3 = ''
            msg4 = ''
        else:
            pyxel.rect(7, y - 1, largura_tela - 14, 7, 0)
            pyxel.rect(7, y1 - 1, largura_tela - 14, 7, 0)
            pyxel.rect(7, y3 - 1, largura_tela - 14, 15, 0)
            msg = 'Welcome to Enduro!'
            msg1 = 'Press UP to begin.'
            msg2 = ''
            msg3 = 'UP to accelerate.'
            msg4 = 'DOWN to brake.'
        # Variável do pyxel que retorna o tamanho das letras
        # Centraliza os textos
        largura_texto = pyxel.FONT_WIDTH * len(msg)
        x = largura_tela / 2 - largura_texto / 2        

        largura_texto1 = pyxel.FONT_WIDTH * len(msg1)
        x1 = largura_tela / 2 - largura_texto1 / 2        

        largura_texto2 = pyxel.FONT_WIDTH * len(msg2)
        x2 = largura_tela / 2 - largura_texto2 / 2

        largura_texto3 = pyxel.FONT_WIDTH * len(msg3)
        x3 = largura_tela / 2 - largura_texto3 / 2

        largura_texto4 = pyxel.FONT_WIDTH * len(msg4)
        x4 = largura_tela / 2 - largura_texto4 / 2
            
        pyxel.text(x, y, msg, cor)
        pyxel.text(x1, y1, msg1, cor)
        pyxel.text(x2, y2, msg2, cor)
        pyxel.text(x3, y3, msg3, cor)
        pyxel.text(x4, y4, msg4, cor)

    def desenha_player(self):
        
        u = 0 # x na imagem do pyxeleditor
        v = 128 # y na imagem do pyxeleditor
        img = 0 # img no pyxeleditor
        altura = 32 # tamanho da imagem
        largura = 24 # tamanho da imagem
        mascara = 11 # cor transparente

        pyxel.blt(p_x, p_y, img, u, v, largura, altura, mascara)

    def desenha_carros(self):

        u = 0 # x na imagem do pyxeleditor
        v = 128 # y na imagem do pyxeleditor
        img = 0 # img no pyxeleditor
        altura = 32 # tamanho da imagem
        largura = 24 # tamanho da imagem
        mascara = 11 # cor transparente

        for x, y in carros:
            pyxel.blt(x, y, img, u, v, largura, altura, mascara)

    def desenha_fundo(self):

        # Cor do fundo
        pyxel.cls(11)

    def desenha_bordas(self):
        
        u = 8 # x na imagem do pyxeleditor
        v = 128 # y na imagem do pyxeleditor
        img = 0 # img no pyxeleditor
        altura = 8 # tamanho da imagem
        largura = 8 # tamanho da imagem
        mascara = 11 # cor transparente

        for b_y in bordas:
            pyxel.blt(0, b_y, img, u, v, largura, altura, mascara)
            pyxel.blt(largura_tela - 8, b_y, img, u, v, largura, altura, mascara)

    def desenha_score(self):
        
        pyxel.rect(0, 0, largura_tela, 30, 0)        
        pyxel.text(10, 10, "SCORE: "+str(score), 15)
        pyxel.text(10, 20, "RECORD: "+str(record), 15)
        pyxel.rect(largura_tela - 17, altura_tela - 10, 17, 10, 0)
        pyxel.text(largura_tela - 16, altura_tela - 8, "V="+str(velocidade), 15)
        
    #===========================================================================
    # Comandos Update e Draw
    #===========================================================================           

    def atualizar_jogo(self): #Função condicional para freezar um menu no início
        self.movimento()
        self.som_vel()
        self.score()
        self.record()
        self.colisoes()
        self.bordas()
        self.carros()
       
    def update(self):
        global ativo
          
        #Reinicia com R
        if pyxel.btnp(pyxel.KEY_R):
            self.reiniciar()
            self.som_abertura()
                        
        #Roda o jogo
        elif ativo:
            self.atualizar_jogo()
                        
        #Ativa com espaço ou seta para cima
        elif pyxel.btnp(pyxel.KEY_UP):
            ativo = True

        # Condição caso se aperte a tecla Q
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self): #desenhando
        # Desenha o fundo
        self.desenha_fundo()

        # Desenha o player
        self.desenha_player()

        # Desenha os obstáculos
        self.desenha_carros()

        # Desenha as bordas
        self.desenha_bordas()
       
        # texto score
        self.desenha_score()

        # Texto das instruções
        self.desenha_instrucoes()

#===============================================================================
# Função que ativa a classe e roda o Game
#===============================================================================    
        
Game()
