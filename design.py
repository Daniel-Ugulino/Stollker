from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from insta_downnloader import insta_D
from PIL import Image 

# https://www.techwithtim.net/tutorials/kivy-tutorial/floatlayout/

class LoginScreen(Screen): 
    user = ObjectProperty(None)
    key = ObjectProperty(None)
    
    def Login(self):
        user = self.user.text
        key = self.key.text
        login = insta_D.Login(user,key)
        if (login==True):
            sm.current = "input"
        else:
            print(login)

class InputScreen(Screen):
    hashtag = ObjectProperty(None)
    date = ObjectProperty(None)
    qtd = ObjectProperty(None)

    def FileInput():
        pass

    pass

class ImamgesScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

sm = WindowManager()

class MyApp(MDApp):
      def build(self):
        kv = Builder.load_file("desing.kv")
               
        screens = [LoginScreen(name="login"),InputScreen(name="input"),ImamgesScreen(name="images")]
        for screen in screens:
            sm.add_widget(screen)

        sm.current = "login"

        return sm

if __name__ == "__main__":
    MyApp().run()