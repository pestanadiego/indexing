import csv
from Historieta import Historieta


def cargar_historietas(historietas):
    with open('historietas.csv', 'r') as archivo_csv:
        csv_reader = csv.reader(archivo_csv)

        for line in csv_reader:
            historieta = Historieta()
            historieta.serial = line[0]
            historieta.titulo = line[1]
            historieta.precio = line[2]
            historieta.stock = line[3]
            historietas.append(historieta)

    return historietas


def guardar_historietas(historietas):
    with open('historietas.csv', 'w') as archivo_csv:
        csv_writer = csv.writer(archivo_csv)

        for historieta in historietas:
            line = '{serial},{titulo},{precio},{stock}'.format(
                serial=historieta.serial,
                titulo=historieta.titulo,
                precio=historieta.precio,
                stock=historieta.stock
            )
            csv_writer.writerow(line)


def main():
    # Inicialización
    historietas = []
    historietas = cargar_historietas(historietas)
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
        while (not seleccion.isnumeric()) or (int(seleccion) not in range(1, 7)):
            seleccion = input('Por favor, ingrese una opción válida: ')

        if seleccion == '1':
            print('To do')

        elif seleccion == '2':
            for historieta in historietas:
                print(historieta)

        elif seleccion == '3':
            print('To do')

        elif seleccion == '4':
            print('To do')

        elif seleccion == '5':
            print('To do')

        elif seleccion == '7':
            print('To do')

        else:
            print('¡Hasta luego!')
            break


if __name__ == "__main__":
    main()
