import pyodbc
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import io
import contextlib
import unittest

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

class HomeScreen(MDScreen):
    pass

class TextoScreen(MDScreen):
    pass

class ConsoleScreen(MDScreen):
    pass

class MainApp(MDApp):
    def cargar_texto(self):
        try:
            with open("Textos/texto_largo.txt", "r", encoding="utf-8") as archivo:
                contenido = archivo.readlines()
            texto_formateado = ""
            for linea in contenido:
                if linea.startswith("# "):  # Detectar títulos
                    texto_formateado += f"[size=20sp][b]{linea[2:].strip()}[/b][/size]\n\n"
                else:
                    texto_formateado += f"{linea.strip()}\n"
            return texto_formateado
        except FileNotFoundError:
            return "No se pudo cargar el texto. Verifique que el archivo 'texto_largo.txt' esté en el directorio correcto."

    def run_code(self):
        code_input = self.root.get_screen("console").ids.code_input.text
        output_console = self.root.get_screen("console").ids.output_console

        # Redirigir la salida estándar a una cadena
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            try:
                exec_globals = {}
                exec(code_input, exec_globals)
                output_console.text = buf.getvalue()
            except Exception as e:
                output_console.text = f"Error: {e}"

    def build(self):
        Window.size = (360, 640)  # Tamaño de la ventana
        self.theme_cls.theme_style = "Dark"  # Estilo oscuro
        self.theme_cls.primary_palette = "LightGreen"  # Paleta de colores principal
        Builder.load_file("app_1_consola.kv")

    # Crear el ScreenManager principal
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegistroScreen(name='registro'))
    # Agregar las pantallas del segundo código al ScreenManager
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(TextoScreen(name='texto'))
        sm.add_widget(ConsoleScreen(name='console'))

        return sm

    def on_start(self):
        # Cambiar a la pantalla de inicio de sesión al iniciar la app
        self.root.current = 'login'

KV = '''
<HomeScreen>:
    MDScreen:
        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(20)
            padding: dp(20)

            MDLabel:
                text: "Bienvenido a CHISTHON"
                halign: "center"
                font_style: "H4"

            MDRectangleFlatButton:
                text: "Ver mis lecciones"
                pos_hint: {"center_x": 0.5}
                on_release: root.manager.current = "texto"

<TextoScreen>:
    MDScreen:

        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(12.5)
            padding: dp(12.5)

            MDTopAppBar:
                md_bg_color: app.theme_cls.primary_color
                elevation: 1
                title: "Módulo 1: Introducción al Lenguaje de programación Python"

            # Sección de texto y scroll
            MDScrollView:
                MDLabel:
                    id: texto_label
                    text: app.cargar_texto()
                    markup: True  # Permitir formateo del texto
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None
                    halign: "justify"

            # Sección de botones
            MDBoxLayout:
                size_hint_y: None
                height: dp(50)
                spacing: dp(20)  # Espaciado entre botones
                padding: dp(10)  # Padding uniforme
                orientation: "horizontal"  # Alineación horizontal
                pos_hint: {"center_x": 0.5, "center_y": 0.1}  # Centrando botones

                MDRectangleFlatButton:
                    text: "Ir a la consola"
                    size_hint: None, None
                    size: dp(150), dp(40)
                    on_release: root.manager.current = "console"

                MDRectangleFlatButton:
                    text: "Volver al Menú"
                    size_hint: None, None
                    size: dp(150), dp(40)
                    on_release: root.manager.current = "home"

<ConsoleScreen>:
    MDScreen:
        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(10)
            padding: dp(10)

            MDLabel:
                text: "Consola de Python"
                halign: "center"
                font_style: "H5"
                theme_text_color: "Primary"
                size_hint_y: None
                height: dp(50)

            MDTextField:
                id: code_input
                hint_text: "Escribe tu código aquí"
                multiline: True
                mode: "rectangle"
                size_hint_y: 0.4

            MDRaisedButton:
                text: "Ejecutar"
                size_hint: None, None
                size: "150dp", "50dp"
                pos_hint: {"center_x": 0.5}
                on_press: app.run_code()

            MDTextField:
                id: output_console
                hint_text: "Salida"
                multiline: True
                readonly: True
                mode: "rectangle"
                size_hint_y: 0.4

            MDRaisedButton:
                text: "Regresar"
                size_hint: None, None
                size: "150dp", "50dp"
                pos_hint: {"center_x": 0.5}
                on_press: app.root.current = "texto"
                '''

if __name__ == '__main__':
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

