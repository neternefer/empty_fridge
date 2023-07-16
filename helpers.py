import constants
import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


APP_ID = "0622cbf0"
APP_KEY = "20bcc138460c6158d0026a33d31fcb1e"
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


def exception_handler(url, params):
    message = ""
    try:
        response = requests.get(url, params)
    except requests.exceptions.HTTPError as err:
        print("Bad Status Code", err.args[0])
        message = "There has been a problem with your request. Please try again later."
        show_message(message, "error")
        raise err
    except requests.exceptions.RequestException as errx:
        print("Exception request", errx)
        message = "There has been a problem with your request. Please try again later."
        show_message(message, "error")
        raise errx
    return response, message


def show_message(msg, msg_type):
    # Show error message in case of request/http errors
    if msg:
        root = Tk()
        messagebox.showerror("showerror", msg) if type == "error" else messagebox.showinfo("showinfo", msg)


def get_demo_data(url, params):
    response, message = exception_handler(url, {})
    data = response.json()
    diet = data["paths"]["/api/recipes/v2"]["get"]["parameters"][7]["items"]["enum"]
    health = data["paths"]["/api/recipes/v2"]["get"]["parameters"][8]["items"]["enum"]
    cuisine = data["paths"]["/api/recipes/v2"]["get"]["parameters"][9]["items"]["enum"]
    meal = data["paths"]["/api/recipes/v2"]["get"]["parameters"][10]["items"]["enum"]
    dish = data["paths"]["/api/recipes/v2"]["get"]["parameters"][11]["items"]["enum"]
    return diet, health, cuisine, meal, dish, message


get_demo_data(DEMO_URL, {})
