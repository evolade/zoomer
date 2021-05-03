from time import sleep
from datetime import datetime
import pyautogui as pg
import json
from playsound import playsound
import webbrowser

# görüntüyü güzelleştiren python modülü
from rich.console import Console
from rich.text import Text 





# alarm sesi dosyası
alarmSound = "sound.mp3"


c = Console()


# json yazma
def jwrite(obj):
    with open("db.json", "w") as fh:
        fh.write(json.dumps(obj, indent = 4))





#json okuma
def jread(obj):
    with open("db.json", "r") as fh:
        return (json.loads(fh.read())[obj])





# id ile katılmak
def idjoin(meeting, password):
    webbrowser.open_new("https://us04web.zoom.us/j/" + str(meeting) + "?from=join")
    sleep(4)
    pg.typewrite(password) 
    sleep(0.5)
    pg.press('enter')
    sleep(3)
    




# link ile katılmak
def linkjoin(link):
    webbrowser.open_new(link)





# yeni program oluşturma
data = {}
def takeInput(type):
    jwrite(data)

    try:
        days = c.input("\n haftanın hangi günleri meeting var\n örnek :\n   pzt sal crs prs cum cmt pzr\n\n (günler arası [white]1 [red]boşluk bırakın[/])\n\n [bold blue]> ")
    
    except:
        c.print("\n [red]türkçe harf hatası")

    if jread("type") == "id":
        passInput = c.input("\n meeting password [bold blue]> ")
        data["password"] = passInput

    alarm = int(c.input("\n meeting başlamadan kaç dk önce alarm çalsın [bold blue]> "))
    arrDays = days.split(" ")
    data["days"] = len(arrDays)
    data["alarm"] = alarm      
    l = 1
    
    print("\n örnek saat: 16:33 ")
    c.print(" kaydetmek için: [green].s[/]")

    for j in range(len(arrDays)):
        data[str(j + 1) + "d"] = str(arrDays[j]) # ayrılmış günleri "data" sözlüğüne kaydetmek
        
        while 1:

            meetingTime = c.input("\n " + str(arrDays[j]) + " " + str(l) + ". meeting saati [bold blue]> ")

            if meetingTime == ".s":    
                c.print("\n [green]kaydedildi")
                jwrite(data)            
                break 
       
            meetings = c.input("\n " + str(arrDays[j]) + " " + str(l) + ". meeting " + str(type) + " [bold blue]> ") 

            # meeting saatini ve id sini "data" ya kaydetmek         
            data[str(j + 1) + str(l) + "t"] = meetingTime
            data[str(j + 1) + str(l) + "m"] = meetings

            if meetings == ".x" or meetingTime == ".x":
                break

            l += 1

        l = 1





# ana fonksiyon (menü)
def userInput():
    ringed = False
    i = 1
    c.print("\n  [bold blue]Zoomer", end = "")
    print("    v1.1\n\n  © 2021 V Dev")
    while 1:
        choice = c.input("\n [green]1[/] - çalıştır\n [green]2[/] - yeni program\n [green]3[/] - programı görüntüle (json)\n [green]4[/] - programı sil\n [green]5[/] - çık\n\n [bold blue]> ")
        
        if choice == "1":

            try:
                now = datetime.now()
                ntoday = now.strftime("%w") # bugünün sayı olarak karşılığı (pazartesi: 1, salı: 2)

                # sayılar ile kullanıcının girdiği günleri eşleştirmek
                if ntoday == "1": today = "pzt"
                if ntoday == "2": today = "sal"
                if ntoday == "3": today = "crs"
                if ntoday == "4": today = "prs"
                if ntoday == "5": today = "cum"
                if ntoday == "6": today = "cmt"
                if ntoday == "0": today = "pzr"

                # programda kaç gün olduğunu bulup içinden bugünün olup olmadığını aramak
                for i in range(jread("days")):

                    if jread(str(i + 1) + "d") == today:
                        itoday = i + 1
                        break
                
                j = 1

            except:
                print("\n program yok")
                continue
            
            try:

                if jread("type") == "id":
                    passwd = jread("password")
                    
                    while 1:
                        now = datetime.now() 

                        # "db.json" dan meetinglerdeki saat, dakike ve id (veya link) bulmak
                        mhour = str(jread(str(itoday) + str(j) + "t")[0]) + str(jread(str(itoday) + str(j) + "t")[1])
                        mminute = str(jread(str(itoday) + str(j) + "t")[3]) + str(jread(str(itoday) + str(j) + "t")[4])
                        mid = str(jread(str(itoday) + str(j) + "m"))
                        
                        # eğer şu anki dakika önümüzdeki meetingin dakikasından "alarm" dakika ilerideyse alarm çal
                        if int(mminute) - int(jread("alarm")) == int(now.strftime("%M")):
                            
                            if ringed == False:
                                playsound(alarmSound)
                                ringed = True
                            
                        # eğer meeting saati şu anki saatten gerideyse bir sonraki meetinge atla (j += 1)
                        if int(mhour) < int(now.strftime("%H")):
                            j += 1
                            continue

                        # eğer meeting dakikası şu anki dakikadan gerideyse bir sonraki meetinge atla, bu şekilde önümüzdeki meetinge geleseye kadar devam ediyor
                        if int(mminute) < int(now.strftime("%M")):
                            j += 1
                            continue
                        
                        if now.strftime("%H") == mhour:
                            print("\n sonraki meeting:", mhour + ":" + mminute)
                            print(" kalan dakika:", int(mminute) - int(now.strftime("%M")))

                            if now.strftime("%M") == mminute:
                                c.print("\n [bold blue]ID ile katılıyor")
                                playsound(alarmSound)
                                playsound(alarmSound)
                                sleep(5)
                                ringed = False
                                idjoin(mid, passwd)
                                j += 1

                        sleep(1)
                
                if jread("type") == "link":

                    while 1:
                        now = datetime.now()
                        mhour = str(jread(str(itoday) + str(j) + "t")[0]) + str(jread(str(itoday) + str(j) + "t")[1])
                        mminute = str(jread(str(itoday) + str(j) + "t")[3]) + str(jread(str(itoday) + str(j) + "t")[4])
                        mid = str(jread(str(itoday) + str(j) + "m"))

                        if int(mminute) - int(jread("alarm")) == int(now.strftime("%M")):
                            
                            if ringed == False:
                                playsound(alarmSound)
                                ringed = True

                        if int(mhour) < int(now.strftime("%H")):
                            j += 1
                            continue
                        
                        if int(mminute) < int(now.strftime("%M")):
                            j += 1
                            continue

                        if now.strftime("%H") == mhour:
                            print("\n sonraki meeting:", mhour + ":" + mminute)
                            print(" kalan dakika:", int(mminute) - int(now.strftime("%M")))

                            if now.strftime("%M") == mminute:
                                c.print("\n [bold blue]link ile katılıyor")
                                playsound(alarmSound)
                                playsound(alarmSound)
                                sleep(5)
                                ringed = False
                                linkjoin(mid)
                                j += 1

                        sleep(1)

            except:
                c.print("\n [bold red]meeting yok")
            
        if choice == "2": 
            confirm = c.input("\n yeni program oluşturmak eski programı siler, emin misin ([green]e [white]/ [red]h[/]) \n\n [bold blue]> ")

            if confirm == "e":
                idtype = c.input("\n [green]1[/] - ID ile giriş \n [green]2[/] - link ile giriş \n\n [bold blue]> ")
                
                if idtype == "1":
                    data["type"] = "id" 
                    takeInput("ID")
                
                if idtype == "2":
                    data["type"] = "link"
                    takeInput("link")

            else:
                continue
        
        if choice == "3": 
            f = open("db.json", "r")
            print("")
            print("-" * 50) # programın görünürlüğünü artırmak için 50 tane çizgi
            print(f.read())
            print("-" * 50)
        
        if choice == "4":
            deleteConfirm = c.input("\n programı silmek istediğine emin misin ([green]e [white]/ [red]h[/]) \n\n [bold blue]> ")
            if deleteConfirm == "e":
                open('db.json', 'w').close() 
                c.print("\n [green]silindi")
            else:
                continue
            
            
            #eraser = {"asd": "abu"}
            #jwrite(eraser)

        if choice == "5":
            exit()
                
                



userInput()
