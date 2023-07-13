import requests

URL = "https://api.edamam.com/api/recipes/v2?type=public"
APP_ID = "2f5152e5"
APP_KEY = "ffe81e3b539b9d8f5225b886b4ef7aa1"


def search_recipes(ingredient, **kwargs):
    # Set the API parameters
    params = {
        "q": ingredient,
        "app_id": APP_ID,
        "app_key": APP_KEY
    }
    for arg in kwargs:
        if kwargs[arg] != "" and kwargs[arg] != [] and kwargs[arg] != [""]:
            params[arg] = kwargs[arg]
    # Make the API request
    response = requests.get(URL, params=params)
    # Process the response
    if response.status_code == 200:
        data = response.json()
        recipes = data["hits"]
        if len(recipes) == 0:
            print("No recipes were found to match your search")
            return []
        recipe_list = []
        for recipe in recipes:
            # Display the recipe information
            print(f"Recipe: {recipe['recipe']['label']}")
            print(f"URL: {recipe['recipe']['url']}")
            print("Ingredients:")
            for ing in recipe['recipe']['ingredientLines']:
                print("- " + ing)
            print()
            print(f"Diet: {recipe['recipe']['dietLabels']}")
            print(f"Cuisine: {recipe['recipe']['cuisineType']}")
            print(f"Meal: {recipe['recipe']['mealType']}")
            print(f"Calories: {round(recipe['recipe']['calories'], 2)} kcal")
            # Extract relevant recipe information
            recipe_list.append({
                "recipe_name": recipe["recipe"]["label"],
                "recipe_url": recipe["recipe"]["url"],
                "recipe_ingredients": recipe["recipe"]["ingredientLines"],
                "diet": recipe['recipe']['dietLabels'],
                "meal": recipe['recipe']['mealType'],
                "cuisine": recipe['recipe']['cuisineType'],
                "calories": round(recipe["recipe"]["calories"], 2)
            })
        print(sorted(recipe_list, key=lambda d: d['recipe_name']))
        return sorted(recipe_list, key=lambda d: d['recipe_name'])
    else:
        print("Error:", response.status_code)

# search_recipes("ham")
# Prompt the user for inputs
# ingredient = input("What ingredients do you have? ")
# dietary_requirement = input("Do you have any dietary requirements?")
# meal_type = input("Is it for breakfast, lunch, or dinner?")
# cuisine_type = input("What cuisine would you like?")
# # Call the function with appropriate arguments
# if dietary_requirement.lower() == 'no':
#     search_recipes(ingredient, None, meal_type, cuisine_type)
# else:
#     search_recipes(ingredient, dietary_requirement, meal_type, cuisine_type)
#
# # compile results and order
# results = search_recipes(ingredient, dietary_requirement, meal_type,
#                          cuisine_type)
# # order by the recipe name alphabetically
# results = sorted(results, key=lambda d: d['recipe_name'])
