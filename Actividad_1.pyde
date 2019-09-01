# Se importa el módulo que genera número aleatorios
import random

# Clase para los botones
class Boton:
    def __init__(self, x, y, ancho, alto, contenido):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.contenido = contenido
        self.color = (255, 255, 255)
        self.colorBorde = 0
        self.tamanoTexto = 20
        self.colorTexto = 0

    def mouseEnBoton(self):
        return (self.x < mouseX < self.x + self.ancho and
                self.y < mouseY < self.y + self.alto)

    def dibujar(self):
        stroke(self.colorBorde)
        fill(self.color[0], self.color[1], self.color[2])
        rect(self.x, self.y, self.ancho, self.alto)
        
        if (type(self.contenido) == str):
            fill(self.colorTexto)
            textSize(self.tamanoTexto)
            text(self.contenido, self.x + 5, self.y + 20)
        else:
            image(self.contenido, self.x, self.y, self.ancho, self.alto)

    def clickeado(self):
        colorOriginal = self.color
        self.color = (0, 0, 0)
        self.dibujar()
        self.color = colorOriginal

# Cantidad de cuadros - 1 por fila o columna
cantidadCuadros = 10

# Tiempo de delay
tiempoDelay = 50

# Genera un array que contendrá los cuadros del mapa  (filas y columnas)
mapa = [
    # Crea un array que contiene cantidadCuadros (10) ceros: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    [0] * cantidadCuadros
    # Repite lo anterior por cantidadCuadros (10) veces
    for i in range(cantidadCuadros)
]

# Se especifica el tamaño del mapa
tamanoMapa = 600 / cantidadCuadros

# (x,y) Coordenadas iniciales del avatar
avatarX = 0
avatarY = 0

# (x,y) Coordenadas iniciales del tesoro
# El mapa es un array de 10 elementos por eso empieza a contar desde 0 y ubica al tesoro en las coordenadas (9, 9)
tesoroX = (cantidadCuadros - 1)
tesoroY = (cantidadCuadros - 1)

# Botones de Métodos
botonBresenham = Boton(620, 20, 170, 25, "Bresenham")
botonMetodo2 = Boton(620, 60, 170, 25, "Metodo 2")
botonMetodo3 = Boton(620, 100, 170, 25, "Metodo 3")
botonMetodo4 = Boton(620, 140, 170, 25, "Metodo 4")

anchoPasos = 50

pasosBresenham = Boton(botonBresenham.x + botonBresenham.ancho, botonBresenham.y, anchoPasos, botonBresenham.alto, "0")
pasosMetodo2 = Boton(botonMetodo2.x + botonMetodo2.ancho, botonMetodo2.y, anchoPasos, botonMetodo2.alto, "0")
pasosMetodo3 = Boton(botonMetodo3.x + botonMetodo3.ancho, botonMetodo3.y, anchoPasos, botonMetodo3.alto, "0")
pasosMetodo4 = Boton(botonMetodo4.x + botonMetodo4.ancho, botonMetodo4.y, anchoPasos, botonMetodo4.alto, "0")

botonReinicio = Boton(620, 550, 220, 25, "Reiniciar")

barra = Boton(720, 290, 20, 200, "")
barra.color = (0, 0, 0)

# Coordenadas y tamaño del deslizador de la barra
deslizador = Boton(barra.x - 5, barra.y + barra.alto, 30, 20, "")
deslizador.color = (255, 0, 0)
mouseSobreDeslizador       = False
barraBloqueada  = False
yOffset         = 0.0

# Coordenadas y porcentaje de barra en texto
porcentajeX = barra.x
porcentajeY = barra.y - 5
porcentaje  = 0.0

# Variables para la ruta a seguir por el avatar
global rutaBresenham, rutaRecorrida
iteradorBresenham = 0


# Configuración de la interfaz y el juego
def setup():
    # Tamaño de la ventana
    size(860, 600)
    
    global jugando, colocandoAvatar, colocandoTesoro, rutaBresenham, rutaRecorrida, bresenhamActivado, yaJugo
    global imagenGrass, imagenAvatar, imagenTesoro, imagenArbol1, imagenArbol2, imagenArbol3, imagenArbol4, imagenArbol5
    global botonAvatar, botonTesoro

    # Lectura de imagenes
    imagenAvatar    = loadImage("assets/avatar.png")
    imagenGrass     = loadImage("assets/grass3.JPG")
    imagenTesoro    = loadImage("assets/treasure.PNG")
    imagenArbol1    = loadImage("assets/tree1.png")
    imagenArbol2    = loadImage("assets/tree2.png")
    imagenArbol3    = loadImage("assets/tree3.png")
    imagenArbol4    = loadImage("assets/tree4.png")
    imagenArbol5    = loadImage("assets/tree5.png")

    botonAvatar = Boton(640, 180, 70, 70, imagenAvatar)
    botonTesoro = Boton(750, 180, 70, 70, imagenTesoro)

    # Configuración inicial del juego
    jugando             = False
    colocandoAvatar     = False
    colocandoTesoro     = False
    rutaBresenham       = []
    rutaRecorrida       = Pila()
    iteradorBresenham   = 0
    bresenhamActivado   = True
    yaJugo              = False


# Método que se ejecuta siempre
def draw():
    # Si el usuario está jugando entonces el programa encuentra la ruta
    if jugando:
        encontrarCamino()
        delay(tiempoDelay)
    
    # Siempre se dibuja la interfaz
    dibujarInterfaz()


# Método que encuentra la ruta
def encontrarCamino():
    global avatarX, avatarY, rutaRecorrida, jugando, iteradorBresenham, bresenhamActivado, mapa, yaJugo
    
    # Array que guarda las alternativas para cambiar la posición inicial del avatar cuando se encuentra con un árbol
    alternativas = []

    # Se comprueba si el programa ganó
    if avatarX == tesoroX and avatarY == tesoroY:
        ganar()
        return

    # Si el método de búsqueda está seleccionado entonces ejecuta el método de bresenham
    if bresenhamActivado:
        bresenham(avatarX, avatarY, tesoroX, tesoroY)
    
    # Imprime en consola la posición actual del avatar
    print("Avatar en: (" + str(avatarX) + "," + str(avatarY) + ")")

    # Comprueba si la ruta tiene al menos una posición y si en la posición del avatar existe un árbol
    if len(rutaBresenham) > 1 and mapa[rutaBresenham[iteradorBresenham][0]][rutaBresenham[iteradorBresenham][1]] < 5:
        # Se guarda el recorrido del avatar
        rutaRecorrida.insertar( (avatarX, avatarY) )

        # Se cambia la posición del avatar a la siguiente posición de la ruta establecida
        avatarX = rutaBresenham[iteradorBresenham][0]
        avatarY = rutaBresenham[iteradorBresenham][1]

        # Se comprueba si el avatar llegó a su destino
        if(avatarX == tesoroX and avatarY == tesoroY):
            # Gana
            ganar()
            return
        
        # Si el avatar no ha llegado a su destino entonces se pasa a la siguiente posición de la ruta
        iteradorBresenham = iteradorBresenham + 1

        # Se cambia a False para que no establezca una nueva ruta mientras se recorra la ruta actual
        bresenhamActivado = False
        return
    else:
        # Si en la siguiente posición de la ruta existe un árbol entonces en la posición actual del mapa aumenta en 1 para que si vuelve a pasar y
        # existe el árbol se cree un nuevo árbol al llegar a 5 pasadas
        mapa[avatarX][avatarY] = mapa[avatarX][avatarY] + 1
    
    # Como encontró un árbol entonces tiene que establecer una nueva ruta
    bresenhamActivado = True

    contador = 0

    # Se busca en los 8 posibles cambios de coordenadas

    # Con este primer bucle ve si aumenta o disminuye la coordenada actual del avatar en 1 unidad en el eje x
    # x toma los valores de [-1, 0, 1]
    for x in range(-1, 2):
        # Con este segundo bucle ve si aumenta o disminuye la coordenada actual del avatar en 1 unidad en el eje y
        # y toma los valores de [-1, 0, 1]
        for y in range(-1, 2):
            # Se calcula el cambio de coordenadas
            cambioCoordenadaX = avatarX + x
            cambioCoordenadaY = avatarY + y
            
            # Se verifica si las opciones se encuentran dentro del mapa
            if 0 <= cambioCoordenadaX <= cantidadCuadros - 1 and 0 <= cambioCoordenadaY <= cantidadCuadros - 1:
                
                # Comprueba si en el cambio de coordenadas no existe un árbol y si el cambio de coordenadas no coincide con las coordenadas actuales
                if rutaRecorrida.cantidad() > 0 and mapa[cambioCoordenadaX][cambioCoordenadaY] < 5 and (cambioCoordenadaX, cambioCoordenadaY) != rutaRecorrida.ultimoElemento() and not (x == 0 and y == 0):
                    contador = contador + 1

                    # Añade el cambio de coordenada como una de las opciones a cambiar
                    alternativas.append( (x, y) )
                elif rutaRecorrida.estaVacia() and mapa[cambioCoordenadaX][cambioCoordenadaY] < 5 and not (x == 0 and y == 0):
                    contador = contador + 1

                    # Añade el cambio de coordenada como una de las opciones a cambiar
                    alternativas.append( (x, y) )
    
    # Si no encontró opciones de cambio de coordenada y recorrió toda su ruta entonces pierde
    if contador == 0 and rutaRecorrida.cantidad() > 0:
        # Toma la última posición de la ruta
        elem = rutaRecorrida.ultimoElemento()

        # Compara si en la última posición no encontró un árbol
        if mapa[elem[0]][elem[1]] < 5:
            # Aumenta en 1 la aparición del árbol en la coordenada actual del avatar
            mapa[avatarX][avatarY] = mapa[avatarX][avatarY] + 1
            
            # Mueve al avatar a la última posición de la ruta
            avatarX = elem[0]
            avatarY = elem[1]

            # Elimina la última posición
            rutaRecorrida.soltar()
            return

        # Pierde
        perder()
        return
    
    # Si no encontró opciones y no hay ruta entonces pierde
    elif contador == 0 and rutaRecorrida.cantidad() == 0:
        # Pierde
        perder()
        return
    
    # Si encuentra opciones entonces escoge la nueva posición de inicio del avatar de manera aleatoria
    aux = random.choice(alternativas)

    # Inserta a la ruta recorrida la posición del avatar
    rutaRecorrida.insertar((avatarX, avatarY))

    # Coloca al avatar en la nueva posición encontrada
    avatarX = avatarX + aux[0]
    avatarY = avatarY + aux[1]

    # Comprueba si con la nueva posición ganó
    if(avatarX == tesoroX and avatarY == tesoroY):
        # Gana
        ganar()
        return


# Método que se ejecuta cuando se gana
def ganar():
    global yaJugo, bresenhamActivado, jugando
    print("GANASTE")
    yaJugo              = True
    bresenhamActivado   = True
    jugando             = False


# Método que se ejecuta cuando se pierde
def perder():
    global yaJugo, bresenhamActivado, jugando
    print("PERDISTE")
    jugando             = False
    bresenhamActivado   = True
    yaJugo              = True


# Método que muestra la interfaz
def dibujarInterfaz():
    background(255)
    dibujarMapa()
    dibujarBotones()
    mostrarPorcentajeBarra()

def dibujarBotones():
    #Dibujar los cuadrados de Pasos
    botonAvatar.dibujar()
    botonTesoro.dibujar()
    botonBresenham.dibujar()
    botonMetodo2.dibujar()
    botonMetodo3.dibujar()
    botonMetodo4.dibujar()
    pasosBresenham.dibujar()
    pasosMetodo2.dibujar()
    pasosMetodo3.dibujar()
    pasosMetodo4.dibujar()
    barra.dibujar()
    dibujarDeslizador()
    botonReinicio.dibujar()

# Dibuja el mapa
def dibujarMapa():
    global mapa
    # Las imagenes se colocan cada tamanoMapa (10) unidades en el eje X e Y con un ancho y alto de tamanoMapa (10) unidades
    
    # Empieza en las coordenadas (0, 0)
    x, y = 0, 0
    
    # Recorre todo el mapa, celda por celda para colocar las imágenes
    for fila in mapa:
        for columna in fila:

            # Siempre coloca grass en cada celda
            image(imagenGrass, x, y, tamanoMapa, tamanoMapa)

            # Verifica si en esa celda va grass o un árbol de cualquier nivel
            image(seleccionarImagen(columna), x, y, tamanoMapa, tamanoMapa)

            # Incrementa el valor de la coordenada X en tamanoMapa (10) unidades por cada columna
            x = x + tamanoMapa

        # Incremente el valor de la coordenada Y en tamanoMapa (10) unidades por cada fila
        y = y + tamanoMapa

        # Reinicia en 0 la coordenada X porque se cambia de fila
        x = 0
    
    # Colocando el tesoro en su ubicación
    image(imagenTesoro, tesoroY * tamanoMapa, tesoroX * tamanoMapa, tamanoMapa, tamanoMapa)

    # Colocando al avatar en su ubicación
    image(imagenAvatar, avatarY * tamanoMapa, avatarX * tamanoMapa, tamanoMapa, tamanoMapa)


def dibujarDeslizador():
    global mouseSobreDeslizador
    if deslizador.mouseEnBoton():
        mouseSobreDeslizador = True
        if not barraBloqueada:
            deslizador.colorBorde = 120
    else:
        deslizador.colorBorde = 255
        mouseSobreDeslizador = False
    deslizador.dibujar()


def mostrarPorcentajeBarra():
    text(str(porcentaje) + "%", porcentajeX-8, porcentajeY)


def quitarAvatar():
    global avatarX, avatarY
    avatarX = -1000/tamanoMapa
    avatarY = -1000/tamanoMapa


def quitarTesoro():
    global tesoroX, tesoroY
    tesoroX = -1000/tamanoMapa
    tesoroY = -1000/tamanoMapa


def limpiarMapa():
    for i in range(cantidadCuadros):
        for j in range(cantidadCuadros):
            mapa[i][j] = 0


def colocarArboles():
    global avatarX, avatarY, tesoroX, tesoroY
    v = [[(j, i) for i in range(0, cantidadCuadros)]
         for j in range(0, cantidadCuadros)]
    limpiarMapa()
    total = cantidadCuadros*cantidadCuadros
    objectsP = int(total*porcentaje)/100
    if avatarX == tesoroX and avatarY == tesoroY:
        avatarX = 0
        avatarY = 0
        tesoroX = cantidadCuadros-1
        tesoroY = cantidadCuadros-1
    if objectsP > total-2:
        objectsP = total-2
    v[avatarX].remove((avatarX, avatarY))
    v[tesoroX].remove((tesoroX, tesoroY))
    print(objectsP)
    while objectsP > 0:
        aux = random.choice(v)
        while len(aux) == 0:
            aux = random.choice(v)
        pos = random.choice(aux)
        if mapa[pos[0]][pos[1]] != 5 and not(pos[0] == avatarX and pos[0] == tesoroX) and not(pos[1] == avatarY and pos[1] == tesoroY):
            mapa[pos[0]][pos[1]] = 5
            objectsP -= 1
            aux.remove(pos)
        elif mapa[pos[0]][pos[1]] != 5 and avatarX == tesoroX and pos[0] == avatarX and pos[1] != avatarY and pos[1] != tesoroY:
            mapa[pos[0]][pos[1]] = 5
            objectsP -= 1
            aux.remove(pos)
        elif mapa[pos[0]][pos[1]] != 5 and avatarY == tesoroY and pos[1] == avatarY and pos[0] != avatarX and pos[0] != tesoroX:
            mapa[pos[0]][pos[1]] = 5
            objectsP -= 1
            aux.remove(pos)


def dda():
    rutita = []
    dx = tesoro2X - avatar2X
    dy = tesoro2Y - avatar2Y
    
    if dx > dy:
        pendiente = dy / dx
        valorConstanteRecta = avatar2Y - pendiente* avatar2X
        if dx<0 :
            dx = -1
        else:
            dx = 1
        while avatar2X != tesoro2X:
            avatar2X += dx
            avatar2Y = round(pendiente * avatar2X + valorConstanteRecta)
            rutita.push( [avatar2X, avatar2Y] )
    elif dy != 0 : 
        pendiente = dx / dy
        valorConstanteRecta = avatar2X - pendiente*avatar2Y
        if dy<0:
            dy =  -1
        else:
            dy =  1
        while avatar2Y != tesoro2Y:
            avatar2Y += dy
            avatar2X = round(pendiente * avatar2Y + valorConstanteRecta)
            rutita.push( [avatar2X, avatar2Y] )
            
    print(rutita)


def bresenham(coordenadaAvatarX, coordenadaAvatarY, coordenadaTesoroX, coordenadaTesoroY):
    global rutaBresenham, iteradorBresenham
    iteradorBresenham = 1
    rutaBresenham = []

    # Se calcula la distancia que hay entre coordenadas con sus respectivos ejes
    distanciaX = coordenadaTesoroX - coordenadaAvatarX
    distanciaY = coordenadaTesoroY - coordenadaAvatarY

    # Se verifica si las distancias son negativas o positivas para comprobar en qué cuadrante se encuentra la ruta 
    # a seguir y así encontrar el vector unitario que indica la dirección de la ruta a seguir

    # Si la ruta se encuentra en el primer cuadrante entonces el vector unitario será (1, 1)
    # Si la ruta se encuentra en el segundo cuadrante entonces el vector unitario será (-1, 1)
    # Si la ruta se encuentra en el tercer cuadrante entonces el vector unitario será (-1, -1)
    # Si la ruta se encuentra en el cuarto cuadrante entonces el vector unitario será (1, -1)

    # Esto le indica cómo moverse en diagonal
    movimientoInclinadoX = 1 if distanciaX >= 0 else -1
    movimientoInclinadoY = 1 if distanciaY >= 0 else -1

    # Se pasa todo al primer cuadrante solo para usar un solo bucle
    distanciaX = abs(distanciaX)
    distanciaY = abs(distanciaY)

    # Comprueba qué distancia es mayor para así indicarle al avatar en qué eje se debe mover sí o sí en una 1 unidad
    # mientras que para la distancia menor se moverá AVECES en 1 unidad en el eje respectivo

    # Esto indica cómo moverse en línea recta
    if distanciaX >= distanciaY:

        # Eje X: (1, 0) o (-1, 0)
        movimientoRectoEjeXX = movimientoInclinadoX
        movimientoRectoEjeXY = 0

        # Eje Y: (0, 1) o (0, -1)
        movimientoRectoEjeYX = 0
        movimientoRectoEjeYY = movimientoInclinadoY
    else:
        # Intercambia las distancias con el fin de usar el mismo algoritmo para el otro caso
        distanciaX, distanciaY = distanciaY, distanciaX

        # Eje Y: (0, 1) o (0, -1)
        movimientoRectoEjeXX = 0
        movimientoRectoEjeXY = movimientoInclinadoX

        # Eje X: (1, 0) o (-1, 0)
        movimientoRectoEjeYX = movimientoInclinadoY
        movimientoRectoEjeYY = 0

    # Nota: en el algoritmo original no se hace las vainas raras que se hacen aquí

    # Constante que verifica en cada iteración del bucle si el avatar se movió en el eje menor en una unidad o no.
    # Para saber de dónde sale el 2 * dy - dx revisar: https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm#Derivation
    constanteP = 2 * distanciaY - distanciaX

    # Parte desde el "origen" (0, 0)
    # x = 0
    y = 0

    print("Ruta establecida:")

    # Se realiza el bucle para buscar la ruta
    # Desde X = 0 hasta X = distanciaX
    for x in range(distanciaX + 1):

        # Avanza de manera diagonal o recta según la constante P
        coordenadaX = coordenadaAvatarX + x * movimientoRectoEjeXX + y * movimientoRectoEjeYX
        coordenadaY = coordenadaAvatarY + x * movimientoRectoEjeXY + y * movimientoRectoEjeYY

        # Inserta la coordenada siguiente en la lista rutaBresenham
        rutaBresenham.append( ( coordenadaX, coordenadaY ) )

        print("\tPosicion N " + str(x + 1) + ": (" + str(coordenadaX) + ", " + str(coordenadaY) + ")")

        # Con esto verifica si el avatar se movió 1 unidad o no en el eje menor
        # Pero como sí o sí se hacen los cálculos como si dx fuese mayor entonces se incrementa en Y aveces
        if constanteP >= 0:
            y = y + 1
            # Este cálculo se hace por el algoritmo
            constanteP = constanteP - 2 * distanciaX
        # Este cálculo se hace por el algoritmo
        constanteP = constanteP + 2 * distanciaY


def mousePressed():
    global colocandoTesoro, colocandoAvatar, mouseSobreDeslizador, barraBloqueada, yOffset, jugando, mapa, yaJugo
    global avatarX, avatarY, tesoroX, tesoroY

    if botonBresenham.mouseEnBoton():
        yaJugo = False
        jugando = True
        botonBresenham.clickeado()

    if botonMetodo2.mouseEnBoton():
        botonMetodo2.clickeado()

    if botonMetodo3.mouseEnBoton():
        botonMetodo3.clickeado()

    if botonMetodo4.mouseEnBoton():
        botonMetodo4.clickeado()

    if botonAvatar.mouseEnBoton():
        yaJugo = False
        botonAvatar.clickeado()
        quitarAvatar()
        colocandoAvatar = True

    if botonTesoro.mouseEnBoton():
        yaJugo = False
        botonTesoro.clickeado()
        quitarTesoro()
        colocandoTesoro = True

    if botonReinicio.mouseEnBoton():
        botonReinicio.clickeado()
        yaJugo = False
        colocarArboles()

    if mouseSobreDeslizador:
        barraBloqueada = True
    else:
        barraBloqueada = False

    if (mouseX/tamanoMapa) < cantidadCuadros and (mouseY/tamanoMapa) < cantidadCuadros:
        yaJugo = False
        if mapa[mouseY/tamanoMapa][mouseX/tamanoMapa] == 5:
            mapa[mouseY/tamanoMapa][mouseX/tamanoMapa] = 0
        else:
            mapa[mouseY/tamanoMapa][mouseX/tamanoMapa] = 5

        if colocandoAvatar:
            avatarX = mouseY/tamanoMapa
            avatarY = mouseX/tamanoMapa
            if(mapa[avatarX][avatarY] >= 0 and mapa[avatarX][avatarY] <= 5):
                mapa[avatarX][avatarY] = 0
            print("AVATAR: "+str(avatarX) + ' ' + str(avatarY))
            colocandoAvatar = False
        elif colocandoTesoro:
            tesoroX = mouseY/tamanoMapa
            tesoroY = mouseX/tamanoMapa
            if(mapa[tesoroX][tesoroY] >= 0 and mapa[tesoroX][tesoroY] <= 5):
                mapa[tesoroX][tesoroY] = 0
            print("TREASURE: "+str(tesoroX) + ' ' + str(tesoroY))
            colocandoTesoro = False
    yOffset = mouseY - deslizador.y


def mouseDragged():
    global porcentaje, yaJugo
    if barraBloqueada:
        yaJugo = False
        deslizador.y = mouseY - yOffset
        if deslizador.y < barra.y:
            deslizador.y = barra.y
        if deslizador.y > barra.y + barra.alto:
            deslizador.y = barra.y + barra.alto
        porcentaje = (float(barra.y+barra.alto-deslizador.y)
                      * 100.0) / float(barra.alto)
        print(porcentaje)
        colocarArboles()


def mouseReleased():
    barraBloqueada = False


# Método que retorna la imagen del valor del árbol
def seleccionarImagen(celda):
    return {
        0: imagenGrass,     # No existe árbol
        1: imagenArbol1,    # Árbol nivel 1
        2: imagenArbol2,    # Árbol nivel 2
        3: imagenArbol3,    # Árbol nivel 3
        4: imagenArbol4,    # Árbol nivel 4
        5: imagenArbol5     # Árbol nivel 5
    }.get(celda, imagenArbol5)  # Si el valor del parámetro es un número que no se encuentra en el intervalo [0 - 5] entonces retorno un árbol de nivel 5


# Creación de la estructura de datos 'Pila'
class Pila:
    # Método constructor
    def __init__(self):
        self.lista = []

    # Devuelve True o False si está vacío o no respectivamente
    def estaVacia(self):
        return self.lista == []

    # Inserta un elemento a la lista en la última posición
    def insertar(self, item):
        self.lista.append(item)

    # Devuelve y elimina el último elemento de la lista
    def soltar(self):
        return self.lista.pop()

    # Devuelve el último elemento de la lista
    def ultimoElemento(self):
        return self.lista[len(self.lista)-1]

    # Devuelve la cantidad de elementos de la lista
    def cantidad(self):
        return len(self.lista)
