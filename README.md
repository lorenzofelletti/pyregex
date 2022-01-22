# pyregex

## What is it

Pyregex is a Regex Engine with backtracking and all major regular-expressions' features.

It is composed of a Lexer, a Parser (a TDRD parser) and finally the Engine.

Features implemented includes:
| Feature | Syntax |
|-|-|
| match start | ^... |
| match end | ...$ |
| escaping | \\ |
| grouping | (...) |
| non-capturing group | (?:...) |
| alternative | a\|b |
| wildcard | . |
| space | \s |
| quantifiers | ? \* + |
| curly brace quantification | {exact} {min,max} {,max} {min,} |
| range element | [a-z\|A-Z\|^059] |

## How to run it

(Linux)

Clone the repo:

```
git clone https://github.com/lorenzofelletti/pyregex
```

Change to the cloned direcory:

```
cd pyregex
```

Create and activate a virtualenv:

```
python3 -m venv venv
source venv/bin/activate
```

Install requirements:

```
pip3 install -r requirements.txt
```

Run tests and print coverage:

```
chmod +x print_coverage.sh
./print_coverage.sh
```

### Play with the engine:

Activate the venv and start the python interpreter in the repo folder:

```
cd pyregex
source venv/bin/activate
python3
```

Play with the engine:

```
from src.engine import RegexEngine

reng = RegexEngine()

reng.match('^my_(beautiful_)+regex', '^my_beautiful_beautiful_beautiful_regex')
```

Or:

Enable execution on `regex.sh`:

```
cd pyregex
chmod +x regex.sh
```

Run regex.sh

```
./regex.sh 'my_regex' 'test_str_1' <'test_str2' ... 'test_str_n'>
```
