import requests
from pprint import pprint
ingredient = input('What do you have in your fridge?')
app_key= 'f17b97e34db858e8b00b3fd21a13b307'
app_id= 'd3ab7791'
url= f'https://api.edamam.com/search?q={ingredient}&app_id={app_id}&app_key={app_key}'
response = requests.get(url)
print(response)
recipe= response.json()
pprint(recipe)
