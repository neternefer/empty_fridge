import tkinter
import webbrowser
from tkinter.ttk import Label, Button

from helpers import *
from tkinter import ttk, LEFT
from tkinter import messagebox

from search_recipes import search_recipes

WELCOME = setup()
DEMO_URL = "https://api.edamam.com/doc/open-api/recipe-search-v2.json"

# For populating gui combos
diet, health, cuisine, meal, dish = get_demo_data(DEMO_URL)


def combo_select(my_combo):
    val = my_combo.get()
    index = my_combo.current()
    return val, index


def create_link_btn(url):
    link_btn = tkinter.Button(recipe_frame, text="View recipe", command=lambda: view_recipe(url))
    link_btn.grid(row=3, column=1, sticky="news", padx=20, pady=10)


def create_select_btn(my_combo, results, accepted):
    btn = Button(info_frame, text="Choose your recipe",
                 command=lambda: create_recipe(my_combo, results, accepted))
    btn.grid(row=1, column=1)


def create_save_btn(my_combo, my_list):
    save_btn = tkinter.Button(recipe_frame, text="Save recipe", command=lambda: save_recipe(my_combo, my_list))
    save_btn.grid(row=4, column=1, sticky="news", padx=20, pady=10)


def create_recipe_select(labels, results, accepted):
    info_combobox = ttk.Combobox(info_frame, values=labels)
    info_combobox.grid(row=1, column=0)
    create_select_btn(info_combobox, results, accepted)


def create_recipe(my_combo, my_list, accepted):
    ing_text = ""
    val, index = combo_select(my_combo)
    ing_list = my_list[index].get("recipe_ingredients")
    for el in ing_list:
        ing_text += ("- " + el + "\n")
    recipe_text = val.capitalize() + "\n\n" + ing_text
    recipe_text += f"\n\n{my_list[index].get('calories')} kcal" if accepted else recipe_text
    recipe_label["text"] = recipe_text
    recipe_url = my_list[index].get("recipe_url")
    create_link_btn(recipe_url)
    create_save_btn(my_combo, my_list)


def view_recipe(url):
    webbrowser.open(url)


def save_recipe(my_combo, my_list):
    val, index = combo_select(my_combo)
    with open(f'{val}.txt', 'w') as my_recipes:
        recipe = f'{val}\n   -{my_list[index].get("url")} \n   -{my_list[index].get("diet")} \n   -{my_list[index].get("cuisine")[0]}\n\n'
        my_recipes.write(recipe)


def enter_data():
    # if accepted, include search for nutrition facts in api call
    accepted = accept_var.get()
    ingredient = first_ingredient_entry.get()
    diet_reqs = [combo_select(diet_combobox)[0]]
    meal_type = combo_select(meal_combobox)[0]
    cuisine_type = combo_select(cuisine_combobox)[0]
    if not ingredient:
        tkinter.messagebox.showwarning(title="Error", message="An ingredient, meal type and cuisine are required.")
        return
    else:
        result_list = search_recipes(ingredient, health=diet_reqs, mealType=meal_type, cuisineType=cuisine_type)
        if len(result_list) > 0:
            label_list = [r["recipe_name"] for r in result_list]
            info_label["text"] = "We've found some recipes for you"
            create_recipe_select(label_list, result_list, accepted)
        else:
            info_label["text"] = 'No recipes were found. No, you can\'t eat salamanders'


# Tkinter setup
window = tkinter.Tk()
window.title("Empty Fridge")
frame = tkinter.Frame(window)
frame.config(height=50, width=60)  # doesn't help with jumping after search, solution needed
frame.pack()
# window.minsize(500, 300)
# window.maxsize(300, 300)

# Left Frame with input fields
interface_frame = tkinter.LabelFrame(frame, borderwidth=0, highlightthickness=0)
interface_frame.grid(row=0, column=0, padx=10, pady=10)
# interface_frame.config(height=25, width=60)

# Right Frame with either a welcome message, result list or a single recipe information
result_frame = tkinter.LabelFrame(frame, borderwidth=0, highlightthickness=0)
result_frame.grid(row=0, column=1, padx=10, pady=10)

# Right Frame first child - empty at the start, with info about recipes found after API call
info_frame = tkinter.LabelFrame(result_frame, borderwidth=0, highlightthickness=0)
info_frame.grid(row=0, column=0, padx=5, pady=5)
info_label = tkinter.Label(info_frame, font=("Arial", 10))
info_label.grid(row=0, column=0, padx=5)

# Right Frame second child with a welcome message or a single recipe information
recipe_frame = tkinter.LabelFrame(result_frame, borderwidth=0, highlightthickness=0)
recipe_frame.grid(row=1, column=0)
recipe_label = tkinter.Label(recipe_frame, text=WELCOME, justify=LEFT, wraplength=300)
recipe_label.grid(row=1, column=0, padx=5)
recipe_label.config(height=15, width=60)  # can be slightly larger height than 10 but the left frame jumps
ing_label = tkinter.Label(recipe_frame, justify=LEFT)
ing_label.grid(row=1, column=1)

# Left Frame first child with input fields for ingredient(s)
ingredients_frame = tkinter.LabelFrame(interface_frame)
ingredients_frame.grid(row=0, column=0, padx=5, pady=5)  # change row if needed

# Ingredients Frame children
first_ingredient_label = tkinter.Label(ingredients_frame, text="Ingredient")
first_ingredient_label.grid(row=0, column=0)
first_ingredient_entry = tkinter.Entry(ingredients_frame)
first_ingredient_entry.grid(row=1, column=0)

meal_label = tkinter.Label(ingredients_frame, text="Meal")
meal_label.grid(row=0, column=1)
meal_combobox = ttk.Combobox(ingredients_frame, values=meal)
meal_combobox.grid(row=1, column=1)

# Left Frame second child with dropdown option for choosing cuisine and/or diet type
type_frame = tkinter.LabelFrame(interface_frame)
type_frame.grid(row=2, column=0, padx=5, pady=5)

# Type Frame children
cuisine_label = tkinter.Label(type_frame, text="Cuisine")
cuisine_label.grid(row=0, column=0)
cuisine_combobox = ttk.Combobox(type_frame, values=cuisine)
cuisine_combobox.grid(row=1, column=0)

diet_label = tkinter.Label(type_frame, text="Diet")
diet_combobox = ttk.Combobox(type_frame, values=health)
diet_label.grid(row=0, column=1)
diet_combobox.grid(row=1, column=1)

# Set children frames padding
for widget in ingredients_frame.winfo_children():
    widget.grid_configure(padx=20, pady=7.5)

for widget in type_frame.winfo_children():
    widget.grid_configure(padx=15, pady=7.5)

# Left Frame third child with checkbox for nutrition facts
terms_frame = tkinter.LabelFrame(interface_frame)
terms_frame.grid(row=3, column=0, sticky="news", padx=5, pady=5)

accept_var = tkinter.StringVar(value="Not Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text="Show nutrition facts",
                                  variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
terms_check.grid(row=0, column=0)

# Left Frame fourth child - search button for making API call
button = tkinter.Button(frame, text="Search for recipes", command=enter_data)
button.grid(row=4, column=0, sticky="news", padx=20, pady=10)

# Start program
window.mainloop()
