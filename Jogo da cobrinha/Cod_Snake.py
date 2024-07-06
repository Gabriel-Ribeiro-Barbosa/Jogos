import pygame
import random
# Configurações iniciais

pygame.init() #Iniciando pygame
pygame.display.set_caption('Jogo Snake') #Exibir nome do jogo
Largura, Altura = 1000, 600
tela = pygame.display.set_mode((Largura,Altura)) # Criando Tela
relogio = pygame.time.Clock() #Criando um relógio

#Cores RGB

preto = (0, 0, 0)
verde = (0, 255, 0)
vermelho = (255, 0, 0)
branco = (255, 255, 255)

# Parametros da snake
tamanho_quadrado = 10 #Pixels
velocidade_jogo = 15


#Função para comida

def gerar_comida():
    comida_x = round(random.randrange(0, Largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado) # Gerando a comida em clugar aleatório / E dividido por 20 para o pixel nãp ficar de fora
    comida_y = round(random.randrange(0, Altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado) # Gerando a comida em clugar aleatório
    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho, tamanho]) #1- Onde sera feito, cor, lista com x,y, largura, tamanho


def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, verde, [pixel[0], pixel[1], tamanho, tamanho] ) # pixel[0] = x pixel[1] = y

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont('Jamer',35 )
    texto = fonte.render(f'Pontos: {pontuacao}', True, branco)
    tela.blit(texto, [1, 1]) # Colocar texto com blit e local [1,1]


def selecionar_velocidade(tecla):
    if tecla ==  pygame.K_DOWN: # Se apertar para baixo
        velocidade_x = 0
        velocidade_y = tamanho_quadrado
    elif tecla ==  pygame.K_UP: # Se apertar para cima
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado
    elif tecla ==  pygame.K_RIGHT: # Se apertar para baixo
        velocidade_x = tamanho_quadrado
        velocidade_y = 0
    elif tecla ==  pygame.K_LEFT: # Se apertar para baixo
        velocidade_x = - tamanho_quadrado
        velocidade_y = 0
    return velocidade_x, velocidade_y



def rodar_jogo():
    fim_jogo = False

    x = Largura/2 #Eixo x
    y = Altura/2 #Eixo y

    velocidade_x = 0 #Velocidade para o eixo x, direita/esquerda
    velocidade_y = 0 #Velocidade para o eixo y, cima/baixo

    tamanho_snake = 1
    pixels = [] #Quadrados presente na cobra relacionados as posições x e y

    # Criando a comida
    comida_x,comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill(preto) # Criando a tela

        for evento in pygame.event.get(): # Verificando evento
            if evento.type == pygame.QUIT: #Verificando fim de jogo
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN: #Se ele apertou algo
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)

        # Desenhar comida
        desenhar_comida(tamanho_quadrado,comida_x, comida_y)

        #Atualizar posição da cobra
        if x < 0 or x >= Largura or y < 0 or y >= Altura:
            fim_jogo = True
        x += velocidade_x
        y += velocidade_y

        # Desenhar cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_snake:
            del pixels[0] #Deletar o ultimo pixel

        # Verificar se a cobra bateu
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fim_jogo = True # Se a cobra bater nela mesma o jogo acaba

        desenhar_cobra(tamanho_quadrado, pixels)
        
        desenhar_pontuacao(tamanho_snake-1) # Desenhar pontos

        #Atualização da tela
        pygame.display.update()
         # Criar uma nova comida
        if x == comida_x and y == comida_y: #Se a cobra tiver entrado totalmente em contato com a comida
            tamanho_snake += 1
            comida_x, comida_y = gerar_comida()


        relogio.tick(velocidade_jogo)

rodar_jogo()