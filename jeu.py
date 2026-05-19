import requests

class Recherche():
    def __init__(self,gameName=""):
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
            f"[id: {self.gameId}] - | {self.name} | "
            f"- LowerPriceEVER : {self.lowerPriceEver}$ "
            f"- LowerPriceNOW : {self.lowerPriceNow}$ "
            f"- StoreID : {self.storeID} "
            f"- StoreName : {self.storeName} "
            f"- Status : {self.storeStatus}"
        )

    def bonJeu(self):
        r = requests.get(f'https://www.cheapshark.com/api/1.0/games?title={self.gameName}', auth=('user','pass'))
        data = r.json()
        enCours = True
        
        print("---------- Choisir le bon jeu ----------\n")

        for n in range(len(data)):
            print(f"{n+1}. {data[n]["external"]}")

        while enCours:
            choix = int(input(">> Entrer nombre du Titre choisie : "))
            self.name = data[choix-1]["external"]
            print(f"Vous avez choisie {self.name}!")
            _ = str(input("C'est bon ?(y/n) : "))
            enCours = False if _ == "y" else True

        self.gameId = data[choix-1]["gameID"]

        return

    def moinChere(self):
        r = requests.get(
            f'https://www.cheapshark.com/api/1.0/games?ids={self.gameId}'
        )

        data = r.json()
        data = data[self.gameId]

        lowest_price = 999999

        for deal in data["deals"]:

            store_id = deal["storeID"]

            q = requests.get(
                'https://www.cheapshark.com/api/1.0/stores'
            )

            stores = q.json()

            store = stores[int(store_id)]

            if store["isActive"] == 1:

                price = float(deal["price"])

                if price < lowest_price:

                    lowest_price = price

                    self.lowerPriceNow = price
                    self.storeID = store_id
                    self.storeName = store["storeName"]
                    self.storeStatus = "On"

        self.lowerPriceEver = float(
            data["cheapestPriceEver"]["price"]
        )

        print(self)
            


test = Recherche("Elden Ring")
test.bonJeu()
test.moinChere()