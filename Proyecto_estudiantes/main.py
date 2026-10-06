# Importamos los campos que tiene un estudiante.
from models import CAMPOS_ESTUDIANTE

# Importamos las funciones que sirven para mostrar mensajes en pantalla.
from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar,
)

# Importamos las funciones que realizan las operaciones con los estudiantes.
from views import (
    crear_estudiante,
    obtener_todos,
    obtener_por_id,
    buscar_estudiantes,
    actualizar_estudiante,
    eliminar_estudiante,
    agregar_nota,
    materias_ofertadas,
    estudiantes_en_comun,
)

# Esta función hace una pausa para que el usuario pueda leer la información.
def pausa():
    input("\nPresione Enter para continuar...")

# Esta función muestra los estudiantes en forma de tabla.
def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CARNET':<15}")
    print("-" * 73)

    # Recorremos todos los estudiantes para mostrarlos.
    for estudiante in estudiantes:
        print(
            f"{estudiante.id:<5}"
            f"{estudiante.obtener_nombre_completo():<25}"
            f"{estudiante.email:<28}"
            f"{estudiante.carnet:<15}"
        )

    print("-" * 73)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")
   
# Esta función permite crear un estudiante nuevo.
def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")

    # Aquí se guardarán los datos que ingrese el usuario.
    datos = {}

    # Se piden todos los datos del estudiante.
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    # Se llama a la función que crea el estudiante.
    exito, mensaje = crear_estudiante(datos)

    # Se muestra un mensaje dependiendo del resultado.
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()
 
# Esta función permite ver todos los estudiantes.
def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")

    # Obtenemos todos los estudiantes guardados.
    estudiantes = obtener_todos()

    # Revisamos si existen estudiantes.
    if not estudiantes:
        imprimir_info(
            "Todavía no hay estudiantes. "
            "Use la opción 1 para crear el primero."
        )
    else:
        mostrar_tabla(estudiantes)

    pausa()
    
# Esta función permite buscar un estudiante.
def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")

    # El usuario escribe el dato que desea buscar.
    termino = input("Nombre, email o carnet: ")

    # Se realiza la búsqueda.
    encontrados = buscar_estudiantes(termino)

    # Se revisa si se encontraron estudiantes.
    if not encontrados:
        imprimir_info(
            f"Ningún estudiante coincide con '{termino}'."
        )
    else:
        mostrar_tabla(encontrados)

    pausa()
    
# Esta función permite ver los datos de un estudiante usando su ID.
def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")

    try:
        # Se pide el ID del estudiante.
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        # Si el usuario escribe algo que no es un número, aparece este mensaje.
        imprimir_error("El id debe ser un número entero")
        return pausa()

    # Buscamos el estudiante por su ID.
    estudiante = obtener_por_id(id_estudiante)

    # Revisamos si el estudiante existe.
    if estudiante is None:
        imprimir_info(
            f"No existe un estudiante con id {id_estudiante}."
        )
    else:
        print()
        print(f"ID: {estudiante.id}")
        print(f"Nombre: {estudiante.obtener_nombre_completo()}")
        print(f"Email: {estudiante.email}")
        print(f"Carnet: {estudiante.carnet}")
        print(f"Materias: {', '.join(sorted(estudiante.materias))}")
        print(f"Promedio: {estudiante.obtener_promedio()}")

    pausa()
  
# Esta función permite actualizar los datos de un estudiante.
def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")

    try:
        # Pedimos el ID del estudiante que queremos modificar.
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    # Buscamos el estudiante.
    estudiante = obtener_por_id(id_estudiante)

    # Si no existe, mostramos un mensaje.
    if not estudiante:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
        return pausa()

    imprimir_info(
        f"Editando a {estudiante.obtener_nombre_completo()}"
    )

    print("Deje en blanco el campo que no quiera cambiar.\n")

    # Aquí se guardan los cambios realizados.
    cambios = {}

    # Recorremos los campos del estudiante.
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(estudiante, campo)
        nuevo = input(
            f"{campo.capitalize()} [{actual}]: "
        ).strip()

        # Solo guardamos los campos que tengan un nuevo valor.
        if nuevo:
            cambios[campo] = nuevo

    # Enviamos los cambios para actualizar el estudiante.
    exito, mensaje = actualizar_estudiante(
        id_estudiante,
        cambios
    )

    # Mostramos si la operación fue exitosa o no.
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()
    
# Esta función permite eliminar un estudiante.
def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")

    try:
        # Pedimos el ID del estudiante.
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    # Buscamos el estudiante antes de eliminarlo.
    estudiante = obtener_por_id(id_estudiante)

    # Si no existe, mostramos un mensaje.
    if not estudiante:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
        return pausa()

    imprimir_info(f"Se eliminará: {estudiante}")

    # Pedimos confirmación antes de eliminar.
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)

        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")

    pausa()
    
# Esta función permite agregar una nota a un estudiante.
def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")

    try:
        # Pedimos el ID del estudiante.
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    # Pedimos la materia.
    materia = input("Materia: ").strip()

    try:
        # Pedimos la nota y la convertimos a número decimal.
        nota = float(input("Nota (0-20): "))
    except ValueError:
        imprimir_error("La nota debe ser un número")
        return pausa()

    # Agregamos la nota al estudiante.
    exito, mensaje = agregar_nota(
        id_estudiante,
        materia,
        nota
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# Esta función permite consultar el promedio de un estudiante.
def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO")

    try:
        # Pedimos el ID del estudiante.
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    # Buscamos al estudiante.
    estudiante = obtener_por_id(id_estudiante)

    # Revisamos si existe.
    if estudiante is None:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
        return pausa()

    print()
    print(f"Estudiante: {estudiante.obtener_nombre_completo()}")
    print(f"Promedio: {estudiante.obtener_promedio()}")

    pausa()
    
# Esta función muestra las materias que tienen dos estudiantes en común.
def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN")

    try:
        # Pedimos los ID de los dos estudiantes.
        id_a = int(input("Id del primer estudiante: "))
        id_b = int(input("Id del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los id deben ser números enteros")
        return pausa()

    # Buscamos las materias que tienen en común.
    materias = estudiantes_en_comun(id_a, id_b)

    # Revisamos si existen materias en común.
    if not materias:
        imprimir_info("No tienen materias en común.")
    else:
        imprimir_info("Materias en común:")

        for materia in sorted(materias):
            print(f"- {materia}")

    pausa()
    
# Esta función muestra todas las materias registradas.
def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS OFERTADAS")

    # Obtenemos las materias disponibles.
    materias = materias_ofertadas()

    if not materias:
        imprimir_info("Todavía no hay materias registradas.")
    else:
        imprimir_info("Materias ofertadas:")

        for materia in sorted(materias):
            print(f"- {materia}")

    pausa()
    
# Este diccionario relaciona cada opción del menú con su función.
OPCIONES = {
    "1": opcion_crear,
    "2": opcion_ver_todos,
    "3": opcion_buscar,
    "4": opcion_ver_por_id,
    "5": opcion_actualizar,
    "6": opcion_eliminar,
    "7": opcion_agregar_nota,
    "8": opcion_ver_promedio,
    "9": opcion_materias_en_comun,
    "10": opcion_materias_ofertadas,
}

# Esta función muestra las opciones que tiene el programa.
def mostrar_menu():
    imprimir_titulo("SISTEMA DE ESTUDIANTES")

    print("1. Crear estudiante")
    print("2. Ver todos")
    print("3. Buscar estudiante")
    print("4. Ver estudiante por ID")
    print("5. Actualizar estudiante")
    print("6. Eliminar estudiante")
    print("7. Agregar nota")
    print("8. Ver promedio")
    print("9. Materias en común")
    print("10. Materias ofertadas")
    print("0. Salir")


# Esta es la función principal del programa.
def main():
    # El menú se mantiene funcionando hasta que el usuario decida salir.
    while True:
        mostrar_menu()

        # Pedimos al usuario que seleccione una opción.
        opcion = input("\nSeleccione una opción: ").strip()

        # Si escribe 0, el programa termina.
        if opcion == "0":
            imprimir_info("Programa finalizado.")
            break

        # Buscamos la función que corresponde a la opción.
        funcion = OPCIONES.get(opcion)

        # Si la opción existe, ejecutamos su función.
        if funcion:
            funcion()
        else:
            # Si no existe, mostramos un mensaje de error.
            imprimir_error("Opción no válida")
            pausa()


# Esta condición inicia el programa principal.
if __name__ == "__main__":
    main()