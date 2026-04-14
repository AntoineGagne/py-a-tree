"""
Set of classes to interact with an ``ATree``.
"""

from __future__ import annotations

class ATreeException(Exception):
    """Base class for the exceptions that can be returned by the ATree"""

    ...

class DuplicateAttributeException(ATreeException): ...
class MissingAttributeException(ATreeException): ...
class NonExistingAttribute(ATreeException): ...
class MismatchingAttributeTypeException(ATreeException): ...
class ParseException(ATreeException): ...
class LockException(ATreeException): ...

class ATree:
    """The A-Tree data structure."""

    def __init__(self, definitions: list[AttributeDefinition]) -> None:
        """Create a new ATree."""
        ...

    def insert(self, subscription_id: int, expression: str) -> None:
        """Insert a boolean expression."""
        ...

    def delete(self, subscription_id: int) -> None:
        """Remove the corresponding expression or the subscription (in the case where more than one subscription is pointing to the same expression)."""
        ...

    def make_event(self) -> EventBuilder:
        """Return an ``EventBuilder`` with all attributes undefined."""
        ...

    def search(self, event: Event) -> Report:
        """Find all expressions that match the event."""
        ...

    def to_graphviz(self) -> str:
        """Export the tree structure as a Graphviz DOT string."""
        ...

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
        """Build the populated ``Event``."""
        ...

class Event:
    """An event to be used for searching for matching subscriptions."""

    ...

class Report:
    """Contains the search results"""

    @property
    def matches(self) -> list[int]:
        """Return the subscription IDs whose expressions matched the event."""
        ...
