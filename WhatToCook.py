#!/usr/bin/env python3

import json
from FridgeUpdate import load_storage
recipe_path = "recipe.txt"

def main():
    # loop through recipes to return cookable ones
    storage_map = load_storage()

    infile = open(recipe_path, 'r')
    recipes = json.load(infile)
    infile.close()

    result = []
    for rname, rgradients in recipes.items():
        satisfy = True
        for gname, gquan in rgradients.items():
            if gname not in storage_map:
                satisfy = False
                break
            if storage_map[gname] < gquan:
                satisfy = False
                break
        if satisfy:
            result.append((rname,rgradients))

    for r in result:
        print(r)

    return 0

if __name__ == "__main__":
    main()