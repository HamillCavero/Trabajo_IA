from builtins import Warning

import pygame
import copy
import numpy
import random

# Define los coles a usarse, pueden agregarse mas
RED = (230, 25, 75)
GREEN = (60, 180, 75)
YELLOW = (255, 225, 25)
BLUE = (0, 130, 200)
ORANGE = (245, 130, 48)
APRICOT = (255, 215, 180)
GRAY = (128, 117, 117)
MINT = (170, 255, 195)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

Colors = [WHITE, GREEN, YELLOW, BLUE, ORANGE, GRAY, MINT, RED, BLACK]
Colors_index = [_ for _ in range(len(Colors))]
# print(Colors_index)

# Ancho y alto de los bloques
WIDTH = 20
HEIGHT = 20

# espacio entre casillas
MARGIN = 1
# alto y largo de la matriz

# Iniciar pygame
pygame.init()

# Establecemos las dimenciones de la aplicacion
ALTO = 400
LARGO = 400
WINDOW_SIZE = [ALTO, LARGO]
screen = pygame.display.set_mode(WINDOW_SIZE)
# print(screen.get_height())
# Titulo
pygame.display.set_caption("Proyecto ia")

# Terminó?
done = False

# Medir el tiempo de renderizado
clock = pygame.time.Clock()


class Bola:
    velocidad = 0
    posX = 0
    posY = 0
    pasoActual = 0
    score = 0
    distancia = 0
    is_ded = False
    choque = False
    mutacion = 0.01

    def __init__(self, v, c, px, py, pasos_maximos=None):
        if pasos_maximos == None:
            self.velocidad = v
            self.color = c
            self.posX = px
            self.posY = py
            self.pasos = []
            self.score = 0
        else:
            self.velocidad = v
            self.color = c
            self.posX = px
            self.posY = py
            self.pasos = []
            self.crear_pasos(pasos_maximos)
            self.score = 0

    def crear_pasos(self, _pasos_maximos):
        for i in range(_pasos_maximos):
            # self.pasos[i] = numpy.random.randint(0, 4)
            self.pasos.append(numpy.random.randint(0, 4))

<<<<<<< HEAD
    def __init__(self, v, c, px, py):
        self.velocidad = v
        self.color = c
        self.posX = px
        self.posY = py
        self.pasos = []
        self.crear_pasos()
        self.score = 0

    def crear_pasos(self):
        for i in range(400):
            #self.pasos[i] = numpy.random.randint(0, 4)
            self.pasos.append(numpy.random.randint(0, 4))
=======
>>>>>>> 2938101a026b249d8803c1374b33efc791031005
        # print(self.pasos)

    def mover(self):
        if not self.is_ded:
            if not self.choque:
                if self.posY < screen.get_height() and self.posX < screen.get_width() and self.posX >= 0 and self.posY >= 0:
                    if self.pasoActual < len(self.pasos):
                        if self.pasos[self.pasoActual] == 0:
                            self.posX -= self.velocidad
                        elif self.pasos[self.pasoActual] == 1:
                            self.posY += self.velocidad
                        elif self.pasos[self.pasoActual] == 2:
                            self.posX += self.velocidad
                        elif self.pasos[self.pasoActual] == 3:
                            self.posY -= self.velocidad
                        else:
                            print("no me muevo", self.pasoActual)
                        self.pasoActual += 1
                        # print(self.pasos)
                    else:
                        self.is_ded = True
                        # self.calcularScore()
                        print("mori de viejo :c")
                else:
                    self.choque = True
                    self.is_ded = True
                    # self.calcularScore()
                    print("choque y mori")

    def graficar(self, screen):
        pygame.draw.circle(screen, self.color, [self.posX, self.posY], 5)

    def calcularScore(self, destX, destY):
        if self.choque:
            self.score = 0
        else:
<<<<<<< HEAD
            self.score = 1000/numpy.sqrt(numpy.power(self.posX - destX, 2) + numpy.power(self.posY - destY, 2))
        print(self.score)
    def returnScore(self):
        return(self.score)
    def returnPasos(self):
        return (self.pasos)
=======
            self.score = 1000 / numpy.sqrt(numpy.power(self.posX - destX, 2) + numpy.power(self.posY - destY, 2))
        # print(self.score)

    def get_pasos(self):
        return self.pasos

    def get_score(self):
        return self.score

>>>>>>> 2938101a026b249d8803c1374b33efc791031005

def dibujar_fondo():
    screen.fill(WHITE)


lista_bolas = {}
destinoX = 200
destinoY = 50
poblacion = 32
pasos_maximos = 200


def crea_bolas(N):
    for _ in range(N):
        lista_bolas[_] = Bola(3, RED, 200, 350, pasos_maximos)
    # print(lista_bolas)
    # input("aaaa")


def mover_bolas():
    for bb in lista_bolas:
        if lista_bolas[bb].is_ded is False:
            # print("Bola: ", bb)
            lista_bolas[bb].mover()


def dibujar_bolas():
    for i in range(len(lista_bolas)):
        lista_bolas[i].graficar(screen)


def calcular_score():
    for i in range(len(lista_bolas)):
        lista_bolas[i].calcularScore(destinoX, destinoY)


def all_dead():
    for _ in lista_bolas:
        if lista_bolas[_].is_ded:
            return True
        else:
            return False

def write_score():
    fic = open("text_1.txt", "w")
    for i in range(len(lista_bolas)):
        fic.write(str(lista_bolas[i].returnPasos()))
        fic.write("\n")
    fic.close()


def revivir(bola):
    bola.is_ded = False
    bola.choque = False
    bola.posX = 200
    bola.posY = 350


def mostrar_lista():
    for _ in lista_bolas:
        print(_, "  ", lista_bolas[_].get_score(), lista_bolas[_].get_pasos())


def Parejas(N):
    Aleatorio = random.sample(range(int(N / 2), N), int(N / 2))
    Pareja = {}
    for i in range(int(N / 2)):
        Pareja[i] = Aleatorio[i]
        Pareja[Aleatorio[i]] = i
    return Pareja


def selecciona_bolitas():
    print('---Seleccion----')
    lista_seleccion = Parejas(poblacion)
    print('Parejas', lista_seleccion)
    for k, v in lista_seleccion.items():
        if lista_bolas[k].score >= lista_bolas[v].score:
            revivir(lista_bolas[k])
            lista_bolas[v] = lista_bolas[k]


def cruzar_bolitas():
    print('-----Cruce ------')
    lista_seleccion = Parejas(poblacion)
    print('Parejas', lista_seleccion)
    item = 0
    for k, v in lista_seleccion.items():
        if item % 2 == 0:
            Punto = random.randint(1, pasos_maximos)
            print('punto', Punto)
            # Hijo1 = Bola(3, RED, 200, 350,pasos_maximos)
            # Hijo2 = Bola(3, RED, 200, 350,pasos_maximos)
            Hijo1 = Bola(3, RED, 200, 350)
            Hijo2 = Bola(3, RED, 200, 350)
            Padre1 = lista_bolas[k]
            Padre2 = lista_bolas[v]

            Hijo1.get_pasos().extend(Padre1.pasos[0:Punto])
            Hijo1.get_pasos().extend(Padre2.pasos[Punto:])
            Hijo2.get_pasos().extend(Padre2.pasos[0:Punto])
            Hijo2.get_pasos().extend(Padre1.pasos[Punto:])

            # Hijo1.extend(Padre1.pasos[0:Punto])
            # Hijo1.extend(Padre2.pasos[Punto:])
            # Hijo2.extend(Padre2.pasos[0:Punto])
            # Hijo2.extend(Padre1.pasos[Punto:])
            lista_bolas[k] = Hijo1
            lista_bolas[v] = Hijo2
        item = item + 1


def mutar_bolitas():
    for _ in lista_bolas:
        if random.random() > lista_bolas[_].mutacion:
            print(lista_bolas[_].pasos)
            random_pos = numpy.random.randint(0, pasos_maximos - 1)
            random_val = numpy.random.randint(0, 4)
            lista_bolas[_].pasos[random_pos] = random_val
            print(lista_bolas[_].pasos)


def iniciar_simulacion():
    done = False

<<<<<<< HEAD
    crea_bolas(10)
    while done is not True:
        if not all_dead():
            mover_bolas()
        #else:
           # calcular_score()
=======
    crea_bolas(poblacion)
    while done is not True:
        if not all_dead():
            mover_bolas()
        else:
            calcular_score()
            print("Bolitas resultado")
            mostrar_lista()
            selecciona_bolitas()
            mostrar_lista()
            cruzar_bolitas()
            mostrar_lista()
            mutar_bolitas()

            # input("Press Enter to continue...")
>>>>>>> 2938101a026b249d8803c1374b33efc791031005
        for event in pygame.event.get():  # Registra eventos variados
            if event.type == pygame.QUIT:  # Cerrar el programa?
                done = True  # Si
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
        dibujar_fondo()
        dibujar_bolas()
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()  # no borrar


iniciar_simulacion()
<<<<<<< HEAD
calcular_score()

write_score()
=======
# print(Parejas(10))
>>>>>>> 2938101a026b249d8803c1374b33efc791031005
