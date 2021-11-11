from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivymd.uix.picker import MDDatePicker
from insta_downnloader import insta_D
from PIL import Image
import easygui

# https://www.techwithtim.net/tutorials/kivy-tutorial/floatlayout/


class LoginScreen(Screen):
    user = ObjectProperty(None)
    key = ObjectProperty(None)

    def Login(self):
        user = self.user.text
        key = self.key.text
        login = insta_D.Login(user, key)
        if (login == True):
            sm.current = "input"
        else:
            print(login)


class InputScreen(Screen):
    hashtag = ObjectProperty(None)
    date = ObjectProperty(None)
    qtd = ObjectProperty(None)
    file_text = ObjectProperty(None)

    def Back(self):
        sm.current = "login"

    def show_time_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.open()      

    def ImagesPicker(self):
        hashtag = self.hashtag.text
        qtd = self.qtd.text
        get_images = insta_D.ByHashtag(str(hashtag), int(qtd))
        if(get_images == True):
            sm.current = "images"
        else:
            print(get_images)

    def FileInput(self):
        file = easygui.fileopenbox()
        try:
            file_nameC = file.rsplit("\\")
            for i in range(len(file_nameC)):
                file_name = file_nameC[i]
            self.file_text.text = file_name
            type = file_name.rsplit('.')
            print(type[1])
            banner = Image.open(file)
            banner = banner.convert("RGB")
            banner = banner.save("banner.jpg")

        except Exception as e:
            print(e)


class ImagesScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

sm = WindowManager()

class MyApp(MDApp):
    def build(self):
        kv = Builder.load_file("desing.kv")

        screens = [LoginScreen(name="login"), InputScreen(
            name="input"), ImagesScreen(name="images")]
        for screen in screens:
            sm.add_widget(screen)
        sm.current = "login"
        return sm

if __name__ == "__main__":
    MyApp().run()
