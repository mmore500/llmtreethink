import dendropy as dp


def sample_phylogeny_newick(num_taxa: int) -> str:

    # Generate a random ultrametric tree using Yule (birth-only) process
    tree = dp.simulate.treesim.birth_death_tree(
        birth_rate=1.0,
        death_rate=0.0,
        num_extant_tips=num_taxa,
    )
    newick_str = (
        tree.as_string(schema="newick")
        .replace("[&]", "")
        .translate({c: None for c in "0123456789"})
        .replace(":", "")
        .replace(".", "")
    )
    return newick_str
