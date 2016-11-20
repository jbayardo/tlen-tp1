from lexer_rules import tokens

from expressions import Addition, Multiplication, Number


def p_expression_plus(subexpressions):
    'expression : expression PLUS term'
    subexpressions[0] = Addition(subexpressions[1], subexpressions[3])


def p_expression_term(subexpressions):
    'expression : term'
    subexpressions[0] = subexpressions[1]


def p_term_times(subexpressions):
    'term : term TIMES factor'
    subexpressions[0] = Multiplication(subexpressions[1], subexpressions[3])


def p_term_factor(subexpressions):
    'term : factor'
    subexpressions[0] = subexpressions[1]


def p_factor_number(subexpressions):
    'factor : NUMBER'
    subexpressions[0] = Number(subexpressions[1])


def p_factor_expression(subexpressions):
    'factor : LPAREN expression RPAREN'
    subexpressions[0] = subexpressions[2]


def p_error(subexpressions):
    raise Exception("Syntax error.")
