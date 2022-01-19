import pandas as pd
import requests


def recipe_search(ingredient, meal_type, cuisine_type, calories, allergies):
    """

    :param ingredient: an input string e.g. chicken
    :param meal_type: an input string e.g. dinner
    :param cuisine_type: an input string e.g. american
    :param calories: a float that searches a value less than the input value
    :param allergies: a string input e.g. dairy-free
    :return: uses the app_id and app_key including inputs to access first layer of the dictionary.
    if statement exists for those who do not have allergies.
    """
    app_id = '0659befd'
    app_key = '363a950b1fbf10052d4cb93fbb353b65'

    if allergies != 'no':
        url = "https://api.edamam.com/api/recipes/v2?type=public&q={}&app_id={}&app_key={}&health={}&cuisineType={}&mealType={}&calories={}".format(
            ingredient, app_id, app_key, allergies, cuisine_type, meal_type, calories)
    else:
        url = "https://api.edamam.com/api/recipes/v2?type=public&q={}&app_id={}&app_key={}&cuisineType={}&mealType={}&calories={}".format(
            ingredient, app_id, app_key, cuisine_type, meal_type, calories)

    result = requests.get(url).json()
    return result['hits']


def run():
    """

    :return: using the input parameters, the function loops through each sub-dictionary to find the ingredient,
    meal type, cuisine type, calories and allergies. the results are printed out given the criteria and sorted according
    to calories - low to high.
    """
    ingredient = input('What ingredient would you like to search for?')
    meal_type = input('What meal type would you like?')
    cuisine_type = input("What cuisine would you prefer?")
    calories = input("Does it need to be less than a certain amount of calories?")
    allergies = input("Do you have any allergies?")

    results = recipe_search(ingredient, meal_type, cuisine_type, calories, allergies)
    list_result = []
    for result in results:
        recipe = result['recipe']
        if recipe['calories'] < float(calories):
            list_result.append((recipe['label'], recipe['calories'], recipe['url']))

    recipe_list_final = pd.DataFrame(data=list_result, columns=['label', 'calories', 'url'])
    recipe_list_final.sort_values('calories', ascending=True, inplace=True)
    pd.set_option('display.expand_frame_repr', True)
    print(recipe_list_final)
    return recipe_list_final


def export_to_csv(result):
    """

    :param result: is the dataframe results from the run function
    :return: csv output that is exported to a directory of choice
    """
    directory = input("Where do you want to save this file? Paste directory")
    result.to_csv(r'{}\recipe_list.csv'.format(directory))



if __name__ == "__main__":
    try:
        list_recipes = run()
    except TypeError:
        print("Wrong inputs given, please try again.")
    else:
        export_to_csv(list_recipes)

