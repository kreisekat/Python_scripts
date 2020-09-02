#!/usr/bin/env python

"""
Copyright (C) 2020, Katrin Kreisel

tss_mousekeep_filter.py is free software: you can redistribute it
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
#import matplotlib; matplotlib.use('agg')
#import matplotlib.pyplot as plt
#import numpy as np
#from matplotlib import rc
import sys
import csv
from operator import itemgetter
from pathlib import Path
#import tsv2csv as t2c



def filter_by_mousekeep(folder_path):
    """finds all *tss.tsv files in the given folder path, filters the entries by sorted_mousekeep.csv entries and generates new csv files from them."""
    import sys
    import pandas as pd
    all_tss_csv = ('*tss.csv')
    for csv in glob.glob(folder_path+all_tss_csv):
        print('csv file found:', csv)
        #csv_file = csv
        tss_csv = pd.read_csv(csv)
        mousekeep = pd.read_csv('sorted_mousekeep.csv')
        #print(csv_table)
        #print(mousekeep)
        #print('new df with these columns is setup:', tss_csv.columns)
        output = pd.DataFrame(columns=tss_csv.columns)
        #print('new output df:', output)
        # iterate over rows with iterrows()
        for index,row in mousekeep.iterrows():
            # access data using column names
            #print('mousekeep chr, start/stop are set for comparison:', index, row['Chr'], row['start'], row['stop'])
            mousekeep_chr = row['Chr']
            mousekeep_start = row['start']
            mousekeep_stop = row['stop']

            for index,row in tss_csv.iterrows():
                #print('tss values for comparison are set:', index, row['Chromosome'], row['Gene Start'], row['Gene End'])
                tss_chr = row['Chromosome']
                tss_start = row['Gene Start']
                tss_stop = row['Gene End']
                if mousekeep_chr != tss_chr:
                    #print('chr matches')
                    if tss_start >= mousekeep_start:
                        #print('TSS start position lies after mousekeep start or is equal')
                        if tss_stop <= mousekeep_stop:
                            print('TSS chr matched with mousekeep entry and start stop lies withing gene start and stop. --> Entry appended to output')
                            output = output.append(row)
                            #print('new output:', output)

        filename_pattern = csv.split('.')[-2:-1]
        print('filename pattern:', filename_pattern)
        filename = []
        filename.append('_'.join(filename_pattern)+"_filtered_mousekeep.csv")
        print('Generating the file:', filename)
        output.to_csv("".join(filename),index=False)




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

    parser = argparse.ArgumentParser(prog=sys.argv[0], description="""tss_sum.py
                                         takes a ..._tss.csv file with these columns: Gene ID	Description	Chromosome	Gene Start	Gene End	Strand	-10000:-9501	-9500:-9001	-9000:-8501	-8500:-8001	-8000:-7501	-7500:-7001	-7000:-6501	-6500:-6001	-6000:-5501	-5500:-5001	-5000:-4501	-4500:-4001	-4000:-3501	-3500:-3001	-3000:-2501	-2500:-2001	-2000:-1501	-1500:-1001	-1000:-501	-500:-1	0:499	500:999	1000:1499	1500:1999	2000:2499	2500:2999	3000:3499	3500:3999	4000:4499	4500:4999	5000:5499	5500:5999	6000:6499	6500:6999	7000:7499	7500:7999	8000:8499	8500:8999	9000:9499	9500:9999
                                         filters the entries for matches with the 27 murine house keeping genes in the file sorted_mousekeeping.csv, returns new *_mousekeep.csv file""")

    parser.add_argument("-p", "--folder_path", required=True, help="""Please specifcy the path to the folder with name_tss.csv files""")


    try:
        args = parser.parse_args()
        print(args)
        print(args.folder_path)
        if not (args.folder_path):
            parser.error("Please specify the path to the folder with name_tss.csv files.")
        else:
            filter_by_mousekeep(args.folder_path)
            print('all *tss.csv files were filtered by sorted_mousekeep.csv')
            #csv_conversion(args.folder_path)
            #print('all *tss.tsv files were used to generate *.csv files')
            #sum_col(args.folder_path)
            #print('all *tss.csv files were visualized.')

    except IOError as e:
        parser.error(str(e))

if __name__ == "__main__":
        main()
