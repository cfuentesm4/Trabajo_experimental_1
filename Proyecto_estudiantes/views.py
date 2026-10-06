# Importamos la clase Estudiante y los campos que tiene un estudiante.
from models import Estudiante, CAMPOS_ESTUDIANTE

# Importamos la clase que permite trabajar con el archivo JSON.
from shared.json_manager import GestorJSON

# Importamos la función que revisa si un correo es válido.
from shared.herramientas import es_email_valido


# Aquí indicamos dónde está guardada la información de los estudiantes.
gestor = GestorJSON("data/estudiantes.json")


# TUPLA de campos obligatorios
# Estos son los datos que obligatoriamente debe tener un estudiante.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")

# TUPLA de campos que podremos buscar
# Estos son los datos que podemos utilizar para buscar estudiantes.
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


# ===================== AYUDAS INTERNAS =====================

# Esta función obtiene los carnets que ya están registrados.
def carnets_registrados(excepto_id=None):
    """CONJUNTO con los carnets ya utilizados."""
    return {
        registro["carnet"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


# Esta función busca cuál será el siguiente ID disponible.
def siguiente_id():
    """Obtiene el siguiente ID disponible."""
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1

# ===================== C · CREATE =====================

# Esta función crea un nuevo estudiante y lo guarda.
def crear_estudiante(datos):
    """Crea un estudiante y lo guarda en el archivo JSON."""
    try:
        # 1) Normalizo los datos
        # Aquí limpiamos los datos que escribió el usuario.
        valores = {
            campo: str(datos.get(campo, "")).strip()
            for campo in CAMPOS_ESTUDIANTE
        }

        # 2) Reviso los campos obligatorios
        # Aquí comprobamos que no falte ningún dato obligatorio.
        faltantes = [
            campo
            for campo in CAMPOS_OBLIGATORIOS
            if not valores[campo]
        ]

        # Si falta algún dato, mostramos cuáles son.
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # 3) Reviso que el email tenga un formato válido
        # Aquí comprobamos que el correo tenga un formato correcto.
        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        # 4) Reviso que el carnet no esté repetido
        # Aquí verificamos que el carnet no exista anteriormente.
        if valores["carnet"].lower() in carnets_registrados():
            return False, "Ese carnet ya está registrado"

        # 5) Creo el objeto Estudiante
        # Aquí creamos un nuevo estudiante con los datos ingresados.
        estudiante = Estudiante(siguiente_id(), **valores)

        # 6) Lo agrego a la LISTA y guardo
        # Primero leemos los estudiantes que ya existen.
        registros = gestor.leer()

        # Después agregamos el nuevo estudiante.
        registros.append(estudiante.a_diccionario())

        # Guardamos nuevamente la información.
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        # Si todo salió bien, mostramos un mensaje.
        return True, (
            f"Estudiante {estudiante.obtener_nombre_completo()} "
            f"creado con id {estudiante.id}"
        )

    # Si ocurre algún error inesperado, lo mostramos.
    except Exception as error:
        return False, f"Error inesperado: {error}"
    
    # ===================== R · READ =====================

# Esta función obtiene todos los estudiantes guardados.
def obtener_todos():
    """Devuelve una LISTA de objetos Estudiante."""
    return [
        Estudiante.desde_diccionario(registro)
        for registro in gestor.leer()
    ]


# Esta función busca un estudiante usando su ID.
def obtener_por_id(id_estudiante):
    """Busca un estudiante por su ID."""

    # Recorremos todos los estudiantes.
    for estudiante in obtener_todos():

        # Comparamos el ID que buscamos con el ID del estudiante.
        if estudiante.id == id_estudiante:
            return estudiante

    # Si no se encuentra, devolvemos None.
    return None

# ===================== S · SEARCH =====================

# Esta función permite buscar estudiantes por diferentes datos.
def buscar_estudiantes(termino):
    """Busca estudiantes por nombre, apellido, email o carnet."""

    # Convertimos el texto a minúsculas para facilitar la búsqueda.
    termino = termino.strip().lower()

    # Si no se escribió nada, no devolvemos resultados.
    if not termino:
        return []

    # Aquí guardaremos los estudiantes encontrados.
    encontrados = []

    # Recorremos los registros guardados.
    for registro in gestor.leer():

        # Revisamos cada campo que se puede utilizar para buscar.
        for campo in CAMPOS_BUSCABLES:

            # Comprobamos si el término está dentro del campo.
            if termino in str(registro.get(campo, "")).lower():

                # Si encontramos coincidencia, agregamos el estudiante.
                encontrados.append(
                    Estudiante.desde_diccionario(registro)
                )

                # Ya no necesitamos revisar los demás campos de ese estudiante.
                break

    # Devolvemos los estudiantes encontrados.
    return encontrados

# ===================== U · UPDATE =====================

# Esta función permite actualizar los datos de un estudiante.
def actualizar_estudiante(id_estudiante, cambios):
    """Actualiza los campos indicados de un estudiante."""
    try:
        # Revisamos que los campos existan
        # Aquí comprobamos que los campos enviados sean válidos.
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)

        # Si existe algún campo que no conocemos, mostramos un error.
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        # Si no se indicó ningún cambio, mostramos un mensaje.
        if not cambios:
            return False, "No se indicó ningún cambio"

        # Si se cambia el email, lo validamos
        # Limpiamos los espacios del nuevo correo.
        if "email" in cambios:
            cambios["email"] = cambios["email"].strip()

            # Comprobamos que el nuevo correo sea válido.
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"

        # Si se cambia el carnet, revisamos que no esté repetido
        if "carnet" in cambios:
            cambios["carnet"] = cambios["carnet"].strip()

            # Revisamos que el nuevo carnet no lo tenga otro estudiante.
            if cambios["carnet"].lower() in carnets_registrados(
                excepto_id=id_estudiante
            ):
                return False, "Ese carnet ya lo usa otro estudiante"

        # Leemos todos los registros guardados.
        registros = gestor.leer()

        # Esta variable guardará la posición del estudiante.
        posicion = None

        # Recorremos todos los registros.
        for indice, registro in enumerate(registros):

            # Buscamos el estudiante por su ID.
            if registro["id"] == id_estudiante:
                posicion = indice
                break

        # Si no encontramos el estudiante, mostramos un error.
        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        # Actualizamos los datos del estudiante.
        registros[posicion].update(cambios)

        # Guardamos nuevamente los cambios.
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        # Mostramos un mensaje indicando que se actualizó.
        return True, (
            f"Estudiante {id_estudiante} actualizado "
            f"({len(cambios)} campo/s)"
        )

    # Capturamos cualquier error inesperado.
    except Exception as error:
        return False, f"Error inesperado: {error}"
    
# ===================== D · DELETE =====================

# Esta función elimina un estudiante usando su ID.
def eliminar_estudiante(id_estudiante):
    """Elimina un estudiante por su ID."""

    # Leemos los estudiantes que están guardados.
    registros = gestor.leer()

    # Creamos una LISTA nueva sin el estudiante indicado
    quedan = [
        registro
        for registro in registros
        if registro["id"] != id_estudiante
    ]

    # Si las listas tienen el mismo tamaño, no se encontró
    # Esto significa que ningún estudiante fue eliminado.
    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"

    # Guardamos la nueva lista
    if not gestor.guardar(quedan):
        return False, "No se pudo escribir el archivo"

    # Si todo salió bien, confirmamos la eliminación.
    return True, f"Estudiante {id_estudiante} eliminado"


# ===================== FUNCIONES ESPECIALES =====================

# Esta función agrega una nota a un estudiante.
def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota a un estudiante."""

    # La nota debe estar entre 0 y 20
    if nota < 0 or nota > 20:
        return False, "La nota debe estar entre 0 y 20"

    # Buscamos al estudiante.
    estudiante = obtener_por_id(id_estudiante)

    # Si no existe, mostramos un mensaje.
    if estudiante is None:
        return False, f"No existe un estudiante con id {id_estudiante}"

    # Quitamos espacios innecesarios del nombre de la materia.
    materia = materia.strip()

    # La materia no puede quedar vacía.
    if not materia:
        return False, "La materia no puede estar vacía"

    # Agregamos la nota a la materia del estudiante.
    estudiante.agregar_nota(materia, nota)

    # Leemos los registros actuales.
    registros = gestor.leer()

    # Buscamos al estudiante para actualizar sus datos.
    for registro in registros:
        if registro["id"] == id_estudiante:
            registro.update(estudiante.a_diccionario())
            break

    # Guardamos los cambios.
    if not gestor.guardar(registros):
        return False, "No se pudo guardar la nota"

    # Confirmamos que la nota se agregó correctamente.
    return True, "Nota agregada correctamente"


# Esta función obtiene todas las materias registradas.
def materias_ofertadas():
    """Devuelve un CONJUNTO con todas las materias inscritas."""

    # Creamos un conjunto vacío para guardar las materias.
    materias = set()

    # Recorremos todos los estudiantes.
    for estudiante in obtener_todos():

        # Agregamos sus materias al conjunto.
        materias.update(estudiante.materias)

    # Devolvemos todas las materias.
    return materias


# Esta función busca las materias que tienen en común dos estudiantes.
def estudiantes_en_comun(id_a, id_b):
    """Devuelve las materias que comparten dos estudiantes."""

    # Buscamos al primer estudiante.
    estudiante_a = obtener_por_id(id_a)

    # Buscamos al segundo estudiante.
    estudiante_b = obtener_por_id(id_b)

    # Si el primer estudiante no existe, devolvemos un conjunto vacío.
    if estudiante_a is None:
        return set()

    # Si el segundo estudiante no existe, devolvemos un conjunto vacío.
    if estudiante_b is None:
        return set()

    # INTERSECCIÓN de conjuntos
    # Aquí obtenemos solamente las materias que tienen los dos estudiantes.
    return estudiante_a.materias & estudiante_b.materias