import tkinter as tk
import time
import threading
from tkinter import ttk
from package.classes import PageWeb, Rectangle

# AFFICHONS LE CODE HTML
def showhtml(root, data):
    # CREATION DE LA FENETRE
    htmlScreen = tk.Text(root, width='1200')
    htmlScreen.pack()
    root.update_idletasks()
    time.sleep(0.1)
    root.add(htmlScreen, text="HTML")
    htmlScreen.delete(1.0, 'end')
    htmlScreen.insert(1.0, data)

#AFFICHONS LE SEO
def showseo(root):
    pass

#AFFICHONS LA LISTE DES LIENS
def showlinks(root, data):
    numberOfLinks = 0
    linkScreen = tk.Text(root, width="1200")
    linkScreen.pack()
    root.add(linkScreen, text="Liens de la page")
    linkScreen.delete(1.0, 'end')
    #LISTONS TOUS LES LIENS
    for link in data.find_all('a'):
        pageweb = PageWeb(link.get('href'))
        linkScreen.insert(1.0, (link.get('href')) + ' ' + str(pageweb.code) + '\n')
        root.update_idletasks()
        time.sleep(0.1)
        numberOfLinks += 1    
    linkScreen.insert(1.0, 'Il y a ' + str(numberOfLinks) + ' liens sur cette page. \n \n')

#AFFICHONS L'ORGANIGRAMME
def showorganigram(root, data, title):
    ### FENETRE CONTENANT LE CANVAS
    canvas = tk.Canvas(root, width="1200")
    canvas.pack()
    #MODELE DE REFERENCE
    pendingrectangle = Rectangle(700,50,850,100, "yellow")
    pendingrectangle.draw(canvas)
    validaterectangle = Rectangle(700, 110, 850, 160, "green")
    validaterectangle.draw(canvas)
    refusedrectangle = Rectangle(700, 170, 850, 220, "red")
    refusedrectangle.draw(canvas)
    validaterectangle.textinside(canvas, "Status OK" )
    pendingrectangle.textinside(canvas, "En cours...")
    refusedrectangle.textinside(canvas, "Erreur de lien")
    # COMMENCONS A DESSINER L'ORGANIGRAME
    x = 50
    y = 50
    dx = 400
    dy = 100
    for link in data.find_all('a'):
        titlelink = link.text
        rectangle = Rectangle(x, y, dx, dy, "yellow")
        rectangle.draw(canvas)
        rectangle.textinside(canvas, titlelink)
        y += 60
        dy += 150
        root.update_idletasks()
        time.sleep(0.1)

def showprogressbar(root):
    analiseprogress = ttk.Progressbar(root, length=100, mode='indeterminate')
    analiseprogress.pack(side='top')
    root.update_idletasks()


# AFFICHONS LE RESULTAT DANS LA FENETRE
def showresult(content, url, root, title):
    showprogressbar(root)
    ### FENETRE CONTENANT LE RESULTAT DE LA REQUETTE

    resultWindow = ttk.Notebook(root, width="1200")
    resultWindow.pack()

    # ON AJOUTE L'ASYNCHRONE
    #th_html = threading.Thread(target=showhtml(resultWindow, content))
    #th_links = threading.Thread(target=showlinks(resultWindow, content))
    th_organigram = threading.Thread(target=showorganigram(resultWindow, content, title))

    #th_html.start()
    #th_links.start()
    th_organigram.start()

    #th_html.join()
    #th_links.join()
    th_organigram.join()

    
    labelScreenWindow = tk.Label(root, text='Resultat de la requete pour ' + url)
    labelScreenWindow.pack()         

