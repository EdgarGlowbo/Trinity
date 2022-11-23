import os
from CancionFormWindow import Ui_MainWindow as Form
from DetallesWindow import Ui_MainWindow as Details
from MainWindow import Ui_MainWindow as Homepage
from PyQt5.QtWidgets import QApplication, QMainWindow

# Variable global que almacena las instancias de los géneros
generos = []

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
        self.ui.genComboBox.currentIndexChanged.connect(self.anadir_cancion_event)                                                       
             
        # Agrega al genComboBox los 4 géneros
        self.ui.genComboBox.addItems(['Electrónica', 'Jazz', 'Pop', 'Hip-Hop'])

    
    def limpiarForm(self):
        self.ui.tituloDeLaCancionLineEdit.clear()
        self.ui.artistaLineEdit.clear()
        self.ui.duracionSpinBox.setValue(0.0)
        self.ui.textEdit.clear()
        self.ui.tituloDeLaCancionLineEdit.setFocus()

    def anadir_cancion_event(self, index):
        if len(generos) > 0:            
            self.ui.addSongBtn.clicked.connect(generos[index].anadir_cancion)
            
    
    


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
            
    def anadir_cancion(self):
        try:
            # Guarda en variables info del form
            titulo = self.form.tituloDeLaCancionLineEdit.text()
            artista = self.form.artistaLineEdit.text()
            genero = self.form.genComboBox.currentText()
            subgenero = self.form.subComboBox.currentText()
            duracion = str(self.form.duracionSpinBox.value())
            letra = self.form.textEdit.toPlainText()
            # Crear instancia de Cancion
            cancion = Cancion(titulo, artista, genero, subgenero, duracion, letra)
            # Crea archivo con el título de la canción en la ruta especificada
            # Regresa la ruta donde se está ejecutando el código
            file_dir = os.path.dirname(os.path.realpath('__file__'))
            # Une la ruta con el titulo de la canción
            if titulo != '':
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
                self.genero.asignar_playlist()
                # Llama al método limpiarForm de la instancia self.form de CancionFormWindow
                window.form.limpiarForm()        
                self.form.statusbar.showMessage("Canción agregada exitosamente")

        except:
            self.form.statusbar.showMessage("Error al añadir la canción")


    def buscar_cancion(self, nombre):
        pass    

    def recuperar_canciones(self):
        return self.canciones


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

    

        