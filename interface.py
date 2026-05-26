import tkinter as tk
from tkinter import messagebox, ttk
import json
import webbrowser
from PIL import Image, ImageTk
from urllib.request import urlopen
import io

from api import Recherche


# =========================
# FENÊTRE
# =========================

fenetre = tk.Tk()
fenetre.title("CheapShark Comparator")
fenetre.geometry("3400x1440")
fenetre.config(bg="#1E1E1E")


# =========================
# NOTEBOOK (ONGLETS)
# =========================

notebook = ttk.Notebook(fenetre)
notebook.pack(fill="both", expand=True)

tab_recherche = tk.Frame(notebook, bg="#1E1E1E")
tab_favoris = tk.Frame(notebook, bg="#1E1E1E")

notebook.add(tab_recherche, text="🔎 Recherche")
notebook.add(tab_favoris, text="⭐ Favoris")


# =========================
# VARIABLES
# =========================

liste_jeux = []
jeu_actuel = None
photo = None


# =========================
# IMAGE
# =========================

image_label = tk.Label(tab_recherche, bg="#1E1E1E")
image_label.pack(pady=10)


def afficherImage(url):

    global photo

    try:
        image_bytes = urlopen(url).read()
        data_stream = io.BytesIO(image_bytes)

        img = Image.open(data_stream)
        img = img.resize((180, 220))

        photo = ImageTk.PhotoImage(img)

        image_label.config(image=photo)
        image_label.image = photo

    except:
        pass


# =========================
# RECHERCHE
# =========================

def rechercher():

    global liste_jeux, jeu_actuel

    nom = entry.get()

    if nom == "":
        return

    with open("historique.txt", "a", encoding="utf-8") as f:
        f.write(nom + "\n")

    jeu_actuel = Recherche(nom)
    liste_jeux = jeu_actuel.chercherJeux()

    listbox.delete(0, tk.END)

    for j in liste_jeux[:20]:
        listbox.insert(tk.END, j["external"])


# =========================
# DEALS
# =========================

def voirDeals():

    sel = listbox.curselection()

    if not sel:
        return

    jeu = liste_jeux[sel[0]]

    afficherImage(jeu["thumb"])

    deals = jeu_actuel.recupererDeals(jeu["gameID"])

    textbox.delete("1.0", tk.END)

    for d in deals:

        textbox.insert(
            tk.END,
            f"{d['store']} | {d['price']}$ | -{d['savings']}%\n"
        )


# =========================
# FAVORIS
# =========================

def ajouterFavori():

    sel = listbox.curselection()

    if not sel:
        return

    jeu = liste_jeux[sel[0]]

    favoris = []

    try:
        with open("favoris.json", "r", encoding="utf-8") as f:
            favoris = json.load(f)
    except:
        pass

    if jeu["external"] not in favoris:
        favoris.append(jeu["external"])

    with open("favoris.json", "w", encoding="utf-8") as f:
        json.dump(favoris, f, indent=4)

    messagebox.showinfo("Favoris", "Ajouté !")


def afficherFavoris():

    liste_fav.delete(0, tk.END)

    try:
        with open("favoris.json", "r", encoding="utf-8") as f:
            favoris = json.load(f)

        for favo in favoris:
            liste_fav.insert(tk.END, favo)

    except:
        pass


# =========================
# OUVRIR DEAL
# =========================

def ouvrirSite():

    sel = listbox.curselection()

    if not sel:
        return

    jeu = liste_jeux[sel[0]]

    url = f"https://www.cheapshark.com/redirect?dealID={jeu['cheapestDealID']}"

    webbrowser.open(url)


# =========================
# UI RECHERCHE
# =========================

title = tk.Label(
    tab_recherche,
    text="🎮 CheapShark Comparator",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="#1E1E1E"
)
title.pack(pady=10)


entry = tk.Entry(
    tab_recherche,
    width=40,
    font=("Arial", 14),
    bg="#2A2A2A",
    fg="white",
    insertbackground="white"
)
entry.pack(pady=10)


tk.Button(
    tab_recherche,
    text="Rechercher",
    command=rechercher
).pack(pady=5)


listbox = tk.Listbox(
    tab_recherche,
    width=60,
    height=10,
    bg="#2A2A2A",
    fg="white",
    selectbackground="#4C8BF5"
)
listbox.pack(pady=10)


tk.Button(
    tab_recherche,
    text="Voir deals",
    command=voirDeals
).pack(pady=5)

tk.Button(
    tab_recherche,
    text="Ajouter favoris",
    command=ajouterFavori
).pack(pady=5)

tk.Button(
    tab_recherche,
    text="Ouvrir deal",
    command=ouvrirSite
).pack(pady=5)


textbox = tk.Text(
    tab_recherche,
    width=80,
    height=12,
    bg="#2A2A2A",
    fg="white"
)
textbox.pack(pady=10)


# =========================
# FAVORIS TAB
# =========================

tk.Label(
    tab_favoris,
    text="⭐ Mes Favoris",
    font=("Arial", 20),
    fg="white",
    bg="#1E1E1E"
).pack(pady=10)


tk.Button(
    tab_favoris,
    text="Actualiser",
    command=afficherFavoris
).pack(pady=10)


liste_fav = tk.Listbox(
    tab_favoris,
    width=60,
    height=20,
    bg="#2A2A2A",
    fg="white"
)
liste_fav.pack(pady=10)


afficherFavoris()


# =========================
# RUN
# =========================

fenetre.mainloop()