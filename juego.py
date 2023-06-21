import pygame
import random
from pygame import mixer


colores = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class Figura:
    x = 0
    y = 0

    figuras = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tipo = random.randint(0, len(self.figuras) - 1)
        self.color = random.randint(1, len(colores) - 1)
        self.rotacion = 0

    def imagen(self):
        return self.figuras[self.tipo][self.rotacion]

    def rotar(self):
        self.rotacion = (self.rotacion + 1) % len(self.figuras[self.tipo])


class Tetris:
    def __init__(self, alto, ancho):
        self.nivel = 2
        self.puntaje = 0
        self.estado = "inicio"
        self.tablero = []
        self.alto = 0
        self.ancho = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figura = None

        self.alto = alto
        self.ancho = ancho
        self.tablero = []
        self.puntaje = 0
        self.estado = "inicio"
        for i in range(alto):
            nueva_linea = []
            for j in range(ancho):
                nueva_linea.append(0)
            self.tablero.append(nueva_linea)

    def nueva_figura(self):
        self.figura = Figura(3, 0)

    def intersecta(self):
        interseccion = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figura.imagen():
                    if i + self.figura.y > self.alto - 1 or \
                            j + self.figura.x > self.ancho - 1 or \
                            j + self.figura.x < 0 or \
                            self.tablero[i + self.figura.y][j + self.figura.x] > 0:
                        interseccion = True
        return interseccion

    def eliminar_lineas(self):
        lineas = 0
        for i in range(1, self.alto):
            ceros = 0
            for j in range(self.ancho):
                if self.tablero[i][j] == 0:
                    ceros += 1
            if ceros == 0:
                lineas += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.ancho):
                        self.tablero[i1][j] = self.tablero[i1 - 1][j]
        self.puntaje += lineas ** 2

    def ir_al_final(self):
        while not self.intersecta():
            self.figura.y += 1
        self.figura.y -= 1
        self.congelar()

    def ir_abajo(self):
        self.figura.y += 1
        if self.intersecta():
            self.figura.y -= 1
            self.congelar()

    def congelar(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figura.imagen():
                    self.tablero[i + self.figura.y][j + self.figura.x] = self.figura.color
        self.eliminar_lineas()
        self.nueva_figura()
        if self.intersecta():
            self.estado = "gameover"

    def ir_lado(self, dx):
        antiguo_x = self.figura.x
        self.figura.x += dx
        if self.intersecta():
            self.figura.x = antiguo_x

    def rotar(self):
        antigua_rotacion = self.figura.rotacion
        self.figura.rotar()
        if self.intersecta():
            self.figura.rotacion = antigua_rotacion


# Inicializar el motor del juego
pygame.init()

# Temporizador
evento_temporizador = pygame.USEREVENT + 1
pygame.time.set_timer(evento_temporizador, 1000)  # Temporizador cada 1 segundo
segundos_temporizador = 60  # Duración del temporizador en segundos
# Definir algunos colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)

tamaño = (400, 500)
pantalla = pygame.display.set_mode(tamaño)

pygame.display.set_caption("Tetris Rap")

# Inicializar el módulo de mezcla
pygame.mixer.init()

# Cargar la música de fondo
pygame.mixer.music.load("musica.wav")

# Comenzar a reproducir la música de fondo en un bucle infinito
pygame.mixer.music.play(-1)

# Loop hasta que el usuario haga clic en el botón de cerrar.
terminado = False
reloj = pygame.time.Clock()
fps = 25
juego = Tetris(20, 10)
contador = 0

presionando_abajo = False

while not terminado:
    if juego.figura is None:
        juego.nueva_figura()
    contador += 1
    if contador > 100000:
        contador = 0

    if contador % (fps // juego.nivel // 2) == 0 or presionando_abajo:
        if juego.estado == "inicio":
            juego.ir_abajo()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            terminado = True
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                juego.rotar()
            if evento.key == pygame.K_DOWN:
                presionando_abajo = True
            if evento.key == pygame.K_LEFT:
                juego.ir_lado(-1)
            if evento.key == pygame.K_RIGHT:
                juego.ir_lado(1)
            if evento.key == pygame.K_SPACE:
                juego.ir_al_final()
            if evento.key == pygame.K_ESCAPE:
                juego.__init__(20, 10)
        if evento.type == evento_temporizador:
            segundos_temporizador -= 1
            if segundos_temporizador == 0:
                juego.estado = "gameover"

    if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_DOWN:
                presionando_abajo = False

    pantalla.fill(BLANCO)

    for i in range(juego.alto):
        for j in range(juego.ancho):
            pygame.draw.rect(pantalla, GRIS, [juego.x + juego.zoom * j, juego.y + juego.zoom * i, juego.zoom, juego.zoom], 1)
            if juego.tablero[i][j] > 0:
                pygame.draw.rect(pantalla, colores[juego.tablero[i][j]],
                                 [juego.x + juego.zoom * j + 1, juego.y + juego.zoom * i + 1, juego.zoom - 2, juego.zoom - 1])

    if juego.figura is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in juego.figura.imagen():
                    pygame.draw.rect(pantalla, colores[juego.figura.color],
                                     [juego.x + juego.zoom * (j + juego.figura.x) + 1,
                                      juego.y + juego.zoom * (i + juego.figura.y) + 1,
                                      juego.zoom - 2, juego.zoom - 2])

    fuente = pygame.font.SysFont('Calibri', 25, True, False)
    fuente1 = pygame.font.SysFont('Calibri', 65, True, False)
    texto = fuente.render("Puntaje: " + str(juego.puntaje), True, NEGRO)
    texto_game_over = fuente1.render("Game Over", True, (255, 125, 0))
    texto_game_over1 = fuente1.render("Presiona ESC", True, (255, 215, 0))
    
    # Dibujar el temporizador en la pantalla
    texto_temporizador = fuente.render("Tiempo: " + str(segundos_temporizador), True, NEGRO)
    pantalla.blit(texto_temporizador, [270, 0])  # Mostrar el tiempo en la esquina superior izquierda

    pantalla.blit(texto, [0, 0])
    if juego.estado == "gameover":
        pantalla.blit(texto_game_over, [20, 200])
        pantalla.blit(texto_game_over1, [25, 265])

    pygame.display.flip()
    reloj.tick(fps)

pygame.quit()

