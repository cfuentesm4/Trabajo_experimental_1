# Importamos json porque necesitamos trabajar con archivos JSON.
import json

# Importamos os para trabajar con carpetas y archivos.
import os


# Esta clase se encarga de leer y guardar información en un archivo JSON.
class GestorJSON:

    # Esta función recibe la ubicación del archivo JSON.
    def __init__(self, ruta):
        self.ruta = ruta

    # Esta función lee la información del archivo.
    def leer(self):
        # Si el archivo no existe, devolvemos una lista vacía.
        if not os.path.exists(self.ruta):
            return []

        # Abrimos el archivo para leerlo.
        with open(self.ruta, "r", encoding="utf-8") as archivo:
            try:
                # Convertimos el contenido JSON a datos de Python.
                return json.load(archivo)
            except json.JSONDecodeError:
                # Si el archivo está vacío o tiene un error,
                # devolvemos una lista vacía.
                return []

    # Esta función guarda los datos en el archivo JSON.
    def guardar(self, datos):
        try:
            # Creamos la carpeta si todavía no existe.
            carpeta = os.path.dirname(self.ruta)

            if carpeta:
                os.makedirs(carpeta, exist_ok=True)

            # Abrimos el archivo para escribir.
            with open(self.ruta, "w", encoding="utf-8") as archivo:

                # Convertimos los datos a formato JSON.
                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=4
                )

            # Indicamos que el guardado fue correcto.
            return True

        except Exception:
            # Si ocurre algún error, devolvemos False.
            return False