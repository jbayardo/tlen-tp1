from lexer_rules import tokens


class SemanticException(Exception):
    pass


def p_array_declaration(subexpressions):
    'array_declaration : TYPE ID LBRACKET NUMBER RBRACKET EQUALS LBRACE number_list RBRACE'
    type_token = subexpressions[1]
    number_token = subexpressions[4]
    number_list = subexpressions[8]
    if number_token["type"] != "int":
        raise SemanticException("Incompatible size definition.")
    if number_list["size"] != number_token["value"]:
        raise SemanticException("Incompatible size.")
    if number_list["size"] > 0 and number_list["type"] != type_token:
        raise SemanticException("Incompatible type.")


def p_number_list_empty(subexpressions):
    'number_list :'
    subexpressions[0] = {"size": 0}


def p_number_list_non_empty(subexpressions):
    'number_list : number_list_non_empty' 
    subexpressions[0] = subexpressions[1]


def p_number_list_one(subexpressions):
    'number_list_non_empty : NUMBER'
    number_token = subexpressions[1]
    subexpressions[0] = {"size": 1, "type": number_token["type"]}


def p_number_list_append(subexpressions):
    'number_list_non_empty : number_list_non_empty COMMA NUMBER'
    number_token = subexpressions[3]
    sub_number_list = subexpressions[1]
    if sub_number_list["type"] != number_token["type"]:
        raise SemanticException("Incompatible type.")
    subexpressions[0] = {"size": sub_number_list["size"] + 1, "type": number_token["type"]}
    


def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
