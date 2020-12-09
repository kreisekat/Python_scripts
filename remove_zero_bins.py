#!/usr/bin/env python

"""
Copyright (C) 2020, Katrin Kreisel

remove_zero_bins.py is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

#import all needed packages
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


#convert all -tss_txt. files in a folder to csv
def txt2tsv(folder_path):
    """finds all files in the specified folder ending with .txt and renames them to .tsv files."""
    print('in txt2tsv')
    #print(folder_path)
    import sys

    types = ('*.txt')
    #print(types)
    for filetype in types:
        #print(filetype)
        for files in glob.glob(folder_path+filetype):
            #print(folder_path+filetype)
            #print("Found the file", files)
            p = Path(files)
            #print(p)
            p.rename(p.with_suffix('.tsv'))
            #print(p)

def csv_conversion(folder_path):
    """finds all *.tsv files in the given folder path and generates csv files
    from them."""
    import sys
    import pandas as pd
    print('in csv conversion')
    all_tss_tsv = ('*.tsv')
    for tsv in glob.glob(folder_path+all_tss_tsv):
        print('tsv file found', tsv)
        tsv_file = tsv
        csv_table = pd.read_csv(tsv_file,sep='\t', skiprows=8)
        filename_pattern = tsv.split('.')[-2:-1]
        #print(filename_pattern)
        filename = []
        filename.append('_'.join(filename_pattern)+".csv")
        print('Generating the file:', filename)
        csv_table.to_csv("".join(filename),index=False)

#for each *tss.tsv or *opp_tss.csv import as pd df, select df with only bins, sum reads in each bin and write new line to a new .csv
def sum_col(folder_path):
    """takes all *.csv files in the specified directory, converts the content
    into a pandas dataframe and removes additional columns that go beyond ID,
    description, chr, start, stop, end, strand and 40bins (46 columns total) """
    print('in sum_col')
    all_tss_csv = ('*.csv')
    for csv_file in glob.glob(folder_path+all_tss_csv):
        print('csv file found:', csv_file)
        csv_df = pd.DataFrame()
        csv_df = pd.read_csv(csv_file)
        #removing columns for GeneID, gene Start/End and Strand
        csv_df = csv_df[[ 'Gene ID', 'Description',	'Chromosome', 'Gene Start',
        'Gene End', 'Strand', '-10000:-9501', '-9500:-9001', '-9000:-8501', '-8500:-8001',
       '-8000:-7501', '-7500:-7001', '-7000:-6501', '-6500:-6001',
       '-6000:-5501', '-5500:-5001', '-5000:-4501', '-4500:-4001',
       '-4000:-3501', '-3500:-3001', '-3000:-2501', '-2500:-2001',
       '-2000:-1501', '-1500:-1001', '-1000:-501', '-500:-1', '0:499',
       '500:999', '1000:1499', '1500:1999', '2000:2499', '2500:2999',
       '3000:3499', '3500:3999', '4000:4499', '4500:4999', '5000:5499',
       '5500:5999', '6000:6499', '6500:6999', '7000:7499', '7500:7999',
       '8000:8499', '8500:8999', '9000:9499', '9500:9999']]

        csv_name_pattern = csv_file.split('/')[-1:]
        csv_name_pattern = ''.join(csv_name_pattern)
        csv_name_pattern = csv_name_pattern.split('.')[-2:-1]
        #print('csv name pattern:', csv_name_pattern)
        csv_df.to_csv(csv_name_pattern + '.csv')





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
                                         takes a ....txt file with these columns: Gene ID	Description	Chromosome	Gene Start	Gene End	Strand	-10000:-9501	-9500:-9001	-9000:-8501	-8500:-8001	-8000:-7501	-7500:-7001	-7000:-6501	-6500:-6001	-6000:-5501	-5500:-5001	-5000:-4501	-4500:-4001	-4000:-3501	-3500:-3001	-3000:-2501	-2500:-2001	-2000:-1501	-1500:-1001	-1000:-501	-500:-1	0:499	500:999	1000:1499	1500:1999	2000:2499	2500:2999	3000:3499	3500:3999	4000:4499	4500:4999	5000:5499	5500:5999	6000:6499	6500:6999	7000:7499	7500:7999	8000:8499	8500:8999	9000:9499	9500:9999
                                         Will remove any additional columns that may have been added by make_heatmap script)""")

    parser.add_argument("-p", "--folder_path", required=True, help= """Please specifcy the path to the folder with *tss.txt files""")


    try:
        args = parser.parse_args()
        print(args)
        print(args.folder_path)
        if not (args.folder_path):
            parser.error("Please specify the path to the folder with name.txt files.")
        else:
            txt2tsv(args.folder_path)
            print('all *.txt files were renamed to *.tsv files')
            csv_conversion(args.folder_path)
            print('all *.tsv files were used to generate *.csv files')
            sum_col(args.folder_path)
            print('all *.csv files were cut to 46 columns')

    except IOError as e:
        parser.error(str(e))

if __name__ == "__main__":
        main()
