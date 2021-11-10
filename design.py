from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from insta_downnloader import insta_D

# https://www.techwithtim.net/tutorials/kivy-tutorial/floatlayout/



class LoginScreen(Screen): 
    user = ObjectProperty(None)
    key = ObjectProperty(None)
    
    def Login(self):
        user = self.user.text
        key = self.key.text
        sla = insta_D.Login(user,key)
        print(sla)
        return(sla)

class MenuScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "My Material Application"
        super().__init__(**kwargs)

if __name__ == "__main__":
    MyApp().run()