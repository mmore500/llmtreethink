import dendropy as dp
import numpy as np


def make_mrca_matrix(tree: dp.Tree) -> np.array:
    taxa = tree.taxon_namespace
    assert sorted(taxa, key=lambda t: t.label) == list(taxa)
    num_taxa = len(taxa)

    mrca_matrix = np.zeros((num_taxa, num_taxa))
    # Fill MRCA matrix with times
    for i in range(num_taxa):
        for j in range(i, num_taxa):
            if i == j:
                mrca_matrix[i, j] = 0
            else:
                # Get the MRCA of the two taxa
                taxon1 = taxa[i]
                taxon2 = taxa[j]
                mrca_node = tree.mrca(
                    taxon_labels=[taxon1.label, taxon2.label]
                )

                # MRCA node's age
                mrca_age = mrca_node.distance_from_root()
                mrca_matrix[i, j] = mrca_matrix[j, i] = mrca_age

    return mrca_matrix
