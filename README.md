# Plox
This is a follow-along copy (I'm the one following along) of the Lox programming language that Robert Nystrom teaches how to interpret in his book, [Crafting Interpreters](https://www.craftinginterpreters.com).
This repository is a version adapted in Python, hence the prefixed "p" that constitutes the name "Plox". I'm aiming to garnish this implementation with some
extras suggested by Nystrom throughout the book, but no promises there :)
The purpose of this repository is one of self-education, as I aim to eventually create a compiler and am in need of basic introduction to language
parsing and execution. The end product will hopefully be a similar such language, but one that is compiled and more type-safe, for instance.

# Running
There should be no dependencies, so simply type:
    `python plox.py [script_name.lox]`
in order to run a program from a file, or simply `python plox.py` for an interactive session.