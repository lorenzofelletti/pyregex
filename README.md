# pyregex
A Regex Engine with backtracking and all major regular expressions features.

It is composed of a Lexer, a Parser (TDRD) and finally the Engine.

Features implemented includes:
| Feature | Syntax |
|-|-|
| match start | ^... |
| match end | ...$ |
| escaping | \\ |
| grouping | (...) |
| alternative | a\|b |
| wildcard | . |
| quantifiers | ? * + |
| curly brace quantification | {exact} {min,max} {,max} {min,} |
| range element | [a-z\|A-Z\|^059] |
