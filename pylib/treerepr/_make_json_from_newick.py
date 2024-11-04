import io
import json

from Bio import Phylo as BioPhylo


def make_json_from_newick(tree: str) -> str:
    tree = BioPhylo.read(io.StringIO(tree), "newick")

    # Helper function to recursively convert tree nodes to dict, including branch lengths
    def clade_to_dict(clade: BioPhylo.BaseTree.Clade) -> dict:
        result = {}
        if clade.name:
            result["name"] = clade.name
        if clade.branch_length is not None:
            result["branch_length"] = clade.branch_length
        if clade.clades:
            result["children"] = [
                clade_to_dict(child) for child in clade.clades
            ]
        return result

    # Start conversion from the root clade
    tree_dict = clade_to_dict(tree.root)

    # Convert the dict to JSON format
    tree_json = json.dumps(tree_dict, indent=2)
    return tree_json
