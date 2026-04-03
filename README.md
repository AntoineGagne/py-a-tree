# py-a-tree

[![CI](https://github.com/AntoineGagne/py-a-tree/actions/workflows/ci.yml/badge.svg)](https://github.com/AntoineGagne/py-a-tree/actions/workflows/ci.yml)

The A-Tree data structure is used to evaluate a large amount of boolean expressions as fast as possible. To achieve this, the data structure tries to reuse the intermediary nodes of the incoming expressions to minimize the amount of expressions that have to be evaluated.

This is a Python wrapper over the Rust crate [`a-tree`](https://github.com/AntoineGagne/a-tree).

## License

This project is licensed under the [Apache 2.0](LICENSE-APACHE) and the [MIT License](LICENSE-MIT).
