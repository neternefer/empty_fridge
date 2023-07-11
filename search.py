#first function asking for input for ingredient - fridge_item
import requests

def fridge_item():
  ingredient = input('What do you have in your fridge? ')
  return ingredient

# second function to call recipes with ingredient, specificing paramters for diet, cuisine, recipe url, recipe name, url. - search

def search(ingredient):
    app_key = 'f17b97e34db858e8b00b3fd21a13b307'
    app_id = 'd3ab7791'
    url = f'https://api.edamam.com/search?q={ingredient}&app_id={app_id}&app_key={app_key}'
    response = requests.get(url)
    data = response.json()
    # print('data:', data)
    if response.status_code == 200:
        recipes = data["hits"]
        if len(recipes) == 0:
            print("No recipes were found. No, we don't have {}".format(ingredient))
            return []
        recipe_list = []
        # print(recipes)
        for recipe in recipes:
            recipe_list.append({
            #'type': type(recipe),
            'recipe': recipe['recipe']["label"],
            'url': recipe['recipe']['url'],
            'diet': recipe['recipe']['dietLabels'],
            'cuisine': recipe['recipe']['cuisineType'],
        })
        return recipe_list
ingredient = fridge_item()
# print(fridge_item())

# results calls the function above
results = search(ingredient)

# order by the recipe name alphabetically
results = sorted(results, key=lambda d: d['recipe'])

# creating a string collection to collect the answers, this is a container for the answers
collection = ""

# looping through results to get them in order I want and adding them in the container
for result in results:
    collection += f'{result["recipe"]}\n   -{result["url"]} \n   -{result["diet"]} \n   -{result["cuisine"][0]}\n\n'

print(collection)

# saving the container with the results to a file
with open('recipe.txt', 'w') as recipes_collection:
    recipes_collection.write(collection)
