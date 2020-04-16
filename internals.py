import json
import os
from random import choice


def load_recipes():
    recipe_blacklist = list(map(lambda s: s.strip(), open(
        'recipe_blacklist.txt', 'r').readlines()))
    recipe_data = {}  # key is the filename, value is the object data.
    for file_handler in os.scandir('recipes/'):
        (basename, ext) = os.path.splitext(file_handler.name)
        if ext == '.json':
            file_data = json.load(open(file_handler.path, 'r'))
            # Some special recipes don't have a result...
            # And we don't scramble files in the blacklist too!
            if file_data.get('result') is None or basename in recipe_blacklist:
                continue
            recipe_data[file_handler.name] = file_data
    return recipe_data


def load_outputs():
    outputs = list(map(lambda s: s.strip(), open(
        'id_list.txt', 'r').readlines()))
    output_blacklist = list(map(lambda s: s.strip(), open(
        'output_blacklist.txt', 'r').readlines()))
    outputs = [x for x in outputs if x not in output_blacklist]
    return outputs


def load_inputs():
    items = list(map(lambda s: s.strip(), open(
        'id_list.txt', 'r').readlines()))
    tags = list(map(lambda s: s.strip(), open(
        'tag_list.txt', 'r').readlines()))
    input_blacklist = list(map(lambda s: s.strip(), open(
        'input_blacklist.txt', 'r').readlines()))
    items = [x for x in items if x not in input_blacklist]
    tags = [x for x in tags if x not in input_blacklist]
    inputs = list(map(lambda s: {'item': s}, items)) \
             + list(map(lambda s: {'tag': s}, tags))
    return inputs


def get_output(recipe):
    result = recipe.get('result')
    # Crafting recipes need an object for the result and everything else needs a string.
    if type(result) is dict:
        return result['item']
    elif type(result) is str:
        return result


def scramble_output(recipe, outputs):
    random_item = choice(outputs)
    result = recipe.get('result')
    # Crafting recipes need an object for the result and everything else needs a string.
    if type(result) is dict:
        recipe['result']['item'] = random_item
    elif type(result) is str:
        recipe['result'] = random_item
    return recipe


def scramble_input(recipe, inputs):
    recipe_type = recipe.get('type')
    # For shaped recipes, we leave the shape as-is, but change the ingredients.
    if recipe_type == 'minecraft:crafting_shaped':
        recipe_key = recipe.get('key')
        for key in recipe_key.keys():
            random_item = choice(inputs)
            recipe['key'][key] = random_item
    elif recipe_type == 'minecraft:crafting_shapeless':
        # For shapeless recipes, we look for the ingredients.
        ingredients = recipe.get('ingredients')
        if type(ingredients) is dict:
            # Got our ingredient, now change it to something else.
            recipe['ingredients'] = choice(inputs)
        else:
            # Replace all ingredients with another ones.
            # This feels like an unnecessarily complicated way of doing it, though.
            choices = dict()
            for i, ingredient in enumerate(ingredients):
                if type(ingredient) is dict:
                    ingredient = list(ingredient.values())[0]
                    if ingredient not in choices:
                        choices[ingredient] = choice(inputs)
                    recipe['ingredients'][i] = choices[ingredient]
                else:
                    for j, sub_ingredient in enumerate(ingredient):
                        sub_ingredient = list(sub_ingredient.values())[0]
                        if sub_ingredient not in choices:
                            choices[sub_ingredient] = choice(inputs)
                        recipe['ingredients'][i][j] = choices[sub_ingredient]
    else:
        # For the rest, we look for an ingredient. Just one.
        ingredient = recipe.get('ingredient')
        if type(ingredient) is dict:
            # Got our ingredient, now change it to something else.
            recipe['ingredient'] = choice(inputs)
        else:
            # Replace all possible ingredients with something else.
            recipe['ingredient'] = [choice(inputs) for _ in ingredient]
    return recipe
