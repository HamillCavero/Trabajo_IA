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
# WIDTH = 20
# HEIGHT = 20

# espacio entre casillas
MARGIN = 0
global grid_1

grid_1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# alto y largo de la matriz
celdaH = len(grid_1)
celdaV = len(grid_1[0])

# Iniciar pygame
pygame.init()

# Establecemos las dimenciones de la aplicacion
ALTO = 420
LARGO = 420
WINDOW_SIZE = [ALTO, LARGO]
screen = pygame.display.set_mode(WINDOW_SIZE)
# Titulo
pygame.display.set_caption("Proyecto ia")

WIDTH = LARGO / (celdaH + MARGIN * 0.5)
HEIGHT = ALTO / (celdaV + MARGIN * 0.5)

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
    mutacion = 0.15

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

        # print(self.pasos)

    def objetivo(self, objetivoX, objetivoY):
        return numpy.sqrt(numpy.power(self.posX - objetivoX, 2) + numpy.power(self.posY - objetivoY, 2)) < 10

    def mover(self, objetivoX, objetivoY):
        if not self.is_ded:
            if not self.choque:
                if self.objetivo(objetivoX, objetivoY):
                    self.is_ded = True
                    print("LLEGUE AAAAAA")
                elif screen.get_height() > self.posY >= 0 and screen.get_width() > self.posX >= 0:
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
                        # print("mori de viejo :c")
                else:
                    self.choque = True
                    self.is_ded = True
                    # self.calcularScore()
                    # print("choque y mori")

    def graficar(self, screen):
        pygame.draw.circle(screen, self.color, [self.posX, self.posY], 5, 1)

    def calcularScore(self, destX, destY, _inicX, _inicY):
        if self.choque:
            self.score = -99
        # else:
        #     self.score = 1000  / numpy.sqrt(numpy.power(self.posX - destX, 2) + numpy.power(self.posY - destY, 2)) + (
        #             len(self.pasos) - self.pasoActual) - 100  / numpy.sqrt(
        #         numpy.power(self.posX - _inicX, 2) + numpy.power(self.posY - _inicY, 2))
        else:
            self.score = numpy.sqrt(numpy.power(_inicX - destX, 2) + numpy.power(_inicY - destY, 2)) /\
                         numpy.sqrt(numpy.power(self.posX - destX, 2) + numpy.power(self.posY - destY, 2)) + (
                    len(self.pasos) - self.pasoActual) - numpy.sqrt(numpy.power(_inicX - destX, 2) +
                                                                    numpy.power(_inicY - destY, 2)) / numpy.sqrt(
                numpy.power(self.posX - _inicX, 2) + numpy.power(self.posY - _inicY, 2))
        print(self.score)
        # print(self.score)

    def get_pasos(self):
        return self.pasos

    def get_score(self):
        return self.score

    def get_pos(self):
        return [self.posX, self.posY]

    def morir(self):
        self.is_ded = True
        self.choque = True
        # print("choque y mori")


class Pared:
    def graficar_pared(self, _screen):
        pygame.draw.rect(_screen, GRAY, self.body, 1)

    def unir(self, _pared):
        pygame.Rect.union_ip(self.body, _pared)

    def choque_pared_bola(self, _pos):
        return pygame.Rect.collidepoint(self.body, _pos[0], _pos[1])

    def get_body(self):
        return self.body

    def __init__(self, _posX, _posY, _alto, _ancho):
        self.posX = _posX
        self.posY = _posY
        self.ancho = _ancho
        self.alto = _alto
        self.body = pygame.Rect((MARGIN + WIDTH) * self.posY, (MARGIN + HEIGHT) * self.posX,
                                WIDTH * self.ancho, HEIGHT * self.alto)


class Juego:
    print("AAAA")

    def dibujar_fondo(self, creacion):
        screen.fill(WHITE)
        for row in range(celdaH):
            for column in range(celdaV):
                color = WHITE
                if grid_1[row][column] == 1:
                    color = GRAY
                elif grid_1[row][column] == 7:
                    color = RED
                elif grid_1[row][column] == 3:
                    color = GREEN
                elif grid_1[row][column] == 5:
                    color = BLACK
                elif grid_1[row][column] == 11:
                    color = ORANGE
                if creacion == 1:
                    pygame.draw.rect(screen,
                                     color,
                                     [(MARGIN + WIDTH) * column,
                                      (MARGIN + HEIGHT) * row,
                                      WIDTH,
                                      HEIGHT])
                else:
                    self.dibujar_paredes()

    def crea_bolas(self, N):
        for _ in range(N):
            self.lista_bolas[_] = Bola(self.velocidad_bola, RED, 200, 350, self.pasos_maximos)
        # print(lista_bolas)
        # input("aaaa")

    def mover_bolas(self):
        for bb in self.lista_bolas:
            if self.lista_bolas[bb].is_ded is False:
                # print("Bola: ", bb)
                self.lista_bolas[bb].mover(self.destinoX, self.destinoY)

    def dibujar_bolas(self):
        for i in range(len(self.lista_bolas)):
            self.lista_bolas[i].graficar(screen)

    def calcular_score(self):
        for i in range(len(self.lista_bolas)):
            self.lista_bolas[i].calcularScore(self.destinoX, self.destinoX, self.inicioX, self.inicioY)

    def all_dead(self):
        for _ in self.lista_bolas:
            if self.lista_bolas[_].is_ded:
                return True
            else:
                return False

    def revivir(self, bola):
        bola.is_ded = False
        bola.choque = False
        bola.posX = 200
        bola.posY = 350

    def mostrar_lista(self):
        for _ in self.lista_bolas:
            print(_, "  ", self.lista_bolas[_].get_score(), self.lista_bolas[_].get_pasos())

    def Parejas(self):
        Aleatorio = random.sample(range(int(self.poblacion / 2), self.poblacion), int(self.poblacion / 2))
        Pareja = {}
        for i in range(int(self.poblacion / 2)):
            Pareja[i] = Aleatorio[i]
            Pareja[Aleatorio[i]] = i
        return Pareja

    def selecciona_bolitas(self):
        print('---Seleccion----')
        lista_seleccion = self.Parejas()
        # print('Parejas', lista_seleccion)
        for k, v in lista_seleccion.items():
            if self.lista_bolas[k].score >= self.lista_bolas[v].score:
                self.revivir(self.lista_bolas[k])
                self.lista_bolas[v] = self.lista_bolas[k]

    def cruzar_bolitas(self):
        print('-----Cruce ------')
        lista_seleccion = self.Parejas()
        # print('Parejas', lista_seleccion)
        item = 0
        for k, v in lista_seleccion.items():
            if item % 2 == 0:
                Punto = random.randint(1, self.pasos_maximos)
                # print('punto', Punto)
                Hijo1 = Bola(self.velocidad_bola, RED, 200, 350)
                Hijo2 = Bola(self.velocidad_bola, RED, 200, 350)
                Padre1 = self.lista_bolas[k]
                Padre2 = self.lista_bolas[v]

                Hijo1.get_pasos().extend(Padre1.pasos[0:Punto])
                Hijo1.get_pasos().extend(Padre2.pasos[Punto:])
                Hijo2.get_pasos().extend(Padre2.pasos[0:Punto])
                Hijo2.get_pasos().extend(Padre1.pasos[Punto:])

                # Hijo1.extend(Padre1.pasos[0:Punto])
                # Hijo1.extend(Padre2.pasos[Punto:])
                # Hijo2.extend(Padre2.pasos[0:Punto])
                # Hijo2.extend(Padre1.pasos[Punto:])
                self.lista_bolas[k] = Hijo1
                self.lista_bolas[v] = Hijo2
            item = item + 1

    def mutar_bolitas(self):
        for _ in self.lista_bolas:
            if random.random() > self.lista_bolas[_].mutacion:
                # print(lista_bolas[_].pasos)
                random_pos = numpy.random.randint(0, self.pasos_maximos - 1)
                random_val = numpy.random.randint(0, 4)
                self.lista_bolas[_].pasos[random_pos] = random_val
                # print(lista_bolas[_].pasos)

            # for i in self.lista_bolas[_].pasos[i]:
            #     if random.random() < self.lista_bolas[_].mutacion:
            #         random_val = numpy.random.randint(0, 4)
            #         self.lista_bolas[_].pasos[i] = random_val

    def dibujar_destino(self):
        pygame.draw.circle(screen, GREEN, [self.destinoX, self.destinoY], 5)

    def borrar_ficha(self, _row, _column):
        if grid_1[_row][_column] == 1:
            grid_1[_row][_column] = 0

    def insertar_pieza(self, _row, _column):
        global grid_1
        # grid2 = grid_1.copy()
        grid2 = copy.deepcopy(grid_1)
        if (grid2[_row][_column] + 1) % 2 != 0:
            grid2[_row][_column] += 1
        else:
            return grid_1
        grid_1 = copy.deepcopy(grid2)

    def crear_laberinto(self):
        for row in range(celdaH):
            for column in range(celdaV):
                if column + 1 < celdaV and row + 1 < celdaH and \
                        grid_1[row][column] == 1 and grid_1[row][column + 1] == 1 and \
                        grid_1[row + 1][column] == 1 and grid_1[row + 1][column + 1] == 1:
                    pared = Pared(row, column, 2, 2)
                    self.paredes.append(pared)
                    grid_1[row][column] = 3
                    grid_1[row][column + 1] = 3
                    grid_1[row + 1][column] = 3
                    grid_1[row + 1][column + 1] = 3
                    print("rect")
                elif column + 1 < celdaV and grid_1[row][column] == 1 and grid_1[row][column + 1] == 1:
                    pared = Pared(row, column, 1, 2)
                    self.paredes.append(pared)
                    grid_1[row][column] = 3
                    grid_1[row][column + 1] = 3
                    print("rect")
                elif row + 1 < celdaH and grid_1[row][column] == 1 and grid_1[row + 1][column] == 1:
                    pared = Pared(row, column, 2, 1)
                    self.paredes.append(pared)
                    grid_1[row][column] = 3
                    grid_1[row + 1][column] = 3
                    print("rect")
                elif grid_1[row][column] == 1:
                    pared = Pared(row, column, 1, 1)
                    self.paredes.append(pared)
                    grid_1[row][column] = 3
                    print("rect")
        #         if grid_1[row][column] == 1:
        #             pared = Pared(row, column, 1, 1)
        #             self.paredes.append(pared)
        #             grid_1[row][column] = 3
        #             print("rect")
        # for _ in range(len(self.paredes[0:])):
        #     self.paredes[0].unir(self.paredes[_].get_body())
        #     # pygame.Rect.unionall_ip(self.paredes[0].body, self.paredes[_].body)

    def dibujar_paredes(self):
        for _ in range(len(self.paredes)):
            self.paredes[_].graficar_pared(screen)

    def choque_pared(self):
        for _ in range(len(self.paredes)):
            for i in range(len(self.lista_bolas)):
                if self.paredes[_].choque_pared_bola(self.lista_bolas[i].get_pos()):
                    self.lista_bolas[i].morir()

    def iniciar_simulacion(self):
        done = False
        go = False
        while go is not True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Cerrar el programa?
                    done = True  # Si
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if event.button == 2:
                        go = True
                        self.crear_laberinto()
                    if pos[0] <= (WIDTH + MARGIN) * celdaV and pos[1] <= (HEIGHT + MARGIN) * celdaH:
                        column = round(pos[0] // (WIDTH + MARGIN))
                        row = round(pos[1] // (HEIGHT + MARGIN))
                        print(grid_1[row][column])
                        if event.button == 3:
                            if grid_1[row][column] != 7 and grid_1[row][column] != 0:
                                self.borrar_ficha(row, column)
                        elif event.button == 1:
                            self.insertar_pieza(row, column)
                        print("Click ", pos, "Grid coordinates: ", row, column)

                # elif event.type == pygame.key.get_pressed():
                #     go = True
                #     print("aa")
            self.dibujar_fondo(1)
            clock.tick(30)
            pygame.display.flip()

        self.crea_bolas(self.poblacion)
        while done is not True:
            if not self.all_dead():
                self.choque_pared()
                self.mover_bolas()
            else:
                self.calcular_score()
                # print("Bolitas resultado")
                # self.mostrar_lista()
                self.selecciona_bolitas()
                # self.mostrar_lista()
                self.cruzar_bolitas()
                # self.mostrar_lista()
                self.mutar_bolitas()

                # input("Press Enter to continue...")
            for event in pygame.event.get():  # Registra eventos variados
                if event.type == pygame.QUIT:  # Cerrar el programa?
                    done = True  # Si
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
            self.dibujar_fondo(0)
            self.dibujar_destino()

            self.dibujar_bolas()
            clock.tick(30)
            pygame.display.flip()
        pygame.quit()  # no borrar

    def __init__(self, IX, IY, DX, DY, PP, PM, _Velocidad_bola):
        self.lista_bolas = {}
        self.destinoX = DX
        self.destinoY = DY
        self.inicioX = IX
        self.inicioY = IY
        self.poblacion = PP
        self.pasos_maximos = PM
        self.paredes = []
        self.velocidad_bola = _Velocidad_bola


Ini_X = 200
Ini_Y = 350
Velocidad_bola = 6
Des_X = 200
Des_Y = 50
Population = 128
Pasos_MAX = 400

juego = Juego(Ini_X, Ini_Y, Des_X, Des_Y, Population, Pasos_MAX, Velocidad_bola)
juego.iniciar_simulacion()
print("a")
