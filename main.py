import requests

name = ""
#str(input("entrer un nom de film en minscule : (batman) :\n"))

r = requests.get(f'https://www.cheapshark.com/api/1.0/games?title=batman', auth=('user','pass'))
data = r.json()

def retourner_titre_jeu(data):
    for n in range(len(data)):
        print(data[n]["external"])
    return 

retourner_titre_jeu(data)
