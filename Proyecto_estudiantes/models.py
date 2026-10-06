# Aquí guardamos los nombres de los campos que tiene un estudiante.
CAMPOS_ESTUDIANTE = (
    "nombre",
    "apellido",
    "email",
    "carnet",
)

# Esta clase representa a un estudiante.
class Estudiante:
    """MODELO: representa a un estudiante. Usa las cuatro colecciones."""

    # Esta función sirve para crear un estudiante con sus datos.
    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet

        # Aquí se guardan las notas de cada materia.
        # Se utiliza un diccionario que contiene listas de notas.
        # {"Matemática": [18, 19], "Inglés": [17]}
        self.notas = notas if notas else {}

        # Aquí se guardan las materias del estudiante.
        # Se utiliza un conjunto para evitar materias repetidas.
        self.materias = set(materias) if materias else set()

    # Esta función une el nombre y apellido del estudiante.
    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    # Esta función permite inscribir al estudiante en una materia.
    def inscribir_materia(self, materia):
        # add() agrega la materia y no permite duplicarla.
        self.materias.add(materia)

    # Esta función agrega una nota a una materia.
    def agregar_nota(self, materia, nota):
        self.inscribir_materia(materia)

        # Si la materia no existe, primero crea una lista.
        # Después agrega la nota a esa lista.
        self.notas.setdefault(materia, []).append(nota)

    # Esta función calcula el promedio de todas las notas.
    def obtener_promedio(self):
        # Aquí se crea una lista para guardar todas las notas.
        todas = []

        # Se recorren las notas de cada materia.
        for lista_notas in self.notas.values():
            todas.extend(lista_notas)

        # Si no hay notas, el promedio será 0.
        if not todas:
            return 0

        # Aquí se calcula el promedio y se dejan dos decimales.
        return round(sum(todas) / len(todas), 2)

    # Esta función busca las materias que tienen en común dos estudiantes.
    def materias_en_comun(self, otro_estudiante):
        # Se usa la intersección para encontrar las materias iguales.
        return self.materias & otro_estudiante.materias

    # Esta función convierte los datos del estudiante en un diccionario.
    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,

            # JSON no puede guardar un conjunto directamente.
            # Por eso las materias se convierten en una lista.
            "materias": sorted(self.materias),
        }

    # Esta función permite crear un estudiante usando los datos de un diccionario.
    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),
            materias=set(datos.get("materias", [])),
        )

    # Esta función indica cómo se mostrará el estudiante cuando se imprima.
    def __str__(self):
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"