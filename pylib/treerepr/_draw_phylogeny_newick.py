import io

from Bio import Phylo as BioPhylo
import matplotlib.pyplot as plt


def draw_phylogeny_newick(source: str) -> None:
    # Parse the Newick string
    tree = BioPhylo.read(io.StringIO(source), "newick")

    # Draw the tree using matplotlib
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)

    BioPhylo.draw(tree, do_show=False, axes=ax)

    # Show the plot
    plt.show()
