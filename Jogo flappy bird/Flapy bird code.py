import pygame
import os
import random
import sys

#Definindo as constantes

#Tela

Largura_Tela = 500
Altura_Tela = 800
pygame.display.set_caption('Jogo Flappy Bird  ')

#Imagens

Imagem_Cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','cano.png')))
Imagem_Chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','chao.png')))
Imagem_Fundo =pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','fundo.png')))
Imagem_Bird = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))), #passaro1
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))), #passaro 2
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png')))  #passaro 3
]

#Texto de pontuação

pygame.font.init() #iniciando a fonte
Pontuacao = pygame.font.SysFont('jamer ',50) #Descrevendo - a

#Objetos/Classes:
def verificar_fim_jogo(birds):
    if len(birds) == 0:
        pygame.quit()
        sys.exit()
class Bird:
    # Angulo de rotação
    IMGS = Imagem_Bird
    Rotacao_max = 25
    Velosidade_Rotacao =  20
    Tempo_Animacao = 5

    # Caracteristicas:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0 #Tempo de rotação
        self.cont_imagens = 0 #Indicação de qual imagem do passaro sera indicada
        self.imagem = self.IMGS[0]

    #Função de pular
    def pular(self):
        self.velocidade = -10.5 #O valor é negativo pois o y cresce para baixo
        self.tempo = 0 #Quando ele pula o tempo é 0
        self.altura = self.y

    #Funcão de mover
    def mover(self):
        # Calcular o deslocamento

        self.tempo += 1

        # Calcular o deslocamento S = pos inicial + velocidade * intervalo de tempo

        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo #Formula do deslocamento

        #Restringir o deslocamento

        if deslocamento >16:
            deslocamento = 16 #Limite
        elif deslocamento < 8:
            deslocamento -= 2 #Buff

        self.y += deslocamento #Posição recebe o deslocamento

        #Angulo do passaro

        if deslocamento < 0 or self.y < (self.altura + 50):#Se o deslocamento for para cima ou se o passaro terminar seu pulo
            if self.angulo < self.Rotacao_max:
                self.angulo = self.Rotacao_max
        else:
            if self.angulo > -90: #Delimitar até onde o passaro pode rodar para cair
                self.angulo = self.Velosidade_Rotacao

    #Função para desenhar o passaro(ocupar das caracteristicas)

    def desenhar(self,tela):
        #Definir qual imagem do passaro será usada
        self.cont_imagens += 1
        if self.cont_imagens < self.Tempo_Animacao:
            self.imagem = self.IMGS[0] #Passaro quase batendo assa
        elif self.cont_imagens < self.Tempo_Animacao*2:
            self.imagem = self.IMGS[1] #Passaro batendo assa
        elif self.cont_imagens < self.Tempo_Animacao*3:
            self.imagem = self.IMGS[2] #Passaro terminado de bater assa
        elif self.cont_imagens < self.Tempo_Animacao*4:
            self.imagem = self.IMGS[1] #Passaro batendo assa de novo
        elif self.cont_imagens >= self.Tempo_Animacao*4 +1:#Se ele for maior que a ultima img
            self.imagem = self.IMGS[0] #Passaro parar de bater assa
            self.cont_imagens = 0 #Volta ao inicio

        #Para o passaro  caindo não bater assa
        if self.angulo <= -80:
            self.imagem =self.IMGS[1] #voltando a imagem de começo de  animação
            self.cont_imagens = self.Tempo_Animacao*2

        # Desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem,self.angulo)
        posicao_centro_imagem = self.imagem.get_rect(topleft= (self.x,self.y)).center#Pegando o centro da imagem
        retangulo = imagem_rotacionada.get_rect(center=posicao_centro_imagem) #Criando um retangulo em volta da imagem para rotaciona-la
        tela.blit(imagem_rotacionada,retangulo.topleft)  #Topleft = top á esquerda
    #Colisão dos objetos
    #Primeiro presisa-se alunar a colisao do retangulo de indentificacao do passaro
    #Basta fazer uma mascara para pixelar o passaro

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem) #Pegando a mascara
class Cano:
    #Constantes:
    Distancia = 200
    Velocidade = 5
    def __init__(self,x):
        self.x = x
        self.altura = 0
        self.posicao_topo = 0
        self.posicao_base = 0
        self.img_cano_topo = pygame.transform.flip(Imagem_Cano,False,True) #Virando o cano ao contrário
        self.img_cano_base = Imagem_Cano
        self.passou = False #Se cano passou ou não do passaro
        self.definir_altura() #Gerar a altura do cano

    def definir_altura(self):
        self.altura = random.randrange(50,450)
        self.posicao_topo = self.altura - self.img_cano_topo.get_height() # altura - tamanho do cano
        self.posicao_base = self.altura + self.Distancia #altura - distancia entre os canos

    def mover(self):
        self.x -= self.Velocidade

    def desenhar(self,tela):
        tela.blit(self.img_cano_topo,(self.x,self.posicao_topo))
        tela.blit(self.img_cano_base,(self.x,self.posicao_base))

    def colidir(self,bird):
        bird_mask = bird.get_mask() #Mascara do passaro
        topo_mask = pygame.mask.from_surface(self.img_cano_topo) #Mascara do topo
        base_mask = pygame.mask.from_surface(self.img_cano_base) #Mascara da base

        #Calcular a colisão entre cano e passaro

        Distancia_topo = (self.x - bird.x, self.posicao_topo - round(bird.y)) #Tupla com posição x e y (Eixo x - passaro no eixo x, posicao do topo - passaro no eixo y)
        Distancia_base = (self.x - bird.x, self.posicao_base - round(bird.y)) #Tupla com posição x e y (Eixo x - passaro no eixo x, posicao do base - passaro no eixo y)
        #Calculando a colisão

        Base_ponto_colisao = bird_mask.overlap(base_mask,Distancia_base) #Colisoa com a base
        Topo_ponto_colisao = bird_mask.overlap(topo_mask, Distancia_topo) #Colisao com o topo

        #Verificando se ouve colisão
        if Base_ponto_colisao or Topo_ponto_colisao:
            return True
        else:
            return False
class Chao:
    #Constantes
    Velocidade_chao = 5
    #Criando a largura para que quando o chao se movimentar outro chao aparecer
    Largura_chao = Imagem_Chao.get_width() #Width = pegar largura
    Img= Imagem_Chao

    def __init__(self,y):
        self.y = y
        self.x1 = 0 #Primeira imagem do chão
        self.x2 = self.Largura_chao #segunda imagem correspondente a largura

    def mover(self):
        self.x1 -= self.Velocidade_chao #Fazendo o chao se movimentar de acordo com as duas imagens
        self.x2 -= self.Velocidade_chao #Negativo pois o chao se movimenta para a esquerda da tela

        #movimentando o chao 2 para o lugar do chao 1, para ter a imagem constante do chao

        if self.x1 + self.Largura_chao < 0:
            self.x1 = self.x2 + self.Largura_chao
        if self.x2 + self.Largura_chao < 0:
            self.x2 = self.x1 + self.Largura_chao

    #Desenhar o chao
    def desenhar(self,tela):
        tela.blit(self.Img,(self.x1, self.y))
        tela.blit(self.Img,(self.x2, self.y))

#Funsão para desenhar a tela
def desenhar_tela(tela, birds, canos, chao, pontos):
    tela.blit(Imagem_Fundo,(0,0)) #Fundo feito
    for bird in birds:
        bird.desenhar(tela) #Passaro feito
    for cano in canos:
        cano.desenhar(tela) #Cano feito
    chao.desenhar(tela) #Chao feito
    texto = Pontuacao.render(f'Pontuação: {pontos}',1,(239, 184, 16.))
    tela.blit(texto,(Largura_Tela - 10 - texto.get_width(), 10)) #Texto Feito
    pygame.display.update() # Atualizando a tela

#Funsão principal

def main():
    birds = [Bird(230, 350)] #Criando o passaro
    chao = Chao(730) #Criado o chao
    canos = [Cano(700)] #Criado o cano
    tela = pygame.display.set_mode((Largura_Tela ,Altura_Tela)) #tela foi criada
    pontos = 0 #Inicando a pontuação
    relogio = pygame.time.Clock() #Tempo no pygame

    rodando = True #Jogo rodando
    while rodando:
        relogio.tick(30) #Fps Relogio rodando
        #Interação do usuário com o jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: #Inserar o jogo
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN: #Teclas
                if evento.key == pygame.K_SPACE: #Se for o botão de espaço
                    for bird in birds:
                        bird.pular()
        #Movimentando os objetos
        for bird in birds:
            bird.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i,bird in enumerate(birds):
                if cano.colidir(bird): #Verificando a colisao
                    birds.pop(i) #Se colidiu o passaro é excluido
                if not cano.passou and bird.x > cano.x: #Se o passaro passou do cano
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.img_cano_topo.get_width() < 0:
                remover_canos.append(cano)
        if adicionar_cano:
            pontos += 1 #Ganhou ponto pois ele passou do cano
            canos.append(Cano(600)) #Adicionar novo cano pois o usuario passou
        for cano in remover_canos:
            canos.remove(cano) #Removeu o cano

        #Verificando se o passaro colidiu com o ceu ou com o chao
    
        for i,bird in enumerate(birds):
            if (bird.y + bird.imagem.get_height()) > chao.y or bird.y < 0: #Se a posicao do passaro + a altura do passaro for maior que o chao
                birds.pop(i)
        desenhar_tela(tela, birds, canos, chao, pontos)
        verificar_fim_jogo(birds)

#Executar
if __name__ == '__main__':
    main()