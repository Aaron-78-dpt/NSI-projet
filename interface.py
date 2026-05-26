import tkinter as tk
from tkinter import messagebox
import json
import webbrowser
from PIL import Image, ImageTk
from urllib.request import urlopen
import io

from api import Recherche


fenetre = tk.Tk()

fenetre.title("Comparateur CheapShark")
fenetre.geometry("900x600")


liste_jeux = []
jeu_actuel = None
image_label = None
photo = None


# =========================
# RECHERCHE
# =========================

def rechercher():

    global liste_jeux
    global jeu_actuel

    nom = entry.get()

    if nom == "":
        return

    # historique
    with open(
        "historique.txt",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(nom + "\n")

    jeu_actuel = Recherche(nom)

    liste_jeux = jeu_actuel.chercherJeux()

    listbox.delete(0, tk.END)

    for jeu in liste_jeux[:20]:

        listbox.insert(
            tk.END,
            jeu["external"]
        )


# =========================
# AFFICHER DEALS
# =========================

def voirDeals():

    selection = listbox.curselection()

    if not selection:
        return

    index = selection[0]

    jeu = liste_jeux[index]

    afficherImage(
        jeu["thumb"]
    )

    gameID = jeu["gameID"]

    deals = jeu_actuel.recupererDeals(gameID)

    textbox.delete("1.0", tk.END)

    for deal in deals:

        texte = (
            f"{deal['store']} | "
            f"{deal['price']}$ | "
            f"-{deal['savings']}%\n"
        )

        textbox.insert(
            tk.END,
            texte
        )

# =========================
# AFFICHER IMAGE
# =========================

def afficherImage(url):

    global photo
    global image_label

    image_bytes = urlopen(url).read()

    data_stream = io.BytesIO(image_bytes)

    pil_image = Image.open(data_stream)

    pil_image = pil_image.resize((200, 250))

    photo = ImageTk.PhotoImage(pil_image)

    image_label.config(image=photo)


# =========================
# FAVORIS
# =========================

def ajouterFavori():

    selection = listbox.curselection()

    if not selection:
        return

    index = selection[0]

    jeu = liste_jeux[index]

    favoris = []

    try:

        with open(
            "favoris.json",
            "r",
            encoding="utf-8"
        ) as f:

            favoris = json.load(f)

    except:
        pass

    favoris.append(jeu["external"])

    with open(
        "favoris.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            favoris,
            f,
            indent=4
        )

    messagebox.showinfo(
        "Favoris",
        "Jeu ajouté aux favoris"
    )


# =========================
# OUVRIR DEAL
# =========================

def ouvrirSite():

    selection = listbox.curselection()

    if not selection:
        return

    index = selection[0]

    jeu = liste_jeux[index]

    url = (
        "https://www.cheapshark.com/"
        f"redirect?dealID={jeu['cheapestDealID']}"
    )

    webbrowser.open(url)


# =========================
# INTERFACE
# =========================

titre = tk.Label(
    fenetre,
    text="Comparateur CheapShark",
    font=("Arial", 22)
)

titre.pack(pady=20)


entry = tk.Entry(
    fenetre,
    width=40,
    font=("Arial", 14)
)

entry.pack(pady=10)


btnRecherche = tk.Button(
    fenetre,
    text="Rechercher",
    command=rechercher
)

btnRecherche.pack(pady=10)


listbox = tk.Listbox(
    fenetre,
    width=50,
    height=10
)

listbox.pack(pady=10)


btnDeals = tk.Button(
    fenetre,
    text="Voir tous les deals",
    command=voirDeals
)

btnDeals.pack(pady=5)


btnFavoris = tk.Button(
    fenetre,
    text="Ajouter aux favoris",
    command=ajouterFavori
)

btnFavoris.pack(pady=5)


btnSite = tk.Button(
    fenetre,
    text="Ouvrir le deal",
    command=ouvrirSite
)

btnSite.pack(pady=5)


textbox = tk.Text(
    fenetre,
    width=70,
    height=15
)

textbox.pack(pady=20)

image_label = tk.Label(fenetre)

image_label.pack(pady=10)

fenetre.mainloop()