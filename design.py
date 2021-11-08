from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from insta_downnloader import insta_D

class MyGrid(Widget): 
    user = ObjectProperty(None)
    key = ObjectProperty(None)
    
    def Login(self):
        user = self.user.text
        key = self.key.text
        sla = insta_D.login(user,key)
        print(sla)
        return(sla)

    # def build(self):
    #     self.window = GridLayout()  
    #     self.window.cols = 1

    #     self.window.add_widget(Image(source="stollker logo.png"))
    #     self.Llogin = Label(text = "Insira seu usuario:")
    #     self.user_text = TextInput(multiline = False)
    #     self.window.add_widget(self.Llogin)
    #     self.window.add_widget(self.user_text)

    #     self.Lkey = Label(text = "Insira sua senha:")
    #     self.key_text = TextInput(multiline = False)
    #     self.window.add_widget(self.Lkey)
    #     self.window.add_widget(self.key_text)

    #     self.Login_button = Button(text = "Logar")
    #     self.Login_button.bind(on_press = self.Login)

    #     self.window.add_widget(self.Login_button)
        
    #     return self.window

class MyApp(App):
    def build(self):
        return MyGrid()
        # self.window.add_widget(Image(source="stollker logo.png"))
        # return self.window


if __name__ == "__main__":
    MyApp().run()