import ply.yacc as yacc
from lexer import *


required = {
    'size': {
        'height': int,
        'width': int
    },
    'rectangle': {
        'upper_left': (int, int),
        'height': int,
        'width': int
    },
    'line': {
        'from': (int, int),
        'to': (int, int)
    },
    'circle': {
        'center': (int, int),
        'radius': int
    },
    'ellipse': {
        'center': (int, int),
        'rx': int,
        'ry': int
    },
    'polyline': {
        'points': [(int, int)]
    },
    'polygon': {
        'points': [(int, int)]
    },
    'text': {
        't': str,
        'at': (int, int)
    }
}

optional = {
    'text': {
        'font-family': str,
        'font-size': str
    }
}

common = {
    'fill': str,
    'stroke': str,
    'stroke-width': int
}


def type_assert(a, b):
    if type(b) == tuple:
        if type(a) is not tuple:
            return False

        for x, y in zip(a, b):
            if not isinstance(x, y):
                return False

        return True
    elif type(b) == list:
        if type(a) is not list:
            return False

        b = b[0]
        for entry in a:
            if not type_assert(entry, b):
                return False

        return True
    else:
        return isinstance(a, b)


def p_statement(subexpressions):
    '''statement : expression
                 | expression statement'''

    subexpressions[0] = [subexpressions[1]]

    if len(subexpressions) == 3:
        subexpressions[0] += subexpressions[2]

        if subexpressions[1][0] == 'size':
            for entry in subexpressions[2]:
                if entry[0] == 'size':
                    # TODO: Size llamado mas de una vez
                    assert False


def p_expression(subexpressions):
    'expression : IDENTIFIER key_value_list'
    subexpressions[0] = (subexpressions[1], subexpressions[2])

    (identifier, arguments) = subexpressions[0]

    for key in required[identifier]:
        assert key in arguments

    # Check types and key validity
    for key in arguments:
        if key in common:
            assert type_assert(arguments[key], common[key])
        elif key in required[identifier]:
            assert type_assert(arguments[key], required[identifier][key])
        elif identifier in optional and key in optional[identifier]:
            assert type_assert(arguments[key], optional[identifier][key])
        else:
            # TODO: Mensaje de error, la clave no existe.
            assert False

def p_key_value_list(subexpressions):
    '''key_value_list : key_value_entry COMMA key_value_list
                      | key_value_entry
    '''

    dict = subexpressions[1]

    if len(subexpressions) == 4:
        dict.update(subexpressions.slice[3].value)

    subexpressions[0] = dict


def p_key_value_entry(subexpressions):
    'key_value_entry : KEY EQUALS value'
    subexpressions[0] = {
        subexpressions[1]: subexpressions[3]
    }


def p_value(subexpressions):
    '''value : STRING
             | NUMBER
             | LPAREN value COMMA value RPAREN
             | LBRACKET array RBRACKET'''

    if subexpressions.slice[1].type == 'STRING':
        subexpressions[0] = str(subexpressions.slice[1].value)[1:-1]
    elif subexpressions.slice[1].type == 'NUMBER':
        subexpressions[0] = int(subexpressions.slice[1].value)
    elif subexpressions.slice[1].type == 'LPAREN':
        subexpressions[0] = (subexpressions[2], subexpressions[4])
    elif subexpressions.slice[1].type == 'LBRACKET':
        subexpressions[0] = subexpressions[2]


def p_array(subexpressions):
    '''array : value
             | value COMMA array'''

    subexpressions[0] = [subexpressions[1]]

    if len(subexpressions) == 4:
        subexpressions[0] += subexpressions[3]


def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)


# Build the parser
parser = yacc.yacc()

def parse(str):
    """Dado un string, me lo convierte a SVG."""
    return parser.parse(str)

if __name__ == '__main__':
    print(parse('''size height=400, width=500
    rectangle upper_left=(3,4), width=3, height=5
    circle center=(5,6), radius=8
    polyline points=[(7,6), (1,2)]
    text t="Hello worldddd is gut", at=(1,2)
    size height=8700, width=345'''))
