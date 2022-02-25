# Snakemake based RNA_pipeline for running on WEXAC cluster

* To run you will need files plate.csv and strain_list.csv and of course your seqeucning files
* strain_list.csv - give to each of your strains number (one for each strain) and record it in a csv files as it is in example [strain_list.csv](https://github.com/vmindel/rna_pipeline/blob/master/data/strain_list.csv)
* plate.csv - is a 8 on 12 representation of library plate which you prepared filled with numbers from strain_list.csv accordingly, see example of [plate.csv](https://github.com/vmindel/rna_pipeline/blob/master/data/plate.csv), if not all of the plate is filled place **None** instead.

## The output is raw reads dataframe and log2 normalized to million reads dataframe
## Look for the snakemake script in a [workflow folder](https://github.com/vmindel/rna_pipeline/blob/master/workflow/Snakefile)

### What to change - 
#### In root directory there is a config.yaml file:
* genome - insert path to your genome built with bowtie2
* gene_list - path to a bed file which contains coordinates and names of relevant genes from the genome you have built 
* barcodes - are the barcodes for the demultiplexing, check [example](https://github.com/vmindel/rna_pipeline/blob/master/data/rna_inner.txt) 
* name - start of your sequencing file names - for example for RNA4_S260_R1_001.fastq.gz and RNA4_S260_R2_001.fastq.gz, the name will be RNA4_S260 as this is the only part that changes
* plate - is the path to your plate mentioned before
* strain_list - is the path to your strain_list file
* raw_results - name to save your raw reads dataframe
* norm_results - name to save your normalized reads dataframe 

### How to run - 
* Snakemake parses the directory from whic you will try to run it, and finds workflow/Snakefile, /Snakefile, snakefile or workflow/snakefile. 
* To dry run it execute `snakemake all -np` 
* To dry run the python script that parses the counts files and outputs dataframes execute `python scripts/get_data.py data/plate.csv data/strain_list.csv results/csvs/raw_df.csv results/csvs/norm_df.csv` as it is exact command that the pipeline will run and I inckuded some counts files to simulate the actual data. 
* To build directed acylic graph of the jobs that will be done execute `snakemake all --dag | dot -Tsvg > dag.svg`
* To run the whole script locally execute `snakemake all --cores 24 `
* To run the whole script on the cluster execute `snakemake all --cluster "bsub -q new-long -n 24" -j 25 `

## The [dag.svg](https://github.com/vmindel/rna_pipeline/blob/master/dag.svg) will show you the path each of the samples will traverse in the pipeline and what are the outputs of each step as well as dependenices of future steps from previous ones.
