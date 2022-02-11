import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
# matplotlib.set('fig', dpi=160)
import seaborn as sns
sns.set_style('whitegrid')
from datetime import date
import sys
import os

#Generating dictionary of well:name_of_sample 
def get_wells(plate, strain_list):  
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
    counts_df = pd.DataFrame()
    for file in counts_files:
        if '.txt' in file:
            data = pd.read_csv(os.path.join('counts',file), delim_whitespace=True, header=None).iloc[:,6]
            col_name = file.split('_')[0].split('.')[1]
            counts_df.loc[:, col_name] = data
    counts_df.columns = wells.values()
    counts_df.index = pd.read_csv(os.path.join('counts',file), delim_whitespace=True, header=None).iloc[:,4].values-1
    return counts_df

def mnase_reads(raw_data):
    mnase_reads = raw_data.loc['MNASE', :].divide(raw_data.sum(axis=0))
    plt.figure(dpi=160)
    mnase_reads.plot.hist()
    plt.title('Reads mapped on Mnase')
    plt.savefig('results/mnase_dist')

def total_reads(raw_data):
    plt.figure(figsize=(20,10), dpi=60)
    raw_data.sort_index(axis=1).plot.bar()
    plt.axhline(y=200000, linestyle='dashed')
    plt.title('Total reads')
    plt.savefig('results/total_reads')

def get_heatmap(norm_data):
    plt.figure(figsize=(20,20), dpi=60)
    sns.heatmap(norm_data.sort_index(axis=1).corr(), cmap='YlGnBu', vmin=0.92)
    plt.title('Correlation of whole genome expression')
    plt.savefig('results/heatmap')

def get_figs(raw_data, norm_data):
    mnase_reads(raw_data)
    total_reads(raw_data)
    get_heatmap(norm_data)
    

if __name__ == "__main__":

    #Always the same paths and files either constant or defined by snakemake
    full_index = pd.read_csv('/home/labs/barkailab/vovam/pipelines/rna_pipe/data/index_for_df.csv', index_col=0)
    counts_files = sorted(os.listdir(r'counts/'))

    #Getting needed paths for analysis from config of snakemake
    plate = pd.read_csv(sys.argv[1], index_col=0).fillna('Nothing')
    strain_list = pd.read_csv(sys.argv[2], index_col=0)


    wells=get_wells(plate, strain_list)
    counts = get_counts(counts_files, wells)
    
    raw_df = full_index.join(counts).fillna(0).set_index('name')
    norm_df = np.log2((raw_df.divide(raw_df.sum(axis=0).values, axis=1) * 1e6).replace(0,1))

    # get_figs(raw_df, norm_df)

    raw_df.to_csv(sys.argv[3])
    norm_df.to_csv(sys.argv[4])


