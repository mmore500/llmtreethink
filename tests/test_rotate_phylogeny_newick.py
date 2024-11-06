from pylib.treeprep._rotate_phylogeny_newick import rotate_phylogeny_newick


def test_rotate_phylogeny_newick():
    newick_str = "((A,B),(C,D));"

    # Manually enumerated possible rotations for the input string
    possible_results = {
        "((A,B),(C,D));",  # Original structure
        "((B,A),(C,D));",  # Swapped A and B within the first pair
        "((A,B),(D,C));",  # Swapped C and D within the second pair
        "((C,D),(A,B));",  # Swapped the two pairs
        "((D,C),(B,A));",  # Swapped within and across pairs
        "((D,C),(B,A));",  # Swapped within and across pairs
    }

    assert rotate_phylogeny_newick(newick_str) in possible_results
