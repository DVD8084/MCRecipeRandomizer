import json
import os
import sys
import zipfile
from time import strftime

import internals

# Check arguments
if len(sys.argv) < 2:
    datapack_path = strftime('scrambled-outputs-%Y%m%d-%H%M%S.zip')
    print(f'Using default datapack name: ./{datapack_path}')
else:
    datapack_path = sys.argv[1]

recipe_data = internals.load_recipes()
outputs = internals.load_outputs()

# Create the zip file and write the pack.mcmeta
try:
    zip_file = zipfile.ZipFile(datapack_path, 'x', zipfile.ZIP_DEFLATED, False)
except FileExistsError:
    print(f'{datapack_path} already exists.')
    exit()

data_folder = os.path.join('data', 'minecraft', 'recipes')
zip_file.writestr('pack.mcmeta', json.dumps({
    'pack': {
        'pack_format': 5,
        'description': 'Randomize all the outputs!'
    }
}))

max_name_length = 0
for i, (filename, recipe) in enumerate(recipe_data.items()):
    if max_name_length < len(filename):
        max_name_length = len(filename)

    recipe = internals.scramble_output(recipe, outputs)
    recipe['group'] = internals.get_output(recipe)
    zip_file.writestr(os.path.join(data_folder, filename), json.dumps(recipe))

    sys.stdout.write('\r' + filename + ' ' * (max_name_length - len(filename)))
    sys.stdout.flush()

zip_file.close()

sys.stdout.write('\r' + ' ' * max_name_length + '\r')
sys.stdout.flush()
print('Done!')
