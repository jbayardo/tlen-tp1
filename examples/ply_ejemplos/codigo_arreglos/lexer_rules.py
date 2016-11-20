tokens = [
   'TYPE',
   'NUMBER',
   'ID',
   'LBRACKET',
   'RBRACKET',
   'LBRACE',
   'RBRACE',
   'COMMA',
   'EQUALS'
]


types = set(['int', 'float'])


def t_ID(token):
    r"[_a-zA-Z][_a-zA-Z0-9]*"
    if token.value in types:
        token.type = 'TYPE'
    return token


def t_NUMBER(token):
    r"[0-9]+(\.[0-9]+)?"
    if token.value.find(".") >= 0:
        number_type = "float"
        number_value = float(token.value)
    else:
        number_type = "int"
        number_value = int(token.value)
    token.value = {"value": number_value, "type": number_type}
    return token


def t_NEWLINE(token):
    r"\n+"
    token.lexer.lineno += len(token.value)


t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_COMMA = r","
t_EQUALS = r"="

t_ignore = " \t"


def t_error(token):
    message = "Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
