py-a-tree: A dynamic data structure for efficiently indexing arbitrary boolean expressions
==========================================================================================

.. image:: https://static.pepy.tech/badge/py-a-tree/month
    :target: https://pepy.tech/project/py-a-tree
    :alt: py-a-tree Downloads Per Month Badge

.. image:: https://img.shields.io/pypi/l/py-a-tree.svg
    :target: https://pypi.org/project/py-a-tree/
    :alt: License Badge

.. image:: https://img.shields.io/pypi/wheel/py-a-tree.svg
    :target: https://pypi.org/project/py-a-tree/
    :alt: Wheel Support Badge

.. image:: https://img.shields.io/pypi/pyversions/py-a-tree.svg
    :target: https://pypi.org/project/py-a-tree/
    :alt: Python Version Support Badge

This is an implementation of the `A-Tree: A Dynamic Data Structure for Efficiently Indexing Arbitrary Boolean Expressions <https://dl.acm.org/doi/10.1145/3448016.3457266>`_ paper.

The A-Tree data structure is used to evaluate a large amount of boolean expressions as fast as possible. To achieve this, the data structure tries to reuse the intermediary nodes of the incoming expressions to minimize the amount of expressions that have to be evaluated.

This is a Python wrapper over the Rust crate `a-tree <https://github.com/AntoineGagne/a-tree>`_.

-------------------

**Example**::

    >> from a_tree import ATree, AttributeDefinition
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


API Documentation
-----------------

For more in-depth documentation (classes, methods, etc.):

.. toctree::
   :maxdepth: 2

   api
