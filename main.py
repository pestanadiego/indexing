import csv
from Historieta import Historieta

# LECTURA/ESCRITURA


def cargar_historietas(historietas):
    with open('historietas.csv', 'r') as archivo_csv:
        csv_reader = csv.reader(archivo_csv)

        for line in csv_reader:
            historieta = Historieta(
                rrn=line[0],
                serial=line[1],
                titulo=line[2],
                precio=line[3],
                stock=line[4]
            )
            historietas.append(historieta)

    return historietas


def guardar_historietas(historietas):
    with open('historietas.csv', 'w') as archivo_csv:
        csv_writer = csv.writer(archivo_csv)

        for historieta in historietas:
            line = [
                historieta.rrn,
                historieta.serial,
                historieta.titulo,
                historieta.precio,
                historieta.stock
            ]
            csv_writer.writerow(line)


# ORDENAMIENTO

def pivote(seriales, bajo, alto):
    pivote = seriales[(bajo + alto) // 2][1]
    i = bajo - 1
    j = alto + 1
    while True:
        i += 1
        while seriales[i][1] < pivote:
            i += 1

        j -= 1
        while seriales[j][1] > pivote:
            j -= 1

        if i >= j:
            return j

        seriales[i], seriales[j] = seriales[j], seriales[i]


def quick_sort(seriales):
    # Función de ayuda recursividad
    def quick_sort_recursivo(seriales, bajo, alto):
        if bajo < alto:
            index_particion = pivote(seriales, bajo, alto)
            quick_sort_recursivo(seriales, bajo, index_particion)
            quick_sort_recursivo(seriales, index_particion + 1, alto)

    quick_sort_recursivo(seriales, 0, len(seriales) - 1)

# BUSQUEDA


def busqueda_binaria(lista, item):
    index_inicial = 0
    index_final = len(lista) - 1

    while index_inicial <= index_final:
        medio = index_inicial + (index_final - index_inicial) // 2
        valor_medio = lista[medio][1]
        if valor_medio == item:
            return medio

        elif item < valor_medio:
            index_final = medio - 1

        else:
            index_inicial = medio + 1

    return "NO"


def busqueda_binaria_titulo(lista, item):
    index_inicial = 0
    index_final = len(lista) - 1

    while index_inicial <= index_final:
        medio = index_inicial + (index_final - index_inicial) // 2
        valor_medio = lista[medio][1]
        if valor_medio == item:
            titulos_rrn = [lista[medio][0]]
            return check_repeated(lista, valor_medio, medio + 1, medio - 1, titulos_rrn)

        elif item < valor_medio:
            index_final = medio - 1

        else:
            index_inicial = medio + 1

    return "NO"


def check_repeated(lista, valor_medio, next, prev, titulos_rrn):
    if len(lista) > next:
        if lista[next][1] == valor_medio:
            titulos_rrn.append(lista[next][0])
            return check_repeated(lista, valor_medio, next+1, prev, titulos_rrn)
    if prev > 0:
        if lista[prev][1] == valor_medio:
            titulos_rrn.append(lista[prev][0])
            return check_repeated(lista, valor_medio, next, prev-1, titulos_rrn)
    return titulos_rrn

    # FUNCIONALIDADES


def registrar_historieta(historietas, seriales_index):
    # RRN
    rrn = len(historietas)
    # Serial
    serial = input('Ingrese el serial de la historieta: ')
    while (not len(serial) == 8) or (not serial.isnumeric()) or (sum(serial_index.count(serial) for serial_index in seriales_index) == 1):
        serial = input('Ingrese un serial válido: ')
    # Titulo
    titulo = input('Ingrese el título de la historieta: ')
    while (len(titulo) > 40) or (len(titulo) < 1):
        titulo = input('Ingrese un título válido: ')
    # Precio (siempre será entero)
    precio = input('Ingrese el precio de la historieta: ')
    while (not precio.isnumeric()) or (int(precio) <= 0) or (len(precio) > 3) or (len(precio) < 1):
        precio = input('Ingrese un precio válido: ')
    # Stock
    stock = input('Ingrese cuántas unidades hay: ')
    while (not stock.isnumeric()) or (len(stock) > 2) or (len(stock) < 1) or (int(stock) <= 0):
        stock = input('Introduzca una cantidad válida: ')

    nueva_historieta = Historieta(rrn, serial, titulo, precio, stock)
    historietas.append(nueva_historieta)
    print('¡Se ha registrado la historieta con éxito!')


def consulta_serial(historietas, seriales, serial):
    index = busqueda_binaria(seriales, serial)
    rrn_consulta = seriales[index][0]
    return historietas[int(rrn_consulta)]


def consulta_titulo(historietas, titulos, titulo):
    count = 0
    found_titles = []
    titulos_index = busqueda_binaria_titulo(titulos, titulo[0])
    if titulos_index == "NO":
        return found_titles
    for index in titulos_index:
        for palabra in titulo:
            if palabra in historietas[int(index)].titulo:
                count += 1
        if count == len(titulo):
            found_titles.append(historietas[int(index)])
            count = 0
        else:
            count = 0
    return found_titles


def reorder_seriales_index(historietas, seriales_index):
    for historieta in historietas:
        serial = [historieta.rrn, historieta.serial]
        seriales_index.append(serial)
    return seriales_index


def reorder_titulos_index(historietas, titulos_index):
    for historieta in historietas:
        if " " in historieta.titulo:
            titulo_separado = historieta.titulo.split(" ")
            for parte_titulo in titulo_separado:
                titulo = [historieta.rrn, parte_titulo]
                titulos_index.append(titulo)
        else:
            titulo = [historieta.rrn, historieta.titulo]
            titulos_index.append(titulo)
    return titulos_index


def buy_historieta(compra):
    monto = 0

    print("\n")
    print("HISTORIETAS A TU ALCANCE")
    print("Productos seleccionados: ")
    for i in range(len(compra)):
        print(
            f'{i+1} titulo: {compra[i][0].titulo} cantidad: {compra[i][1]} Precio unidad: ${compra[i][0].precio}')
        aux = int(compra[i][0].precio)
        aux1 = aux*(int(compra[i][1]))
        monto += aux1
        compra[i][0].stock = str(int(compra[i][0].stock)-int(compra[i][1]))

    print("----------------------------------------------------")
    print(f'Total: ${monto}')
    print("\n")

    selection = input("Ingrese el pin de su tarjeta de credito: ")
    while(len(selection) != 4):
        selection = input("Ingrese un numero de tarjeta valido: ")

    print("Su compra fue realizada con exito!")


def consulta(historietas, seriales_index, titulos_index):
    seleccion_consulta = input(
        '¿Desea buscar por serial (1) o título (2)?: ')
    while (not seleccion_consulta.isnumeric()) or (len(seleccion_consulta) != 1) or (int(seleccion_consulta) <= 0) or (int(seleccion_consulta) > 2):
        seleccion_consulta = input('Ingrese una opción válida: ')

    if(seleccion_consulta == '1'):
        lista=[]
        serial = input('Ingrese el serial de la historieta: ')
        while (not len(serial) == 8) or (not serial.isnumeric()):
            serial = input('Ingrese un serial válido: ')
        historieta_consulta = consulta_serial(
            historietas, seriales_index, serial)
        lista.append(historieta_consulta)
        print(historieta_consulta.titulo,
              historieta_consulta.precio, historieta_consulta.stock)
        return lista
    else:
        titulo = input(
            'Ingrese el nombre de la historieta: ')
        while (len(titulo.split(" ")) > 2 or len(titulo) == 0):
            titulo = input('Ingrese un titulo con 1 o 2 palabras: ')
        titulo = titulo.split(" ")
        historieta_consulta = consulta_titulo(
            historietas, titulos_index, titulo)
        if len(historieta_consulta) == 0:
            print("No se han encontrado historietas con ese título")
        elif len(historieta_consulta) == 1:
            print(historieta_consulta[0].titulo,
                  historieta_consulta[0].precio, historieta_consulta[0].stock)
        else:
            n = 0
            print(
                "Se han encontrado las siguientes historietas:")
            for historieta in historieta_consulta:
                n += 1
                print(str(n) + ". ", historieta.titulo)
        return historieta_consulta



# MAIN


def main():
    # Inicialización
    historietas = []
    historietas = cargar_historietas(historietas)
    titulos_index = []
    seriales_index = []

    # Se crea el index de los seriales y se ordenan de menor a mayor
    seriales_index = reorder_seriales_index(historietas, seriales_index)
    quick_sort(seriales_index)

    # Se crea el index de los titulos y se ordenan alfabéticamente
    titulos_index = reorder_titulos_index(historietas, titulos_index)
    quick_sort(titulos_index)

    print('Manejo de inventario')

    while True:
        seleccion = input('''Por favor, seleccione una opción:
        1. Registro.
        2. Consulta.
        3. Compra.
        4. Reabastecimiento.
        5. Eliminación.
        6. Compactador.
        7. Salir.
        >> ''')
        while (not seleccion.isnumeric()) or (int(seleccion) not in range(1, 8)):
            seleccion = input('Por favor, ingrese una opción válida: ')

        if seleccion == '1':
            registrar_historieta(historietas, seriales_index)
            guardar_historietas(historietas)

        elif seleccion == '2':
            consulta(historietas, seriales_index, titulos_index)

        elif seleccion == '3':
                
            returned = consulta(historietas, seriales_index, titulos_index)
            if (len(returned)>1):
                selection = input("Ingrese el numero correspondiente a la historieta que desea comprar")
                while(int(selection) > len(returned)):
                    selection=input("Ingrese un indice válido: ")
                
                story = returned[int(selection)-1]
                print(story.stock)

            #quantity = input(
            #    "Por favor ingrese el numero de ejemplares que desea comprar: ")
            #while((int(quantity) > int(historietas[int(selected)-1].stock)) or ((int(quantity)) < 0) or (quantity.isalpha())):
            #    quantity: input(
            #        "No contamos con esa cantidad de ejemplares, por favor ingrese una cantidad valida: ")
            #
            #story.append(quantity)
            #seleccion.append(story)
#
            #buy_historieta(seleccion)

        elif seleccion == '4':
            reabastecer = consulta(historietas, seriales_index, titulos_index)
            while True:
                try:
                    if len(reabastecer) == 1:
                        escoge = input('''Desea reabastecer el stock de esta historieta?
                        1. Si
                        2. No
                        >> ''')
                        if int(escoge) < 0 or int(escoge) > 2:
                            raise Exception
                        else:
                            break
                except:
                    print("Ingrese una opción válida")

        elif seleccion == '5':
            print('To do')

        else:
            print('¡Hasta luego!')
            break


if __name__ == "__main__":
    main()
