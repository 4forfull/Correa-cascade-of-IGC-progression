"""PICRUSt2 command templates; run each stage with matching input files."""
import subprocess

def step_1():
    subprocess.run(['qiime', 'tools', 'export', '--input-path', 'merged_table_ASV_noHP_filtered_HOMD.qza', '--output-path', 'table'], check=True)

def step_2():
    subprocess.run(['qiime', 'tools', 'export', '--input-path', 'merged_rep-seqs_ASV_noHP_filtered_HOMD.qza', '--output-path', 'seqs'], check=True)

def step_3():
    subprocess.run(['picrust2_pipeline.py', '-i', 'feature-table.biom', '-s', 'dna-sequences.fasta', '-o', 'picrust2_out', '-p', '8'], check=True)

def step_4():
    subprocess.run(['pathway_pipeline.py', '-i', 'ko.tsv.gz', '-o', 'KEGG_pathways_out', '--no_regroup', '-m', 'KEGG_pathways_to_KO.tsv', '-p', '14'], check=True)

