import tkinter
import webbrowser

from helpers import *
from search_recipes import *
from tkinter import ttk, LEFT
from tkinter import messagebox
from tkinter.ttk import Button
from PIL import ImageTk, Image
from urllib.request import urlopen

WELCOME = setup()
DEMO_URL = "https://api.edamam.com/doc/open-api/recipe-search-v2.json"

# For populating gui combos
diet, health, cuisine, meal, dish, message = get_demo_data(DEMO_URL, {})


def combo_select(my_combo):
    val = my_combo.get()
    index = my_combo.current()
    return val, index


def create_link_btn(url):
    link_btn = tkinter.Button(buttons_frame, text="View recipe", command=lambda: view_recipe(url))
    link_btn.grid(row=0, column=0, sticky="news", padx=20, pady=10)


def create_select_btn(my_combo, results, accepted):
    btn = Button(info_frame, text="Choose your recipe",
                 command=lambda: create_recipe(my_combo, results, accepted))
    btn.grid(row=0, column=1, padx=10)


def create_save_btn(my_combo, my_list):
    save_btn = tkinter.Button(buttons_frame, text="Save recipe", command=lambda: save_recipe(my_combo, my_list))
    save_btn.grid(row=1, column=0, sticky="news", padx=20, pady=10)


def create_recipe_select(labels, results, accepted):
    info_combobox = ttk.Combobox(info_frame, values=labels)
    info_combobox.grid(row=0, column=0)
    create_select_btn(info_combobox, results, accepted)


def create_recipe(my_combo, my_list, accepted):
    ing_text = ""
    val, index = combo_select(my_combo)
    ing_list = my_list[index].get("recipe_ingredients")
    for el in ing_list:
        ing_text += ("- " + el + "\n")
    recipe_text = val.upper() + "\n\n" + ing_text
    recipe_text += f"\n\n{my_list[index].get('calories')} kcal" if accepted else recipe_text
    recipe_label["text"] = recipe_text
    recipe_url = my_list[index].get("recipe_url")
    recipe_img_url = my_list[index].get("small_img")
    add_recipe_img(recipe_img_url)
    create_link_btn(recipe_url)
    create_save_btn(my_combo, my_list)


def view_recipe(url):
    webbrowser.open(url)


def save_recipe(my_combo, my_list):
    # Saves current recipe in the current folder
    val, index = combo_select(my_combo)
    with open(f'{val}.txt', 'w') as my_recipes:
        recipe = f'{val} \n-URL: {my_list[index].get("recipe_url")}  \n'
        if len(my_list[index].get("diet")) > 0:
            recipe += '-Diet: '
            for dietary in my_list[index].get("diet"):
                recipe += dietary + ", "
            recipe = recipe[:-2]
            recipe += '\n'
        recipe += f'-Cuisine: {my_list[index].get("cuisine")[0]} \n-Calories: {my_list[index].get("calories")} \n\n'
        recipe += '- Ingredients:\n'
        for ing in my_list[index].get("recipe_ingredients"):
            recipe += f'\t-{ing}\n'
        my_recipes.write(recipe)


def add_recipe_img(url):
    data = urlopen(url)
    raw_data = data.read()
    data.close()
    photo = ImageTk.PhotoImage(data=raw_data)
    img_label = tkinter.Label(result_frame, image=photo)
    img_label.image = photo
    img_label.grid(row=1, column=0, padx=5, pady=5)
    return img_label


def enter_data():
    # if accepted, include search for nutrition facts in api call
    accepted = accept_var.get()
    ingredient = first_ingredient_entry.get()
    combos = [diet_combobox, meal_combobox, cuisine_combobox, restrictions_combobox]
    inputs = {
        "dietLabels": [combo_select(diet_combobox)[0]],
        "mealType": combo_select(meal_combobox)[0],
        "cuisineType": combo_select(cuisine_combobox)[0],
        "healthLabels": combo_select(restrictions_combobox)[0]
    }
    if not ingredient:
        tkinter.messagebox.showwarning(title="Error", message="An ingredient is required.")
        return
    else:
        result_list = search_recipes(ingredient, inputs)
        if len(result_list) > 0:
            label_list = [r["recipe_name"] for r in result_list]
            recipe_label["text"] = "We've found some recipes for you"
            create_recipe_select(label_list, result_list, accepted)
        else:
            recipe_label["text"] = 'No recipes were found. No, you can\'t eat salamanders'
            show_message('No recipes were found. No, you can\'t eat salamanders', "info")
        first_ingredient_entry.delete(0, END)
        for combo in combos:
            combo.set("")


# Tkinter setup
window = tkinter.Tk()
window.title("Empty Fridge")
window.geometry("900x600")
window.resizable(False, False)

style = ttk.Style(window)
style.theme_use("default")

frame = tkinter.Frame(window)
frame.config(height=600, width=900)
frame.pack()
frame.pack_propagate(False)

# Left Frame with input fields
interface_frame = tkinter.LabelFrame(frame, width=450, height=500)
interface_frame.grid(rowspan=6, column=0, padx=10, pady=5)

# Right Frame with either a welcome message, result list or a single recipe information
result_frame = tkinter.LabelFrame(frame, borderwidth=0, width=450, height=500)
result_frame.grid(row=0, column=1, padx=10, pady=5)
result_frame.grid_propagate(False)

# Right Frame first child - empty at the start, with info about recipes found after API call
info_frame = tkinter.LabelFrame(result_frame, borderwidth=0, highlightthickness=0)
info_frame.grid(row=0, column=0, padx=5, pady=(80, 15))

recipe_label = tkinter.Label(result_frame, text=WELCOME, wraplength=300, justify=LEFT)
recipe_label.grid(row=2, column=0, padx=(10, 5))

# ADDING A SCROLLBAR
# my_scrollbar = Scrollbar(result_frame,orient="vertical")
# my_scrollbar.grid(row=2, column=1)

ing_label = tkinter.Label(result_frame, justify=LEFT)
ing_label.grid(rowspan=6, column=0)

buttons_frame = tkinter.LabelFrame(result_frame, borderwidth=0)
buttons_frame.grid(row=1, column=1, padx=5)

# Left Frame first child with input fields for ingredient(s)
ingredients_frame = tkinter.LabelFrame(interface_frame, borderwidth=0)
ingredients_frame.grid(row=0, column=0, padx=5, pady=5)

# Ingredients Frame children
first_ingredient_label = tkinter.Label(ingredients_frame, text="Ingredient")
first_ingredient_label.grid(row=0, columnspan=2)
first_ingredient_entry = tkinter.Entry(ingredients_frame)
first_ingredient_entry.grid(row=1, columnspan=2)

# Left Frame second child with dropdown option for choosing cuisine and/or diet type
type_frame = tkinter.LabelFrame(interface_frame)
type_frame.grid(row=2, column=0, padx=5, pady=5)

# Type Frame children
meal_label = tkinter.Label(type_frame, text="Meal")
meal_label.grid(row=0, column=0)
meal_combobox = ttk.Combobox(type_frame, values=meal)
meal_combobox.grid(row=1, column=0)

cuisine_label = tkinter.Label(type_frame, text="Cuisine")
cuisine_label.grid(row=0, column=1)
cuisine_combobox = ttk.Combobox(type_frame, values=cuisine)
cuisine_combobox.grid(row=1, column=1)

diet_label = tkinter.Label(type_frame, text="Diet")
diet_label.grid(row=2, column=0)
diet_combobox = ttk.Combobox(type_frame, values=diet)
diet_combobox.grid(row=3, column=0)

restrictions_label = tkinter.Label(type_frame, text="Restrictions")
restrictions_label.grid(row=2, column=1)
restrictions_combobox = ttk.Combobox(type_frame, values=health)
restrictions_combobox.grid(row=3, column=1)

# Set children frames padding
for widget in ingredients_frame.winfo_children():
    widget.grid_configure(padx=20, pady=7.5)

for widget in type_frame.winfo_children():
    widget.grid_configure(padx=15, pady=7.5)

# Left Frame third child with checkbox for nutrition facts
terms_frame = tkinter.LabelFrame(interface_frame)
terms_frame.grid(row=4, column=0, sticky="news", padx=5, pady=5)

accept_var = tkinter.StringVar(value="Not Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text="Show nutrition facts",
                                  variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
terms_check.grid(row=0, column=0, pady=5)

# Left Frame fourth child - search button for making API call
button = ttk.Button(interface_frame, text="Search for recipes", command=enter_data)
button.grid(row=5, column=0, padx=20, pady=5)

# Start program
window.mainloop()
