import ply.yacc as yacc
from .lexer import *


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

class SemanticException(Exception):
    pass

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
                 | statement expression'''


    if len(subexpressions) == 3:
        subexpressions[0] = [subexpressions[2]]
        subexpressions[0] += subexpressions[1]

        if subexpressions[2][0] == 'size':
            for entry in subexpressions[1]:
                if entry[0] == 'size':
                    raise SemanticException("Size defined twice.")
    else:
        subexpressions[0] = [subexpressions[1]]

def p_expression(subexpressions):
    'expression : IDENTIFIER key_value_list'
    subexpressions[0] = (subexpressions[1], subexpressions[2])

    (identifier, arguments) = subexpressions[0]

    unmet_requirements = []
    for key in required[identifier]:
        if not key in arguments:
            unmet_requirements.append(key)

    if len(unmet_requirements) > 0:
        raise SemanticException("Parameters {} need to be defined for {}".format(unmet_requirements, identifier))

    # Check types and key validity
    for key in arguments:
        if key in common:
            if type_assert(arguments[key], common[key]):
                return
            raise SemanticException("Type of parameter {} for {} is {}, not {}".format(key, identifier, common[key], arguments[key]))
        elif key in required[identifier]:
            if type_assert(arguments[key], required[identifier][key]):
                return
            raise SemanticException("Type of parameter {} for {} is {}, not {}".format(key, identifier, required[key], arguments[key]))
        elif identifier in optional and key in optional[identifier]:
            if type_assert(arguments[key], optional[identifier][key]):
                return
            raise SemanticException("Type of parameter {} for {} is {}, not {}".format(key, identifier, optional[identifier][key], arguments[key]))
        else:
            raise SemanticException("Unknown parameter {} for {}.".format(key, identifier))

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
    document = parser.parse(str)

    canvas = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n'
    shapes = []

    for key, value in reversed(document):
        if key == 'size':
            canvas = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{}" height="{}">\n'.format(value['width'], value['height'])
            continue
        if key == 'rectangle':
            element = '<rect x="{}" y="{}" height="{}" width="{}"'.format(
                value['upper_left'][0],
                value['upper_left'][1],
                value['height'],
                value['width']
            )
        elif key == 'line':
            element = '<line x1="{}" y1="{}" x2="{}" y2="{}"'.format(
                value['from'][0],
                value['from'][1],
                value['to'][0],
                value['to'][1]
            )
        elif key == 'circle':
            element = '<circle cx="{}" cy="{}" r="{}"'.format(
                value['center'][0],
                value['center'][1],
                value['radius']
            )
        elif key == 'ellipse':
            element = '<ellipse cx="{}" cy="{}" rx="{}" ry="{}"'.format(
                value['center'][0],
                value['center'][1],
                value['rx'],
                value['ry']
            )
        elif key == 'polyline':
            element = '<polyline points="{}"'.format(
                " ".join(["{},{}".format(point[0], point[1]) for point in value['points']])
            )
        elif key == 'polygon':
            element = '<polygon points="{}"'.format(
                " ".join(["{},{}".format(point[0], point[1]) for point in value['points']])
            )
        elif key == 'text':
            element = '<text x="{}" y="{}"'.format(
                value['at'][0],
                value['at'][1]
            )
            if 'font-family' in value:
                element += ' font-family="{}"'.format(value['font-family'])
            if 'font-size' in value:
                element += ' font-size="{}"'.format(value['font-size'])
        for par in common:
            if par in value:
                element += ' {}="{}"'.format(
                    par,
                    value[par]
                )
        if key == 'text':
            element += '>{}</text>'.format(value['text'])
        else:
            element += '/>'
        shapes.append(element)

    return "{}{}\n</svg>".format(canvas, "\n".join(shapes))



if __name__ == '__main__':
    print(parse('''size height=400, width=500
    rectangle upper_left=(3,4), width=3, height=5
    circle center=(5,6), radius=8
    polyline points=[(7,6), (1,2)]
    text t="Hello worldddd is gut", at=(1,2)
    size height=8700, width=345'''))
