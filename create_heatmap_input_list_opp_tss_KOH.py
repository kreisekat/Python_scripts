#!/usr/bin/env python3
# coding: utf-8
"""
Copyright (C) 2020, Katrin Kreisel

create_heatmap_input_list_opp_tss_KOH.py is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

import os
import sys
import glob
import argparse
import pandas as pd

class CreateFisherFile(object):

    def __init__(self, opts):
        self.filepath = opts.d

        if not self.filepath.endswith("/"):
            self.filepath += "/"

        print("file path being searched...{0}".format(self.filepath))
        self.gz_ending_remover = lambda x: x[:-3] if x.endswith('.gz') else x
        self.file_list_KOH_for = self._grab_filenames_KOH_for()
        self.file_list_KOH_rev = self._grab_filenames_KOH_rev()
        self.filename = self._generate_output_filename()
        self.df = self._create_dataframe()
        self._write_dataframe_to_disk()

    def _grab_filenames_KOH_for(self):
        import sys

        file_list_KOH_for = []
        types = ('*KOH*forward.bedgraph.gz', '*KOH*forward.bedgraph') # the tuple of file types, now only KOH forward
        for filetype in types:
            for files in glob.glob(self.filepath+filetype):
                print("files found ", files)
                if "*.fix" not in files:
                    file_list_KOH_for.append(files)# no more split command because we want the whole filepath, not only the file name

        if len(file_list_KOH_for) == 0:
            sys.exit("Cannot find KOH forward bedgraph files, please check the path and file name format.")

        return file_list_KOH_for


    def _grab_filenames_KOH_rev(self):
        import sys

        file_list_KOH_rev = []
        all_KOH_for = ('*KOH*forward.bedgraph')
        all_KOH_rev = ('*KOH*reverse.bedgraph')
        for KOH_for in glob.glob(self.filepath+all_KOH_for):
            KOH_rev_file_search_pattern = KOH_for.split("-")[-7:-4]
            print("KOH_rev file search pattern:", KOH_rev_file_search_pattern)
            #if "forward" in KOH:
                #direction = "forward"
            #if "reverse" in KOH:
                #direction = "reverse"
            #print("direction:", direction)
            for KOH_rev in glob.glob(self.filepath+all_KOH_rev):
                if all(x in KOH_rev for x in KOH_rev_file_search_pattern):
                    file_list_KOH_rev.append(KOH_rev) #.split("/")[-1])

        if len(file_list_KOH_rev) == 0:
            sys.exit("Cannot find KOH_rev bedgraph files, please check the path and file name format.")


        return file_list_KOH_rev


    def _generate_output_filename(self):
        import sys

        filename = []
        all_KOH = ('*KOH*forward.bedgraph')
        for KOH in glob.glob(self.filepath+all_KOH):
            filename_pattern = KOH.split("-")[-7:-4]
            print("filename pattern:", filename_pattern)

            filename.append('_'.join(filename_pattern)+"_heatmap_KOH_out4-10000-500-40-opp_tss.txt")

        return filename



    def _create_dataframe(self):

        header = ['FileNameKOH_for', 'CorrFileNameKOH_rev', 'filename']
        df = pd.DataFrame(columns=header)
        df['FileNameKOH_for'] = self.file_list_KOH_for
        df['CorrFileNameKOH_rev'] = self.file_list_KOH_rev
        df['GeneratedOutputFileName'] = self.filename
        df.drop_duplicates(['FileNameKOH_for'], inplace=True)
        return df

    def _write_dataframe_to_disk(self):
        self.df.to_csv(self.filepath+"opp_tss_heatmap_KOH_input.csv", index=False, header=False, sep=" ")


if __name__ == '__main__':

    '''
        The method that runs when the script is invoked from the commandline
    '''

    parser = argparse.ArgumentParser(description='A script that generates the fisher.csv file needed for fishertest automation with the code: while read -r a b c; do sh stats.sh "$a" "$b" "$c"; done < fisher.csv. Can take .bedgraph files. Make sure for each KOH file there is the corresponding KCl! and that the following name formating is present: alignmenttype.organism_chr.date-initials-organismsID-organism-organOrTissue-KOHorKCl-restrictionensyme-index1-index2_forwardORreverse.bedgraph Run the script in the run environment. It will spit out a file fisher.csv listing all KOH files, corresponding KCl files and the generated name to use for the stats.sh script')

    parser.add_argument('--d', metavar='--> directory containing files', required=True, action='store')

    try:
        results = parser.parse_args()

        if not (results.d or results.s):
            parser.error("You have to specify the --d directory!")
        else:
            if os.path.exists(results.d) == False:
                sys.exit("Something went wrong accessing the path to where fisher.csv will be created.")

            CreateFisherFile(results)

    except IOError as e:
        parser.error(str(e))
