from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image as CoreImage
from insta_downnloader import insta_D
from PIL import Image
import easygui
import glob
from googletrans import Translator

# global hashtag
hashtag = ""
# global folder
folder = ""

translator = Translator()
# global folder 
# folder = ""
# https://www.techwithtim.net/tutorials/kivy-tutorial/floatlayout/
def show_alert_dialog(self,erro):
    
    # sla = self.dialog.dismiss(force=True)
    if not self.dialog:
        self.dialog = MDDialog(
            text=str(erro),
            buttons=[
                MDFlatButton(
                    text="SAIR", on_release = self.close_dialog,
                ),
            ],
            )
    self.dialog.open()


class LoginScreen(Screen):
    def close_dialog(self,erro):
        self.dialog.dismiss()
    dialog = None

    user = ObjectProperty(None)
    key = ObjectProperty(None)

    def Login(self):
        user = self.user.text
        key = self.key.text
        login = insta_D.Login(user, key)
        if (login == True):
            sm.current = "input"
        else:
            error = translator.translate(login, dest='pt')
            show_alert_dialog(self,error.text)

class InputScreen(Screen):
    def close_dialog(self,erro):
        self.dialog.dismiss()
    dialog = None

    hashtag = ObjectProperty(None)
    dia = ObjectProperty(None)
    qtd = ObjectProperty(None)
    file_text = ObjectProperty(None)

    def Back(self):
        sm.current = "login"

    def on_save(self,instance, value, date_range):
        day = value.strftime("%d/%m/%Y")
        self.dia.text = day
        
    def show_time_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()      

    def ImagesPicker(self):
        global hashtag
        hashtag = self.hashtag.text
        qtd = self.qtd.text
        dia = self.dia.text
        if dia == "Insira a data da publicação":
            dia = ""
        get_images = insta_D.ByHashtag(str(hashtag), int(qtd), dia)
        global folder
        if(get_images != ""):
            sm.current = "images"
            # print(get_images)
            folder = get_images
        else:
            error = translator.translate(get_images, dest='pt')
            show_alert_dialog(self,error.text)

    def FileInput(self):
        file = easygui.fileopenbox()
        try:
            file_nameC = file.rsplit("\\")
            for i in range(len(file_nameC)):
                file_name = file_nameC[i]
            self.file_text.text = file_name
            # type = file_name.rsplit('.')
            banner = Image.open(file)
            banner = banner.convert("RGB")
            banner = banner.save("banner.jpg")

        except Exception as e:
            print(e)



class ImagesScreen(Screen):
    # print(folder,hashtag)
    def add_pictures(self, **kwargs):
        super(ImagesScreen, self)
        self.carousel = Carousel(direction="right")
        # self.carousel = self.ids['carrousel']
        qtd_folder = (glob.glob(f"./temp_{hashtag}/*.jpg"))
        for i in range(len(qtd_folder)):
            # print(i)
            file = (f"{folder}/{hashtag}_fotos_{i+1}.jpg")
            # print(file)
            img = CoreImage(source=file,size_hint=(0.6,0.6),pos_hint={"center_x":0.5,"y":0.25})
            self.carousel.add_widget(img)
        self.add_widget(self.carousel)
    

# ImagesScreen.add_widget(add_pictures())

class WindowManager(ScreenManager):
    pass

sm = WindowManager()

class MyApp(MDApp):
    def build(self):
        self.icon = "stollker logo.png"
        self.title = "Stollker"

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "600"
        kv = Builder.load_file("desing.kv")

        screens = [LoginScreen(name="login"), InputScreen(
            name="input"), ImagesScreen(name="images")]
        for screen in screens:
            sm.add_widget(screen)
        sm.current = "login"
        return sm

if __name__ == "__main__":
    MyApp().run()
