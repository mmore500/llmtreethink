import random

import dendropy as dp

from .._auxlib._swap_words import swap_words


def shuffle_taxa_newick(newick_str: str) -> str:
    assert ":" not in newick_str

    orig_tree = dp.Tree.get(data=newick_str, schema="newick")
    for node in orig_tree.preorder_node_iter():
        node.edge.length = 1
    tree = orig_tree.clone(depth=1)

    for __ in range(10000):
        leaves = [*tree.leaf_node_iter()]

        for i in range(0, len(leaves)-2):
            j = random.randint(i, len(leaves)-1)
            leaves[i].taxon, leaves[j].taxon = leaves[j].taxon, leaves[i].taxon

            if dp.calculate.treecompare.weighted_robinson_foulds_distance(orig_tree, tree) > 0:
                for node in tree.preorder_node_iter():
                    node.edge.length = None
                return tree.as_string(schema="newick").replace(".", "")
    else:
        assert False
