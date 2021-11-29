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
                stock=line[4],
                muerto=line[5]
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
                historieta.stock,
                historieta.muerto
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
    if int(prev) >= 0:
        if lista[prev][1] == valor_medio:
            titulos_rrn.append(lista[prev][0])
            return check_repeated(lista, valor_medio, next, prev-1, titulos_rrn)
    return titulos_rrn

# FUNCIONALIDADES

def registrar_historieta(historietas, seriales_index):
    # RRN
    rrn = str(len(historietas))
    # Serial
    serial = input('Ingrese el serial de la historieta: ')
    while (not len(serial) == 8) or (not serial.isnumeric()) or (sum(serial_index.count(serial) for serial_index in seriales_index) == 1):
        serial = input('Ingrese un serial válido: ')
    # Titulo
    titulo = input('Ingrese el título de la historieta: ').lower()
    while (len(titulo) > 40) or (len(titulo) < 1):
        titulo = input('Ingrese un título válido: ').lower()
    titulo = titulo.title()
    # Precio (siempre será entero)
    precio = input('Ingrese el precio de la historieta: ')
    while (not precio.isnumeric()) or (int(precio) <= 0) or (len(precio) > 3) or (len(precio) < 1):
        precio = input('Ingrese un precio válido: ')
    # Stock
    stock = input('Ingrese cuántas unidades hay: ')
    while (not stock.isnumeric()) or (len(stock) > 2) or (len(stock) < 1) or (int(stock) <= 0):
        stock = input('Introduzca una cantidad válida: ')

    nueva_historieta = Historieta(rrn, serial, titulo, precio, stock, "0")
    historietas.append(nueva_historieta)
    print('¡Se ha registrado la historieta con éxito!')
    return historietas

def consulta_serial(historietas, seriales, serial):
    index = busqueda_binaria(seriales, serial)
    if index != "NO":
        rrn_consulta = seriales[index][0]
        if historietas[int(rrn_consulta)].muerto == "0":
            return historietas[int(rrn_consulta)]
        else:
            return "Muerto"
    else:
        return "Nada"

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
        if count == len(titulo) and (historietas[int(index)].muerto == '0'):
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

def buy_historieta(compra, monto):
    aux = 0
    print("\n")
    print("HISTORIETAS A TU ALCANCE")
    print("Productos seleccionados: ")
    print(
        f'titulo: {compra[0].titulo} cantidad: {compra[1]} Precio unidad: ${compra[0].precio}')
    aux = int(compra[0].precio)
    monto = aux*(int(compra[1]))
    compra[0].stock = str(int(compra[0].stock)-int(compra[1]))

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
        lista = []
        serial = input('Ingrese el serial de la historieta: ')
        while (not len(serial) == 8) or (not serial.isnumeric()):
            serial = input('Ingrese un serial válido: ')
        historieta_consulta = consulta_serial(
            historietas, seriales_index, serial)
        if historieta_consulta != "Nada" and historieta_consulta != "Muerto":
            print("\nNombre: " + historieta_consulta.titulo,
                  "\nPrecio: $"+historieta_consulta.precio, "\nStock: " + historieta_consulta.stock+"\n")
            lista.append(historieta_consulta)
        else:
            print("No se han encontrado coincidencias de ese serial.")

        return lista

    else:
        titulo = input(
            'Ingrese el nombre de la historieta: ').lower()
        while (len(titulo.split(" ")) > 2 or len(titulo) == 0):
            titulo = input('Ingrese un titulo con 1 o 2 palabras: ').lower()
        titulo = titulo.title()
        titulo = titulo.split(" ")
        historieta_consulta = consulta_titulo(
            historietas, titulos_index, titulo)
        if len(historieta_consulta) == 0:
            print("No se han encontrado historietas con ese título")
        elif len(historieta_consulta) == 1:
            print("\nNombre: " + historieta_consulta[0].titulo,
                  "\nPrecio: $"+historieta_consulta[0].precio, "\nStock: " + historieta_consulta[0].stock+"\n")
        else:
            n = 0
            print(
                "Se han encontrado las siguientes historietas:\n")
            for historieta in historieta_consulta:
                n += 1
                print(str((n)) + ".", "Nombre: " + historieta.titulo, "\nPrecio: $" +
                      historieta.precio, "\nStock:", historieta.stock + "\n")
        return historieta_consulta

def reabastecer_historietas(historietas, seriales_index, titulos_index):
    reabastecer = consulta(historietas, seriales_index, titulos_index)
    if len(reabastecer) == 1:
        while True:
            try:
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

        if escoge == "1":
            cant = input(
                "Ingrese la cantidad de historietas que desea agregar al stock: ")
            while not cant.isnumeric() or int(cant) < 0:
                cant = input("Ingrese una cantidad válida: ")
            reabastecer[0].stock = str(int(
                reabastecer[0].stock) + int(cant))
    else:
        while True:
            try:
                escoge = input('''Desea reabastecer el stock de alguna de las historietas encontradas?
                1. Si
                2. No
                >> ''')
                if int(escoge) < 0 or int(escoge) > 2:
                    raise Exception
                else:
                    break
            except:
                print("Ingrese una opción válida")
        if escoge == "1":
            while True:
                try:
                    historieta = input(
                        "Seleccione el número correspondiente a la historieta que desea reabastecer: ")
                    if int(historieta) > len(reabastecer) or int(historieta) <= 0:
                        raise Exception
                    else:
                        break
                except:
                    print("Seleccione un número válido. \n")
            cant = input(
                "Ingrese la cantidad de historietas que desea agregar al stock: ")
            while not cant.isnumeric() or int(cant) < 0:
                cant = input("Ingrese una cantidad válida: ")
            reabastecer[int(
                historieta)-1].stock = str(int(reabastecer[int(historieta)-1].stock) + int(cant))

def eliminar_historieta(historietas, seriales_index, titulos_index):
    historietas_encont = consulta(
        historietas, seriales_index, titulos_index)
    if len(historietas_encont) == 1:
        while True:
            try:
                escoge = input('''¿Desea eliminar esta historieta?
                1. Si
                2. No
                >> ''')
                if int(escoge) < 0 or int(escoge) > 2:
                    raise Exception
                else:
                    break
            except:
                print("Ingrese una opción válida")

        if escoge == "1":
            historietas_encont[0].muerto = '1'
    else:
        while True:
            try:
                escoge = input('''Desea eliminar alguna de las historietas encontradas?
                1. Si
                2. No
                >> ''')
                if int(escoge) < 0 or int(escoge) > 2:
                    raise Exception
                else:
                    break
            except:
                print("Ingrese una opción válida")
        if escoge == "1":
            while True:
                try:
                    historieta = input(
                        "Seleccione el número correspondiente a la historieta que desea eliminar: ")
                    if int(historieta) > len(historietas_encont) or int(historieta) <= 0:
                        raise Exception
                    else:
                        break
                except:
                    print("Seleccione un número válido. \n")
            historietas_encont[int(
                historieta)-1].muerto = '1'

def checkout(historietas, seriales_index, titulos_index):
    buying = []
    monto = 0
    returned = consulta(historietas, seriales_index, titulos_index)
    if (len(returned) > 1):
        selection = input(
            "Ingrese el numero correspondiente a la historieta que desea comprar: ")
        while(int(selection) > len(returned)):
            selection = input("Ingrese un indice válido: ")

        story = returned[int(selection)-1]
        buying.append(story)
        print("Nombre: " + story.titulo,
              "\nPrecio: $" + story.precio, "\nStock:" + story.stock)

        v = input(
            "Desea comprar esta historieta? ingrese 'Y' para comprarla, otro caracter si no: ")

        if((v.lower() == 'y') and (int(story.stock) > 0)):
            quantity = input(
                "Ingrese el numero de ejemplares que desea comprar: ")
            while(int(quantity) <= 0 or (quantity.isalpha()) or int(quantity) > int(story.stock)):
                quantity = input(
                    "Ingrese un número válido. Asegurese de que esté comprando una cantidad menor o igual a la disponible: ")
            buying.append(quantity)
            buy_historieta(buying, monto)

        elif((int(story.stock) <= 0)):
            print(
                'No se puede realizar la compra ya que no existen ejemplares de esta historieta.')

        else:
            print('Se ha cancelado la compra')
    elif len(returned) == 1:
        v = input(
            "Desea comprar esta historieta? ingrese 'Y' para comprarla, otro caracter si no: ")
        if(v.lower() == 'y' and (int(returned[0].stock) > 0)):
            buying.append(returned[0])
            quantity = input(
                "Ingrese el numero de ejemplares que desea comprar: ")
            while(int(quantity) <= 0 or (quantity.isalpha()) or int(quantity) > int(returned[0].stock)):
                quantity = input(
                    "Ingrese un número válido. Asegurese de que esté comprando una cantidad menor o igual a la disponible: ")
            buying.append(quantity)
            buy_historieta(buying, monto)
        elif((int(returned[0].stock) <= 0)):
            print(
                'No se puede realizar la compra ya que no existen ejemplares de esta historieta.')
        else:
            print('Se ha cancelado la compra')
    else:
        pass

def compactador(historietas):
    count = 0
    if len(historietas) < 1:
        print("No hay historietas en el inventario, no se puede compactar.")
    else:
        for i in range(len(historietas)):
            i = i - count
            historietas[i].rrn = str(int(historietas[i].rrn)-count)
            if historietas[i].muerto == "1":
                count += 1
                historietas.remove(historietas[i])
        print("Se ha compactado exitosamente")
    return historietas

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
    print(historietas)
    print(titulos_index)
    print(seriales_index)

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
            historietas = registrar_historieta(historietas, seriales_index)
            # Cargamos los cambios al CSV
            guardar_historietas(historietas)
            # Vaciamos y volvemos a crear y ordenar el index de seriales
            seriales_index = []
            seriales_index = reorder_seriales_index(
                historietas, seriales_index)
            quick_sort(seriales_index)
            # Vaciamos y volvemos a crear y ordenar el index de titulos
            titulos_index = []
            titulos_index = reorder_titulos_index(historietas, titulos_index)
            quick_sort(titulos_index)

        elif seleccion == '2':
            consulta(historietas, seriales_index, titulos_index)

        elif seleccion == '3':
            checkout(historietas, seriales_index, titulos_index)
            # Cargamos los cambios al CSV
            guardar_historietas(historietas)

        elif seleccion == '4':
            reabastecer_historietas(historietas, seriales_index, titulos_index)
            # Cargamos los cambios al CSV
            guardar_historietas(historietas)

        elif seleccion == '5':
            eliminar_historieta(historietas, seriales_index, titulos_index)
            # Cargamos los cambios al CSV
            guardar_historietas(historietas)

        elif seleccion == "6":
            historietas = compactador(historietas)
            # Cargamos los cambios al CSV
            guardar_historietas(historietas)
            # Vaciamos y volvemos a crear y ordenar el index de seriales
            seriales_index = []
            seriales_index = reorder_seriales_index(
                historietas, seriales_index)
            quick_sort(seriales_index)
            # Vaciamos y volvemos a crear y ordenar el index de titulos
            titulos_index = []
            titulos_index = reorder_titulos_index(historietas, titulos_index)
            quick_sort(titulos_index)

        else:
            print('¡Hasta luego!')
            break

if __name__ == "__main__":
    main()
