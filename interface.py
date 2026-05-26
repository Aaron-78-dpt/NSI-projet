import requests
import tkinter as tk
from tkinter import messagebox


class Recherche():

    def __init__(self, gameName=""):

        self.gameId = ""
        self.name = ""
        self.lowerPriceEver = 0
        self.lowerPriceNow = 0
        self.site = ""
        self.gameName = gameName
        self.storeID = ""
        self.storeName = ""
        self.storeStatus = 0

    def __str__(self):

        return (
            f"Jeu : {self.name}\n"
            f"Prix le plus bas EVER : {self.lowerPriceEver}$\n"
            f"Prix actuel le plus bas : {self.lowerPriceNow}$\n"
            f"Magasin : {self.storeName}\n"
            f"Status : {self.storeStatus}"
        )

    def chercherJeux(self):

        r = requests.get(
            f'https://www.cheapshark.com/api/1.0/games?title={self.gameName}'
        )

        return r.json()

    def choisirJeu(self, choix, data):

        self.name = data[choix]["external"]
        self.gameId = data[choix]["gameID"]

    def moinChere(self):

        r = requests.get(
            f'https://www.cheapshark.com/api/1.0/games?ids={self.gameId}'
        )

        data = r.json()
        data = data[self.gameId]

        lowest_price = 999999

        q = requests.get(
            'https://www.cheapshark.com/api/1.0/stores'
        )

        stores = q.json()

        for deal in data["deals"]:

            store_id = deal["storeID"]

            store = stores[int(store_id)]

            if store["isActive"] == 1:

                price = float(deal["price"])

                if price < lowest_price:

                    lowest_price = price

                    self.lowerPriceNow = price
                    self.storeID = store_id
                    self.storeName = store["storeName"]
                    self.storeStatus = "ON"

        self.lowerPriceEver = float(
            data["cheapestPriceEver"]["price"]
        )


# =========================
# INTERFACE GRAPHIQUE
# =========================

fenetre = tk.Tk()
fenetre.title("Comparateur CheapShark")
fenetre.geometry("700x500")
fenetre.config(bg="#1e1e1e")

jeu_actuel = None
liste_jeux = []


# ===== Recherche =====

def rechercher():

    global jeu_actuel
    global liste_jeux

    nom = entry.get()

    if nom == "":
        messagebox.showerror("Erreur", "Entre un nom de jeu")
        return

    jeu_actuel = Recherche(nom)

    liste_jeux = jeu_actuel.chercherJeux()

    listbox.delete(0, tk.END)

    for jeu in liste_jeux[:20]:

        listbox.insert(tk.END, jeu["external"])


# ===== Sélection =====

def selectionner():

    global jeu_actuel
    global liste_jeux

    selection = listbox.curselection()

    if not selection:
        messagebox.showerror("Erreur", "Choisis un jeu")
        return

    index = selection[0]

    jeu_actuel.choisirJeu(index, liste_jeux)

    jeu_actuel.moinChere()

    resultat.config(
        text=str(jeu_actuel)
    )


# ===== Widgets =====

titre = tk.Label(
    fenetre,
    text="Comparateur de Prix Jeux Vidéo",
    font=("Arial", 20),
    bg="#1e1e1e",
    fg="white"
)

titre.pack(pady=20)

entry = tk.Entry(
    fenetre,
    width=40,
    font=("Arial", 14)
)

entry.pack(pady=10)

boutonRecherche = tk.Button(
    fenetre,
    text="Rechercher",
    command=rechercher,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12)
)

boutonRecherche.pack(pady=10)

listbox = tk.Listbox(
    fenetre,
    width=50,
    height=10,
    font=("Arial", 12)
)

listbox.pack(pady=10)

boutonChoix = tk.Button(
    fenetre,
    text="Voir le meilleur prix",
    command=selectionner,
    bg="#2196F3",
    fg="white",
    font=("Arial", 12)
)

boutonChoix.pack(pady=10)

resultat = tk.Label(
    fenetre,
    text="",
    font=("Arial", 12),
    bg="#1e1e1e",
    fg="white",
    justify="left"
)

resultat.pack(pady=20)

fenetre.mainloop()