"""
Type stubs for a_tree_py — PyO3 bindings for the `a-tree` Rust crate.
"""

from __future__ import annotations

class AttributeDefinition:
    """Describes the name and type of a single attribute accepted by an ATree."""

    @staticmethod
    def boolean(name: str) -> AttributeDefinition:
        """Create a boolean attribute definition."""
        ...

    @staticmethod
    def integer(name: str) -> AttributeDefinition:
        """Create an integer (i64) attribute definition."""
        ...

    @staticmethod
    def float(name: str) -> AttributeDefinition:
        """Create a float attribute definition.

        Values are set as (mantissa, scale) pairs where the float equals
        ``mantissa * 10^(-scale)``.
        """
        ...

    @staticmethod
    def string(name: str) -> AttributeDefinition:
        """Create a string attribute definition."""
        ...

    @staticmethod
    def integer_list(name: str) -> AttributeDefinition:
        """Create an integer-list attribute definition."""
        ...

    @staticmethod
    def string_list(name: str) -> AttributeDefinition:
        """Create a string-list attribute definition."""
        ...

class Event:
    """A fully constructed event produced by ``EventBuilder.build()``.

    Pass to ``ATree.search()`` or ``ATreeStr.search()``.
    """

    ...

class EventBuilder:
    """Builder for an Event.  Obtain via ``ATree.make_event()``."""

    def with_boolean(self, name: str, value: bool) -> None:
        """Set a boolean attribute."""
        ...

    def with_integer(self, name: str, value: int) -> None:
        """Set an integer attribute."""
        ...

    def with_float(self, name: str, mantissa: int, scale: int) -> None:
        """Set a float attribute as ``mantissa * 10^(-scale)``."""
        ...

    def with_string(self, name: str, value: str) -> None:
        """Set a string attribute."""
        ...

    def with_integer_list(self, name: str, value: list[int]) -> None:
        """Set an integer-list attribute."""
        ...

    def with_string_list(self, name: str, values: list[str]) -> None:
        """Set a string-list attribute."""
        ...

    def with_undefined(self, name: str) -> None:
        """Mark an attribute as undefined."""
        ...

    def build(self) -> Event:
        """Produce the ``Event``.  Raises ``RuntimeError`` on invalid input."""
        ...

class EventBuilderStr:
    """Builder for an Event.  Obtain via ``ATreeStr.make_event()``."""

    def with_boolean(self, name: str, value: bool) -> None: ...
    def with_integer(self, name: str, value: int) -> None: ...
    def with_float(self, name: str, mantissa: int, scale: int) -> None: ...
    def with_string(self, name: str, value: str) -> None: ...
    def with_integer_list(self, name: str, value: list[int]) -> None: ...
    def with_string_list(self, name: str, values: list[str]) -> None: ...
    def with_undefined(self, name: str) -> None: ...
    def build(self) -> Event: ...

class Report:
    """Search result from ``ATree.search()``.  IDs are ``int``."""

    def matches(self) -> list[int]:
        """Return the subscription IDs whose expressions matched the event."""
        ...

class ReportStr:
    """Search result from ``ATreeStr.search()``.  IDs are ``str``."""

    def matches(self) -> list[str]:
        """Return the subscription IDs whose expressions matched the event."""
        ...

class ATree:
    """A-Tree with integer (``int`` / ``u64``) subscription IDs.

    Example::

        from a_tree_py import ATree, AttributeDefinition

        tree = ATree([
            AttributeDefinition.string_list("deal_ids"),
            AttributeDefinition.integer("exchange_id"),
            AttributeDefinition.boolean("debug"),
            AttributeDefinition.integer_list("segment_ids"),
        ])

        tree.insert(1, 'deal_ids one of ["deal-1", "deal-2"]')
        tree.insert(2, 'segment_ids one of [1, 2, 3, 4]')

        builder = tree.make_event()
        builder.with_string_list("deal_ids", ["deal-2"])
        builder.with_integer_list("segment_ids", [1, 2])
        builder.with_boolean("debug", False)
        event = builder.build()

        report = tree.search(event)
        print(report.matches())  # [1, 2]
    """

    def __init__(self, definitions: list[AttributeDefinition]) -> None:
        """Create a new ATree.

        :param definitions: Attribute definitions; names must be unique.
        :raises RuntimeError: On duplicate attribute names.
        """
        ...

    def insert(self, subscription_id: int, expression: str) -> None:
        """Insert a boolean expression.

        :param subscription_id: Non-negative integer key.
        :param expression: DSL expression string.
        :raises RuntimeError: On parse or semantic errors.
        """
        ...

    def delete(self, subscription_id: int) -> None:
        """Remove the expression for *subscription_id* (no-op if missing)."""
        ...

    def make_event(self) -> EventBuilder:
        """Return a fresh ``EventBuilder`` with all attributes undefined."""
        ...

    def search(self, event: Event) -> Report:
        """Find all expressions that match *event*.

        :raises RuntimeError: On internal errors.
        """
        ...

    def to_graphviz(self) -> str:
        """Export the tree structure as a Graphviz DOT string."""
        ...
