library(dplyr)
library(readr)
edges_all <- read.table("edges_for_cytoscape_strict.tsv",
                        header=TRUE,
                        sep="\t",
                        check.names=FALSE,
                        quote="")
groups <- c("NAG","AG","IM","GC")
node_list_all <- list()
for (g in groups) {
  infile <- paste0("spearman_input_", g, ".txt")
  if (!file.exists(infile)) {
    next
  }
  mat <- read.table(infile,
                    header=TRUE,
                    sep="\t",
                    row.names=1,
                    check.names=FALSE,
                    quote="")
  genus_mean <- colMeans(mat, na.rm=TRUE)
  node_df <- data.frame(
    Genus = names(genus_mean),
    MeanAbundance = as.numeric(genus_mean),
    Group = g,
    stringsAsFactors = FALSE
  )
  node_list_all[[g]] <- node_df
  edges_g <- edges_all %>% filter(Group == g)
  used_nodes <- unique(c(edges_g$Source, edges_g$Target))
  node_g <- node_df %>% filter(Genus %in% used_nodes)
  write.table(edges_g,
              file=paste0("cyto_edges_", g, ".tsv"),
              sep="\t",
              quote=FALSE,
              row.names=FALSE)
  write.table(node_g,
              file=paste0("cyto_nodes_", g, ".tsv"),
              sep="\t",
              quote=FALSE,
              row.names=FALSE)
}
node_all <- do.call(rbind, node_list_all)
write.table(node_all,
            file="node_attributes_all_groups_long.tsv",
            sep="\t",
            quote=FALSE,
            row.names=FALSE)
