import requests


class Recherche:

    def __init__(self, gameName=""):

        self.gameName = gameName

    def chercherJeux(self):

        r = requests.get(
            f"https://www.cheapshark.com/api/1.0/games?title={self.gameName}"
        )

        return r.json()

    def recupererDeals(self, gameID):

        r = requests.get(
            f"https://www.cheapshark.com/api/1.0/games?ids={gameID}"
        )

        data = r.json()[gameID]

        q = requests.get(
            "https://www.cheapshark.com/api/1.0/stores"
        )

        stores = q.json()

        deals_final = []

        for deal in data["deals"]:

            store_id = deal["storeID"]

            for store in stores:

                if store["storeID"] == store_id:

                    if store["isActive"] == 1:

                        deals_final.append({

                            "store": store["storeName"],

                            "price": float(deal["price"]),

                            "savings": round(
                                float(deal["savings"]), 2
                            ),

                            "dealID": deal["dealID"]
                        })

        deals_final.sort(
            key=lambda x: x["price"]
        )

        return deals_final