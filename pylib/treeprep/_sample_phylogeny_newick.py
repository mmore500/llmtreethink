import random

import dendropy as dp


def sample_phylogeny_newick(num_taxa: int) -> str:

    # Generate a random ultrametric tree using Yule (birth-only) process
    tree = dp.simulate.treesim.birth_death_tree(
        birth_rate=1.0,
        death_rate=0.0,
        num_extant_tips=num_taxa,
    )

    leaves = [*tree.leaf_node_iter()]
    num_leaves = len(leaves)
    random.shuffle(leaves)
    for i, node in enumerate(leaves):
        node.taxon.label = "T" + str(i).zfill(len(str(num_leaves)))

    for node in tree.preorder_node_iter():
        node.edge.length = None
    newick_str = (
        tree.as_string(schema="newick")
        .replace("[&]", "")
        .replace(".", "")
    )
    return newick_str
