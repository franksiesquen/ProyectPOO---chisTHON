from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.snackbar import Snackbar
import sys
import io
import time
import os
import unittest
import pyodbc
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# Clase para la pantalla de inicio de sesión
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Título
        titulo = Label(text="Ingresar a chisTHON", font_size=24, color=(0.2, 0.5, 0.7, 1), bold = True)
        layout.add_widget(titulo)

        # Etiqueta y campo de texto para el correo electrónico
        email_label = Label(text="Correo Electrónico:", color=(1, 1, 1), font_size = 16)
        self.email_input = TextInput(multiline=False, foreground_color=(0, 0, 0, 1), font_size = 16, size_hint_y = None, height = 40)
        layout.add_widget(email_label)
        layout.add_widget(self.email_input)

        # Botón de inicio de sesión
        login_button = Button(text="Ingresar", size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5}, background_color=(0.2, 0.5, 0.7, 1), font_size = 18)
        login_button.bind(on_press=self.iniciar_sesion)
        layout.add_widget(login_button)

        # Botón para ir a la pantalla de registro
        registrar_button = Button(text="¿No tienes una cuenta? Regístrate", size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5}, background_color=(0.7, 0.2, 0.5, 1), font_size = 14)
        registrar_button.bind(on_press=self.ir_a_registro)
        layout.add_widget(registrar_button)

        self.add_widget(layout)

    def iniciar_sesion(self, instance):
        email = self.email_input.text

        conn_str = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=grupo6poo.database.windows.net;"
            "Database=chiston;"
            "UID=adminchiston;"
            "PWD=Chiston2024;"
        )

        try:
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM dbo.Usuarios WHERE CorreoElectronico = ?", (email,))
                user = cursor.fetchone()
                if user:
                    self.parent.current = 'home'
                else:
                    self.mostrar_popup("Error", "Correo electrónico no registrado. Por favor, regístrate.")
        except Exception as e:
            self.mostrar_popup("Error", str(e))

    def ir_a_registro(self, instance):
        self.parent.current = 'registro'

    def mostrar_popup(self, titulo, mensaje):
        popup = Popup(title=titulo, content=Label(text=mensaje, color=(0, 0, 0, 1)), size_hint=(0.6, 0.4))
        popup.open()

# Clase para la pantalla de registro
class RegistroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Título
        titulo = Label(text="¡Bienvenido a chisTHON!", font_size=20, color=(0.2, 0.5, 0.7, 1))
        layout.add_widget(titulo)

        # Etiqueta y campo de texto para el nombre de usuario
        usuario_label = Label(text="Nombre de Usuario:", color=(1, 1, 1))
        self.usuario_input = TextInput(multiline=False, foreground_color=(0, 0, 0, 1), font_size = 16, size_hint_y = None, height = 40)
        layout.add_widget(usuario_label)
        layout.add_widget(self.usuario_input)

        # Etiqueta y campo de texto para el correo electrónico
        email_label = Label(text="Correo Electrónico:", color=(1, 1, 1))
        self.email_input = TextInput(multiline=False, foreground_color=(0, 0, 0, 1), font_size = 16, size_hint_y = None, height = 40)
        layout.add_widget(email_label)
        layout.add_widget(self.email_input)

        # Botón de registro
        registrar_button = Button(text="Registrar", size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5}, background_color=(0.2, 0.5, 0.7, 1))
        registrar_button.bind(on_press=self.registrar)
        layout.add_widget(registrar_button)

        self.add_widget(layout)

    def registrar(self, instance):
        username = self.usuario_input.text
        email = self.email_input.text

        conn_str = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=grupo6poo.database.windows.net;"
            "Database=chiston;"
            "UID=adminchiston;"
            "PWD=Chiston2024;"
        )

        try:
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM dbo.Usuarios WHERE CorreoElectronico = ?", (email,))
                existing_user = cursor.fetchone()
                if existing_user:
                    self.mostrar_popup("Error", "Este correo electrónico ya está registrado.")
                else:
                    cursor.execute("INSERT INTO dbo.Usuarios (NombreUsuario, CorreoElectronico) VALUES (?, ?)", (username, email))
                    conn.commit()
                    self.mostrar_popup("Registro exitoso", "Usuario registrado correctamente.")
                    self.parent.current = 'home'
        except Exception as e:
            self.mostrar_popup("Error", str(e))

    def mostrar_popup(self, titulo, mensaje):
        popup = Popup(title=titulo, content=Label(text=mensaje, color=(0, 0, 0, 1)), size_hint=(0.6, 0.4))
        popup.open()

# Pantallas que usaremos para pinteractuar con la app

# Se define la clase para la pantalla de bienvenida
class HomeScreen(MDScreen):
    pass

# Se define la clase de la pantalla para el menu
class LeccionesScreen(MDScreen):
    pass

# Se define la clase para la pantalla que contendrá la información para el módulo 1
class Modulo1Screen(MDScreen):
    pass

# Se define la clase para la pantalla que contendrá la información para el módulo 2
class Modulo2Screen(MDScreen):
    pass

# Se define la clase para la pantalla que contendrá la información para el módulo 3
class Modulo3Screen(MDScreen):
    pass

# Aqui se define la clase para la pantalla en donde va a aparecer la consola
class ConsoleScreen(MDScreen):
    pass

class Test1Screen(MDScreen):
    pass

class ResultadosScreen(MDScreen):
    pass

class MainApp(MDApp):

    # Se define el método principal "build" donde construiremos la bases de nuestra app, definiendo las pantallas a usar,
    # configurando la estética de nuestro ventana, conectando con archivos .kv entre otros
    def build(self):
        # Se configura la estética de la ventana
        Window.size = (360, 640)  # Tamaño de la ventana
        self.theme_cls.theme_style = "Dark"  # Estilo oscuro
        self.theme_cls.primary_palette = "LightGreen"  # Escogemos una paleta de colores que querramos, en este caso verde

        # Importante: en esta línea se usa el método 'Builder' para conectar manualmente con el archivo .kv
        # en donde configuraremos todos los widgets a usar
        Builder.load_file("app_1_consola.kv")
        Builder.load_file("app_2.kv")
        Builder.load_file("test1.kv")

        sm = ScreenManager()
        # En esta parte se les da a cada pantalla definida previamente un nombre que se usará para interactuar
        # fácilmente en el archivo .kv
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegistroScreen(name='registro'))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(LeccionesScreen(name="lecciones"))
        sm.add_widget(Modulo1Screen(name="modulo1"))
        sm.add_widget(Modulo2Screen(name="modulo2"))
        sm.add_widget(Modulo3Screen(name="modulo3"))
        sm.add_widget(ConsoleScreen(name="console"))
        sm.add_widget(Test1Screen(name="test1"))
        sm.add_widget(ResultadosScreen(name="results"))
        return sm

    # Se define el método que nos ayudará a abrir el texto que contiene la información del primer módulo
    def cargar_texto_modulo1(self):
        # Se usa un bloque try-except para ver si el archivo .txt es correcto o no
        try:
            with open("Textos/teoria_modulo1.txt", "r", encoding="utf-8") as archivo:
                contenido = archivo.readlines()
            texto_formateado = ""
            # Si no hay problema, a todos los que tengan este formato de texto: '# Título' se les modifica el tipo de letra
            # con tal de que sean los subtítulos
            for linea in contenido:
                if linea.startswith("# "):  # Detectar títulos
                    texto_formateado += f"[size=20sp][b]{linea[2:].strip()}[/b][/size]\n\n"
                else:
                    texto_formateado += f"{linea.strip()}\n"
            return texto_formateado
        # Si hay algo mal con el archivo, se lanza el siguiente mensaje
        except FileNotFoundError:
            return "No se pudo cargar el texto. Verifique que el archivo 'teoria_modulo1.txt' esté en el directorio correcto."

    def cargar_texto_modulo2(self):
        # Se usa un bloque try-except para ver si el archivo .txt es correcto o no
        try:
            with open("Textos/teoria_modulo2.txt", "r", encoding="utf-8") as archivo:
                contenido = archivo.readlines()
            texto_formateado = ""
            # Si no hay problema, a todos los que tengan este formato de texto: '# Título' se les modifica el tipo de letra
            # con tal de que sean los subtítulos
            for linea in contenido:
                if linea.startswith("# "):  # Detectar títulos
                    texto_formateado += f"[size=20sp][b]{linea[2:].strip()}[/b][/size]\n\n"

                else:
                    texto_formateado += f"{linea.strip()}\n"
            return texto_formateado
        # Si hay algo mal con el archivo, se lanza el siguiente mensaje
        except FileNotFoundError:
            return "No se pudo cargar el texto. Verifique que el archivo 'teoria_modulo2.txt' esté en el directorio correcto."

    def cargar_texto_modulo3(self):
        # Se usa un bloque try-except para ver si el archivo .txt es correcto o no
        try:
            with open("Textos/teoria_modulo3.txt", "r", encoding="utf-8") as archivo:
                contenido = archivo.readlines()
            texto_formateado = ""
            # Si no hay problema, a todos los que tengan este formato de texto: '# Título' se les modifica el tipo de letra
            # con tal de que sean los subtítulos
            for linea in contenido:
                if linea.startswith("# "):  # Detectar títulos
                    texto_formateado += f"[size=20sp][b]{linea[2:].strip()}[/b][/size]\n\n"

                else:
                    texto_formateado += f"{linea.strip()}\n"
            return texto_formateado
        # Si hay algo mal con el archivo, se lanza el siguiente mensaje
        except FileNotFoundError:
            return "No se pudo cargar el texto. Verifique que el archivo 'teoria_modulo3.txt' esté en el directorio correcto."

    # En esta parte se encuentran los cuatro métodos que usaremos para medir el tiempo en la que hemos estado en la app

    def on_start(self):
        self.start_time = time.time()  # Registrar tiempo de inicio
        self.total_usage_time = self.load_usage_time()  # Cargar tiempo acumulado

    def on_stop(self):
        end_time = time.time()  # Registrar tiempo de salida
        session_time = end_time - self.start_time  # Calcular tiempo de la sesión
        self.total_usage_time += session_time
        self.save_usage_time()  # Guardar tiempo acumulado
        print(f"Tiempo total de uso: {self.total_usage_time:.2f} segundos")

    def load_usage_time(self):
        if os.path.exists("usage_time.txt"):
            with open("usage_time.txt", "r") as file:
                return float(file.read())
        return 0

    def save_usage_time(self):
        with open("usage_time.txt", "w") as file:
            file.write(str(self.total_usage_time))


    def go_to_console(self):
        # Guardamos la pantalla actual antes de ir a la consola
        self.previous_screen = self.root.current
        self.root.current = "console"

    def go_back(self):
        # Regresamos a la pantalla almacenada en 'previous_screen'
        if self.previous_screen:
            self.root.current = self.previous_screen
            self.previous_screen = None  # Limpiamos el valor para evitar un regreso inesperado


    # Se define el método que ayudará a la pantalla que corresponde a la consola, que funcione
    # como si fuera una terminal interactiva
    def run_code(self):
        # Se codifica las entradas y salidas del código que usaremos para nuestra consola
        # Recordar que el nombre de la pantalla de la consola, en archivo .kv lo hemos determinado como "console"
        code_input = self.root.get_screen("console").ids.code_input
        output_console = self.root.get_screen("console").ids.output_console

        # Redirigir salida estándar
        code = code_input.text
        output = io.StringIO()
        sys.stdout = output
        sys.stderr = output

        # Se usa un bloque try-except para evaluar si el código ingresado es correcto y ver que
        # no levante excepción
        try:
            exec(code, {})  # Ejecutar el código de manera segura
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sys.stdout = sys.__stdout__  # Restaurar salida estándar
            sys.stderr = sys.__stderr__

        # Mostrar el resultado en el TextField de salida
        output_console.text = output.getvalue()

    # Se define las respuestas del test

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Inicializa las respuestas con un valor vacío
        self.answers = {f"q{i}": "" for i in range(1, 11)}
        # Respuestas correctas para cada pregunta
        self.correct_answers = {
            "q1": "float", "q2": "x = 5", "q3": "len()", "q4": "def",
            "q5": "dict = {}", "q6": "append()", "q7": "8", "q8": "==",
            "q9": "input()", "q10": "# Esto es un comentario"
        }

    # Aquí se evalua las opciones del test

    def set_answer(self, question, answer, active):
        """Almacena las respuestas seleccionadas por el usuario."""
        if active:  # Solo se almacena cuando el checkbox se activa
            self.answers[question] = answer
        else:  # Si se desmarca, eliminar la respuesta seleccionada
            if self.answers.get(question) == answer:
                self.answers[question] = ""

    def evaluate_answers(self):
        """
        Evalúa las respuestas seleccionadas, calcula el progreso y muestra los resultados.
        """
        # Comparar respuestas seleccionadas con las correctas
        wrong_questions = [
            f"Pregunta {i + 1}: Respuesta incorrecta"
            for i, (q, ans) in enumerate(self.answers.items())
            if ans != self.correct_answers[q]
        ]
        correct_count = sum(1 for q, ans in self.answers.items() if ans == self.correct_answers[q])

        # Calcular porcentaje de progreso
        progress = (correct_count / len(self.correct_answers)) * 100

        # Actualizar la pantalla de resultados
        results_screen = self.root.get_screen("results")
        results_screen.ids.results_label.text = "\n".join(wrong_questions) or "¡Todas las respuestas son correctas!"
        results_screen.ids.progress_bar.value = progress

        # Cambiar a la pantalla de resultados
        self.root.current = "results"

    def clear_checkboxes(self):
        """Desmarca todos los checkboxes en la pantalla de quiz."""
        quiz_screen = self.root.get_screen("test1")  # Obtiene la pantalla de quiz
        for widget in quiz_screen.walk():  # Recorre todos los widgets de la pantalla
            if isinstance(widget, MDCheckbox):  # Si el widget es un MDCheckbox
                widget.active = False  # Desmarcarlo

    def reset_quiz(self):
        """Reinicia el quiz y vuelve a la pantalla inicial."""
        self.answers = {q: "" for q in self.answers}  # Limpiar respuestas
        self.clear_checkboxes()  # Desmarcar visualmente los checkboxes
        self.root.current = "test1"  # Cambiar a la pantalla de quiz
        Snackbar(text="Quiz reiniciado").open()

if __name__ == "__main__":
    MainApp().run()

    #Pruebas automatizadas
class TestLoginScreen(unittest.TestCase):
    def setUp(self):
        self.app = MDApp.get_running_app()
        self.login_screen = LoginScreen(name='login')
        self.app.root = ScreenManager()
        self.app.root.add_widget(self.login_screen)

    def test_iniciar_sesion_exito(self):
        self.login_screen.email_input.text = "usuario@ejemplo.com"
        self.login_screen.iniciar_sesion(None)
        self.assertEqual(self.app.root.current, 'home')

    def test_iniciar_sesion_error(self):
        self.login_screen.email_input.text = "no_registrado@ejemplo.com"
        self.login_screen.iniciar_sesion(None)
        self.assertNotEqual(self.app.root.current, 'home')

class TestRegistroScreen(unittest.TestCase):
    def setUp(self):
        self.app = MDApp.get_running_app()
        self.registro_screen = RegistroScreen(name='registro')
        self.app.root = ScreenManager()
        self.app.root.add_widget(self.registro_screen)

    def test_registrar_exito(self):
        self.registro_screen.usuario_input.text = "nuevo_usuario"
        self.registro_screen.email_input.text = "nuevo@ejemplo.com"
        self.registro_screen.registrar(None)
        self.assertEqual(self.app.root.current, 'home')

    def test_registrar_error(self):
        self.registro_screen.usuario_input.text = "usuario_existente"
        self.registro_screen.email_input.text = "existente@ejemplo.com"
        self.registro_screen.registrar(None)
        self.assertNotEqual(self.app.root.current, 'home')

class TestMainApp(unittest.TestCase):
    def setUp(self):
        self.app = MainApp()
        self.app.build()

    def test_cargar_texto_exito(self):
        resultado = self.app.cargar_texto()
        self.assertNotEqual(resultado, "No se pudo cargar el texto. Verifique que el archivo 'texto_largo.txt' esté en el directorio correcto.")

    def test_cargar_texto_error(self):
        self.app.cargar_texto = lambda: "No se pudo cargar el texto. Verifique que el archivo 'texto_largo.txt' esté en el directorio correcto."
        resultado = self.app.cargar_texto()
        self.assertEqual(resultado, "No se pudo cargar el texto. Verifique que el archivo 'texto_largo.txt' esté en el directorio correcto.")

class TestConsoleScreen(unittest.TestCase):
    def setUp(self):
        self.app = MDApp.get_running_app()
        self.console_screen = ConsoleScreen(name='console')
        self.app.root = ScreenManager()
        self.app.root.add_widget(self.console_screen)

    def test_run_code_exito(self):
        self.console_screen.ids.code_input.text = "print('Hola Mundo')"
        self.app.run_code()
        self.assertIn("Hola Mundo", self.console_screen.ids.output_console.text)

    def test_run_code_error(self):
        self.console_screen.ids.code_input.text = "print(1/0)"
        self.app.run_code()
        self.assertIn("Error", self.console_screen.ids.output_console.text)

if __name__ == '__main__':
    unittest.main()
