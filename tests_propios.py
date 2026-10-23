import unittest
import os
from buscaminas import (crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,
                                reiniciar_juego, colocar_minas, calcular_numeros, verificar_victoria,
                                guardar_estado, cargar_estado, BOMBA, BANDERA, VACIO, EstadoJuego,)

#Importo funciones auxiliares
from buscaminas import(es_matriz,estado_valido,estructura_y_tipos_validos,son_el_mismo_tablero)

#funciones auxiliares
def cant_minas_en_tablero(tablero: list[list[int]]) -> int:
    """Chequea que el número de minas en el tablero sea igual al número de minas esperado"""
    contador_minas:int = 0
    for fila in tablero:
        for celda in fila:
            if celda == -1:
                contador_minas += 1
    return contador_minas

def son_solo_ceros_y_bombas (tablero: list[list[int]]) -> bool:
    for fila in tablero:
        for celda in fila:
            if celda not in [0, -1]:
                return False
    return True

def dimension_correcta(tablero: list[list[int]], filas: int, columnas: int) -> bool:
    """Chequea que el tablero tenga las dimensiones correctas"""
    if len(tablero) != filas:
        return False
    for fila in tablero:
        if len(fila) != columnas:
            return False
    return True

def cant_ceros_en_tablero (tablero:list[list[int]])-> int:
    '''Cuenta cuantos ceros hay en tablero'''
    contador_ceros:int = 0
    for fila in tablero:
        for celda in fila:
            if celda == 0:
                contador_ceros += 1
    return contador_ceros

def tablero_visible_vacio(tablero_visible:list[list[str]]) -> bool:
    '''Devuelve True si todas las celdas de tablero_visible son VACIO'''

    for f in range(len(tablero_visible)):
        for c in range(len(tablero_visible[0])):
            if tablero_visible[f][c] != VACIO:
                return False
    return True

def contar_caracter_en_texto(caracter:str,texto:str):
    '''Cuenta la cantidad de veces que aparece un caracter en un texto.'''
    
    total = 0

    for letra in texto:
        if caracter == letra:
            total+=1

    return total

def contar_comas(lineas_tablero:list[str])->int:
    '''cuenta cantidad de comas de una lista de str'''
    comas_en_tablero = 0
    for linea in lineas_tablero:
        comas_en_tablero += contar_caracter_en_texto(",",linea)
    return comas_en_tablero

def contar_minas(lineas_tablero:list[str])->int:
    '''cuenta cantidad de "-1" de una lista de str'''
    minas_en_tablero = 0
    for linea in lineas_tablero:
        for caracter in range (len(linea)):
            if linea[caracter] == "-" and linea[caracter+1] == "1":
                minas_en_tablero+=1
    return minas_en_tablero

def quitar_comas(lineas_tablero:list[str])->list[str]:
    '''saca todas las comas de una lista de str'''
    lineas_tablero_sin_comas:list[str]=[]
    for linea in lineas_tablero:
        for caracter in linea:
            if caracter != ",":
                lineas_tablero_sin_comas+= caracter
    return lineas_tablero_sin_comas

def contar_lineas_validas(lineas:list[str])->int:
    '''Cuenta la cantidad de lineas que hay en una lista, ignorando las lineas vacias'''
    total:int = 0
    agregar:bool = False

    for linea in lineas:
        for letra in linea:
            if letra != "\n" and letra !=" ":
                agregar = True

        #Si en la linea habian caracteres, sumar 1.    
        if agregar:
            total+=1
        agregar = False

    return total


#1
class colocar_minasTest(unittest.TestCase):
    def test_2x2(self):
        filas = 2
        columnas = 2
        minas = 2
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        # agrego: testeamos que el tablero sea matriz
        self.assertTrue(es_matriz(tablero))
        # agrego: testeamos que (filas*columnas-minas) sea igual a cantidad de 0
        self.assertEqual(cant_ceros_en_tablero(tablero), filas*columnas-minas)

    def test_minimo_tablero_posible(self):
        filas = 2
        columnas = 1
        minas = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        # agrego: testeamos que el tablero sea matriz
        self.assertTrue(es_matriz(tablero))
        # agrego: testeamos que (filas*columnas-minas) sea igual a cantidad de 0
        self.assertEqual(cant_ceros_en_tablero(tablero), filas*columnas-minas)
    
    def test_minimo_tablero_posible_invertido(self):
        filas = 1
        columnas = 2
        minas = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        # agrego: testeamos que el tablero sea matriz
        self.assertTrue(es_matriz(tablero))
        # agrego: testeamos que (filas*columnas-minas) sea igual a cantidad de 0
        self.assertEqual(cant_ceros_en_tablero(tablero), filas*columnas-minas)

    def test_maximo_posible_minas(self):
        filas = 5
        columnas = 5
        minas = 24
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya 24 minas en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        # agrego: testeamos que el tablero sea matriz
        self.assertTrue(es_matriz(tablero))
        # agrego: testeamos que (filas*columnas-minas) sea igual a cantidad de 0
        self.assertEqual(cant_ceros_en_tablero(tablero), filas*columnas-minas)

    def test_tablero_muy_grande(self):
        filas = 18
        columnas = 15
        minas = 150
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya 150 minas en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        # agrego: testeamos que el tablero sea matriz
        self.assertTrue(es_matriz(tablero))
        # agrego: testeamos que (filas*columnas-minas) sea igual a cantidad de 0
        self.assertEqual(cant_ceros_en_tablero(tablero), filas*columnas-minas)
    
    def test_mas_filas_que_columnas(self):
        filas = 7
        columnas = 3
        minas = 16
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya 16 minas en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        # agrego: testeamos que el tablero sea matriz
        self.assertTrue(es_matriz(tablero))
        # agrego: testeamos que (filas*columnas-minas) sea igual a cantidad de 0
        self.assertEqual(cant_ceros_en_tablero(tablero), filas*columnas-minas)
    
    def test_mas_columnas_que_filas(self):
        filas = 4
        columnas = 9
        minas = 20
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya 20 minas en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        # agrego: testeamos que el tablero sea matriz
        self.assertTrue(es_matriz(tablero))
        # agrego: testeamos que (filas*columnas-minas) sea igual a cantidad de 0
        self.assertEqual(cant_ceros_en_tablero(tablero), filas*columnas-minas)


#2
class calcular_numerosTest(unittest.TestCase):
    def test_2x2(self):
        tablero = [[ 0, 0],
                   [-1, 0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[ 1, 1],
                                   [-1, 1]])
        
    def test_tablero_mas_chico_posible(self):
        tablero = [[0,-1]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1,-1]])

    def test_tablero_mas_chico_posible_invertido(self):
        tablero = [[ 0 ],
                   [-1 ]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[ 1 ],
                                   [-1 ]])

    def test_mina_en_los_bordes(self):
        tablero = [[-1,-1,-1,-1],
                   [-1, 0, 0,-1],
                   [-1, 0, 0,-1],
                   [-1,-1,-1,-1]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[-1,-1,-1,-1],
                                   [-1, 5, 5,-1],
                                   [-1, 5, 5,-1],
                                   [-1,-1,-1,-1]])

    def test_minas_en_esquinas(self):
        tablero = [[-1, 0, 0, 0,-1],
                   [ 0, 0, 0, 0, 0],
                   [ 0, 0, 0, 0, 0],
                   [-1, 0, 0, 0,-1]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[-1, 1, 0, 1,-1],
                                   [ 1, 1, 0, 1, 1],
                                   [ 1, 1, 0, 1, 1],
                                   [-1, 1, 0, 1,-1]])

    def test_hay_8_minas_alrededor(self):
        tablero = [[-1, -1, -1],
                   [-1,  0, -1 ],
                   [-1, -1, -1 ]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero,  [[-1, -1, -1],
                                    [-1,  8, -1 ],
                                    [-1, -1, -1 ]])

    def test_tablero_8x8(self):
        tablero = [[-1,-1, 0, 0, 0, 0, 0, 0],
                   [ 0, 0, 0, 0, 0, 0, 0, 0],
                   [ 0,-1, 0,-1, 0, 0, 0, 0],
                   [ 0, 0, 0, 0, 0, 0, 0, 0],
                   [ 0, 0, 0,-1,-1, 0, 0, 0],
                   [ 0, 0, 0, 0, 0,-1, 0, 0],
                   [ 0, 0,-1, 0, 0, 0, 0, 0],
                   [-1,-1, 0, 0, 0, 0, 0, 0]]
        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero,  [[-1,-1, 1, 0, 0, 0, 0, 0],
                                    [ 3, 3, 3, 1, 1, 0, 0, 0],
                                    [ 1,-1, 2,-1, 1, 0, 0, 0],
                                    [ 1, 1, 3, 3, 3, 1, 0, 0],
                                    [ 0, 0, 1,-1,-1, 2, 1, 0],
                                    [ 0, 1, 2, 3, 3,-1, 1, 0],
                                    [ 2, 3,-1, 1, 1, 1, 1, 0],
                                    [-1,-1, 2, 1, 0, 0, 0, 0]])
    
    def test_tablero_1x10(self):
        tablero = [[-1,0,-1,0,0,0,0,0,0,0]]
        calcular_numeros(tablero)

        self.assertEqual(tablero, [[-1,2,-1,1,0,0,0,0,0,0]])

    def test_tablero_10x1(self):
        tablero = [[0],[0],[0],[0],[0],[0],[-1],[0],[-1],[-1]]
        calcular_numeros(tablero)

        self.assertEqual(tablero,[[0],[0],[0],[0],[0],[1],[-1],[2],[-1],[-1]])

#3
class crear_juegoTest(unittest.TestCase):
    def test_2x2(self):
        filas = 2
        columnas = 2
        minas = 2
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)

    def test_juego_dificil(self):
        filas = 22
        columnas = 27
        minas = 100
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))#dimensiones correctas?
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))#dimensiones correctas?
        for fila in estado['tablero_visible']:#tablero visible vacío?
            for celda in fila:
                self.assertEqual(celda, VACIO)

        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)#coinciden las minas?

        #Testeamos la la estructura y tipos validos
        self.assertTrue(es_matriz(estado['tablero']))
        self.assertTrue(es_matriz(estado['tablero_visible']))
        self.assertTrue(estado_valido(estado))

        #Testeo que volver a calcular los numeros no cambia nada
        tablero_copia = estado['tablero'].copy()
        calcular_numeros(tablero_copia)
        self.assertEqual(estado['tablero'],tablero_copia)

    def test_juego_1x23(self):
        filas = 1
        columnas = 23
        minas = 20
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))#dimensiones correctas?
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))#dimensiones correctas?
        for fila in estado['tablero_visible']:#tablero visible vacío?
            for celda in fila:
                self.assertEqual(celda, VACIO)

        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)#coinciden las minas?

        #Testeamos la la estructura y tipos validos
        self.assertTrue(es_matriz(estado['tablero']))
        self.assertTrue(es_matriz(estado['tablero_visible']))
        self.assertTrue(estado_valido(estado))

        #Testeo que volver a calcular los numeros no cambia nada
        tablero_copia = estado['tablero'].copy()
        calcular_numeros(tablero_copia)
        self.assertEqual(estado['tablero'],tablero_copia)
    
    def test_juego_17x2(self):
        filas = 17
        columnas = 2
        minas = 20
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))#dimensiones correctas?
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))#dimensiones correctas?
        for fila in estado['tablero_visible']:#tablero visible vacío?
            for celda in fila:
                self.assertEqual(celda, VACIO)

        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)#coinciden las minas?

        #Testeamos la la estructura y tipos validos
        self.assertTrue(es_matriz(estado['tablero']))
        self.assertTrue(es_matriz(estado['tablero_visible']))
        self.assertTrue(estado_valido(estado))

        #Testeo que volver a calcular los numeros no cambia nada
        tablero_copia = estado['tablero'].copy()
        calcular_numeros(tablero_copia)
        self.assertEqual(estado['tablero'],tablero_copia)

    def test_juego_maximo_minas_menos_uno(self):
        filas = 5
        columnas = 5
        minas = 24  # Solo una celda sin mina
        estado : EstadoJuego = crear_juego(filas, columnas, minas)

        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        for fila in estado['tablero_visible']:#tablero visible vacío?
            for celda in fila:
                self.assertEqual(celda, VACIO)

        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)

        #Testeamos la la estructura y tipos validos
        self.assertTrue(es_matriz(estado['tablero']))
        self.assertTrue(es_matriz(estado['tablero_visible']))
        self.assertTrue(estado_valido(estado))

        #Testeo que volver a calcular los numeros no cambia nada
        tablero_copia = estado['tablero'].copy()
        calcular_numeros(tablero_copia)
        self.assertEqual(estado['tablero'],tablero_copia)

#4
class obtener_estado_tableroTest(unittest.TestCase):
    def test_2x2(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 2,
            'tablero': [
                [-1, 1 ],
                [ 1, -1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
         # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
            [-1, 1 ],
            [ 1, -1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])

    def test_juego_comenzado(self):
        estado: EstadoJuego = {"filas": 4,
                               "columnas" :4,
                               "minas": 3,
                               "juego_teminado": False,
                               "tablero":[[-1,2,0,0],
                                          [-1,2,0,0],
                                          [1,1,1,1],
                                          [0,0,1,-1]],
                               "tablero_visible":[[BANDERA,"2","0","0"],
                                                  [" ","2","0","0"],
                                                  [" ","1","1","1"],
                                                  [" "," "," "," "]]
                            }
        
        tablero_visible_original = estado['tablero_visible']
        tablero_visible_copia = obtener_estado_tablero_visible(estado)
        self.assertEqual(tablero_visible_original,tablero_visible_copia)#son iguales?

        tablero_visible_copia[0][0] = BOMBA
        self.assertEqual(tablero_visible_original[0][0],BANDERA)#testeo que el original no cambia

    def test_tablero_visible_vacio(self):
        estado:EstadoJuego = crear_juego(10,10,10) #creo un juego nuevo (tablero visible vacio)

        tablero_visible_original = estado['tablero_visible']
        tablero_visible_copia = obtener_estado_tablero_visible(estado)
        self.assertEqual(tablero_visible_original,tablero_visible_copia)#son iguales?

        tablero_visible_copia[0][0] = BOMBA
        self.assertEqual(tablero_visible_original[0][0]," ")#testeo que el original no cambia

    def test_juego_terminado(self):
        estado: EstadoJuego = {"filas": 2,
                               "columnas" :6,
                               "minas": 3,
                               "juego_teminado": True,
                               "tablero":[[1,-1,2,-1,-1,1],
                                          [1, 1,2 ,2, 2,1]],
                               "tablero_visible":[["1",VACIO,"2",BANDERA,BANDERA,"1"],
                                                  ["1", "1" ,"2",  "2"  ,  "2"  ,"1"]]
                            }
        
        tablero_visible_original = estado['tablero_visible']
        tablero_visible_copia = obtener_estado_tablero_visible(estado)
        self.assertEqual(tablero_visible_original,tablero_visible_copia)#son iguales?

        tablero_visible_copia[0][0] = VACIO
        self.assertEqual(tablero_visible_original[0][0],"1")#testeo que el original no cambia

    def test_tablero_con_numeros(self):
        estado: EstadoJuego = {"filas": 2,
                                "columnas": 2,
                                "minas": 1,
                                "juego_teminado": False,
                                "tablero": [[-1, 1], [1, 1]],
                                "tablero_visible": [
                                [BANDERA, "1"],
                                ["1", "1"]]
                                }

        copia = obtener_estado_tablero_visible(estado)
        self.assertEqual(copia, estado['tablero_visible'])
        copia[1][1] = BOMBA
        self.assertEqual(estado['tablero_visible'][1][1], "1")
    def test_solo_banderas(self):
        estado: EstadoJuego = {
                            "filas": 3,
                            "columnas": 3,
                            "minas": 4,
                            "juego_teminado": False,
                            "tablero": [[-1, 1, 0], [1, 2, 1], [0, 1, -1]],
                            "tablero_visible": [
                            [BANDERA, BANDERA, BANDERA],
                            [BANDERA, BANDERA, BANDERA],
                            [BANDERA, BANDERA, BANDERA]]
                                }

        copia = obtener_estado_tablero_visible(estado)
        self.assertEqual(copia, estado['tablero_visible'])
        copia[0][0] = "1"
        self.assertEqual(estado['tablero_visible'][0][0], BANDERA)  # original no cambia

#5
class marcar_celdaTest(unittest.TestCase):
    def test_2x2(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 2,
            'tablero': [
                [-1, 1],
                [1, -1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, -1]
        ])
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)

    def test_saco_bandera(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 2,
            'tablero': [
                [-1, -1, 1],
                [ 2,  2, 1]
            ],
            'tablero_visible': [
                [BANDERA, VACIO, VACIO],
                [  "2"  , VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)

        # Testeamos que se quitó la bandera
        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO,VACIO],
                                                     ["2",   VACIO,VACIO]])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [[-1, -1,1],
                                             [ 2,  2,1]])
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que hayan dos minas en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)

    def bandera_en_celda_descubierta(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 2,
            'tablero': [
                [-1, -1,1],
                [ 2,  2,1]
            ],
            'tablero_visible': [
                [BANDERA, VACIO,"1"],
                ["2",     VACIO,"1"]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 1, 2) #intentamos marcar la celda con "1"

        # Testeamos que no se aplica la bandera
        self.assertEqual(estado['tablero_visible'], [[BANDERA, VACIO,"1"],
                                                    [   "2"  , VACIO,"1"]])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [[-1, -1,1],
                                             [ 2,  2,1]])
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que hayan dos minas en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)

    def bandera_en_juego_terminado(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 2,
            'tablero': [
                [-1, -1, 1],
                [ 2,  2, 1]
            ],
            'tablero_visible': [
                [BANDERA, BANDERA,"1"],
                [  "2"  ,  "2"   ,"1"]
            ],
            'juego_terminado': True
        }
        marcar_celda(estado, 2, 0) #intentamos marcar la celda con "2"
        #testeamos que el tablero visible se queda igual
        self.assertEqual(estado['tablero_visible'],[[BANDERA, BANDERA,"1"],
                                                    [  "2"  ,  "2"   ,"1"]])

#6
class descubrir_celdaTest(unittest.TestCase):
    def test_3x3(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 2,
            'tablero': [
                [ 1, -1, 1],
                [ 1, 2 , 1],
                [-1, 1 , 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 2, 2)
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO, VACIO],
            [VACIO, "2", "1"],
            [VACIO, "1", "0"]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
            [ 1,-1, 1],
            [ 1, 2, 1],
            [-1, 1, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)
        self.assertFalse(estado['juego_terminado'])

    def test_muchos_caminos(self):
        estado: EstadoJuego = {
            'filas': 5,
            'columnas': 5,
            'minas': 3,
            'tablero': [[1,-1,1, 0, 0],
                        [1, 1,1, 0, 0],
                        [0, 0,0, 0, 0],
                        [0, 0,1, 2, 2],
                        [0, 0,1,-1,-1]],
            'tablero_visible': [
                [VACIO, VACIO,VACIO,VACIO,VACIO],
                [VACIO, VACIO,VACIO,VACIO,VACIO],
                [VACIO, VACIO,VACIO,VACIO,VACIO],
                [VACIO, VACIO,VACIO,VACIO,VACIO],
                [VACIO, VACIO,VACIO,VACIO,VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 4)
        #Testeamos que se hayan mostrado varias celdas
        self.assertEqual(estado['tablero_visible'], [
            [VACIO,VACIO, "1",   "0","0"],
            [  "1",  "1", "1",   "0","0"],
            [  "0",  "0", "0",   "0","0"],
            [  "0",  "0", "1",   "2","2"],
            [  "0",  "0", "1", VACIO,VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 5)
        self.assertEqual(estado['columnas'], 5)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
                        [1,-1,1, 0, 0],
                        [1, 1,1, 0, 0],
                        [0, 0,0, 0, 0],
                        [0, 0,1, 2, 2],
                        [0, 0,1,-1,-1]])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertFalse(estado['juego_terminado'])

    def test_descubre_un_numero(self):
        estado: EstadoJuego = {
            'filas': 1,
            'columnas': 3,
            'minas': 1,
            'tablero': [[-1, 1, 0]],
            'tablero_visible': [[VACIO, VACIO, VACIO]],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 1)
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [[VACIO, "1", VACIO]])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 1)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1, 0]])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertFalse(estado['juego_terminado'])

    def test_descubre_una_mina(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 2,
            'tablero': [[-1, 1],
                        [ 1,-1]],
            'tablero_visible': [[VACIO,   "1"  ],
                                [VACIO, VACIO]],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 0)
        # Testeamos que "juego_terminado" sea True
        self.assertTrue(estado['juego_terminado'])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [[-1, 1],
                                             [ 1,-1]],)
        # Testeamos se muestren las bombas 
        self.assertEqual(estado['tablero_visible'],[[BOMBA,  "1"  ],
                                                    [VACIO,BOMBA]])

    def test_gana_el_juego(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1, 1],
                        [ 1, 1]],
            'tablero_visible': [[VACIO,   "1"  ],
                                [  "1"  , VACIO]],
            'juego_terminado': False
        }
        descubrir_celda(estado, 1, 1)
        # Testeamos que "juego_terminado" sea True
        self.assertTrue(estado['juego_terminado'])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1],
                                             [ 1, 1]],)
        #podria testear que se muestra en tablero visible, pero nose que deberia mostrar.. revisar especificación
        
        
    def test_juego_terminado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1, 1],
                        [ 1, 1]],
            'tablero_visible': [[VACIO,   1  ],
                                [  1  ,   1  ]],
            'juego_terminado': True
        }
        descubrir_celda(estado, 1, 1)
        # Testeamos que "juego_terminado" sea True
        self.assertTrue(estado['juego_terminado'])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1],
                                             [ 1, 1]],)
        # Testeamos que tablero visible sigue igual
        self.assertEqual(estado['tablero_visible'],[[VACIO,  1  ],
                                                    [  1  ,  1  ]])
        


#7
class verificar_victoriaTest(unittest.TestCase):
    def test_2x2(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 2,
            'tablero': [
                [-1, 1],
                [ 1,-1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                ["1", VACIO]
            ],
            'juego_terminado': False
        }
        # Testeamos que el juego no esté terminado y que no haya ganado
        self.assertTrue(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1,-1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            ["1", VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])

    def test_banderas_vacios(self):
        estado: EstadoJuego = {
            'filas': 4,
            'columnas': 4,
            'minas': 2,
            'tablero': [[0,0, 1,-1],
                        [0,1, 2, 2],
                        [0,1,-1, 1],
                        [0,1, 1, 1]],
            'tablero_visible': [["0","0","1",BANDERA],
                                ["0","1","2",  "2"],
                                ["0","1",VACIO,"1"],
                                ["0","1","1",  "1"]],
            'juego_terminado': False
        }
        # Testeamos que el juego no esté terminado y que no haya ganado
        self.assertTrue(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 4)
        self.assertEqual(estado['columnas'], 4)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
                        [0,0, 1,-1],
                        [0,1, 2, 2],
                        [0,1,-1, 1],
                        [0,1, 1, 1]])
        self.assertEqual(estado['tablero_visible'], 
                                [["0","0","1",BANDERA],
                                ["0","1","2",  "2"],
                                ["0","1",VACIO,"1"],
                                ["0","1","1",  "1"]])
        self.assertFalse(estado['juego_terminado'])

    def test_no_gana(self):
        estado: EstadoJuego = {
            'filas': 4,
            'columnas': 4,
            'minas': 2,
            'tablero': [[0,0, 1,-1],
                        [0,1, 2, 2],
                        [0,1,-1, 1],
                        [0,1, 1, 1]],
            'tablero_visible': [["0","0","1",BANDERA],
                                ["0","1","2",  "2"],
                                ["0","1",VACIO,"1"],
                                ["0","1",VACIO,  "1"]],
            'juego_terminado': False
        }
        # Testeamos que el juego no esté terminado y que no haya ganado
        self.assertFalse(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 4)
        self.assertEqual(estado['columnas'], 4)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
                        [0,0, 1,-1],
                        [0,1, 2, 2],
                        [0,1,-1, 1],
                        [0,1, 1, 1]])
        self.assertEqual(estado['tablero_visible'], 
                                [["0","0","1",BANDERA],
                                ["0","1","2",  "2"],
                                ["0","1",VACIO,"1"],
                                ["0","1",VACIO,  "1"]])
        self.assertFalse(estado['juego_terminado'])

    def test_todas_seguras_descubiertas(self):
        estado: EstadoJuego = {
        'filas': 3,
        'columnas': 3,
        'minas': 2,
        'tablero': [
            [0, 1, -1],
            [1, 2, 1],
            [-1, 1, 0]],
        'tablero_visible': [
            ["0", "1", BANDERA],
            ["1", "2", "1"],
            [BANDERA, "1", "0"]],
        'juego_terminado': True
                }
        # Testeamos que el juego termino y que ganó
        self.assertTrue(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
                        [0,1,-1],
                        [1,2,1],
                        [-1,1,0]])
        self.assertEqual(estado['tablero_visible'], 
                                [["0","1",BANDERA],
                                ["1","2","1"],
                                [BANDERA,"1","0"]])
        self.assertTrue(estado['juego_terminado'])

    def test_todo_vacio(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 7,
            'minas': 2,
            'tablero': [
                [-1, 1, 0, 1, -1, 1, 0],
                [ 1, 1, 0 , 1, 1, 1, 0]
                        ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO]
                                ],
            'juego_terminado': False
                            }
        self.assertFalse(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 7)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
                        [-1, 1, 0, 1, -1, 1, 0],
                        [ 1, 1, 0 , 1, 1, 1, 0]])
        self.assertEqual(estado['tablero_visible'], 
                                [[VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO],
                                [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO, VACIO]
                                ])
        self.assertFalse(estado['juego_terminado'])
#8
class reiniciar_juegoTest(unittest.TestCase):
    def test_2x2(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 2,
            'tablero': [
                [-1, 1],
                [ 1,-1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        reiniciar_juego(estado)
        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [
            [-1, 1],
            [ 1,-1]
        ])
    
    def test_sin_empezar(self):
        estado: EstadoJuego = crear_juego(11,10,9)
        estado_copia_original = estado.copy()
        reiniciar_juego(estado)
        
        # Testeamos que el tablero visible se reinicia
        self.assertTrue(tablero_visible_vacio(estado["tablero_visible"]))
        
        #Testeamos que no hayan cambiado los parametros
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 9)
        self.assertEqual(estado['filas'], 11)
        self.assertEqual(estado['columnas'], 10)
        self.assertEqual(estado['minas'], 9)
        self.assertEqual(len(estado['tablero']), 11)
        self.assertEqual(len(estado['tablero'][0]), 10)
        self.assertFalse(estado['juego_terminado'])

        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], estado_copia_original["tablero"])

        self.assertTrue(estado_valido(estado))

    def test_mas_chico_posible(self):
        estado: EstadoJuego = {
            'filas': 1,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1, 1]] ,
            'tablero_visible': [[VACIO, "1"]],
            'juego_terminado': False
        }
        copiaEstado=estado.copy()

        reiniciar_juego(estado)

        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'],[[VACIO, VACIO]])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 1)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 1)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que es diferente tablero
        self.assertFalse(son_el_mismo_tablero(estado['tablero'],copiaEstado['tablero']))
        self.assertFalse(son_el_mismo_tablero(estado['tablero_visible'],copiaEstado['tablero_visible']))


#9 
class guardar_estadoTest(unittest.TestCase):
    def test_chiquito(self):   
        ruta = "."
        ruta_tablero = os.path.join(ruta,"tablero.txt")
        ruta_tablero_visible = os.path.join(ruta,"tablero_visible.txt")

        estado: EstadoJuego = {
                'filas': 2,
                'columnas': 2,
                'minas': 1,
                'tablero': [
                    [-1, 1],
                    [ 1, 1]
                ],
                'tablero_visible': [
                    [BANDERA, "1"],
                    [VACIO, VACIO]
                ],
                'juego_terminado': False
            }
        guardar_estado(estado,ruta) #Guardamos el estado

        #Abrimos los archivos
        archivo = open(ruta_tablero, "r")
        lineas_tablero = archivo.readlines()
        archivo.close()

        archivo = open(ruta_tablero_visible, "r")
        lineas_tablero_visible = archivo.readlines()
        archivo.close()

        self.assertEqual(estado["filas"],len(lineas_tablero))
        self.assertEqual(estado["filas"],len(lineas_tablero_visible))

        
        for f in range(estado["filas"]):
            cantidad_comas_tablero = contar_caracter_en_texto(",",lineas_tablero[f])
            cantidad_comas_tablero_visible = contar_caracter_en_texto(",",lineas_tablero_visible[f])
            cantidad_de_espacios_tablero = contar_caracter_en_texto(" ",lineas_tablero[f])
            cantidad_de_espacios_tablero_visible = contar_caracter_en_texto(" ",lineas_tablero_visible[f])

            #Testeamos que la cantidad de "," por linea sea igual a la cantidad de columnas -1
            self.assertEqual(estado["columnas"]-1,cantidad_comas_tablero)
            self.assertEqual(estado["columnas"]-1,cantidad_comas_tablero_visible)

            #Testeamos que no hayan espacios en ambos archivos
            self.assertEqual(cantidad_de_espacios_tablero,0)
            self.assertEqual(cantidad_de_espacios_tablero_visible,0)

    def test_juego_grande(self):
        estado = crear_juego(23,27,99)

        #marco algunas celdas
        marcar_celda(estado,10,10)
        marcar_celda(estado,0,0)

        ruta = "."
        ruta_tablero = os.path.join(ruta,"tablero.txt")
        ruta_tablero_visible = os.path.join(ruta,"tablero_visible.txt")

        guardar_estado(estado,ruta) #Guardamos el estado

        #Abrimos los archivos
        archivo = open(ruta_tablero, "r")
        lineas_tablero = archivo.readlines()
        archivo.close()

        archivo = open(ruta_tablero_visible, "r")
        lineas_tablero_visible = archivo.readlines()
        archivo.close()

        self.assertEqual(estado["filas"],len(lineas_tablero))
        self.assertEqual(estado["filas"],len(lineas_tablero_visible))

        
        for f in range(estado["filas"]):
            cantidad_comas_tablero = contar_caracter_en_texto(",",lineas_tablero[f])
            cantidad_comas_tablero_visible = contar_caracter_en_texto(",",lineas_tablero_visible[f])
            cantidad_de_espacios_tablero = contar_caracter_en_texto(" ",lineas_tablero[f])
            cantidad_de_espacios_tablero_visible = contar_caracter_en_texto(" ",lineas_tablero_visible[f])

            #Testeamos que la cantidad de "," por linea sea igual a la cantidad de columnas -1
            self.assertEqual(estado["columnas"]-1,cantidad_comas_tablero)
            self.assertEqual(estado["columnas"]-1,cantidad_comas_tablero_visible)

            #Testeamos que no hayan espacios en ambos archivos
            self.assertEqual(cantidad_de_espacios_tablero,0)
            self.assertEqual(cantidad_de_espacios_tablero_visible,0)

    def test_una_fila(self):
        ruta = "."
        ruta_tablero = os.path.join(ruta,"tablero.txt")
        ruta_tablero_visible = os.path.join(ruta,"tablero_visible.txt")

        estado: EstadoJuego = {
                'filas': 1,
                'columnas': 8,
                'minas': 1,
                'tablero': [[1,-1,1,0,0,0,0,0]],
                'tablero_visible': [[VACIO,VACIO,VACIO,VACIO,VACIO,VACIO,VACIO,VACIO]],
                'juego_terminado': False
            }
        
        guardar_estado(estado,ruta) #Guardamos el estado
        
        #Abrimos los archivos
        archivo = open(ruta_tablero, "r")
        lineas_tablero = archivo.readlines()
        archivo.close()

        archivo = open(ruta_tablero_visible, "r")
        lineas_tablero_visible = archivo.readlines()
        archivo.close()

        self.assertEqual(estado["filas"],len(lineas_tablero))
        self.assertEqual(estado["filas"],len(lineas_tablero_visible))

        
        for f in range(estado["filas"]):
            cantidad_comas_tablero = contar_caracter_en_texto(",",lineas_tablero[f])
            cantidad_comas_tablero_visible = contar_caracter_en_texto(",",lineas_tablero_visible[f])
            cantidad_de_espacios_tablero = contar_caracter_en_texto(" ",lineas_tablero[f])
            cantidad_de_espacios_tablero_visible = contar_caracter_en_texto(" ",lineas_tablero_visible[f])

            #Testeamos que la cantidad de "," por linea sea igual a la cantidad de columnas -1
            self.assertEqual(estado["columnas"]-1,cantidad_comas_tablero)
            self.assertEqual(estado["columnas"]-1,cantidad_comas_tablero_visible)

            #Testeamos que no hayan espacios en ambos archivos
            self.assertEqual(cantidad_de_espacios_tablero,0)
            self.assertEqual(cantidad_de_espacios_tablero_visible,0)

    def test_una_columna(self):
        ruta = "."
        ruta_tablero = os.path.join(ruta,"tablero.txt")
        ruta_tablero_visible = os.path.join(ruta,"tablero_visible.txt")

        estado: EstadoJuego = {
                'filas': 8,
                'columnas': 1,
                'minas': 1,
                'tablero': [[1],[-1],[1],[0],[0],[0],[0],[0]],
                'tablero_visible': [[VACIO],[VACIO],[VACIO],[VACIO],[VACIO],[VACIO],[VACIO],[VACIO]],
                'juego_terminado': False
            }
        
        guardar_estado(estado,ruta) #Guardamos el estado
        
        #Abrimos los archivos
        archivo = open(ruta_tablero, "r")
        lineas_tablero = archivo.readlines()
        archivo.close()

        archivo = open(ruta_tablero_visible, "r")
        lineas_tablero_visible = archivo.readlines()
        archivo.close()

        self.assertEqual(estado["filas"],len(lineas_tablero))
        self.assertEqual(estado["filas"],len(lineas_tablero_visible))

        
        for f in range(estado["filas"]):
            cantidad_comas_tablero = contar_caracter_en_texto(",",lineas_tablero[f])
            cantidad_comas_tablero_visible = contar_caracter_en_texto(",",lineas_tablero_visible[f])
            cantidad_de_espacios_tablero = contar_caracter_en_texto(" ",lineas_tablero[f])
            cantidad_de_espacios_tablero_visible = contar_caracter_en_texto(" ",lineas_tablero_visible[f])

            #Testeamos que la cantidad de "," por linea sea igual a la cantidad de columnas -1
            self.assertEqual(estado["columnas"]-1,cantidad_comas_tablero)
            self.assertEqual(estado["columnas"]-1,cantidad_comas_tablero_visible)

            #Testeamos que no hayan espacios en ambos archivos
            self.assertEqual(cantidad_de_espacios_tablero,0)
            self.assertEqual(cantidad_de_espacios_tablero_visible,0)

#10
class cargar_estadoTest(unittest.TestCase):
    def test_chico_con_muchos_saltos(self):
        ruta = os.path.join(".","tableros_para_test/tablero_chico_feo")
        estado = crear_juego(10,10,10) #creo un estado cualquiera
        
        cargar_estado(estado,ruta)

        ruta_tablero = os.path.join(ruta, "tablero.txt")
        ruta_visible = os.path.join(ruta, "tablero_visible.txt")

        #Cargamos los archivos para testear
        archivo_tablero = open(ruta_tablero, "r")
        lineas_tablero = archivo_tablero.readlines()
        archivo_tablero.close()

        archivo_visible = open(ruta_visible, "r")
        lineas_tablero_visible = archivo_visible.readlines()
        archivo_visible.close()

        #cargar_estado deberia dar True
        self.assertTrue(cargar_estado(estado,ruta))

        #testeo si los archivos tablero.txt y tablero_visible.txt existen
        self.assertTrue(os.path.exists(ruta_tablero))
        self.assertTrue(os.path.exists(ruta_visible))
        
        #testeo que la cantidad de lı́neas en tablero.txt es igual a la cantidad de lı́neas en tablero visible.txt
        self.assertEqual(contar_lineas_validas(lineas_tablero),contar_lineas_validas(lineas_tablero_visible))
        
        
        #testeamos que los archivos contienen la misma cantidad de comas (‘,’)
        self.assertEqual(contar_comas(lineas_tablero),contar_comas(lineas_tablero_visible))
        
        #estado["minas"] = cantidad de -1 en tablero.txt
        self.assertEqual(estado["minas"],contar_minas(lineas_tablero))

        #estado["juego terminado"] = F alse
        self.assertFalse(estado["juego_terminado"])

        #estado["tablero"] = es igual, posición a posición, a los valores en tablero.txt
        self.assertEqual(estado["tablero"],[[-1,-1,-1,2,1],
                                            [3,5,4,-1,2],
                                            [-1,3,-1,3,-1],
                                            [-1,5,2,3,1],
                                            [-1,3,-1,1,0]])
        #estado[′ tablero visible′ ] es igual, posición a posición, a los valores en tablero visible.txt,
        #cambiando ‘∗’ por BANDERA y ‘?’ por VACIO)
        self.assertEqual(estado["tablero_visible"],[[VACIO,VACIO,VACIO,VACIO,VACIO], 
                                                    [VACIO,VACIO,VACIO,VACIO,VACIO],
                                                    [VACIO, '3' ,VACIO,VACIO,VACIO],
                                                    [VACIO,VACIO,VACIO, '3' , '1' ],
                                                    [VACIO,VACIO,VACIO, '1' , '0' ]])
        #estado[′ f ilas′ ] = cantidad de lı́neas en tablero.txt
        self.assertEqual(estado["filas"],len(lineas_tablero))
        #estado[′ columnas′ ] = 1+ cantidad de comas (‘,’) por lı́nea en tablero.txt
        self.assertEqual(estado["columnas"],contar_caracter_en_texto(",",lineas_tablero[1])+1)
        self.assertTrue(estado_valido(estado))

    def test_no_hay_archivos(self):
        ruta = os.path.join(".","tableros_para_test/carpeta_sin_archivos")
        estado = crear_juego(10,10,10) #creo un estado cualquiera
        
        cargar_estado(estado,ruta)

        ruta_tablero = os.path.join(ruta, "tablero.txt")
        ruta_visible = os.path.join(ruta, "tablero_visible.txt")

        #testeo si los archivos tablero.txt y tablero_visible.txt existen
        self.assertFalse(os.path.exists(ruta_tablero))
        self.assertFalse(os.path.exists(ruta_visible))
        #cargar_estado tiene que devolver false
        self.assertFalse(cargar_estado(estado,ruta))

    def test_no_coinciden_archivos(self):
        ruta = os.path.join(".","tableros_para_test/carpeta_archivos_distintos")
        estado = crear_juego(10,10,10) #creo un estado cualquiera
        
        cargar_estado(estado,ruta)

        ruta_tablero = os.path.join(ruta, "tablero.txt")
        ruta_visible = os.path.join(ruta, "tablero_visible.txt")

        #testeo si los archivos tablero.txt y tablero_visible.txt existen
        self.assertFalse(os.path.exists(ruta_tablero))
        self.assertFalse(os.path.exists(ruta_visible))
        #cargar_estado tiene que devolver false
        self.assertFalse(cargar_estado(estado,ruta))

    def test_juego_defectuoso(self):
        ruta = os.path.join(".","tableros_para_test/tablero_juego_defectuoso")
        estado = crear_juego(10,10,10) #creo un estado cualquiera
        
        cargar_estado(estado,ruta)

        ruta_tablero = os.path.join(ruta, "tablero.txt")
        ruta_visible = os.path.join(ruta, "tablero_visible.txt")
        
        #testeo que cargar_estado tiene que devolver false
        self.assertFalse(cargar_estado(estado,ruta))
    
    def test_no_coinciden_lineas(self):
        ruta = os.path.join(".","tableros_para_test/no_coinciden_filas")
        estado = crear_juego(10,10,10) #creo un estado cualquiera
        
        cargar_estado(estado,ruta)

        ruta_tablero = os.path.join(ruta, "tablero.txt")
        ruta_visible = os.path.join(ruta, "tablero_visible.txt")

        #Cargamos los archivos para testear
        archivo_tablero = open(ruta_tablero, "r")
        lineas_tablero = archivo_tablero.readlines()
        archivo_tablero.close()

        archivo_visible = open(ruta_visible, "r")
        lineas_tablero_visible = archivo_visible.readlines()
        archivo_visible.close()

        #cargar_estado deberia dar False
        self.assertFalse(cargar_estado(estado,ruta))

        #testeo si los archivos tablero.txt y tablero_visible.txt existen
        self.assertTrue(os.path.exists(ruta_tablero))
        self.assertTrue(os.path.exists(ruta_visible))
        
        #testeo que la cantidad de lı́neas en tablero.txt, en este caso, no es igual a la cantidad de lı́neas en tablero visible.txt
        self.assertNotEqual(len(lineas_tablero),len(lineas_tablero_visible))

    def test_numeros_invalidos(self):
        ruta = os.path.join(".","tableros_para_test/tablero_numero_invalido")
        estado = crear_juego(2,2,1) #creo un estado cualquiera

        #en tablero hay un 9 dando vueltas (numero invalido)
        self.assertFalse(cargar_estado(estado,ruta))

        #testeo si los archivos tablero.txt y tablero_visible.txt existen
        ruta_tablero = os.path.join(ruta, "tablero.txt")
        ruta_visible = os.path.join(ruta, "tablero_visible.txt")

        self.assertTrue(os.path.exists(ruta_tablero))
        self.assertTrue(os.path.exists(ruta_visible))

    def test_tablero_visible_invalido(self):
        ruta = os.path.join(".","tableros_para_test/tablero_visible_invalido")
        estado = crear_juego(2,2,1) #creo un estado cualquiera

        #en tablero visible hay una X dando vueltas
        self.assertFalse(cargar_estado(estado,ruta))

        #testeo si los archivos tablero.txt y tablero_visible.txt existen
        ruta_tablero = os.path.join(ruta, "tablero.txt")
        ruta_visible = os.path.join(ruta, "tablero_visible.txt")

        self.assertTrue(os.path.exists(ruta_tablero))
        self.assertTrue(os.path.exists(ruta_visible))

    def test_tablero_sin_minas(self):
        ruta = os.path.join(".","tableros_para_test/tablero_sin_minas")
        estado = crear_juego(2,2,1) #creo un estado cualquiera

        self.assertFalse(cargar_estado(estado,ruta))

        #testeo si los archivos tablero.txt y tablero_visible.txt existen
        ruta_tablero = os.path.join(ruta, "tablero.txt")
        ruta_visible = os.path.join(ruta, "tablero_visible.txt")

        self.assertTrue(os.path.exists(ruta_tablero))
        self.assertTrue(os.path.exists(ruta_visible))

#Auxiliares
class es_matrizTest(unittest.TestCase):
    def test_tamano_incorrecto(self):
        tablero = [[VACIO,VACIO],
                   [VACIO,VACIO],
                   [VACIO,VACIO,VACIO,]]

        self.assertFalse(es_matriz(tablero))

class estado_vaidoTest(unittest.TestCase):
    def test_bomba_tablero_visible(self):
        estado: EstadoJuego = {
                'filas': 2,
                'columnas': 2,
                'minas': 2,
                'tablero': [
                    [-1, 2],
                    [ 2,-1]
                ],
                'tablero_visible': [
                    [BOMBA, "1"],
                    ["1", VACIO]
                ],
                'juego_terminado': False
            }
        self.assertFalse(estado_valido(estado))

    def test_bomba_pero_no_mina(self):
        estado: EstadoJuego = {
                'filas': 2,
                'columnas': 2,
                'minas': 2,
                'tablero': [
                    [-1, 2],
                    [ 2,-1]
                ],
                'tablero_visible': [
                    [VACIO, "2"],
                    [BOMBA, VACIO]#dice Bomba pero en tablero no hay nada
                ],
                'juego_terminado': True
            }
        self.assertFalse(estado_valido(estado))

    def test_numeros_incorrectos(self):
        estado: EstadoJuego = {
                'filas': 2,
                'columnas': 2,
                'minas': 2,
                'tablero': [
                    [-1, 5],#numero incorrecto
                    [ 2,-1]
                ],
                'tablero_visible': [
                    [VACIO, "5"],
                    [VACIO, VACIO]
                ],
                'juego_terminado': False
            }
        self.assertFalse(estado_valido(estado))

    def test_mas_minas_que_celdas(self):
        estado: EstadoJuego = {
                'filas': 2,
                'columnas': 2,
                'minas': 27,
                'tablero': [
                    [-1, 2],
                    [ 2,-1]
                ],
                'tablero_visible': [
                    [VACIO, "2"],
                    [VACIO, VACIO]
                ],
                'juego_terminado': False
            }
        self.assertFalse(estado_valido(estado))

    def test_cantidad_minas_diferente(self):
        estado: EstadoJuego = {
                'filas': 2,
                'columnas': 2,
                'minas': 1,#una mina pero hay dos
                'tablero': [
                    [-1, 2],
                    [ 2,-1]
                ],
                'tablero_visible': [
                    [VACIO, "2"],
                    [VACIO, VACIO]
                ],
                'juego_terminado': False
            }
        self.assertFalse(estado_valido(estado))

    def test_tablero_visible_invalido(self):
        estado: EstadoJuego = {
                'filas': 2,
                'columnas': 2,
                'minas': 2,
                'tablero': [
                    [-1, 2],
                    [ 2,-1]
                ],
                'tablero_visible': [#Testeamos strings claramente invalidos
                    [VACIO, "And if a double decker bus"],
                    ["Crashes into us...", VACIO]],
                'juego_terminado':False
            }
        self.assertFalse(estado_valido(estado))

    def test_valores_en_tablero_invalidos(self):
        estado: EstadoJuego = {
                'filas': 2,
                'columnas': 2,
                'minas': 2,
                'tablero': [
                    [-1, 27],#Numeros sin sentido
                    [ -2,-1]
                ],
                'tablero_visible': [
                    [VACIO, VACIO],
                    [VACIO, VACIO]],
                'juego_terminado':False
            }
        self.assertFalse(estado_valido(estado))

    def test_filas_cero(self):
        estado: EstadoJuego = {
                'filas': 0,
                'columnas': 2,
                'minas': 2,
                'tablero': [
                    [-1, 27],#Numeros sin sentido
                    [ -2,-1]
                ],
                'tablero_visible': [
                    [VACIO, VACIO],
                    [VACIO, VACIO]],
                'juego_terminado':False
            }
        self.assertFalse(estado_valido(estado))

    def test_juego_terminado_invalido(self):
        estado: EstadoJuego = {
                'filas': 2,
                'columnas': 2,
                'minas': 2,
                'tablero': [
                    [-1, 2],
                    [ 2,-1]
                ],
                'tablero_visible': [
                    [VACIO, VACIO],
                    [VACIO, VACIO]],
                'juego_terminado':"Falso" #testeamos con un valor no booleano
            }
        self.assertFalse(estado_valido(estado))



class estructura_tipos_validosTest(unittest.TestCase):
    def test_estado_con_muchas_keys(self):
        estado: EstadoJuego = {
                'filas': 2,
                'columnas': 2,
                'minas': 2,
                'tablero': [
                    [-1, 2],
                    [ 2,-1]
                ],
                'tablero_visible': [
                    [VACIO, VACIO],
                    [VACIO, VACIO]],
                'juego_terminado':False,
                #keys de mas:
                'To die by your side':False,
                'Is such a heavenly way to die': True
            }
        self.assertFalse(estructura_y_tipos_validos(estado))
    
    def test_tableros_distinta_dimension(self):
        estado: EstadoJuego = {
                'filas': 2,
                'columnas': 2,
                'minas': 2,
                'tablero': [
                    [-1, 2],
                    [ 2,-1]
                ],
                'tablero_visible': [
                    [VACIO, VACIO],
                    [VACIO, VACIO],
                    [VACIO, VACIO]],#una dimension extra
                'juego_terminado':False
            }
        self.assertFalse(estructura_y_tipos_validos(estado))

    def test_columnas_no_coincide(self):
        estado: EstadoJuego = {
                'filas': 2,
                'columnas': 3,
                'minas': 2,
                'tablero': [
                    [-1, 2],
                    [ 2,-1]
                ],
                'tablero_visible': [
                    [VACIO, VACIO],
                    [VACIO, VACIO]],
                'juego_terminado':False
            }
        self.assertFalse(estructura_y_tipos_validos(estado))

class son_el_mismo_tableroTest(unittest.TestCase):
    def test_dimensiones_diferentes(self):
        tablero1 = [[0,0,0,0,0],
                    [0,0,0,0,0]]
        
        tablero2 = [[0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0]]
        
        self.assertFalse(son_el_mismo_tablero(tablero1,tablero2))

    def test_mismo_tablero(self):
        tablero1 = [[1,2,3,4,5,6,7],
                    [3,4,5,6,7,8,9],
                    [1,2,3,4,5,6,7],
                    [3,4,5,6,7,8,9]]
        
        tablero2 = [[1,2,3,4,5,6,7],
                    [3,4,5,6,7,8,9],
                    [1,2,3,4,5,6,7],
                    [3,4,5,6,7,8,9]]
        
        self.assertTrue(son_el_mismo_tablero(tablero1,tablero2))


    
        
   

if __name__ == '__main__':
    unittest.main(verbosity=2)
