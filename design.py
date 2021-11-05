from typing import Text
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class Login(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1

        self.window.add_widget(Image(source="./temp_vasco/vasco_fotos_2_printed.jpg"))
        #add widgets to window
        self.Llogin = Label(text = "Insira seu usuario:")
        self.user_text = TextInput(multiline = False)
        self.window.add_widget(self.Llogin)
        self.window.add_widget(self.user_text)

        self.Lkey = Label(text = "Insira sua senha:")
        self.key_text = TextInput(multiline = False)
        self.window.add_widget(self.Lkey)
        self.window.add_widget(self.key_text)

        self.Login_button = Button(text = "Logar")
        self.window.add_widget(self.Login_button)


        return self.window

class Search(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 3
        return self.window


if __name__ == "__main__":
    Login().run()