"""
Set of classes to interact with an ATree
"""

from __future__ import annotations

class AttributeDefinition:
    """An attribute of the ATree (name and type)"""

    @staticmethod
    def boolean(name: str) -> AttributeDefinition:
        """Create a boolean attribute definition."""
        ...

    @staticmethod
    def integer(name: str) -> AttributeDefinition:
        """Create an integer attribute definition."""
        ...

    @staticmethod
    def float(name: str) -> AttributeDefinition:
        """Create a float attribute definition."""
        ...

    @staticmethod
    def string(name: str) -> AttributeDefinition:
        """Create a string attribute definition."""
        ...

    @staticmethod
    def integer_list(name: str) -> AttributeDefinition:
        """Create a list of integers attribute definition."""
        ...

    @staticmethod
    def string_list(name: str) -> AttributeDefinition:
        """Create a list of strings attribute definition."""
        ...

class Event:
    """An event to be used for searching for matching subscriptions."""

    ...

class EventBuilder:
    """Builder for an Event."""

    def with_boolean(self, name: str, value: bool) -> None:
        """Set a boolean attribute."""
        ...

    def with_integer(self, name: str, value: int) -> None:
        """Set an integer attribute."""
        ...

    def with_float(self, name: str, mantissa: int, scale: int) -> None:
        """Set a float attribute as ``number * 10^(-scale)``."""
        ...

    def with_string(self, name: str, value: str) -> None:
        """Set a string attribute."""
        ...

    def with_integer_list(self, name: str, value: list[int]) -> None:
        """Set a list of integers attribute."""
        ...

    def with_string_list(self, name: str, values: list[str]) -> None:
        """Set a list of strings attribute."""
        ...

    def with_undefined(self, name: str) -> None:
        """Mark an attribute as undefined."""
        ...

    def build(self) -> Event:
        """Produce the populated ``Event``."""
        ...

class Report:
    """Search result from ``ATree.search()``.  IDs are ``int``."""

    def matches(self) -> list[int]:
        """Return the subscription IDs whose expressions matched the event."""
        ...

class ATree:
    """A-Tree with uint64 subscription IDs.

    >> from a_tree_py import ATree, AttributeDefinition
    >>
    >> tree = ATree([
    >>     AttributeDefinition.string_list("deal_ids"),
    >>     AttributeDefinition.integer("exchange_id"),
    >>     AttributeDefinition.boolean("debug"),
    >>     AttributeDefinition.integer_list("segment_ids"),
    >> ])
    >> tree.insert(1, 'deal_ids one of ["deal-1", "deal-2"]')
    >> tree.insert(2, 'segment_ids one of [1, 2, 3, 4]')
    >>
    >> builder = tree.make_event()
    >> builder.with_string_list("deal_ids", ["deal-2"])
    >> builder.with_integer_list("segment_ids", [1, 2])
    >> builder.with_boolean("debug", False)
    >> event = builder.build()
    >>
    >> report = tree.search(event)
    >> report.matches()
    [1, 2]
    """

    def __init__(self, definitions: list[AttributeDefinition]) -> None:
        """Create a new ATree.

        :param definitions: The definitions of the attributes that can be used by the arbitrary boolean expressions. These attributes must be uniques (no duplicates are allowed).
        """
        ...

    def insert(self, subscription_id: int, expression: str) -> None:
        """Insert a boolean expression.

        :param subscription_id: The subscription ID for that boolean expression
        :param expression: An arbitrary boolean expression
        """
        ...

    def delete(self, subscription_id: int) -> None:
        """Remove the corresponding expression or the subscription (in the case where more than one subscription is pointing to the same expression)."""
        ...

    def make_event(self) -> EventBuilder:
        """Return a fresh ``EventBuilder`` with all attributes undefined."""
        ...

    def search(self, event: Event) -> Report:
        """Find all expressions that match *event*.

        :param event: The event to search the tree with
        """
        ...

    def to_graphviz(self) -> str:
        """Export the tree structure as a Graphviz DOT string."""
        ...
