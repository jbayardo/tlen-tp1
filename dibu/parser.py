import ply.yacc as yacc
from .lexer import *

def p_statement(subexpressions):
    '''statement : expression
                 | expression statement'''


def p_expression(subexpressions):
    'expression : IDENTIFIER key_value_list'


def p_key_value_list(subexpressions):
    '''key_value_list : key_value_entry COMMA key_value_list
                      | key_value_entry
    '''


def p_key_value_entry(subexpressions):
    'key_value_entry : KEY EQUALS value'


def p_value(subexpressions):
    '''value : STRING
             | NUMBER
             | LPAREN value COMMA value RPAREN
             | LBRACKET array RBRACKET'''


def p_array(subexpressions):
    '''array : value
             | value COMMA array'''


def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)


# Build the parser
parser = yacc.yacc(debug=True)

def parse(str):
    """Dado un string, me lo convierte a SVG."""
    return parser.parse(str)
