# Input and output filenames are relative to the working directory.
library(microeco)
library(ggplot2)
library(magrittr)
library(ggpubr)
library(ggsci)
library(dplyr)
group1 <- "AG"
group2 <- "GC"
prefix <- paste0("L6-ML-", group1, "&", group2)
tax   <- read.table(paste0(prefix, "-tax.txt"),
                    header = TRUE, row.names = 1, sep = "\t", check.names = FALSE)
asv   <- read.table(paste0(prefix, "-asv.txt"),
                    header = TRUE, row.names = 1, sep = "\t", check.names = FALSE)
group <- read.table(paste0(prefix, "-group.txt"),
                    header = TRUE, row.names = 1, sep = "\t", check.names = FALSE)
common_samples <- intersect(colnames(asv), rownames(group))
asv <- asv[, common_samples, drop = FALSE]
group <- group[common_samples, , drop = FALSE]
if ("group" %in% colnames(group)) {
  keep <- !is.na(group$group) & group$group != ""
  group <- group[keep, , drop = FALSE]
  asv <- asv[, rownames(group), drop = FALSE]
} else {
  stop("Metadata must contain a group column.")
}
dup_idx <- duplicated(rownames(group))
if (any(dup_idx)) {
  group <- group[!dup_idx, , drop = FALSE]
  asv <- asv[, rownames(group), drop = FALSE]
}
tax %<>% tidy_taxonomy
common_features <- intersect(rownames(tax), rownames(asv))
tax <- tax[common_features, , drop = FALSE]
asv <- asv[common_features, , drop = FALSE]
Table <- microtable$new(
  otu_table = asv,
  tax_table = tax,
  sample_table = data.frame(group = group$group,
                            row.names = rownames(group),
                            check.names = FALSE),
  auto_tidy = FALSE
)
Table$tidy_dataset()
Table$cal_abund()
lefse <- trans_diff$new(
  dataset = Table,
  method  = "lefse",
  group   = "group",
  p_adjust_method = "none"
)
plot_data <- subset(lefse$res_diff, abs(LDA) > 3.5)
write.csv(plot_data,
          file = paste0(prefix, "-plotdata.csv"),
          row.names = FALSE)
df <- read.delim(
  paste0(prefix, "-LEfSe-plot.txt"),
  header = TRUE, sep = '\t', stringsAsFactors = FALSE, check.names = FALSE
) %>% arrange(LDA)
color_dict <- c(
  NAG = "#BFDFD2",
  AG  = "#257D8A",
  IM  = "#68BDD9",
  GC  = "#ECA45A"
)
col_map <- c(color_dict[[group1]], color_dict[[group2]])
names(col_map) <- c(group1, group2)
eps <- diff(range(df$LDA)) * 0.02
p <- ggplot(df, aes(x = reorder(name, LDA), y = LDA, fill = Type)) +
  geom_bar(stat = "identity", color = "black", width = 0.8) +
  geom_text(
    aes(y = ifelse(LDA > 0, -eps, eps),
        label = name,
        hjust = ifelse(LDA > 0, 1, 0)),
    size = 7,
    family = "serif",
    fontface = "italic",
    color = "black"
  ) +
  scale_fill_manual(values = col_map) +
  labs(y = "LDA SCORE (Log10)", x = NULL) +
  coord_flip(clip = "off") +
  theme_classic() +
  theme(
    axis.line.y = element_blank(),
    axis.ticks.y = element_blank(),
    axis.text.y = element_blank(),
    axis.title.y = element_blank(),
    axis.line.x = element_line(linewidth = 0.75, color = "black"),
    axis.title.x = element_text(size = 18, family = "serif"),
    axis.text.x  = element_text(size = 16, family = "serif"),
    legend.position = "none",
    plot.margin = unit(c(1, 3, 1, 3), "lines")
  ) +
  expand_limits(y = c(min(df$LDA) - eps*6, max(df$LDA) + eps*6))
p
ggsave(paste0(prefix, "-LEfSe-plot.png"),
       p, width = 7.29, height = 7.48, dpi = 600, bg = "transparent")
