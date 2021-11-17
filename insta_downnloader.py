import os
from instagrapi import Client
import win32print
import win32api
from datetime import date, datetime

cl = Client()


class insta_D():
    def Login(user, key):
        try:
            login = cl.login(user, key)
            return(True)
        except Exception as e:
            return(e)

    def ByHashtag(hashtags, qtd, day_selected=""):
       
        # try:
        #     data = cl.hashtag_medias_recent(hashtags, amount="")

        # except:
        # hashtags = input("Insira a hashtag desejada:")
        # qtd = int(input("Insira a quantidade de posts desejados:"))

        # print("Coletando imagens")
        urls = []
        dates = []
        try:
            print("Coletando dados")
            hashtag1 = cl.hashtag_info(hashtags)
            qtd_total = hashtag1.dict()
            qtd_total = int(qtd_total["media_count"])
            if (int(qtd_total) >= 500):
                qtd_total = 500
            print("Coletando imagens")
            print(qtd_total)
            data = cl.hashtag_medias_recent(hashtags, amount=qtd_total)
            
            for i in range(len(data)):
                # print(i)
                data_obj = data[i].dict()
                day_taken_formated = data_obj["taken_at"].date() 

                day_taken = data_obj["taken_at"]

                dates.append(day_taken)

                if (day_selected != ""):
                    day_taken_formated = day_taken_formated.strftime("%d/%m/%Y")
                    # print(day_taken,day_selected)
                    if(day_selected == day_taken_formated):
                        data_url = str(data_obj["thumbnail_url"])
                        if(data_url != "None"):
                            data_url = data_url.replace("HttpUrl(", "")
                            data_url = data_url.replace("'", "")
                            urls.append(data_url)
                            
                        elif(data_url == "None"):
                            res = data_obj["resources"]
                            for j in range(len(res)):
                                res1 = res[j]
                                urls.append(str(res1["thumbnail_url"]))
                else:
                    data_url = str(data_obj["thumbnail_url"])
                    if(data_url != "None"):
                        data_url = data_url.replace("HttpUrl(", "")
                        data_url = data_url.replace("'", "")
                        urls.append(data_url)
                    elif(data_url == "None"):
                        res = data_obj["resources"]
                        for j in range(len(res)):
                            res1 = res[j]
                            urls.append(str(res1["thumbnail_url"]))

            # count = 0
            photo_folder = "./temp_" + hashtags

            if(os.path.isdir(photo_folder) == False):
                # count += 1
                # photo_folder = "./temp_" + str(count) + "_" + hashtags
                os.makedirs(photo_folder)
            print(len(dates))
            print(qtd)
            for i in range(qtd):
                dates_formated = str(dates[i])
                dates_formated = dates_formated.replace(':',"_")
                dates_formated = dates_formated.replace(' ',"_")
                dates_formated = dates_formated.replace('+',"_")

                cl.photo_download_by_url(url=urls[i], filename= (
                    hashtags + "_fotos_" + str(dates_formated) ), folder=photo_folder)
                # print(f"Imagem {i+1} da {hashtags} baixada")

            return(True)

        except Exception as e:
            return(e)

    def Print_out():

        # print("Imprimindo imagem")

        # img = Image.open('./temp_1_brasileirao/brasileirao_fotos_1.jpg')
        img = "brasileirao_fotos_2.jpg"
        caminho = "./temp_brasileirao/"
        defprt = win32print.GetDefaultPrinter()
        prt = win32print.SetDefaultPrinter(defprt)

        win32api.ShellExecute(0, "print", img, None, caminho, 0)
        # win32print.StartDocPrinter(prt, 1, ("Imagem Instagram", None, None))
        # win32print.WritePrinter(prt, img)
        # win32print.EndDocPrinter(prt)
        # win32print.ClosePrinter(prt)

