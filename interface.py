import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
import webbrowser
from PIL import Image
from urllib.request import urlopen
import io

from api import Recherche


# =========================
# STYLE GLOBAL
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("CheapShark Pro Comparator")
app.geometry("3400x1440")


# =========================
# VARIABLES
# =========================

liste_jeux = []
jeu_actuel = None


# =========================
# IMAGE
# =========================

def afficherImage(url):

    try:
        data = urlopen(url).read()
        img = Image.open(io.BytesIO(data))
        img = img.resize((180, 220))

        photo = ctk.CTkImage(light_image=img, size=(180, 220))
        image_label.configure(image=photo)
        image_label.image = photo

    except:
        pass


# =========================
# RECHERCHE JEUX
# =========================

def rechercher():

    global liste_jeux, jeu_actuel

    nom = entry.get()

    if not nom:
        return

    with open("historique.txt", "a", encoding="utf-8") as f:
        f.write(nom + "\n")

    jeu_actuel = Recherche(nom)
    liste_jeux = jeu_actuel.chercherJeux()

    listbox.delete(0, tk.END)

    for j in liste_jeux[:25]:
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

    textbox.delete("0.0", tk.END)

    for d in deals:
        textbox.insert(
            tk.END,
            f"{d['store']} | {d['price']}$ | -{d['savings']}%\n"
        )


# =========================
# FAVORIS
# =========================

def charger_favoris():

    try:
        with open("favoris.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def sauvegarder_favoris(data):

    with open("favoris.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def ajouterFavori():

    sel = listbox.curselection()
    if not sel:
        return

    jeu = liste_jeux[sel[0]]

    fav = charger_favoris()

    if jeu["external"] not in fav:
        fav.append(jeu["external"])

    sauvegarder_favoris(fav)

    messagebox.showinfo("Favoris", "Ajouté ⭐")

    afficherFavoris()


def supprimerFavori():

    sel = fav_list.curselection()
    if not sel:
        return

    fav = charger_favoris()

    del fav[sel[0]]

    sauvegarder_favoris(fav)

    afficherFavoris()


def afficherFavoris():

    fav_list.delete(0, tk.END)

    fav = charger_favoris()

    for f in fav:
        fav_list.insert(tk.END, f)


def ouvrirFavori(event):

    sel = fav_list.curselection()
    if not sel:
        return

    game = fav_list.get(sel[0])

    url = f"https://www.cheapshark.com/search?q={game}"
    webbrowser.open(url)

def rechercherFavoris():

    query = fav_search.get().lower()

    fav_list.delete(0, tk.END)

    fav = charger_favoris()

    for f in fav:
        if query in f.lower():
            fav_list.insert(tk.END, f)

# =========================
# PANIER
# =========================

def charger_panier():
    try:
        with open("panier.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def sauvegarder_panier(data):
    with open("panier.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def ajouterPanier():

    sel = listbox.curselection()
    if not sel:
        return

    jeu = liste_jeux[sel[0]]

    panier = charger_panier()

    panier.append({
        "name": jeu["external"],
        "id": jeu["gameID"]
    })

    sauvegarder_panier(panier)

    messagebox.showinfo("Panier", "Ajouté 🛒")

    afficherPanier()


def ouvrirPanier():

    sel = cart_list.curselection()
    if not sel:
        return

    jeu = cart_list.get(sel[0])

    url = f"https://www.cheapshark.com/search?q={jeu}"
    webbrowser.open(url)


def supprimerPanier():

    sel = cart_list.curselection()
    if not sel:
        return

    panier = charger_panier()

    del panier[sel[0]]

    sauvegarder_panier(panier)

    afficherPanier()


def afficherPanier():

    cart_list.delete(0, tk.END)

    panier = charger_panier()

    total = 0

    for item in panier:

        cart_list.insert(tk.END, item["name"])

        try:
            deals = jeu_actuel.recupererDeals(item["id"])
            if deals:
                total += deals[0]["price"]
        except:
            pass

    total_label.configure(text=f"Total: {round(total,2)}$")

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
# UI PRINCIPALE
# =========================

frame = ctk.CTkFrame(app, corner_radius=20)
frame.pack(padx=20, pady=20, fill="both", expand=True)


title = ctk.CTkLabel(
    frame,
    text="🎮 CheapShark PRO Comparator",
    font=("Arial", 24, "bold")
)
title.pack(pady=10)


# =========================
# SEARCH BAR
# =========================

entry = ctk.CTkEntry(frame, placeholder_text="Search game...", width=300, corner_radius=15)
entry.pack(pady=5)

ctk.CTkButton(frame, text="Search", corner_radius=15, command=rechercher).pack(pady=5)


# =========================
# LISTE JEUX
# =========================

listbox = tk.Listbox(
    frame,
    height=8,
    width=60,
    bg="#1f1f1f",
    fg="white",
    selectbackground="#3b82f6"
)
listbox.pack(pady=10)

ctk.CTkButton(frame, text="Show Deals", corner_radius=15, command=voirDeals).pack(pady=5)
ctk.CTkButton(frame, text="Open Deal", corner_radius=15, command=ouvrirSite).pack(pady=5)
ctk.CTkButton(frame, text="Add Favorite", corner_radius=15, command=ajouterFavori).pack(pady=5)


# =========================
# IMAGE + DEALS
# =========================

image_label = ctk.CTkLabel(frame, text="")
image_label.pack(pady=10)

textbox = ctk.CTkTextbox(frame, width=650, height=160, corner_radius=15)
textbox.pack(pady=10)


# =========================
# FAVORIS SECTION AVANCEE
# =========================

ctk.CTkLabel(frame, text="⭐ FAVORIS", font=("Arial", 18, "bold")).pack(pady=5)

fav_search = ctk.CTkEntry(frame, placeholder_text="Search favorites...", width=300, corner_radius=15)
fav_search.pack(pady=5)

ctk.CTkButton(frame, text="Search Fav", command=rechercherFavoris, corner_radius=15).pack(pady=5)

fav_list = tk.Listbox(
    frame,
    height=6,
    width=60,
    bg="#1f1f1f",
    fg="white"
)
fav_list.pack(pady=5)

fav_list.bind("<Double-Button-1>", ouvrirFavori)

ctk.CTkButton(frame, text="Delete Favorite", command=supprimerFavori, corner_radius=15).pack(pady=5)


# =========================
# INIT
# =========================

afficherFavoris()
app.mainloop()