from pylib.treeprep._swap_taxa_newick import swap_taxa_newick


def test_swap_taxa_newick():
    newick_str = "((A,B),(C,D));"

    possible_results = {
        "((C,B),(A,D));",
        "((D,B),(C,A));",
        "((A,C),(B,D));",
        "((A,D),(C,B));",
    }

    assert swap_taxa_newick(newick_str) in possible_results
