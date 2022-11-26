import os
from CancionFormWindow import Ui_MainWindow as Form
from DetallesWindow import Ui_MainWindow as Details
from ArtistaFormWindow import Ui_MainWindow as ArtistaForm
from MainWindow import Ui_MainWindow as Homepage
from PyQt5.QtWidgets import QApplication, QMainWindow

# Variable global que almacena las instancias de los géneros
generos = []

class ArtistaWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ArtistaWindow, self).__init__(parent)
        self.ui = ArtistaForm()
        # self.form = CancionFormWindow().ui
        self.ui.setupUi(self)
         # Agrega al genComboBox los 4 géneros
        self.ui.genComboBox.addItems(['Electrónica', 'Jazz', 'Pop', 'Hip-Hop'])
        self.ui.clearArtistaFormBtn.clicked.connect(self.limpiarForm)
        self.ui.addArtistaBtn.clicked.connect(self.anadir_artista)
        
    def anadir_artista(self):
        try:        
            # Guarda en variables info del form
            nombre = self.ui.nombreArtistaLineEdit.text()
            seudonimo = self.ui.seudonimoLineEdit.text()
            nacionalidad = self.ui.nacionalidadLineEdit.text()
            nacimiento = self.ui.nacimientoLineEdit.text()
            genero = self.ui.genComboBox.currentText()
            sencillos = self.ui.sencillosLineEdit.text()

            if len(nombre) == 0 or len(seudonimo) == 0 or len(nacionalidad) == 0 or len(nacimiento) == 0 or len(sencillos) == 0:
                raise Exception("Debes llenar todos los campos")
            # Crear instancia de Artista
            artista = Artista(nombre, seudonimo, nacimiento, nacionalidad, genero, sencillos)
            # Crea archivo con el seudonimo en la ruta especificada
            # Regresa la ruta donde se está ejecutando el código
            file_dir = os.path.dirname(os.path.realpath('__file__'))
            # Une la ruta
            file_name = os.path.join(file_dir, f"artistas\{seudonimo}")            
            archivo = open(file_name, 'w')
            archivo.write(artista.recuperar_datos())
            archivo.close()
            # Añade línea al archivo Artistas
            file_name_artista = os.path.join(file_dir, f"artistas\Artistas") 
            artistaArchivo = open(file_name_artista, 'a')
            artistaArchivo.write(artista.seudonimo + "\n")                       
            artistaArchivo.close()            
            # self.form.artistaComboBox.clear()                                    
            # self.form.artistaComboBox.addItems(lineas)
            self.limpiarForm()        
            self.ui.statusbar.showMessage("Artista agregado exitosamente")
        except:
            self.ui.statusbar.showMessage("Error al añadir el artista")

    def limpiarForm(self):
        self.ui.nombreArtistaLineEdit.clear()
        self.ui.seudonimoLineEdit.clear()
        self.ui.nacionalidadLineEdit.clear()
        self.ui.nacimientoLineEdit.clear()
        self.ui.sencillosLineEdit.clear()        
        self.ui.nombreArtistaLineEdit.setFocus()

class DetallesWindow(QMainWindow):
    def __init__(self, parent=None):
        super(DetallesWindow, self).__init__(parent)
        self.ui = Details()
        self.ui.setupUi(self)


class CancionFormWindow(QMainWindow):
    def __init__(self, parent=None):
        super(CancionFormWindow, self).__init__(parent)
        self.ui = Form()
        self.ui.setupUi(self)                                                                   
        self.ui.addSongBtn.clicked.connect(self.anadir_cancion)        
        # Agrega al genComboBox los 4 géneros
        self.ui.genComboBox.addItems(['Electrónica', 'Jazz', 'Pop', 'Hip-Hop'])
        self.artista = ArtistaWindow(self)
        self.ui.addArtistBtn.clicked.connect(self.openArtistaWindow)
        self.asignar_artistas()

    def anadir_cancion(self):
        try:        
            # Guarda en variables info del form
            titulo = self.ui.tituloDeLaCancionLineEdit.text()
            artista = self.ui.artistaComboBox.currentText()
            genero = self.ui.genComboBox.currentText()
            subgenero = self.ui.subComboBox.currentText()
            duracion = str(self.ui.duracionSpinBox.value())
            letra = self.ui.textEdit.toPlainText()

            if len(titulo) == 0 or len(artista) == 0 or len(letra) == 0 or genero == None:
                raise Exception("Debes llenar todos los campos")
            # Crear instancia de Cancion
            cancion = Cancion(titulo, artista, genero, subgenero, duracion, letra)
            # Crea archivo con el título de la canción en la ruta especificada
            # Regresa la ruta donde se está ejecutando el código
            file_dir = os.path.dirname(os.path.realpath('__file__'))
            # Une la ruta con el titulo de la canción
            
            file_name = os.path.join(file_dir, f"canciones\{titulo}")            
            archivo = open(file_name, 'w')
            archivo.write(cancion.recuperar_datos())
            archivo.close()
            # Añade línea al archivo del género elegido
            file_name_playlist = os.path.join(file_dir, f"playlists\{genero}") 
            playlistArchivo = open(file_name_playlist, 'a')
            playlistArchivo.write(cancion.nombre + " - " + cancion.artista + "\n")            
            playlistArchivo.close()
            # Actualiza las listas en MainWindow
            generos[self.ui.genComboBox.currentIndex()].genero.asignar_playlist()        
            self.limpiarForm()        
            self.ui.statusbar.showMessage("Canción agregada exitosamente")

        except:
            self.ui.statusbar.showMessage("Error al añadir la canción")

    def asignar_artistas(self):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        # Añade línea al archivo Artistas
        file_name_artista = os.path.join(file_dir, f"artistas\Artistas")
        artistaArchivo = open(file_name_artista, 'r')
        lineas = artistaArchivo.readlines()
        artistaArchivo.close()            
        self.ui.artistaComboBox.clear()                                    
        self.ui.artistaComboBox.addItems(lineas)
    
    def limpiarForm(self):
        self.ui.tituloDeLaCancionLineEdit.clear()        
        self.ui.duracionSpinBox.setValue(0.0)
        self.ui.textEdit.clear()
        self.ui.tituloDeLaCancionLineEdit.setFocus()
            
    def openArtistaWindow(self):
        self.artista.show()
    
class VentanaPrincipal(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaPrincipal, self).__init__(parent)
        self.ui = Homepage()
        self.form = CancionFormWindow(self)
        self.details = DetallesWindow(self)
        self.ui.setupUi(self)

        # Abre CancionFormWindow cuando se clickea el botón agregar
        self.ui.addSongBtn.clicked.connect(self.openCancionFormWindow)
        # Abre DetallesWindow cuando se clickea el botón Ver detalles
        self.ui.detailsBtn.clicked.connect(self.openDetallesWindow)
        self.ui.searchBtn.clicked.connect(lambda: self.buscar_cancion(self.ui.searchBar.text()))
        


    def buscar_cancion(self, nombre):
        try:
            if len(nombre) == 0:
                raise Exception("Debes colocar al menos un caracter")
            file_dir = os.path.dirname(os.path.realpath('__file__'))            
            playlist_dir = os.path.join(file_dir, "playlists")
            playlists = os.listdir(playlist_dir)
            # Itera por cada archivo en la carpeta playlists
            for playlist in playlists:
                playlist_file = os.path.join(file_dir, f"playlists\{playlist}")
                archivo = open(playlist_file, 'r')
                lineas = archivo.readlines()
                for i in range(0, len(lineas)):
                    if nombre in lineas[i]:
                        self.ui.electronicList.clearSelection()
                        self.ui.hiphopList.clearSelection()
                        self.ui.jazzList.clearSelection()
                        self.ui.popList.clearSelection()                                                                
                        if playlist == "Electrónica":
                            self.ui.electronicList.setCurrentRow(i)                            
                        elif playlist == "Hip-Hop":
                            self.ui.hiphopList.setCurrentRow(i)                            
                        elif playlist == "Jazz":
                            self.ui.jazzList.setCurrentRow(i)                            
                        elif playlist == "Pop":
                            self.ui.popList.setCurrentRow(i)                            
                        break
            self.ui.searchBar.clear()
            self.ui.statusbar.showMessage('Canción encontrada exitosamente')  
        except:
            self.ui.statusbar.showMessage('Canción no encontrada')              

    def openCancionFormWindow(self):
        self.form.show()

    def openDetallesWindow(self):
        self.details.show()

    
class Cancion:
    def __init__(self,  nombre, artista, genero, subgenero, duracion,letra):
        self.nombre = nombre
        self.artista = artista
        self.genero = genero
        self.subgenero = subgenero
        self.duracion = duracion        
        self.letra = letra

    def asignar_duracion(self, duracion):
        self.duracion = duracion

    def asignar_artista(self, artista):
        self.artista = artista

    def asignar_nombre(self, nombre):
        self.nombre = nombre

    def asignar_genero(self, genero):
        self.genero = genero

    def asignar_subgenero(self, subgenero):
        self.subgenero = subgenero

    def asignar_letra(self, letra):
        self.letra = letra

    def recuperar_duracion(self):
        return self.duracion

    def recuperar_artista(self):
        return self.artista

    def recuperar_nombre(self):
        return self.nombre

    def recuperar_genero(self):
        return self.genero

    def recuperar_subgenero(self):
        return self.subgenero

    def recuperar_letra(self):
        return self.letra

    def recuperar_datos(self):
        return self.nombre + "$" + self.artista + "$" + self.genero + "$" + self.subgenero + "$" + self.duracion + "$" + self.letra


class Genero:   
    def __init__(self, nombre, subgeneros, window):        
        self.nombre = nombre
        self.subgeneros = subgeneros       
        self.ui = window.ui
        self.form = window.form.ui
        self.asignar_playlist()
        if len(generos) > 0:
            self.asignar_subgeneros(0)

        
        # Hace que los items de subgenComboBox cambien cuando cambia el index de genComboBox
        self.form.genComboBox.currentIndexChanged.connect(self.asignar_subgeneros)         

    def asignar_playlist(self):
        # Agrega las líneas del archivo correspondiente a la lista como items
        # Regresa la ruta donde se está ejecutando el código
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        # Une la ruta con el nombre del género (mismo que el archivo)       
        file_name = os.path.join(file_dir, f"playlists\{self.nombre}")            
        archivo = open(file_name, 'r')
        lineas = archivo.readlines()
        # Contrala a qué lista se añadirá el item
        if self.nombre == "Electrónica":
            self.ui.electronicList.clear()
            self.ui.electronicList.addItems(lineas)
        elif self.nombre == "Jazz":
            self.ui.jazzList.clear()
            self.ui.jazzList.addItems(lineas)
        elif self.nombre == "Pop":
            self.ui.popList.clear()
            self.ui.popList.addItems(lineas)
        elif self.nombre == "Hip-Hop":
            self.ui.hiphopList.clear()
            self.ui.hiphopList.addItems(lineas)
        archivo.close()
    
    def asignar_subgeneros(self, index):
        self.form.subComboBox.clear()
        self.form.subComboBox.addItems(generos[index].genero.subgeneros)


class Subgenero(Genero):    
    def __init__(self, nombre, playlist, subgeneros, historia):
        super().__init__(nombre, playlist, subgeneros)
        self.historia = historia

    def asignar_historia(self, historia):
        self.historia = historia

    def recuperar_historia(self):
        return self.historia

    def recuperar_datos(self):
        return self.historia + "," + self.nombre + "," + self.playlist + "," + self.subgeneros + ","

class Playlist:
    def __init__(self, window, genero):                     
        self.form = window.form.ui
        self.genero = genero          

    def recuperar_canciones(self):
        return self.canciones


class Artista:
    def __init__(self, nombre, seudonimo, nacimiento, nacionalidad, genero, sencillos):
        self.nombre = nombre
        self.seudonimo = seudonimo
        self.nacimiento = nacimiento
        self.genero = genero
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
        return self.nombre + "$" + self.seudonimo + "$" + self.nacimiento + "$" + self.nacionalidad + "$" + self.sencillos + "$" + self.genero


# main method
if __name__ == '__main__':    

    # Ejecuta la ventana
    import sys    
    app = QApplication(sys.argv)      
    window = VentanaPrincipal()    
    window.show()
    # Agrega las instancias a la lista géneros
    generos.append(Playlist(window, Genero('Electrónica', ['Tecno', 'House'], window)))
    generos.append(Playlist(window, Genero('Jazz', ['R&B'], window)))
    generos.append(Playlist(window, Genero('Pop', ['Pop latino', 'Country pop'], window)))
    generos.append(Playlist(window, Genero('Hip-Hop', ['Trap'], window)))
    
    sys.exit(app.exec())