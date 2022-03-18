# pyregex(p)

## What is it

Pyregex(p) is a Regex Engine with backtracking and all major regular-expressions' features.

It is composed of a Lexer, a Parser (a TDRD parser) and finally the Engine.

Features implemented includes:
| Feature | Syntax |
|-|-|
| match start | ^... |
| match end | ...$ |
| escaping | \\ |
| grouping | (...) |
| named group | (?\<name\>...) | 
| non-capturing group | (?:...) |
| alternative | a\|b |
| wildcard | . |
| space | \s |
| quantifiers | ? \* + |
| curly brace quantification | {exact} {min,max} {,max} {min,} |
| range element | [^a-zA-Z059] |


## Play with the engine:

```Python
from pyregexp.engine import RegexEngine

reng = RegexEngine()

reng.match('^my_(beautiful_)+regex', '^my_beautiful_beautiful_beautiful_regex')
```
