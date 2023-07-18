from helpers import exception_handler, show_message

URL = "https://api.edamam.com/api/recipes/v2?type=public"
APP_ID = "e93629f9"
APP_KEY = "5294032d759309c54ca82c88ac027bc3"


def search_recipes(ingredient, params_dict):
    # Set the API parameters
    params = {
        "q": ingredient,
        "app_id": APP_ID,
        "app_key": APP_KEY
    }
    for arg in params_dict:
        if params_dict[arg] != "" and params_dict[arg] != [] and params_dict[arg] != [""]:
            params[arg] = params_dict[arg]
    # Make the API request
    response, message = exception_handler(URL, params=params)
    # Process the response
    if response.status_code == 200:
        data = response.json()
        recipes = data["hits"]
        print(recipes)
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
            print(f"Restrictions: {recipe['recipe']['healthLabels']}")
            print(f"Cuisine: {recipe['recipe']['cuisineType']}")
            print(f"Meal: {recipe['recipe']['mealType']}")
            print(f"Calories: {round(recipe['recipe']['calories'], 2)} kcal")
            # Extract relevant recipe information
            recipe_list.append({
                "recipe_name": recipe["recipe"]["label"],
                "recipe_url": recipe["recipe"]["url"],
                "recipe_ingredients": recipe["recipe"]["ingredientLines"],
                "diet": recipe['recipe']['dietLabels'],
                "restrictions": recipe['recipe']['healthLabels'],
                "meal": recipe['recipe']['mealType'],
                "cuisine": recipe['recipe']['cuisineType'],
                "calories": round(recipe["recipe"]["calories"], 2),
                "small_img": recipe['recipe']['images']["SMALL"]['url']
            })
        # print(sorted(recipe_list, key=lambda d: d['recipe_name']))
        return sorted(recipe_list, key=lambda d: d['recipe_name'])
    else:
        show_message(message, "error")
        return []


