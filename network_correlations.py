"""Spearman correlations with two-sided permutation p-values.
Run after network_preprocessing.R. Input rows are samples and columns are taxa.
"""
import numpy as np
import pandas as pd


def main():
    rng = np.random.default_rng(42)
    n_permutations = 1000
    for group in ("NAG", "AG", "IM", "GC"):
        data = pd.read_csv(f"spearman_input_{group}.txt", sep="\t", index_col=0)
        correlation = data.corr(method="spearman")
        counts = np.zeros(correlation.shape, dtype=int)
        for _ in range(n_permutations):
            shuffled = data.apply(lambda column: rng.permutation(column.values))
            counts += np.abs(shuffled.corr(method="spearman")) >= np.abs(correlation)
        pvalues = (counts + 1) / (n_permutations + 1)
        pvalues = pd.DataFrame(pvalues, index=data.columns, columns=data.columns)
        pvalues = pvalues.where(correlation.notna())
        correlation.to_csv(f"spearman_cor_{group}.txt", sep="\t")
        pvalues.to_csv(f"spearman_pvals_{group}.txt", sep="\t", float_format="%.6f")


if __name__ == "__main__":
    main()
