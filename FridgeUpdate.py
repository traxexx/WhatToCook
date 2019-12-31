#!/usr/bin/env python3

import argparse
import json
import logging

storage_path = "storage.json"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", default="fridge-update.txt", required=False, 
        help="Input list of added ingredients")
    args = parser.parse_args()

    infile = open(args.input, 'r')
    update_storage(infile)
    infile.close()

    return 0

def update_storage(infile):
    storage_map = load_storage()
    for line in infile:
        line = line.rstrip()
        iname, iquan = line.split(' ')
        iquan = int(iquan)
        if iname not in storage_map:
            logging.warning("Adding new item: %s" % iname)
            storage_map[iname] = 0
        storage_map[iname]+= iquan
        logging.info("Updated %s with %d" % (iname, iquan))
    outfile = open(storage_path, 'w')
    json.dump(storage_map, outfile)
    outfile.close()

def load_storage():
    infile = open(storage_path, 'r')
    injson = json.load(infile)
    infile.close()
    return injson

if __name__ == "__main__":
    main()