#!/usr/bin/env python

"""
Copyright (C) 2020, Katrin Kreisel

extract_top_n_rows.py is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""


import pandas as pd
import os
import glob
import matplotlib; matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
import sys
import csv
from operator import itemgetter
from pathlib import Path

def extract_topNrows(folder_path, number_of_rows):
    types = ('*mt_sorted.csv', '*nuc_sorted.csv')
    n = number_of_rows
    n_int = int(number_of_rows)
    for type in types:
        for file in glob.glob(folder_path+type):
            print('file found:', file)
            name_pattern = file.split('/')[-1:]
            name_pattern = ''.join(map(str, name_pattern))
            name_pattern = name_pattern[:-4]
            output_name = name_pattern+'_top_'+n+'.csv'
            #print('output name:', output_name)
            csv_df = pd.DataFrame()
            csv_df = pd.read_csv(file)
            output_df = pd.DataFrame()
            output_df = csv_df.head(n=n_int)
            #print(output_df)
            output_df.to_csv(output_name, index = False)

def main():
    print('in main')
    try:
        import argparse

    except ImportError:
        sys.stderr.write("[Error] The python module 'argparse' is not installed\n")
        sys.stderr.write("[--] Would you like to install it now using 'sudo easy_install' [Y/N]? ")
        answer = sys.stdin.readline()
        if answer[0].lower() == "y":
            sys.stderr.write("[--] Running 'sudo easy_install argparse'\n")
            from subprocess import call
            call(["sudo", "easy_install", "argparse"])
        else:
            sys.exit("[Error] Exiting due to missing dependency 'argparser'")

    parser = argparse.ArgumentParser(prog=sys.argv[0], description="""extract_top_n_rows.py goes through all *mt/nuc_sorted.csv and wirtes first n rows to new output csv""")

    parser.add_argument("-p", "--folder_path", required=True, help="""Please specifcy the path to the folder with *nuc/mt_sorted files""")
    parser.add_argument("-n", "--number_of_rows", required=True, help="""Please specifcy the number of rows you want to extract""")


    try:
        args = parser.parse_args()
        print(args)
        #print(args.folder_path)
        if not (args.folder_path):
            parser.error("Please specify the path to the folder with nuc/mt_sorted files.")
        if not (args.number_of_rows):
            parser.error("Please specify the the number of rows you want to extract from specified files.")
        else:
            extract_topNrows(args.folder_path, args.number_of_rows)
            print('top n rows were written to new output')
            #groupby_and_sort(args.folder_path)


    except IOError as e:
        parser.error(str(e))

if __name__ == "__main__":
        main()
