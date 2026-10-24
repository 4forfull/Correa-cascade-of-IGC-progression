"""QIIME 2 command templates. Call individual steps after setting input filenames.
Requires a QIIME 2 environment; steps represent alternative analysis branches.
"""
import subprocess

def step_01():
    subprocess.run(['qiime', 'taxa', 'filter-table', '--i-table', './dada2_table.qza', '--i-taxonomy', './taxonomy.qza', '--p-exclude', 'f__Helicobacteraceae', '--o-filtered-table', './dada2_table_noHP.qza'], check=True)

def step_02():
    subprocess.run(['qiime', 'taxa', 'filter-seqs', '--i-sequences', './dada2_rep_set.qza', '--i-taxonomy', './taxonomy.qza', '--p-exclude', 'f__Helicobacteraceae', '--o-filtered-sequences', './dada2_rep_set_noHP.qza'], check=True)

def step_03():
    subprocess.run(['qiime', 'taxa', 'barplot', '--i-table', './dada2_table.qza', '--i-taxonomy', './taxonomy.qza', '--m-metadata-file', 'metadata.tsv', '--o-visualization', './taxa_barplot_withHP.qzv'], check=True)

def step_04():
    subprocess.run(['qiime', 'taxa', 'barplot', '--i-table', './dada2_table_noHP.qza', '--i-taxonomy', './taxonomy.qza', '--m-metadata-file', 'metadata.tsv', '--o-visualization', './taxa_barplot_noHP.qzv'], check=True)

def step_05():
    subprocess.run(['qiime', 'taxa', 'collapse', '--i-table', './dada2_table_noHP.qza', '--i-taxonomy', './taxonomy.qza', '--p-level', '6', '--o-collapsed-table', './merge/paired-V3V4_table_L6_noHP.qza'], check=True)

def step_06():
    subprocess.run(['qiime', 'feature-table', 'merge', '--i-tables', 'paired-V3V4_table_L6_noHP.qza', '--i-tables', 'paired-V4_table_L6_noHP.qza', '--i-tables', 'SRP109017_table_L6_noHP.qza', '--i-tables', 'PRJNA972854_table_L6_noHP.qza', '--o-merged-table', 'merged_L6_noHP.qza'], check=True)

