import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import seaborn as sns
sns.set_style('whitegrid')
from datetime import date
import sys
import os

#Generating dictionary of well:name_of_sample 
def get_wells(plate, strain_list):
    '''
    Generating dict that connects names of samples and their postions in the plate
    
    input:
    plate -> csv file of 8 on 12 matrix with number in it each number indicate one strain
    strain_list -> csv file that connects number of the strain to it's name
    '''
    wells = {}
    for key,value in plate.to_dict().items():
        for letter, sample in value.items():
            if int(key) < 10 :
                wells[str(letter)+'0'+str(key)] = sample
            else:
                wells[str(letter)+str(key)] = sample
    
    #Sorting the dictionary by wells A01, A02, A03, ... and appending the real names 
    wells = {value[0]:strain_list.loc[value[1],].values[0] for value in sorted(wells.items(), key=lambda item: item[0])}
    return wells

# Generating dataframe of raw_counts of reads
def get_counts(counts_files, wells):
    '''
    Counts raw reads of each samples and creates data frame of it
    
    input:
    counts_files -> list of files with genomic reads counts
    wells -> dict of number:strain 
    '''
    counts_df = pd.DataFrame()
    for file in counts_files:
        if '.txt' in file:
            data = pd.read_csv(os.path.join('counts',file), delim_whitespace=True, header=None).iloc[:,6]
            col_name = file.split('.')[1].split('_')[0]
            counts_df.loc[:, col_name] = data
    counts_df.columns = wells.values()
    counts_df.index = pd.read_csv(os.path.join('counts',file), delim_whitespace=True, header=None).iloc[:,4].values-1
    return counts_df

def get_reads(raw_data):
    '''
    Counting reads from raw reads DataFrame and sorting samples alphabetically,
    the dashed line is a common threshold of 250000 reads
    
    input:
    raw_data -> DataFrame with raw reads counts
    '''
    plt.figure(figsize=(30,20))
    raw_data.sort_index(axis=1).sum().plot.bar()
    plt.axhline(250000, color='k', linestyle='dashed')
    plt.savefig('results/reads_barplot')

if __name__ == "__main__":

    #Always the same paths and files either constant or defined by snakemake
    full_index = pd.read_csv('data/index_for_df.csv', index_col=0)

    counts_files = sorted(os.listdir(r'counts/'))

    #Getting needed paths for analysis from config of snakemake
    plate = pd.read_csv(sys.argv[1], index_col=0).fillna('Nothing')
    strain_list = pd.read_csv(sys.argv[2], index_col=0)

    wells=get_wells(plate, strain_list)
    counts = get_counts(counts_files, wells)
    
    raw_df = full_index.join(counts).fillna(0).set_index('name')
    norm_df = np.log2((raw_df.divide(raw_df.sum(axis=0).values, axis=1) * 1e6).replace(0,1))

    get_reads(raw_df)

    raw_df.to_csv(sys.argv[3])
    norm_df.to_csv(sys.argv[4])



