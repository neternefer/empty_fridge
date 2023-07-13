import constants
import requests

APP_ID = "2f5152e5"
APP_KEY = "ffe81e3b539b9d8f5225b886b4ef7aa1"
DEMO_URL = "https://api.edamam.com/doc/open-api/recipe-search-v2.json"


def setup():
    """Set up the console window, introduce the user to the application"""
    welcome = """
    Hungry and staring at your almost empty fridge? \n
    We know that feeling!\n
    Take a closer look, there must be something in there.\n
    Found it? Our virtual assistant will find some recipes for you.\n
    Unless it's a salamander. They're not edible, you know?\n
    """
    return welcome


def get_demo_data(url):
    response = requests.get(url)
    data = response.json()
    diet = data["paths"]["/api/recipes/v2"]["get"]["parameters"][7]["items"]["enum"]
    health = data["paths"]["/api/recipes/v2"]["get"]["parameters"][8]["items"]["enum"]
    cuisine = data["paths"]["/api/recipes/v2"]["get"]["parameters"][9]["items"]["enum"]
    meal = data["paths"]["/api/recipes/v2"]["get"]["parameters"][10]["items"]["enum"]
    dish = data["paths"]["/api/recipes/v2"]["get"]["parameters"][11]["items"]["enum"]
    return diet, health, cuisine, meal, dish
