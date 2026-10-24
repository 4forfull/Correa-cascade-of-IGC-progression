library(dplyr)
groups <- c("NAG","AG","IM","GC")
edge_all <- list()
for (g in groups) {
  cor_mat_file <- paste0("spearman_cor_", g, ".txt")
  p_mat_file   <- paste0("spearman_pvals_", g, ".txt")
  if (!file.exists(cor_mat_file) || !file.exists(p_mat_file)) {
    next
  }
  cor_mat <- as.matrix(read.table(cor_mat_file,
                                  header=TRUE,
                                  row.names=1,
                                  sep="\t",
                                  check.names=FALSE,
                                  fill=TRUE,
                                  comment.char=""))
  p_mat   <- as.matrix(read.table(p_mat_file,
                                  header=TRUE,
                                  row.names=1,
                                  sep="\t",
                                  check.names=FALSE,
                                  fill=TRUE,
                                  comment.char=""))
  common_taxa <- intersect(rownames(cor_mat), colnames(cor_mat))
  common_taxa <- intersect(common_taxa, rownames(p_mat))
  common_taxa <- intersect(common_taxa, colnames(p_mat))
  bad_taxa <- common_taxa[
    apply(cor_mat[common_taxa, common_taxa, drop=FALSE], 1,
          function(x) all(is.na(x)))
  ]
  keep_taxa <- setdiff(common_taxa, bad_taxa)
  if (length(keep_taxa) < 2) {
    next
  }
  cor_mat2 <- cor_mat[keep_taxa, keep_taxa, drop=FALSE]
  p_mat2   <- p_mat[keep_taxa, keep_taxa, drop=FALSE]
  comb <- expand.grid(
    Var1 = keep_taxa,
    Var2 = keep_taxa,
    stringsAsFactors = FALSE
  )
  comb <- comb[comb$Var1 < comb$Var2, ]
  df <- comb
  df$Correlation <- mapply(function(a,b) cor_mat2[a,b], df$Var1, df$Var2)
  df$Pvalue      <- mapply(function(a,b) p_mat2[a,b], df$Var1, df$Var2)
  df$Correlation <- as.numeric(df$Correlation)
  df$Pvalue      <- as.numeric(df$Pvalue)
  df <- df[!is.na(df$Correlation), ]
  df$Group <- g
  df$Sign  <- ifelse(df$Correlation > 0, "positive","negative")
  edge_all[[g]] <- df
}
edge_all <- bind_rows(edge_all)
edge_sig_loose <- edge_all %>%
  filter(!is.na(Correlation)) %>%
  filter(abs(Correlation) > 0.3)
edge_sig_loose_out <- edge_sig_loose %>%
  dplyr::rename(
    Source = Var1,
    Target = Var2
  )
write.table(edge_sig_loose_out,
            file = "edges_for_cytoscape_loose.tsv",
            sep = "\t",
            quote = FALSE,
            row.names = FALSE)
edge_sig_strict <- edge_all %>%
  filter(!is.na(Correlation)) %>%
  filter(!is.na(Pvalue)) %>%
  filter(abs(Correlation) > 0.2,
         Pvalue < 0.05)
edge_sig_strict_out <- edge_sig_strict %>%
  dplyr::rename(
    Source = Var1,
    Target = Var2
  )
write.table(edge_sig_strict_out,
            file = "edges_for_cytoscape_strict.tsv",
            sep = "\t",
            quote = FALSE,
            row.names = FALSE)
if (file.exists("node_attributes_mean_abundance_top20.tsv")) {
  node_attr <- read.table("node_attributes_mean_abundance_top20.tsv",
                          header=TRUE,
                          sep="\t",
                          check.names=FALSE)
  write.table(node_attr,
              file = "nodes_for_cytoscape.tsv",
              sep = "\t",
              quote = FALSE,
              row.names = FALSE)
} else {
}
