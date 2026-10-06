# Importamos os porque lo usamos para limpiar la pantalla.
import os


# DICCIONARIO: cada color tiene su etiqueta y su código de consola
# Aquí guardamos los códigos de los colores que usará el programa.
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}


# TUPLA: respuestas afirmativas aceptadas
# Estas son las respuestas que el programa considera como un "sí".
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


# Esta función limpia la pantalla de la consola.
def limpiar_pantalla():
    # Dependiendo del sistema operativo se utiliza un comando diferente.
    os.system("clear" if os.name == "posix" else "cls")
    

# Esta función muestra un texto utilizando el color indicado.
def imprimir_color(texto, color):
    # Buscamos el código del color en el diccionario.
    codigo = COLORES.get(color, COLORES["BLANCO"])

    # Mostramos el texto con el color seleccionado.
    print(f"{codigo}{texto}{COLORES['RESET']}")


# Esta función muestra un título en la pantalla.
def imprimir_titulo(texto):

    # Primero limpiamos la pantalla.
    limpiar_pantalla()

    # Mostramos una línea azul.
    imprimir_color("=" * 60, "AZUL")

    # Mostramos el título en el centro.
    print(f"  {texto}".center(60))

    # Mostramos otra línea azul.
    imprimir_color("=" * 60, "AZUL")

    print()


# Esta función muestra un mensaje de éxito.
def imprimir_exito(mensaje):
    imprimir_color(f"✓ {mensaje}", "VERDE")


# Esta función muestra un mensaje de error.
def imprimir_error(mensaje):
    imprimir_color(f"✗ {mensaje}", "ROJO")


# Esta función muestra un mensaje informativo.
def imprimir_info(mensaje):
    imprimir_color(f"ℹ {mensaje}", "CYAN")


# Esta función pregunta al usuario si quiere confirmar una acción.
def confirmar(pregunta):

    # Guardamos la respuesta y la convertimos a minúsculas.
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()

    # Revisamos si la respuesta está dentro de las respuestas aceptadas.
    return respuesta in RESPUESTAS_SI


# Esta función revisa si un correo tiene un formato válido.
def es_email_valido(texto):

    # Quitamos espacios que puedan estar al principio o al final.
    texto = texto.strip()

    # El correo debe tener solamente un símbolo @.
    if texto.count("@") != 1:
        return False

    # Separamos el correo en usuario y dominio.
    usuario, dominio = texto.split("@")

    # Comprobamos que exista usuario, que el dominio tenga un punto
    # y que no termine en punto.
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")