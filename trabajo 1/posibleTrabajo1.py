from builtins import Warning

import pygame
import pygame_menu
import copy
import numpy
import random
import csv
import pandas as pd


# Define los colores a usarse, pueden agregarse mas
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

# Ancho y alto de los bloques
# WIDTH = 20
# HEIGHT = 20

# espacio entre casillas
MARGIN = 0
global grid_1 #Consideramos a esta variable global como el mapa de nuestro pantalla, donde cada 0 representara 42 * 42 pixeles.

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


class Bola:  # Creacion de clase Bola la cual es el gen que se utilizar para poder realizar este proyecto.
    velocidad = 0 # Velocidad de la bola
    posX = 0
    posY = 0    # Posiciones de Inicio 
    score = 0    #Heuristica Basada en su puntaje
    distancia = 0   # Distancia hasta el objetivo
    is_ded = False
    choque = False
    mutacion = 0.15 # Porcentaje de mutacion

    def __init__(self, v, c, px, py, pasos_maximos=None):
        if pasos_maximos == None:
            self.velocidad = v
            self.color = c
            self.posX = px
            self.posY = py
            self.pasos = []
            self.score = 0
            self.pasoActual=0            
        else:
            self.velocidad = v
            self.color = c
            self.posX = px
            self.posY = py
            self.pasos = []
            self.crear_pasos(pasos_maximos)
            self.score = 0
            self.pasoActual=0

    def crear_pasos(self, _pasos_maximos): # Inicializa un random asiganandole 4  valores random, el cual sera los pasos que dara la bola(gen).
        for i in range(_pasos_maximos):
            self.pasos.append(numpy.random.randint(0, 4))

    def objetivo(self, objetivoX, objetivoY): #Nos permite saber a que distancia se encuenta la bola(gen) del objetivo(meta)
        return numpy.sqrt(numpy.power(self.posX - objetivoX, 2) + numpy.power(self.posY - objetivoY, 2)) < 10

    def mover(self, objetivoX, objetivoY): #Definimos esta funcions para que la bola(gen) realice sus movimientos respecto a los pasos asiganos anteriormente
        if not self.is_ded:
            if not self.choque:
                if self.objetivo(objetivoX, objetivoY):
                    self.is_ded = True
                    print("Llegue al objetivo")
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
                    else:
                        self.is_ded = True
                else:
                    self.choque = True
                    self.is_ded = True

    def graficar(self, screen):
        pygame.draw.circle(screen, self.color, [self.posX, self.posY], 5, 1)

    def calcularScore(self, destX, destY, _inicX, _inicY): #Utilizamos esta funcion para poder calcular el valor de la heuristca que tiene cada bola respecto al objetivo(meta)
        if self.choque:
            self.score = -99
        else:
            self.score = numpy.sqrt(numpy.power(_inicX - destX, 2) + numpy.power(_inicY - destY, 2)) /\
                         numpy.sqrt(numpy.power(self.posX - destX, 2) + numpy.power(self.posY - destY, 2)) + (
                    len(self.pasos) - self.pasoActual) - (numpy.sqrt(numpy.power(_inicX - destX, 2) +
                                                                    numpy.power(_inicY - destY, 2)) / numpy.sqrt(
                numpy.power(self.posX - _inicX, 2) + numpy.power(self.posY - _inicY, 2)))
        print(self.score)

    def get_pasos(self):
        return self.pasos

    def get_score(self):
        return self.score

    def get_pos(self):
        return [self.posX, self.posY]

    def morir(self):
        self.is_ded = True
        self.choque = True

    def reiniciar_pasos(self): #Utilizamos esta funcion para poder reniciar los pasos que la bola(gen) tenia cuando se guardo y asi solo tener el valor real de sus pasos.
        self.pasoActual=0

class Pared: #Se crea esta clase la cual nos permitira la creacion de paredes dentro del mapa de juego.
    def graficar_pared(self, _screen):
        pygame.draw.rect(_screen, GRAY, self.body, 1)

    def unir(self, _pared):  # 
        pygame.Rect.union_ip(self.body, _pared)

    def choque_pared_bola(self, _pos): #Verificacion si la bola(gen), colisionaron entre ellas
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

class Juego: #Se define esta clase puesto que sera la controladora para iniciar el juego.
    def init_menu(self): #Se define esta funcion para la creacion de un menu.
        surface = pygame.display.set_mode(WINDOW_SIZE)   
        menu = pygame_menu.Menu('Main Menu',400, 400,theme=pygame_menu.themes.THEME_BLUE)

        about_menu=pygame_menu.Menu(400,400,"Sobre Nosotros",theme=pygame_menu.themes.THEME_DARK)
        about_menu.add.label("Realizado por :",align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        about_menu.add.label(" Hamill Cavero - u201821775",align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        about_menu.add.label(" Elvis Morales - u201820751",align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        about_menu.add.label(" Aldo Gomez - u201822450",align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        about_menu.add.vertical_margin(30)
        about_menu.add.button('Return to menu', pygame_menu.events.BACK)

        instrucciones_menu=pygame_menu.Menu(400,400,"Instrucciones",theme=pygame_menu.themes.THEME_DARK)
        instrucciones_menu.add.label("El juego se autoguarda cuando se cierra.",align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        instrucciones_menu.add.label("Numero 7 : para definir posicion \n del enemigo",align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        instrucciones_menu.add.label("Numero 8 : para definir posicion \n del del jugador",align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        instrucciones_menu.add.label("Click Izquierdo: Poner paredes",align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        instrucciones_menu.add.label("Click Derecho: Quitar paredes",align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        instrucciones_menu.add.label("Click Scroll Mouse: Iniciar la genetica",align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        instrucciones_menu.add.label("Numero 9: Para abrir un mapa guardado \nal iniciar el juego",align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        instrucciones_menu.add_button("Return to menu",pygame_menu.events.BACK)
           
        menu.add.button('Play',self.iniciar_simulacion)
        menu.add.button('About', about_menu)
        menu.add.button('Instrucciones', instrucciones_menu)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        
        menu.mainloop(surface)
        
    def dibujar_fondo(self, creacion): # Se utiliza esta funcion para poder dibujar en la pantalla
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

    def crea_bolas(self, N): #Esta funcion nos permite la creacion de la lista de bola segun la poblacion ingresada.
        for _ in range(N):
            self.lista_bolas[_] = Bola(self.velocidad_bola, RED, self.inicioX, self.inicioY, self.pasos_maximos)
    def mover_bolas(self): #Realiza el movimiento de las bolas(genes)
        for bb in self.lista_bolas:
            if self.lista_bolas[bb].is_ded is False:
                self.lista_bolas[bb].mover(self.destinoX, self.destinoY)

    def dibujar_bolas(self): #Imprime las bolas(genes) en pantalla
        for i in range(len(self.lista_bolas)):
            self.lista_bolas[i].graficar(screen)

    def calcular_score(self):#Calcula el valor de heuristica para cada bola dentro de la lista de bolas(genes)
        for i in range(len(self.lista_bolas)):
            self.lista_bolas[i].calcularScore(self.destinoX, self.destinoX, self.inicioX, self.inicioY)

    def all_dead(self): #Verifica si las bolas(genes) murieron(colisonaron)
        for _ in self.lista_bolas:
            if self.lista_bolas[_].is_ded:
                return True
            else:
                return False

    def mostrar_lista(self):
        for _ in self.lista_bolas:
            print(_, "  ", self.lista_bolas[_].get_score(), self.lista_bolas[_].get_pasos())

    #Utilizamos esta funcion para poder guardar los valores de inicializacion de las Bolas(Genes)
    def guardar_datos_inicializacion(self,iniciox,inicioy,llegadax,llegaday,velocidad,pobla,max_pasos):
        fic=open('LasList.txt',"w")
        fic.write(str(iniciox)+",")
        fic.write(str(inicioy)+",")
        fic.write(str(llegadax)+",")
        fic.write(str(llegaday)+",")
        fic.write(str(velocidad)+",")
        fic.write(str(pobla)+",")
        fic.write(str(max_pasos))
      
    #Esta funcion nos permite leer los valores de inicializacion guardados
    def abrir_Valores_inicializacion(self):
        fic=open("LasList.txt","r")
        dtos=fic.readlines()
        sv=[]
        for lines in dtos:
            sv.append(lines.split(","))     
        self.inicioX =int(sv[0][0])
        self.inicioY =int(sv[0][1])
        self.destinoX = int(sv[0][2])
        self.destinoY = int(sv[0][3])
        self.velocidad_bola =int(sv[0][4])
        self.poblacion = int(sv[0][5])
        self.pasos_maximos = int(sv[0][6])

    #Esta funcion nos permite guardar la ultima generacion de las bolas(Genes) directamente del diccionario
    def guardar_ultimageneracion(self):
        numpy.save("ultima_gen.npy",self.lista_bolas) 

    #Nos permite leer los datos guardados de la ultima generacion y insertalos en la lista de bolas
    def cargar_ultimageneracion(self):
        self.lista_bolas = numpy.load("ultima_gen.npy", allow_pickle="TRUE").item()
        for _ in self.lista_bolas:
            self.lista_bolas[_]=self.lista_bolas[_].reiniciar_pasos()

    def Parejas(self): #Utilizamos esta funcion para agregar parejas a nuestra poblacion de genes de forma random (aleatoria).
        Aleatorio = random.sample(range(int(self.poblacion / 2), self.poblacion), int(self.poblacion / 2))
        Pareja = {}
        for i in range(int(self.poblacion / 2)):
            Pareja[i] = Aleatorio[i]
            Pareja[Aleatorio[i]] = i
        return Pareja

    def selecciona_bolitas(self): #Selecciona las parejas con mayor puntaje en el juego para poder obtener a los mejores de su generacion
        print('---Seleccion----')
        lista_seleccion = self.Parejas()
        for k, v in lista_seleccion.items():
            if self.lista_bolas[k].score >= self.lista_bolas[v].score:
                self.lista_bolas[v] = self.lista_bolas[k]
            else:
                self.lista_bolas[k] = self.lista_bolas[v]

    def cruzar_bolitas(self):
        print('-----Cruce ------')
        lista_seleccion = self.Parejas()
        item = 0
        for k, v in lista_seleccion.items():
            if item % 2 == 0:
                Punto = random.randint(1, self.pasos_maximos)
                Hijo1 = Bola(self.velocidad_bola, RED, self.inicioX, self.inicioY)
                Hijo2 = Bola(self.velocidad_bola, RED, self.inicioX, self.inicioY)
                Padre1 = self.lista_bolas[k]
                Padre2 = self.lista_bolas[v]

                Hijo1.get_pasos().extend(Padre1.pasos[0:Punto])
                Hijo1.get_pasos().extend(Padre2.pasos[Punto:])
                Hijo2.get_pasos().extend(Padre2.pasos[0:Punto])
                Hijo2.get_pasos().extend(Padre1.pasos[Punto:])

                self.lista_bolas[k] = Hijo1
                self.lista_bolas[v] = Hijo2
            item = item + 1

    def mutar_bolitas(self): # Muta un valor en los pasos que da la bola, para que  pueda aprender hasta llegar a la meta.
        for _ in self.lista_bolas:
            if random.random() > self.lista_bolas[_].mutacion:
                random_pos = numpy.random.randint(0, self.pasos_maximos - 1)
                random_val = numpy.random.randint(0, 4)
                self.lista_bolas[_].pasos[random_pos] = random_val

    def dibujar_destino(self): #Imprime el punto de destino
        pygame.draw.circle(screen, GREEN, [self.destinoX, self.destinoY], 5)

#Estas dos funciones nos permiten poner paredes en el mapa y borrarlas antes de iniciar el juego
    def borrar_ficha(self, _row, _column):
        if grid_1[_row][_column] == 1:
            grid_1[_row][_column] = 0

    def insertar_pieza(self, _row, _column):
        global grid_1
        grid2 = copy.deepcopy(grid_1)
        if (grid2[_row][_column] + 1) % 2 != 0:
            grid2[_row][_column] += 1
        else:
            return grid_1
        grid_1 = copy.deepcopy(grid2)
#Esta funcion realiza la creacion del laberinto, segun el tamaño de la CELDAH y CELDA V
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
    
    #Nos permite guardar el mapa, en el que estamos trabajando
    def guardar_mapa2(self):
        fic=open("mapa_save.txt","w")
        for i in range(len(grid_1)):
            for j in range(len(grid_1[i])):
                fic.write(str(grid_1[i][j]))
       
    #Nos permite leer y cargar el mapa guardado
    def cargar_mapa2(self):
        global grid_1
        fic=open("mapa_save.txt","r")
        dtos=fic.read()
        sv=[]
        w=10
        h=10
        jb=[[0 for x in range(w)] for y in range(h)]
        fila=0
        for lines in dtos:
            sv.extend(lines.split())

        sv=[int(x) for x in sv]
  
        for f in range(int(len(sv)/10)):
            for g in range(int(len(sv)/10)):
                jb[f][g]=sv[fila]
                print(fila)
                fila=fila+1
                
        grid_1=copy.deepcopy(jb)
        for i in range(len(grid_1)):
           for j in range(len(grid_1[i])):
                if grid_1[i][j]==3:
                    grid_1[i][j]=1
    
    def dibujar_paredes(self):
        for _ in range(len(self.paredes)):
            self.paredes[_].graficar_pared(screen)

    #Verifica si la bola(gen) choco contra alguna pared
    def choque_pared(self):
        for _ in range(len(self.paredes)):
            for i in range(len(self.lista_bolas)):
                if self.paredes[_].choque_pared_bola(self.lista_bolas[i].get_pos()):
                    self.lista_bolas[i].morir()

    #Inicializa todas las funciones para poder comenzar con el juego de Inteligencia Artificial mediante algoritmos geneticos
    def iniciar_simulacion(self):
        done = False
        go = False
        save=False
        while go is not True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Cerrar el programa?
                    done = True  # Si
                    pygame.quit() #Cierra el programa

                elif event.type==pygame.KEYDOWN: #Verifica si se ha presionado alguna tecla
                    if  event.key==pygame.K_9: #Inicializa el juego con los datos guardados
                        go=True
                        self.cargar_mapa2()
                        self.abrir_Valores_inicializacion()
                        self.cargar_ultimageneracion()
                        self.crear_laberinto()

                    if  event.key==pygame.K_7: #Nos permite seleccionar el inicio de la bola(gen)
                        save=False
                        while save is not True:
                            for evento in pygame.event.get():
                                if evento.type == pygame.MOUSEBUTTONDOWN:  
                                    pos = pygame.mouse.get_pos()
                                    self.inicioX=pos[0]
                                    self.inicioY=pos[1]
                                    print(self.inicioX,self.inicioY)
                                    save=True

                    if  event.key==pygame.K_8:#Nos permite seleccionar el destino que tendra que llegar la bola(gen)
                        save=False
                        while save is not True:
                            for evento in pygame.event.get():
                                if evento.type == pygame.MOUSEBUTTONDOWN:  
                                    pos = pygame.mouse.get_pos()
                                    self.destinoX=pos[0]
                                    self.destinoY=pos[1]
                                    print(self.destinoX,self.destinoY)
                                    save=True
                        
                elif event.type == pygame.MOUSEBUTTONDOWN: #Detecta si estamos realizando clicks con el mouse
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

               self.selecciona_bolitas()

               self.cruzar_bolitas()

               self.mutar_bolitas()

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

        self.guardar_mapa2()
        self.guardar_datos_inicializacion(self.inicioX,self.inicioY,self.destinoX,self.destinoY,self.velocidad_bola,self.poblacion,self.pasos_maximos)
        self.guardar_ultimageneracion()
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

#Valores iniciales del juego
Velocidad_bola = 6
Population = 128
Pasos_MAX = 400
Ini_X = 200
Ini_Y = 350
Des_X = 200
Des_Y = 50
#Comienza a correr todo el programa
juego = Juego(Ini_X, Ini_Y, Des_X, Des_Y, Population, Pasos_MAX, Velocidad_bola)
juego.init_menu()
