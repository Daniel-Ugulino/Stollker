from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton, MDRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.card import MDCard
from kivymd.utils.fitimage import FitImage
from insta_downnloader import insta_D
from PIL import Image
import easygui
import glob
import win32print
import win32api
from googletrans import Translator
# global hashtag
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
        print(get_images)
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
    # print(folder,hashtag)
  
    def add_pictures(self):
        # self.carousel = Carousel(direction="right")
          
        def Back():
            sm.current = "input"

        self.carousel = self.ids['carrousel']
        files = (glob.glob(f"./temp_focanomil/*.jpg"))
        for i in range(len(files)):
            # self.carousel.add_widget(FloatLayout)
            card =  MDCard(size_hint=(0.30190,0.4465), pos_hint={"center_x":0.5,"y":0.44})
            img = FitImage(size_hint_y= 1, source=files[i])
            print(img.source)
            card.add_widget(img)
            # print(i)
            # img = CoreImage(source=file,size_hint=(0.6,0.6),pos_hint={"center_x":0.5,"y":0.25})
            self.carousel.add_widget(card)
        # o bug ta aqui embaixo
        # self.add_widget(self.carousel)

        
        # self.button1 = MDRoundFlatIconButton(font_size=20,icon="arrow-left-bold-circle-outline",text="Voltar",pos_hint={"center_x":0.4, "y":0.05},on_release=Back())
        # self.button2 = MDRoundFlatIconButton(font_size=20,icon="printer",text="Imprimir",pos_hint={"center_x":0.6, "y":0.05})
        # self.add_widget(self.button1)
        # self.add_widget(self.button2)
    
    def printFile(self):
        self.carousel = self.ids['carrousel']
        sla = self.carousel.current_slide    
        #ta en sla.chldren.0.source
        #parte pra imprimir: funciona

        # banner = Image.open("banner.jpg")
        # img = Image.open("./temp_fluminense/fluminense_fotos_2021-11-17_12_00_13_00_00.jpg")
        # img_2 = img.resize((367,409))
        # full_img = banner.copy()
        # full_img.paste(img_2,(56,31))
        # full_img.save("print.jpg")
        # photo_path = "print.jpg"
        # defprt = win32print.GetDefaultPrinter()
        # prt = win32print.SetDefaultPrinter(defprt)
        # win32api.ShellExecute(0, "print", photo_path, None, None, 0)

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
        sm.current = "images"
        return sm

if __name__ == "__main__":
    MyApp().run()
