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

def match_gene_symbol(folder_path, tss_gene_list):
    #print('folderPath:', folder_path)
    #print('gene symbol list', tss_gene_list)
    for file in glob.glob(folder_path+'*sorted_top_*.csv'):
        #print('filename:', file)
        topN_df = pd.DataFrame()
        topN_df = pd.read_csv(file)
        #print('topN:', topN_df.head())
        name_pattern = file.split('/')[-1:]
        name_pattern = ''.join(map(str, name_pattern))
        name_pattern = name_pattern[:-4]
        output_name = name_pattern+'_genes.csv'

        for tss_gene_file in glob.glob(tss_gene_list+'refTSS_v3.1_mouse_annotation.csv'):
            tss_genes =  pd.DataFrame()
            tss_genes = pd.read_csv(tss_gene_file)
            #print('tss_genes:', tss_genes.head())
            tss_genes_filtered = pd.DataFrame()
            tss_genes_filtered = tss_genes.filter(['Transcript_name', 'Gene_name', 'Gene_symbol'])
            tss_genes_filtered['Gene ID'] = tss_genes['#refTSSID']
            merged = pd.merge(tss_genes_filtered, topN_df, on='Gene ID', suffixes=('_tss', '_topN'))
            print(merged.head())
            merged.to_csv(output_name)


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

    parser = argparse.ArgumentParser(prog=sys.argv[0], description="""matches gene symbol with tss gene ID""")

    parser.add_argument("-p", "--folder_path", required=True, help="""Please specifcy the path to the folder with *nuc/mt_sorted_top_n files""")
    parser.add_argument("-g", "--tss_gene_list", required=True, help="""Please specifcy the number of rows you want to extract""")


    try:
        args = parser.parse_args()
        print(args)
        #print(args.folder_path)
        if not (args.folder_path):
            parser.error("Please specify the path to the folder with nuc/mt_sorted files.")
        if not (args.tss_gene_list):
            parser.error("Please specify the path to the tss_gene_and_transcript_info file")
        else:
            match_gene_symbol(args.folder_path, args.tss_gene_list)
            print('matched gene symbol with tss gene ID and added it as a new column, wrote everything to new file')
            #groupby_and_sort(args.folder_path)


    except IOError as e:
        parser.error(str(e))

if __name__ == "__main__":
        main()
