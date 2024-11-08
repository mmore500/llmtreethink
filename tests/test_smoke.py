from pylib.prompt._build_prompt import build_prompt
from pylib.prompt._question_equivalence_identical import (
    question_equivalence_identical,
)
from pylib.prompt._question_equivalence_rotate_tree import (
    question_equivalence_rotate_tree,
)
from pylib.prompt._question_equivalence_shufflerotate_tree import (
    question_equivalence_shufflerotate_tree,
)
from pylib.prompt._question_equivalence_swap_taxa import (
    question_equivalence_swap_taxa,
)
from pylib.prompt._question_most_related import question_identify_most_related
from pylib.prompt._question_most_related_to_x import question_most_related_to_x
from pylib.query._query_openai import query_openai
from pylib.treeprep._sample_phylogeny_newick import sample_phylogeny_newick
from pylib.treeprep._scientific_phylogeny_newick import (
    scientific_phylogeny_newick,
)
from pylib.treerepr._make_json_from_newick import make_json_from_newick


def test_smoke_question_most_related():
    num_taxa = 5
    newick_tree = sample_phylogeny_newick(num_taxa)
    question, choices, true_answer, _ = question_identify_most_related(
        newick_tree,
    )

    json_tree = make_json_from_newick(newick_tree)
    prompt = build_prompt(json_tree, question, choices)
    print("prompt:", prompt)
    result = query_openai(prompt, choices, true_answer)
    print(f"{result=}")


def test_smoke_question_most_related_to_x():
    num_taxa = 10
    newick_tree = sample_phylogeny_newick(num_taxa)
    question, choices, true_answer, _ = question_most_related_to_x(
        newick_tree,
    )

    json_tree = make_json_from_newick(newick_tree)
    prompt = build_prompt(json_tree, question, choices)
    print("prompt:", prompt)
    result = query_openai(prompt, choices, true_answer)
    print(f"{result=}")


def test_smoke_question_equivalence_identical():
    num_taxa = 10
    newick_tree = sample_phylogeny_newick(num_taxa)
    question, choices, true_answer, trees = question_equivalence_identical(
        newick_tree,
    )

    json_trees = [make_json_from_newick(tree) for tree in trees]
    prompt = build_prompt(json_trees, question, choices)
    print("prompt:", prompt)
    result = query_openai(prompt, choices, true_answer)
    print(f"{result=}")



def test_smoke_question_equivalence_shufflerotate_tree():
    num_taxa = 10
    newick_tree = sample_phylogeny_newick(num_taxa)
    question, choices, true_answer, trees = question_equivalence_shufflerotate_tree(
        newick_tree,
    )

    json_trees = [make_json_from_newick(tree) for tree in trees]
    prompt = build_prompt(json_trees, question, choices)
    print("prompt:", prompt)
    result = query_openai(prompt, choices, true_answer)
    print(f"{result=}")


def test_smoke_question_equivalence_rotate_tree():
    num_taxa = 10
    newick_tree = sample_phylogeny_newick(num_taxa)
    question, choices, true_answer, trees = question_equivalence_rotate_tree(
        newick_tree,
    )

    json_trees = [make_json_from_newick(tree) for tree in trees]
    prompt = build_prompt(json_trees, question, choices)
    print("prompt:", prompt)
    result = query_openai(prompt, choices, true_answer)
    print(f"{result=}")


def test_smoke_question_equivalence_swap_taxa():
    num_taxa = 10
    newick_tree = sample_phylogeny_newick(num_taxa)
    question, choices, true_answer, trees = question_equivalence_swap_taxa(
        newick_tree,
    )

    json_trees = [make_json_from_newick(tree) for tree in trees]
    prompt = build_prompt(json_trees, question, choices)
    print("prompt:", prompt)
    result = query_openai(prompt, choices, true_answer)
    print(f"{result=}")


def test_smoke_scientific_phylogeny_newick():
    num_taxa = 3
    newick_tree = scientific_phylogeny_newick(num_taxa)
    question, choices, true_answer, trees = question_equivalence_swap_taxa(
        newick_tree,
    )

    json_trees = [make_json_from_newick(tree) for tree in trees]
    prompt = build_prompt(json_trees, question, choices)
    print("prompt:", prompt)
    result = query_openai(prompt, choices, true_answer)
    print(f"{result=}")


def test_smoke_notree():
    num_taxa = 3
    newick_tree = scientific_phylogeny_newick(num_taxa)
    question, choices, true_answer, trees = question_equivalence_swap_taxa(
        newick_tree,
    )

    prompt = build_prompt([], question, choices)
    print("prompt:", prompt)
    result = query_openai(prompt, choices, true_answer)
    print(f"{result=}")
