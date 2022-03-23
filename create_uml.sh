#!/bin/bash
pyreverse -o re_ast.png -A -S -mn -f ALL ./pyregexp/re_ast.py
mv classes.re_ast.png docs/uml

pyreverse -o engine.png -A -S -mn -f ALL ./pyregexp/engine.py
mv classes.engine.png docs/uml

pyreverse -o lexer.png -A -S -mn -f ALL ./pyregexp/lexer.py
mv classes.lexer.png docs/uml

pyreverse -o match.png -A -S -mn -f ALL ./pyregexp/match.py
mv classes.match.png docs/uml

pyreverse -o pyrser.png -A -S -mn -f ALL ./pyregexp/pyrser.py
mv classes.pyrser.png docs/uml

pyreverse -o tokens.png -A -S -mn -f ALL ./pyregexp/tokens.py
mv classes.tokens.png docs/uml

pyreverse -o pyregexp.png -A -S -mn ./pyregexp/*
mv classes.pyregexp.png docs/uml
mv packages.pyregexp.png docs/uml
