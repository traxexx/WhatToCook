#!/usr/bin/env python3

import json
import argparse
from FridgeUpdate import load_storage, storage_path

meat_gradients = ["pork", "beef", "lamb", "tofu", "egg", "chicken", "sausage", "shrimp"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", dest="time", default="999999", required=False, type=int,
        help="Time to cook (minutes)")
    parser.add_argument("-r", "--restrictions", dest="restrictions", default=None, required=False, type=str,
        help="Restrict type: veggie, meat or noodle")
    args = parser.parse_args()

    # loop through recipes to return cookable ones
    storage_map = load_storage()
    recipes = load_recipe()

    result = []
    for rname, rvals in recipes.items():
        if rvals["time"] > args.time:
            continue
        rgradients = rvals["ingradient"]
        if args.type is not None:
            rtype = tell_type(list(rgradients.keys()))
        if rtype != args.type:
            continue
        satisfy = True
        for gname, gquan in rgradients.items():
            if gname not in storage_map:
                satisfy = False
                break
            if storage_map[gname] < gquan:
                satisfy = False
                break
        if satisfy:
            result.append((rname,rvals["time"],rgradients))

    for r in result:
        print(r[0] + "   " + str(r[1]) + " min")
        print("  " + str(r[2]))

    return 0

def tell_type(gradients):
    if noodle in gradients:
        return "noodle"
        
    for g in gradients:
        for mg in meat_gradients:
            if mg in g:
                return "meat"
    return "veggie"

def load_recipe():
    recipe_path = "recipe.txt"
    recipes = {}
    infile = open(recipe_path, 'r')
    for line in infile:
        line = line.rstrip()
        if not line:
            continue

        if line.startswith('#'):
            rname, rtime = line.split(' ')
            rname = rname[1:]
            recipes[rname] = {}
            recipes[rname]["time"] = int(rtime)
        else:
            fields = line.split(' ')
            if len(fields) % 2 != 0:
                raise Exception("Malformatted gradient line: %s" % line)
            recipes[rname]["ingradient"] = {}
            for i in range(0,len(fields), 2):
                recipes[rname]["ingradient"][fields[i]] = int(fields[i+1])
                i += 1
    infile.close()
    return recipes

if __name__ == "__main__":
    main()