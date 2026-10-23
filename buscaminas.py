from typing import TextIO #importo tipo de dato TextIo para archivos
from random import randint
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))

#1.
def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    '''Devuelve un tablero de dimension "filas x columnas", y coloca una cantidad de minas aleatoriamente.'''

    tablero:list[list[int]] = []

    for fila in range(filas): #se crea un tablero vacio con las dimensiones dadas
        tablero += [[]]

        for _ in range(columnas):
            tablero[fila].append(0)

    insertar_minas_aleatoriamente(tablero,minas) # llamo a la funcion para colocar aleatoriamente la cantidad de minas

    #debería ocurrir: es_matriz(tablero) == True 
        
    return tablero

def es_matriz(t:list[list[Any]]) -> bool:
    '''Devuelve True si el tablero es matriz.'''

    largo_filas:int = len(t)
    largo_columnas:int = len(t[0])
    resultado:bool = True

    if largo_columnas <= 0 or largo_filas <=0:
        resultado = False
    
    i=0
    while resultado and i < largo_filas: #comprueba si todas las columnas miden lo mismo
        largo_columna_actual:int = len(t[i])
        
        if largo_columna_actual != largo_columnas:
            resultado = False
        
        i+=1
    
    return resultado

def insertar_minas_aleatoriamente(tablero: list[list[int]],cantidad: int): 
    '''Funcion auxiliar que modifica el tablero, insertando cierta cantidad de minas en posiciones aleatorias.'''

    largo_filas:int = len(tablero)
    largo_columnas:int  = len(tablero[0])

    while cantidad > 0:
        #se elige una celda random
        fila_random:int = randint(0,largo_filas-1)
        columna_random:int = randint(0,largo_columnas-1)

        #si en la celda no hay minas, agregar una mina
        if tablero[fila_random][columna_random] != -1:
            tablero[fila_random][columna_random] = -1
            cantidad-=1


#2
def calcular_numeros(tablero: list[list[int]]) -> None:
    '''Modifica el valor de cada celda del tablero según las minas que tenga alrededor.

    Si la celda es una mina, no se modifica.
    Sino, el valor de la celda será igual a la cantidad de minas adyacentes que haya.
    '''
    largo_filas:int = len(tablero)
    largo_columnas:int = len(tablero[0])

    for x in range(largo_filas):
        for y in range(largo_columnas):

            if  tablero[x][y]!= -1:#si en la posicion actual no hay una mina

                adyacentes:list[int] = celdas_adyacentes(tablero,(x,y))
                cantidad_minas:int = contar_minas(adyacentes)
                tablero[x][y] = cantidad_minas

def celdas_adyacentes(tablero: list[list[int]],posicion:tuple[int,int] ) -> list[int]:
    '''Funcion auxiliar que devuelve el valor que tengan las celdas adyacentes a la posición dada.'''

    largo_filas:int = len(tablero)-1
    largo_columnas:int = len(tablero[0])-1
    celdas:list[int] = []
    x:int = posicion[0]
    y:int = posicion[1]

    #posiciones alrededor de la posicion dada
    posiciones_adyacentes:list[tuple[int,int]] = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]
    
    for fila,columna in posiciones_adyacentes:#recorro todas las posiciones adyacentes
        
        #chequea que la posicion no esté fuera del tablero
        if not((fila>largo_filas or fila < 0) or (columna > largo_columnas or columna<0)):
            celdas.append(tablero[fila][columna])

    return celdas

def contar_minas(celdas:list[int]) -> int:
    '''Funcion auxiliar que cuenta las minas que hay en una lista'''

    cantidad:int = 0
    for celda in celdas:
        if celda == -1:
            cantidad+=1
    
    return cantidad
        
    
# EJERCICIO 3
def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    '''Devuelve un EstadoJuego con una cierta cantidad de filas, columnas y minas.
    
    El EstadoJuego que devuelve es equivalente a una partida sin comenzar.
    '''
    nuevo_dicc: dict= {}
    nuevo_dicc["filas"] = filas
    nuevo_dicc["columnas"] = columnas
    nuevo_dicc["minas"] = minas

    tablero_visible:list[list[str]] = []
    fila_tablero:list[str] = []

    for fila in range(filas):
        for columna in range(columnas):
            fila_tablero.append(" ")
        tablero_visible.append(fila_tablero)
        fila_tablero = []

    nuevo_dicc["tablero"] = colocar_minas(filas, columnas, minas)
    calcular_numeros(nuevo_dicc["tablero"])
    nuevo_dicc["tablero_visible"] = tablero_visible
    nuevo_dicc["juego_terminado"] = False

    #esto deberia poder cumpir estado_valido(nuevo_dicc)

    return nuevo_dicc

#Estas funciones tal vez se usen en los casos de test:
def estado_valido(estado: EstadoJuego) -> bool:
    '''Devuelve True si los valores en estado no se contradicen.
    
    Nota: También se comprueba estructura_y_tipos_validos(estado)
    '''
    resultado:bool = True
    
    minas:int = 0
    for fila in estado["tablero"]:
        minas += contar_minas(fila)

    bomba_en_tablero_visible:bool = False
    for fila in estado["tablero_visible"]:
        
        if BOMBA in fila:
            bomba_en_tablero_visible = True
    
    tablero_copia:list[list[int]] = []

    #Copio el tablero
    for f in range(len(estado["tablero"])):
        tablero_copia.append([])
        for c in range(len(estado["tablero"][0])):
            tablero_copia[f].append(estado["tablero"][f][c])
            
    calcular_numeros(tablero_copia)

    calcular_numeros_no_cambia:bool = True
    BOMBA_entonces_hay_mina:bool = True
    tablero_visible_valido:bool = True

    for f in range(estado["filas"]):
        for c in range(estado["columnas"]):
            
            if estado["tablero_visible"][f][c] == BOMBA and estado["tablero"][f][c] != -1:
                BOMBA_entonces_hay_mina = False
            
            if not (estado["tablero_visible"][f][c] in [VACIO,BANDERA,BOMBA]) and estado["tablero_visible"][f][c] != str(estado["tablero"][f][c]):
                tablero_visible_valido = False

            if estado["tablero"][f][c] != tablero_copia[f][c]:
                calcular_numeros_no_cambia = False


    #--------------------------------------------
    if not estructura_y_tipos_validos(estado):
        resultado = False

    elif minas != estado["minas"]:
        resultado = False

    elif calcular_numeros_no_cambia == False:
        resultado = False

    elif estado["juego_terminado"] == False and (todas_celdas_seguras_descubiertas(estado["tablero"],estado["tablero_visible"]) or bomba_en_tablero_visible):
        resultado = False

    elif BOMBA_entonces_hay_mina == False:
        resultado = False

    elif tablero_visible_valido == False:
        resultado = False
    
    return resultado


def estructura_y_tipos_validos(estado:EstadoJuego) -> bool:
    '''Devuelve True si la estructura y los valores son los esperados'''
    
    resultado:bool = True
    
    valores_en_tablero_validos:bool = True
    tablero_visible_valido:bool = True
    validas_tablero_visible:tuple[str, ...] = (VACIO,BOMBA,BANDERA,"0","1","2","3","4","5","6","7","8")

    filas = estado["filas"]
    columnas = estado["columnas"]
    tablero = estado["tablero"]
    tablero_visible = estado["tablero_visible"]
    minas = estado["minas"]
    juego_termiado = estado["juego_terminado"]
    #----------------------------------------


    #chequeo valores_en_tablero_validos y tablero_visible_valido
    for f in range(filas):
        for celda in tablero[f]:

            if not (celda >= -1 and celda <=8):
                valores_en_tablero_validos = False
        
        for celda in tablero_visible[f]:

            if not celda in validas_tablero_visible:
                tablero_visible_valido = False

        
    #----------------------------------------
    
    if not (filas > 0 and columnas > 0):    #Tambien pide comprobar que filas y columnas sean enteros.
        resultado = False

    elif not (minas > 0 and minas < filas*columnas):
        resultado = False

    elif not (juego_termiado in [True,False]):
        resultado = False

    elif not valores_en_tablero_validos:
        resultado = False

    elif not tablero_visible_valido:
        resultado = False

    elif len(list(estado.keys())) !=6:
        resultado = False

    elif not son_matriz_y_misma_dimension(tablero,tablero_visible):
        resultado = False

    elif not (len(tablero) == filas and len(tablero[0]) == columnas):
        resultado = False
    
    return resultado

def son_matriz_y_misma_dimension(t1:list[list[Any]],t2:list[list[Any]]) -> bool:
    '''Devuelve True si ambos tableros cumplen es_matriz(), y tienen la misma cantidad de filas y columnas.'''
    if es_matriz(t1) and es_matriz(t2) and len(t1) == len(t2) and len(t1[0]) == len(t2[0]):
        return True

    return False

def todas_celdas_seguras_descubiertas(tablero:list[list[int]], tablero_visible:list[list[str]]) -> bool:
    '''Devuelve True si solo quedan cubiertas las celdas con minas'''
    for f in range(len(tablero)):
        for c in range(len(tablero[0])):
            if tablero[f][c] == -1 :
                #si hay una bomba y fue explotada
                if tablero_visible[f][c] != VACIO and tablero_visible[f][c] != BANDERA:
                    return False
            else:
                #si no hay una bomba, y la celda esta cubierta
                if  tablero_visible[f][c] != str(tablero[f][c]):
                    return False
    return True

#4
def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    '''Devuelve una copia del tablero visible de estado.'''

    original = estado["tablero_visible"]
    copia: list[list[str]] = []
    
    for i in range(len(original)):
        fila = []
        for j in range(len(original[i])):
            fila.append(original[i][j])
        copia.append(fila)
    
    return copia

#5 
def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    '''Modifica el tablero, agregando o sacando una bandera en la posicion (fila,columna)'''        

    if not(estado["juego_terminado"]== True or (estado["tablero_visible"][fila][columna] != VACIO and estado["tablero_visible"][fila][columna] != BANDERA)):

        if estado["tablero_visible"][fila][columna] == VACIO:
            estado["tablero_visible"][fila][columna] = BANDERA

        elif estado["tablero_visible"][fila][columna] == BANDERA:
            estado["tablero_visible"][fila][columna] = VACIO    


#6
def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    '''Modifica estado, muestra en su tablero visible lo que hay en el tablero en la posicion (fila,columna).
    
    Nota: Si en la posicion dada hay un cero, descubre todas las celdas cercanas seguras.
    '''

    if not estado["juego_terminado"]: #Si el juego no terminó

        if estado["tablero"][fila][columna] == -1:
            estado["juego_terminado"] = True

            for f,c in posiciones_con_minas(estado["tablero"]):
                estado["tablero_visible"][f][c] = BOMBA

        else:            
            for f,c in caminos_descubiertos(estado["tablero"],estado["tablero_visible"],fila,columna):
                estado["tablero_visible"][f][c] = str(estado["tablero"][f][c])
            
            
            if todas_celdas_seguras_descubiertas(estado["tablero"],estado["tablero_visible"]):
                estado["juego_terminado"] = True


def posiciones_con_minas(tablero:list[list[int]]) -> list[tuple[int,int]]:
    '''Funcion auxiliar que devuelve todas las posiciones del tablero en donde hay minas'''

    largo_fila:int = len(tablero)
    largo_columna:int = len(tablero[0])
    posiciones:list[tuple[int,int]] = []

    for f in range(largo_fila):
        for c in range(largo_columna):
            if tablero[f][c] == -1:
                posiciones.append((f,c))
    
    return posiciones

def caminos_descubiertos(tablero:list[list[int]],tablero_visible:list[list[str]],f:int,c:int)-> list[tuple[int,int]]:
    '''Devuelve una lista con las posiciones seguras conectadas a la posicion (f,c)'''

    res:list[tuple[int,int]] = [(f,c)]

    if tablero[f][c] == 0 and tablero_visible[f][c] != BANDERA:
        
        #funcion recursiva que agrega a res las posiciones adyacentes que cumplen lo pedido
        def descubrir_caminos(posicion:tuple[int,int]):
            
            for fila,columna in posiciones_adyacentes(tablero,posicion):
                
                if tablero[fila][columna] != -1 and tablero_visible[fila][columna] != BANDERA and not ((fila,columna) in res):
                    res.append((fila,columna))

                    if tablero[fila][columna] == 0:
                        descubrir_caminos((fila,columna))
        
        descubrir_caminos((f,c))

    return res

def posiciones_adyacentes(tablero: list[list[int]],posicion:tuple[int,int] ) -> list[tuple[int,int]]:
    '''Funcion auxiliar que devuelve las posiciones adyacentes de una posicion dada'''

    largo_filas:int = len(tablero)-1
    largo_columnas:int = len(tablero[0])-1
    celdas:list[tuple[int,int]] = []
    x:int = posicion[0]
    y:int = posicion[1]

    #coordenadas de las posiciones alrededor de la posicion dada
    posiciones_adyacentes:list[tuple[int,int]] = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]
    
    for fila,columna in posiciones_adyacentes:#recorro todas las posiciones adyacentes
        
        #chequea que la posicion no esté fuera del tablero
        if not((fila>largo_filas or fila < 0) or (columna > largo_columnas or columna<0)):
            celdas.append((fila,columna))

    return celdas

#7
def verificar_victoria(estado: EstadoJuego) -> bool:
    '''Devuelve True si el usuario gana (solo quedan cubiertas las celdas con minas).'''

    return todas_celdas_seguras_descubiertas(estado["tablero"],estado["tablero_visible"])

#8
def reiniciar_juego(estado: EstadoJuego) -> None:
    '''Modifica estado, crea un nuevo juego con la misma cantidad de filas, columnas y minas.'''

    estado["juego_terminado"] = False
    estado_nuevo:EstadoJuego = crear_juego(estado["filas"],estado["columnas"],estado["minas"])

    while son_el_mismo_tablero(estado["tablero"],estado_nuevo["tablero"]):
        estado_nuevo:EstadoJuego = crear_juego(estado["filas"],estado["columnas"],estado["minas"])
    
    estado["tablero"] = estado_nuevo["tablero"]
    estado["tablero_visible"] = estado_nuevo["tablero_visible"]

    #hay que probar en los test que finalmente estado_valido(estado) == True

def son_el_mismo_tablero(t1:list[list[Any]],t2:list[list[Any]]) -> bool:
    '''Fucion auxiliar que compara las dimensiones y valores de dos tableros (visibles o no).

    Argumentos:
        t1: primer tablero
        t2: segundo tablero

    Devuelve:
        True si son el mismo tablero, False si no.
    '''

    if son_matriz_y_misma_dimension(t1,t2):
        
        for f in range(len(t1)): #Habria que hacerlo con while mejor, de paso sacamos los returns esos feos
            for c in range(len(t1[0])):
                
                if t1[f][c] != t2[f][c]:
                    return False
    else:
        return False
    
    return True

#9 
def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    '''Guarda los tableros en archivos txt en ruta_directorio.
    
    Nota: Si no existían los archivos, los crea. Si existían los archivos, los sobreescribe.
    '''

    ruta_tablero:str = os.path.join(ruta_directorio, 'tablero.txt') #Une uno o más componentes de ruta de manera segura, utilizando el separador adecuado para el sistema operativo.
    ruta_visible:str = os.path.join(ruta_directorio, 'tablero_visible.txt')
    tablero:list[list[int]] = estado["tablero"]
    visible:list[list[str]]= estado["tablero_visible"]
    filas:int = estado["filas"]
    columnas:int = estado["columnas"]

    f:str = ""
    for fila in range(filas):        
        for columna in range(columnas):
            valor:str = str(tablero[fila][columna])
            f += valor
            if columna != columnas - 1:  # Si NO es el último, agregar coma
                f += ","
        f += "\n"
    archivo_tablero:TextIO = open(ruta_tablero, 'w') #con w se borra todo lo que habia en el archivo e ingresa lo nuevo 
    archivo_tablero.write(f)
    archivo_tablero.close()

    
    linea:str = ""
    for fila in range(filas):
        for columna in range(columnas):
            v:str = str(visible[fila][columna])
            if v == VACIO:
                v = '?'
            if v == BANDERA:
                v = '*'
            linea += v
            if columna != columnas - 1:  # Si NO es el último, agregar coma
                linea += ","
        linea += "\n"
    archivo_visible:TextIO = open(ruta_visible, 'w')
    archivo_visible.write(linea)
    archivo_visible.close()

#10
def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    '''Modifica estado para que sea equivalente a los tableros guardados.
        Devuelve True si se pudieron cargar correctamente los datos.
    '''

    if not (existe_archivo(ruta_directorio, "tablero.txt") and existe_archivo(ruta_directorio, "tablero_visible.txt")):
        return False

    ruta_tablero:str= os.path.join(ruta_directorio, "tablero.txt")
    ruta_visible:str = os.path.join(ruta_directorio, "tablero_visible.txt")

    archivo_tablero:TextIO = open(ruta_tablero, "r")
    lineas_tablero:list[str] = archivo_tablero.readlines()
    archivo_tablero.close()

    archivo_visible:TextIO = open(ruta_visible, "r")
    lineas_visible:list[str] = archivo_visible.readlines()
    archivo_visible.close()    


    filas: int = contar_lineas_validas(lineas_tablero)
    if filas != contar_lineas_validas(lineas_visible):
        return False

    tablero:list[list[int]] = []
    tablero_visible:list[list[str]] = []
    columnas:int = -1

    minas:int = 0
    for i in range(filas):
        fila_num:list[int]= lista_num(lineas_tablero[i])
        fila_vis:list[str]= lista_str(lineas_visible[i])

        if columnas == -1:
            columnas:int = len(fila_num)

        if len(fila_num) != columnas or len(fila_vis) != columnas: #si hay una columna con diferente tamaño
            return False

        for j in range(columnas):
            val:int = fila_num[j] #si hay un numero de mas de una cifra en el archivo lo va a separar por digitos (que mal), igual no deben ser mayor a 8 o menor a -1 (que bien)
            if val == -1:
                minas += 1
            elif val < 0 or val > 8:
                return False

            vis:str = fila_vis[j]
            if vis != '?' and vis != '*': 
                if vis in ("0","1","2","3","4","5","6","7","8"):
                    if int(vis) != val:
                        return False
                else: 
                    return False

        tablero.append(fila_num)

        fila_visible_convertida:list[str] = []
        for j in range(columnas):
            if fila_vis[j] == '?':
                fila_visible_convertida.append(VACIO)
            elif fila_vis[j] == '*':
                fila_visible_convertida.append(BANDERA)
            else:
                fila_visible_convertida.append(fila_vis[j])
        tablero_visible.append(fila_visible_convertida)

    if minas == 0:
        return False

    estado.clear()
    estado["filas"] = filas
    estado["columnas"] = columnas
    estado["minas"] = minas
    estado["tablero"] = tablero
    estado["tablero_visible"] = tablero_visible
    estado["juego_terminado"] = False

    return estado_valido(estado)    

def contar_lineas_validas(lineas: list[str]) -> int:
    '''Cuenta la cantidad de caracteres validos en lineas'''

    contador:int = 0
    for i in range(len(lineas)):
        vacia:bool = True
        j:int = 0
        while j < len(lineas[i]):
            if lineas[i][j] != '\n':
                vacia = False
            j += 1
        if not vacia:
            contador += 1
    return contador    

def lista_num(linea: str) -> list[int]:
    '''Devuelve los datos de linea, los pasa de string a int'''
    resultado:list[int] = []
    i:int = 0
    while i < len(linea):
        signo:int = 1

        if linea[i] == '-': 
            signo = -1
            i += 1
        
        if i < len(linea):
            if linea[i] != ',' and linea[i] != '\n':
                
                numero = int(linea[i])
                #if 0 <= numero <= 8: #No es necesario
                resultado.append(signo * numero)
            
            i += 1
    return resultado


def lista_str(linea: str) -> list[str]:
    '''Devuelve en una lista los datos en linea'''
    resultado:list[str] = []
    i:int = 0
    while i < len(linea):
        c = linea[i]
        if c != ',' and c != '\n':
            resultado.append(c)
        i += 1
    return resultado