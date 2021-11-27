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
    # Función de ayuda (recursividad)
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
    while (not precio.isnumeric()) or (int(precio) < 0) or (len(precio) > 3) or (len(precio) < 1):
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

def consulta_titulo():
    pass


# MAIN

def main():
    # Inicialización
    historietas = []
    historietas = cargar_historietas(historietas)
    
    seriales_index = []
    for historieta in historietas:
        serial = [historieta.rrn, historieta.serial]
        seriales_index.append(serial)
    quick_sort(seriales_index)

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
            seleccion_consulta = input('¿Desea buscar por serial (1) o título (2)?: ')
            while (not seleccion_consulta.isnumeric()) or (len(seleccion_consulta) != 1) or (int(seleccion_consulta) <= 0) or (int(seleccion_consulta) > 2):
                seleccion_consulta = input('Ingrese una opción válida: ')

            if(seleccion_consulta == '1'):
                serial = input('Ingrese el serial de la historieta: ')
                while (not len(serial) == 8) or (not serial.isnumeric()): 
                    serial = input('Ingrese un serial válido: ')
                historieta_consulta = consulta_serial(historietas, seriales_index, serial)
                print(historieta_consulta.titulo, historieta_consulta.precio, historieta_consulta.stock)
            else:
                # TO DO
                consulta_titulo()

        elif seleccion == '3':
            for historieta in historietas:
                print(historieta.rrn, historieta.serial, historieta.titulo, historieta.precio, historieta.stock)

        elif seleccion == '4':
            print('To do')

        elif seleccion == '5':
            print('To do')

        else:
            print('¡Hasta luego!')
            break


if __name__ == "__main__":
    main()
