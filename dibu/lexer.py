import ply.lex as lex

"""
Lista de tokens

El analizador léxico de PLY (al llamar al método lex.lex()) va a buscar
para cada uno de estos tokens una variable "t_TOKEN" en el módulo actual.

t_TOKEN puede ser:

- Una expresión regular
- Una función cuyo docstring sea una expresión regular (bizarro).

En el segundo caso, podemos hacer algunas cosas "extras", como quedarnos
con algún valor de ese elemento.

"""


tokens = [
    'IDENTIFIER',
    'STRING',
    'NUMBER',
    'KEY',
    'COMMA',
    'EQUALS',
    'LBRACKET',
    'RBRACKET',
    'LPAREN',
    'RPAREN',
    'NEWLINE'
]


def t_error(token):
    message = "Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)


t_IDENTIFIER = r'(size|rectangle|line|circle|ellipse|polyline|polygon|text)'
t_STRING = r'\"([^\\\n]|(\\.))*?\"'
t_KEY = r'\w[\w\d_-]*'
t_COMMA = r","
t_EQUALS = r"="
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_LPAREN = r"\("
t_RPAREN = r"\)"


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large", t.value)
        t.value = 0
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

t_ignore = ' \t'

# Build the lexer
lexer = lex.lex(debug=True)


def apply(string):
    u"""Aplica el análisis léxico al string dado."""
    lex.input(string)

    return list(lexer)
