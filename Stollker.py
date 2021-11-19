from sys import argv
from typing import DefaultDict
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton, MDRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.card import MDCard
from kivymd.utils.fitimage import FitImage
from kivy.uix.image import Image as KivyImage
from insta_downnloader import insta_D
from PIL import Image
import easygui
import glob
import win32print
import win32api
from googletrans import Translator
from kivy.config import Config
from kivy.core.window import Window


_fixed_size = (800, 600 ) #desired fix size
def reSize(*args):
   Window.size = _fixed_size
   return True
Window.bind(on_resize = reSize)
hashtag = ""

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

# def show_spinner(self):
#     # sla = self.dialog.dismiss(force=True)
#     if not self.dialog:
#         self.dialog = MDDialog(
#             spiner = Spinner(size_hint=(0.5,0.5),pos_hint={"center_x":0.5,"y":0.5},active=True)
#             )
#     self.dialog.open()

class LoginScreen(Screen):
    def close_dialog(self,erro):
        self.dialog.dismiss()
    dialog = None

    user = ObjectProperty(None)
    key = ObjectProperty(None)

    def Login(self):
        # show_spinner(self)
        # self.add_widget()
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

    def ImagesSelector(self):
        global hashtag
        hashtag = self.hashtag.text
        qtd = self.qtd.text
        dia = self.dia.text
        if dia == "Insira a data da publicação":
            dia = ""
        get_images = insta_D.ByHashtag(str(hashtag), qtd, dia)
        global folder
        # print(get_images)
        if(get_images == True):
            sm.current = "images"
            # print(get_images)
            # folder = get_images
            # print(folder)
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
    banner_photo = ObjectProperty(None)

    # print(folder,hashtag)
    def Back(self,obj):
        self.remove_widget(self.button1)
        self.remove_widget(self.button2)
        self.banner_photo.source = ""
        sm.current = "input"


    def get_current_img(self):
        self.carousel = self.ids['carrousel']
        sla = self.carousel.current_slide   
        global current_img
        current_img = sla.children[0].source
        #parte pra imprimir: funciona

        
    def print_file(self,obj):
        banner = Image.open("banner.jpg")
        img = Image.open(current_img)
        img_2 = img.resize((367,409))
        full_img = banner.copy()
        full_img.paste(img_2,(56,31))
        full_img.save("print.jpg")
        photo_path = "print.jpg"
        defprt = win32print.GetDefaultPrinter()
        prt = win32print.SetDefaultPrinter(defprt)
        win32api.ShellExecute(0, "print", photo_path, None, None, 0)


    def add_pictures(self):
        # self.carousel = Carousel(direction="right")
        self.banner_photo.source = "banner.jpg"

        self.carousel = self.ids['carrousel']
        self.carousel.clear_widgets()
        files = (glob.glob(f"./temp_{hashtag}/*.jpg"))
        for i in range(len(files)):
            # self.carousel.add_widget(FloatLayout)
            card =  MDCard(size_hint=(0.30190,0.4465), pos_hint={"center_x":0.5,"y":0.44})
            # card =  MDCard(size_hint=(0.30190,0.4465), pos_hint={"center_x":0.5,"y":0.44})
            img = FitImage(size_hint_y= 1, source=files[i])
            # print(img.source)
            card.add_widget(img)
            # print(i)
            # img = CoreImage(source=file,size_hint=(0.6,0.6),pos_hint={"center_x":0.5,"y":0.25})
            self.carousel.add_widget(card)
        
        self.button1 = MDRoundFlatIconButton(font_size=20,icon="arrow-left-bold-circle-outline",text="Voltar",pos_hint={"center_x":0.4, "y":0.05},on_release=self.Back)
        self.button2 = MDRoundFlatIconButton(font_size=20,icon="printer",text="Imprimir",pos_hint={"center_x":0.6, "y":0.05},on_release=self.print_file)
        self.add_widget(self.button1)
        self.add_widget(self.button2)
        #parte a fazer: criar arquivo csv

        # with open('persons.csv', 'wb') as csvfile:
        #     filewriter = csv.writer(csvfile, delimiter=',',
        #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #     filewriter.writerow(['Name', 'Profession'])
        #     filewriter.writerow(['Derek', 'Software Developer'])
        #     filewriter.writerow(['Steve', 'Software Developer'])
        #     filewriter.writerow(['Paul', 'Manager'])
        # os.remove(img_path)
        # full_img.show()
    
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
