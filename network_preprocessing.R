input_file <- "all_samples_genus_table.csv"
dat_raw <- read.csv(input_file,
                    header = TRUE,
                    row.names = 1,
                    check.names = FALSE,
                    quote = "",
                    comment.char = "")
group_col <- "Group"
if (!(group_col %in% colnames(dat_raw))) {
  stop("Missing Group column.")
}
abund <- dat_raw[, colnames(dat_raw) != group_col, drop = FALSE]
meta  <- dat_raw[, group_col, drop = FALSE]
colnames(meta) <- "Group"
row_sums <- rowSums(abund)
stopifnot(all(is.finite(row_sums)), all(row_sums > 0))
if ( any(abs(row_sums - 1) > 1e-6) ) {
  abund_rel <- abund / row_sums
} else {

  abund_rel <- abund
}
keep_threshold_prop <- 0.05
keep_threshold_abun <- 0.001
abund_rel_num <- as.data.frame(lapply(abund_rel, as.numeric),
                               check.names = FALSE)
rownames(abund_rel_num) <- rownames(abund_rel)
present_prop <- colMeans(abund_rel_num > keep_threshold_abun, na.rm = TRUE)
keep_taxa <- names(present_prop)[present_prop >= keep_threshold_prop]
abund_filt <- abund_rel_num[, keep_taxa, drop = FALSE]
mean_abun_global <- colMeans(abund_filt, na.rm = TRUE)
mean_abun_global <- sort(mean_abun_global, decreasing = TRUE)
topN <- 20
all_taxa_sorted <- names(mean_abun_global)
all_taxa_sorted <- all_taxa_sorted[!is.na(all_taxa_sorted) & all_taxa_sorted != ""]
all_taxa_sorted <- all_taxa_sorted[all_taxa_sorted %in% colnames(abund_filt)]
top_taxa <- head(all_taxa_sorted, topN)
if (length(top_taxa) == 0) {
  stop("No taxa remain after filtering.")
}
abund_top20 <- abund_filt[, top_taxa, drop = FALSE]
print(top_taxa)
groups <- unique(na.omit(meta$Group))
for (g in groups) {
  sub_mat <- abund_top20[meta$Group == g, , drop = FALSE]
  out_file <- paste0("spearman_input_", g, ".txt")
  write.table(sub_mat,
              file = out_file,
              sep = "\t",
              quote = FALSE,
              row.names = TRUE,
              col.names = TRUE)
}
mean_abun_by_group <- do.call(rbind, lapply(groups, function(g) {
  sub_mat <- abund_top20[meta$Group == g, , drop = FALSE]
  data.frame(
    Genus = colnames(sub_mat),
    MeanAbundance = colMeans(sub_mat),
    Group = g,
    stringsAsFactors = FALSE
  )
}))
write.table(mean_abun_by_group,
            file = "node_attributes_mean_abundance_top20.tsv",
            sep = "\t",
            quote = FALSE,
            row.names = FALSE)
