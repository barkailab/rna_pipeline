# Snakemake based RNA_pipeline for running on WEXAC cluster

* To run you will need files plate.csv and strain_list.csv and of course your seqeucning files
* strain_list.csv - give to each of your strains number (one for each strain) and record it in a csv files as it is in example [strain_list.csv](https://github.com/vmindel/rna_pipeline/blob/master/data/strain_list.csv)
* plate.csv - is a 8 on 12 representation of library plate which you prepared filled with numbers from strain_list.csv accordingly, see example of [plate.csv](https://github.com/vmindel/rna_pipeline/blob/master/data/plate.csv), if not all of the plate is filled place **None** instead.

## Look for the snakemake script in a [workflow folder](https://github.com/vmindel/rna_pipeline/blob/master/workflow/Snakefile)

* Snakemake parses the directory from whic you will try to run it, and finds workflow/Snakefile, /Snakefile, snakefile or workflow/snakefile. 
* To dry run it execute `snakemake all -np` 
* To build directed acylic graph of the jobs that will be done execute `snakemake all --dag | dot -Tsvg > dag.svg`
* To run the whole script locally execute `snakemake all --cores 24 `
* To run the whole script on the cluster execute `snakemake all --cluster "bsub -q new-long -n 24" -j 25 `

## The [dag.svg](https://github.com/vmindel/rna_pipeline/blob/master/dag.svg) will show you the path each of the samples will traverse in the pipeline and what are the outputs of each step as well as dependenices of future steps from previous ones.
