import pytest

from a_tree import ATree, ATreeException, AttributeDefinition

SOME_ATTRIBUTES = [
    AttributeDefinition.boolean("private"),
    AttributeDefinition.integer("exchange_id"),
    AttributeDefinition.string_list("deal_ids"),
    AttributeDefinition.integer_list("segment_ids"),
]
SOME_ATTRIBUTES_WITH_DUPLICATES = [
    AttributeDefinition.boolean("private"),
    AttributeDefinition.integer("exchange_id"),
    AttributeDefinition.string_list("deal_ids"),
    AttributeDefinition.integer_list("segment_ids"),
    AttributeDefinition.boolean("private"),
]
A_SUBSCRIPTION_ID = 1
ANOTHER_SUBSCRIPTION_ID = 2
AN_EXPRESSION = (
    "(not private) or (exchange_id = 1 and deal_ids one of ['deal-1', 'deal-2'] and segment_ids one of [1, 2, 3])"
)
ANOTHER_EXPRESSION = (
    "(not private) or (exchange_id = 2 and deal_ids one of ['deal-3', 'deal-4'] and segment_ids one of [1, 2, 3])"
)
SOME_EXPRESSION_WITH_NON_EXISTING_ATTRIBUTE = "non_existing or private"
SOME_EXPRESSION_WITH_SYNTACTIC_ERRORS = (
    "(not private) or (exchange_id = 1 and deal_ids one of ['deal-1', 'deal-2' and segment_ids one of [1, 2, 3])"
)
SOME_EXPRESSION_WITH_MISMATCHING_TYPES = "exchange_id = 'deal-1'"


def test_that_it_can_create_an_atree():
    tree = ATree(SOME_ATTRIBUTES)

    assert tree is not None


def test_that_it_fails_to_create_an_atree_if_there_are_some_duplicated_attributes():
    with pytest.raises(Exception):
        ATree(SOME_ATTRIBUTES_WITH_DUPLICATES)


def test_that_it_can_insert_expression():
    tree = ATree(SOME_ATTRIBUTES)

    tree.insert(A_SUBSCRIPTION_ID, AN_EXPRESSION)


def test_that_it_fails_to_insert_expression_when_it_refers_to_non_existing_attributes():
    tree = ATree(SOME_ATTRIBUTES)
    with pytest.raises(ATreeException):
        tree.insert(A_SUBSCRIPTION_ID, SOME_EXPRESSION_WITH_NON_EXISTING_ATTRIBUTE)


def test_that_it_fails_to_insert_expression_when_it_has_syntactic_errors():
    tree = ATree(SOME_ATTRIBUTES)
    with pytest.raises(ATreeException):
        tree.insert(A_SUBSCRIPTION_ID, SOME_EXPRESSION_WITH_SYNTACTIC_ERRORS)


def test_that_it_fails_to_insert_expression_when_it_has_mismatching_types():
    tree = ATree(SOME_ATTRIBUTES)
    with pytest.raises(ATreeException):
        tree.insert(A_SUBSCRIPTION_ID, SOME_EXPRESSION_WITH_MISMATCHING_TYPES)


def test_that_it_can_search_an_atree():
    tree = ATree(SOME_ATTRIBUTES)
    tree.insert(A_SUBSCRIPTION_ID, AN_EXPRESSION)
    tree.insert(ANOTHER_SUBSCRIPTION_ID, ANOTHER_EXPRESSION)

    builder = tree.make_event()
    builder.with_boolean("private", False)
    event = builder.build()
    found = tree.search(event)

    assert [A_SUBSCRIPTION_ID, ANOTHER_SUBSCRIPTION_ID] == found.matches


@pytest.mark.skip(reason="There seems to be an issue with deletion")
def test_that_it_can_remove_a_subscription():
    tree = ATree(SOME_ATTRIBUTES)
    tree.insert(A_SUBSCRIPTION_ID, AN_EXPRESSION)
    tree.insert(ANOTHER_SUBSCRIPTION_ID, ANOTHER_EXPRESSION)
    builder = tree.make_event()
    builder.with_boolean("private", False)
    event = builder.build()
    found = tree.search(event)

    tree.delete(ANOTHER_SUBSCRIPTION_ID)
    found_2 = tree.search(event)

    assert [A_SUBSCRIPTION_ID, ANOTHER_SUBSCRIPTION_ID] == found.matches
    assert [A_SUBSCRIPTION_ID] == found_2.matches


def test_that_it_can_render_atree_to_graphviz():
    tree = ATree(SOME_ATTRIBUTES)
    tree.insert(A_SUBSCRIPTION_ID, AN_EXPRESSION)
    tree.insert(ANOTHER_SUBSCRIPTION_ID, ANOTHER_EXPRESSION)

    rendered = tree.to_graphviz()

    assert rendered is not None
