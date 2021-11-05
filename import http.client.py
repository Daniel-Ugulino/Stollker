import os
from instagrapi import Client
import win32print
import win32api

cl = Client()

def login():
    user = input("Insira seu usuario:")

    senha = input("Insira sua senha:")
    print("Logando")
    login = cl.login(user, senha)
    print("Logado")

def getImgaes(): 

    # hashtag1 = cl.hashtag_info(hashtags)
    # qtd = hashtag1.dict()
    # qtd = int(qtd["media_count"])
    
    hashtags = input("Insira a hashtag desejada:")
    qtd = int(input("Insira a quantidade de posts desejados:"))
    print("Coletando imagens")
    urls = []
    data = cl.hashtag_medias_recent(hashtags, amount=qtd)
    for i in range(len(data)):
        data_obj = data[i].dict()
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
                
    return [urls,hashtags] 

def dowloadImages():

    dados = getImgaes()

    urls = dados[0]
    hashtags = dados[1]

    count = 0
    photo_folder = "./temp_" + hashtags

    if(os.path.isdir(photo_folder) == False):
        # count += 1
        # photo_folder = "./temp_" + str(count) + "_" + hashtags
        os.makedirs(photo_folder)


    for i in range(len(urls)):
        cl.photo_download_by_url(url=urls[i], filename=(
            hashtags + "_fotos_" + str(i + 1)), folder=photo_folder)
        print(f"Imagem {i+1} da {hashtags} re-baixada")

def printingImages():
    print("Imprimindo imagen")

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

login()
dowloadImages()
# sla