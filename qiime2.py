"""QIIME 2 command templates. Call individual steps after setting input filenames.
Requires a QIIME 2 environment; steps represent alternative analysis branches.
"""
import subprocess

def step_01():
    subprocess.run(['qiime', 'tools', 'import', '--type', 'SampleData[SequencesWithQuality]', '--input-path', 'V4_SE_manifest.csv', '--output-path', 'V4_SE_demux.qza', '--input-format', 'SingleEndFastqManifestPhred33V2'], check=True)

def step_02():
    subprocess.run(['qiime', 'tools', 'import', '--type', 'SampleData[PairedEndSequencesWithQuality]', '--input-path', 'V3V4_PE_manifest.csv', '--output-path', 'V3V4_PE_demux.qza', '--input-format', 'PairedEndFastqManifestPhred33V2'], check=True)

def step_03():
    subprocess.run(['qiime', 'cutadapt', 'trim-single', '--i-demultiplexed-sequences', 'V4_SE_demux.qza', '--p-front', 'FORWARD_PRIMER_SEQ', '--p-discard-untrimmed', '--o-trimmed-sequences', 'V4_SE_trimmed.qza', '--verbose'], check=True)

def step_04():
    subprocess.run(['qiime', 'cutadapt', 'trim-paired', '--i-demultiplexed-sequences', 'V3V4_PE_demux.qza', '--p-front-f', 'FORWARD_PRIMER_SEQ', '--p-front-r', 'REVERSE_PRIMER_SEQ', '--p-discard-untrimmed', '--o-trimmed-sequences', 'V3V4_PE_trimmed.qza', '--verbose'], check=True)

def step_05():
    subprocess.run(['qiime', 'quality-filter', 'q-score', '--i-demux', 'demux_trim.qza', '--o-filtered-sequences', 'SRP109017_qfiltered.qza', '--o-filter-stats', 'SRP109017_qfilter-stats.qza'], check=True)

def step_06():
    subprocess.run(['qiime', 'quality-filter', 'q-score', '--i-demux', 'demux_trim.qza', '--o-filtered-sequences', 'paired-V3V4_qfiltered.qza', '--o-filter-stats', 'paired-V3V4_qfilter-stats.qza'], check=True)

def step_07():
    subprocess.run(['qiime', 'demux', 'summarize', '--i-data', 'SRP109017_qfiltered.qza', '--o-visualization', 'SRP109017_qfiltered.qzv'], check=True)

def step_08():
    subprocess.run(['qiime', 'demux', 'summarize', '--i-data', 'paired-V4_qfiltered_merged.qza', '--o-visualization', 'paired-V4_qfiltered_merged.qzv'], check=True)

def step_09():
    subprocess.run(['qiime', 'deblur', 'denoise-16S', '--i-demultiplexed-seqs', 'SRP109017_qfiltered.qza', '--p-trim-length', '380', '--p-sample-stats', '--o-representative-sequences', 'SRP109017_rep-seqs_ASV.qza', '--o-table', 'SRP109017_SE_table_ASV.qza', '--o-stats', 'SRP109017_SE_deblur-stats.qza'], check=True)

def step_10():
    subprocess.run(['qiime', 'deblur', 'visualize-stats', '--i-deblur-stats', 'paired-V4_deblur-stats.qza', '--o-visualization', 'paired-V4_deblur-stats.qzv'], check=True)

def step_11():
    subprocess.run(['qiime', 'feature-classifier', 'classify-sklearn', '--i-classifier', 'silva-138-99-nb-classifier.qza', '--i-reads', 'SRP109017_rep-seqs_ASV.qza', '--o-classification', 'SRP109017_taxonomy.qza'], check=True)

def step_12():
    subprocess.run(['qiime', 'feature-classifier', 'classify-sklearn', '--i-classifier', 'silva-138-99-nb-classifier.qza', '--i-reads', 'V3V4_PE_rep-seqs_ASV.qza', '--o-classification', 'V3V4_PE_taxonomy.qza'], check=True)

def step_13():
    subprocess.run(['qiime', 'taxa', 'filter-table', '--i-table', 'SRP109017_table_ASV.qza', '--i-taxonomy', 'SRP109017_taxonomy.qza', '--p-exclude', 'mitochondria,chloroplast', '--o-filtered-table', 'SRP109017_table_ASV_filtered.qza'], check=True)

def step_14():
    subprocess.run(['qiime', 'taxa', 'filter-table', '--i-table', 'V3V4_PE_table_ASV.qza', '--i-taxonomy', 'V3V4_PE_taxonomy.qza', '--p-exclude', 'mitochondria,chloroplast', '--o-filtered-table', 'V3V4_PE_table_ASV_filtered.qza'], check=True)

def step_15():
    subprocess.run(['qiime', 'taxa', 'filter-seqs', '--i-sequences', 'SRP109017_rep-seqs_ASV.qza', '--i-taxonomy', 'SRP109017_taxonomy.qza', '--p-exclude', 'mitochondria,chloroplast', '--o-filtered-sequences', 'SRP109017_rep-seqs_ASV_filtered.qza'], check=True)

def step_16():
    subprocess.run(['qiime', 'alignment', 'mafft', '--i-sequences', 'PRJNA639644_rep-seqs_ASV_filtered_HOMD.qza', '--o-alignment', 'PRJNA639644_rep-seqs_ASV_filtered-aligned-rep-seqs_HOMD.qza'], check=True)

def step_17():
    subprocess.run(['qiime', 'alignment', 'mask', '--i-alignment', 'PRJNA639644_rep-seqs_ASV_filtered-aligned-rep-seqs_HOMD.qza', '--o-masked-alignment', 'PRJNA639644_rep-seqs_ASV_filtered-masked-aligned-rep-seqs_HOMD.qza'], check=True)

def step_18():
    subprocess.run(['qiime', 'phylogeny', 'fasttree', '--i-alignment', 'PRJNA639644_rep-seqs_ASV_filtered-masked-aligned-rep-seqs_HOMD.qza', '--o-tree', 'PRJNA639644_rep-seqs_ASV_filtered-unrooted-tree_HOMD.qza'], check=True)

def step_19():
    subprocess.run(['qiime', 'phylogeny', 'midpoint-root', '--i-tree', 'PRJNA639644_rep-seqs_ASV_filtered-unrooted-tree_HOMD.qza', '--o-rooted-tree', 'PRJNA639644_rep-seqs_ASV_filtered-rooted-tree_HOMD.qza'], check=True)

def step_20():
    subprocess.run(['qiime', 'diversity', 'alpha-rarefaction', '--i-table', 'PRJNA639644_table_ASV_filtered_HOMD.qza', '--p-max-depth', '10000', '--m-metadata-file', 'metadata.tsv', '--o-visualization', 'PRJNA639644_alpha-rarefaction_HOMD.qzv'], check=True)

def step_21():
    subprocess.run(['qiime', 'diversity', 'core-metrics-phylogenetic', '--i-phylogeny', 'PRJNA639644_rep-seqs_ASV_filtered-rooted-tree_HOMD.qza', '--i-table', 'PRJNA639644_table_ASV_filtered_HOMD.qza', '--p-sampling-depth', '8000', '--m-metadata-file', 'metadata.tsv', '--output-dir', 'core_8000HOMD'], check=True)

def step_22():
    subprocess.run(['qiime', 'tools', 'export', '--input-path', 'shannon_vector.qza', '--output-path', 'output'], check=True)

def step_23():
    subprocess.run(['qiime', 'tools', 'export', '--input-path', 'bray_curtis_distance_matrix.qza', '--output-path', 'bray_export'], check=True)

def step_24():
    subprocess.run(['qiime', 'feature-table', 'merge', '--i-tables', 'PRJNA478252_table_ASV.qza', '--i-tables', 'PRJNA639644_table_ASV.qza', '--i-tables', 'PRJNA678413_table_ASV.qza', '--o-merged-table', 'merged_table_ASV_nofiltered.qza'], check=True)

def step_25():
    subprocess.run(['qiime', 'feature-table', 'merge-seqs', '--i-data', 'PRJNA478252_rep-seqs_ASV.qza', '--i-data', 'PRJNA639644_rep-seqs_ASV.qza', '--i-data', 'PRJNA678413_rep-seqs_ASV.qza', '--o-merged-data', 'merged_rep-seqs_ASV_nofiltered.qza'], check=True)

def step_26():
    subprocess.run(['qiime', 'feature-table', 'merge-taxa', '--i-data', 'PRJNA639644_HOMD_taxonomy.qza', '--i-data', 'PRJNA478252_HOMD_taxonomy.qza', '--i-data', 'PRJNA678413_HOMD_taxonomy.qza', '--o-merged-data', 'taxonomy_HOMD_merged_from_eachtax.qza'], check=True)

def step_27():
    subprocess.run(['qiime', 'taxa', 'barplot', '--i-table', 'merged_table_ASV_filtered_HOMD.qza', '--i-taxonomy', 'taxonomy_HOMD_merged_from_eachtax.qza', '--m-metadata-file', 'metadata-ALL.tsv', '--o-visualization', 'taxa_barplot_merged_HOMD_ASV_from_eachtax.qzv'], check=True)

def step_28():
    subprocess.run(['qiime', 'tools', 'export', '--input-path', 'taxonomy_HOMD_merged_from_eachtax.qza', '--output-path', 'taxonomy_export'], check=True)

def step_29():
    subprocess.run(['qiime', 'tools', 'import', '--input-path', 'taxonomy_fixed.tsv', '--type', 'FeatureData[Taxonomy]', '--input-format', 'TSVTaxonomyFormat', '--output-path', 'taxonomy_HOMD_merged_fixed.qza'], check=True)

def step_30():
    subprocess.run(['qiime', 'taxa', 'barplot', '--i-table', 'merged_table_ASV_filtered_HOMD.qza', '--i-taxonomy', 'taxonomy_HOMD_merged_fixed.qza', '--m-metadata-file', 'metadata-ALL.tsv', '--o-visualization', 'taxa_barplot_merged_HOMD_ASV_fixed.qzv'], check=True)

def step_31():
    subprocess.run(['qiime', 'feature-table', 'merge', '--i-tables', 'V4_SE_table_ASV_filtered.qza', '--i-tables', 'ANOTHER_V4_SE_table_ASV_filtered.qza', '--o-merged-table', 'V4_all_table_ASV_filtered_merged.qza'], check=True)

def step_32():
    subprocess.run(['qiime', 'feature-table', 'merge-seqs', '--i-data', 'V4_SE_rep-seqs_ASV_filtered.qza', '--i-data', 'ANOTHER_V4_SE_rep-seqs_ASV_filtered.qza', '--o-merged-data', 'V4_all_rep-seqs_ASV_filtered_merged.qza'], check=True)

def step_33():
    subprocess.run(['qiime', 'feature-table', 'merge', '--i-tables', 'paired-V3V4_table_ASV_filtered_noHP.qza', '--i-tables', 'paired-V4_table_ASV_filtered_noHP.qza', '--i-tables', 'PRJNA1113136_table_ASV_filtered_noHP.qza', '--i-tables', 'PRJNA972854_table_ASV_filtered_noHP.qza', '--i-tables', 'SRP109017_table_ASV_filtered_noHP.qza', '--o-merged-table', 'merged_ASV_table_noHP.qza'], check=True)

def step_34():
    subprocess.run(['qiime', 'feature-table', 'merge-seqs', '--i-data', 'paired-V3V4_rep-seqs_ASV_filtered_HOMD.qza', '--i-data', 'paired-V4_rep-seqs_ASV_filtered_HOMD.qza', '--i-data', 'PRJNA1113136_rep-seqs_ASV_filtered_HOMD.qza', '--i-data', 'PRJNA972854_rep-seqs_ASV_filtered_HOMD.qza', '--i-data', 'SRP109017_rep-seqs_ASV_filtered_HOMD.qza', '--o-merged-data', 'merged_ASV_rep-seqs_HOMD.qza'], check=True)

def step_35():
    subprocess.run(['qiime', 'vsearch', 'cluster-features-closed-reference', '--i-table', 'merged_ASV_table.qza', '--i-sequences', 'merged_ASV_rep-seqs.qza', '--i-reference-sequences', 'silva-138-99-seqs.qza', '--p-perc-identity', '0.99', '--o-clustered-table', 'pooled_OTU_table.qza', '--o-clustered-sequences', 'pooled_OTU_rep-seqs.qza', '--o-unmatched-sequences', 'unmatched_ASV.qza'], check=True)

def step_36():
    subprocess.run(['qiime', 'feature-classifier', 'classify-sklearn', '--i-classifier', 'silva-138-99-nb-classifier.qza', '--i-reads', 'pooled_OTU_rep-seqs_HOMD.qza', '--o-classification', 'taxonomy_merged_HOMD.qza'], check=True)

def step_37():
    subprocess.run(['qiime', 'taxa', 'barplot', '--i-table', 'pooled_OTU_table_HOMD.qza', '--i-taxonomy', 'taxonomy_merged_HOMD.qza', '--m-metadata-file', 'metadata.tsv', '--o-visualization', 'taxa_barplot_merged_HOMD.qzv'], check=True)

