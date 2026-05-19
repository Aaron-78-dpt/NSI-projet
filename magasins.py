import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

r = requests.get('https://www.cheapshark.com/api/1.0/stores', auth=('user', 'pass'))
donnee = r.json()

print(donnee[0]['storeName'])

url_logo = "https://www.cheapshark.com" + donnee[0]['images']['banner']

reponse = requests.get(url_logo)

img = Image.open(BytesIO(reponse.content))
plt.imshow(img)
plt.axis('off')
plt.show()
