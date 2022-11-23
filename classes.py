

class Playlist:

    def __init__(self, canciones):
        self.canciones = canciones

    def anadir_cancion(self, canciones):
        self.canciones = canciones

    def buscar_canciones(self):
        return self.canciones

    def recuperar_canciones(self):
        return self.canciones



class Artista:
    def __init__(self, nombre, seudonimo, nacimiento, nacionalidad, sencillos):
        self.nombre = nombre
        self.seudonimo = seudonimo
        self.nacimiento = nacimiento
        self.nacionalidad = nacionalidad
        self.sencillos = sencillos

    def asignar_nombre(self, nombre):
        self.nombre = nombre
    def asignar_seudonimo(self, seudonimo):
        self.seudonimo = seudonimo
    def asignar_nacimiento(self, nacimiento):
        self.nacimiento = nacimiento
    def asignar_nacionalidad(self, nacionalidad):
        self.nacionalidad = nacionalidad
    def asignar_sencillos(self, sencillos):
        self.sencillos = sencillos
    def recuperar_nombre(self):
        return self.nombre
    def recuperar_seudonimo(self):
        return self.seudonimo
    def recuperar_nacimiento(self):
        return self.nacimiento
    def recuperar_nacionalidad(self):
        return self.nacionalidad
    def recuperar_sencillos(self):
        return self.sencillos
    def recuperar_datos(self):
        return self.nombre + "," + self.seudonimo + "," + self.nacimiento + "," + self.nacionalidad + "," + self.sencillos