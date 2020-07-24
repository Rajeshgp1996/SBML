# Rajesh Prabhakar - 112872762

import sys

variable_dict = {}
functions_Name_dict = {}
funVariableStack = []

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'True': 'TRUE',
    'False': 'FALSE',
    'div': 'DIVIDE',
    'mod': 'MODULUS',
    'in': 'INSIDE',
    'not': 'NEGATION',
    'andalso': 'CONJUNCTION',
    'orelse': 'DISJUNCTION',
    'print': 'PRINT',
    'fun': 'FUNCTION'
}


tokens = [ 'COMMA', 'HASH', 'STRING', 'SBMLVAR', 'INTEGER', 'REAL', 'POWER', 'TIMES', 'INTDIVIDE', 'PLUS',
           'MINUS', 'CONS', 'LESSTHAN', 'LESSEQUAL', 'EQUALTO', 'NOTEQUAL', 'GREATEREQUAL', 'GREATERTHAN',
          'LPAREN', 'RPAREN', 'LSQRBRCS', 'RSQRBRCS', 'ASSIGNMENT', 'SEMICOLON', 'LFLOWERPAREN', 'RFLOWERPAREN'] + list(reserved.values())


precedence = (('left', 'DISJUNCTION'),
              ('left', 'CONJUNCTION'),
              ('left', 'NEGATION'),
              ('left', 'LESSTHAN', 'LESSEQUAL', 'EQUALTO', 'NOTEQUAL', 'GREATEREQUAL', 'GREATERTHAN', 'ASSIGNMENT'),
              ('right', 'CONS'),
              ('left', 'INSIDE'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE', 'INTDIVIDE', 'MODULUS'),
              ('right', 'UMINUS'),
              ('right', 'POWER'),
              ('left', 'LSQRBRCS', 'RSQRBRCS'),
              ('left', 'LPAREN', 'RPAREN'),
              )


t_TRUE = r'True'
t_FALSE = r'False'
t_POWER = r'\*\*'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_INTDIVIDE = r'div'
t_MODULUS = r'mod'
t_PLUS = r'\+'
t_MINUS = r'-'
t_INSIDE = r'in'
t_CONS = r'::'
t_NEGATION = r'not'
t_CONJUNCTION = r'andalso'
t_DISJUNCTION = r'orelse'
t_LESSTHAN = r'<'
t_LESSEQUAL = r'<='
t_EQUALTO = r'=='
t_NOTEQUAL = r'<>'
t_GREATEREQUAL = r'>='
t_GREATERTHAN = r'>'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LSQRBRCS = r'\['
t_RSQRBRCS = r'\]'
t_COMMA = r','
t_HASH = r'\#'
t_ASSIGNMENT = r'='
t_SEMICOLON = r';'
t_PRINT = r'print'
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_LFLOWERPAREN = r'{'
t_RFLOWERPAREN = r'}'
t_FUNCTION = r'fun'
t_ignore = ' \t'


def t_REAL(t):
    r'[0-9]*\.[0-9]*([eE][-+]?[0-9]+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("float value too large ", t.value)
        t.value = 0
    return t


def t_INTEGER(t):
    r'[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_STRING(t):
    r'\'[^\']*\'|\"[^"]*\"'
    t.value = str(t.value)[1:-1]
    return t


def t_SBMLVAR(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'SBMLVAR')  # Check for reserved words
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    raise SyntaxError


def p_prop_main_block(p):
    '''block : subBlock
            | funDef funDefTail subBlock
            | funDef subBlock
            | funDef '''
    # for i in len(p):
    #     p
    p[0] = MainBlock(p[1:])


def p_prop_sub_block(p):
    '''subBlock : LFLOWERPAREN subBlock RFLOWERPAREN
            | LFLOWERPAREN multiStatement RFLOWERPAREN
            | LFLOWERPAREN  RFLOWERPAREN'''
    if len(p) > 3:
        p[0] = BlockStatements(p[2])


def p_prop_fun_def(p):
    '''funDef : FUNCTION SBMLVAR LPAREN params RPAREN ASSIGNMENT subBlock prop SEMICOLON
              | FUNCTION SBMLVAR LPAREN params RPAREN ASSIGNMENT subBlock SEMICOLON
              | FUNCTION SBMLVAR LPAREN RPAREN ASSIGNMENT subBlock prop SEMICOLON
              | FUNCTION SBMLVAR LPAREN RPAREN ASSIGNMENT subBlock SEMICOLON'''

    if len(p) > 9:
        p[0] = FunctionDef(p[2], p[4], p[7], p[8])
    elif p[5] == ')':
        p[0] = FunctionDef(p[2], p[4], p[7])
    elif len(p) > 8:
        p[0] = FunctionDef(p[2], None, p[6], p[7])
    else:
        p[0] = FunctionDef(p[2], None, p[6])


def p_prop_para(p):
    '''params : SBMLVAR COMMA params
            | SBMLVAR'''
    if len(p) > 2:
        p[0] = Params(p[1], p[3])
    else:
        p[0] = Params(p[1], None)


def p_prop_funDefTail(p):
    '''funDefTail : funDef funDefTail
                  | funDef'''
    if len(p) > 2:
        p[0] = Params(p[1], p[3])
    else:
        p[0] = Params(p[1], None)


def p_prop_multi_statements(p):
    '''multiStatement : multiStatement statement
                    |  statement'''
    if len(p) > 2:
        p[0] = MultiStatements(p[1], p[2])
    else:
        p[0] = MultiStatements(p[1])


def p_prop_statement(p):
    '''statement : IF LPAREN prop RPAREN subBlock ELSE subBlock
                | IF LPAREN prop RPAREN subBlock
                | WHILE LPAREN prop RPAREN subBlock
                | PRINT LPAREN prop RPAREN SEMICOLON
                | prop ASSIGNMENT prop SEMICOLON
                | prop SEMICOLON
                | subBlock'''
    if len(p) > 6:
        p[0] = IfBlock(p[3], p[5], p[7])
    elif p[1] == 'if':
        p[0] = IfBlock(p[3], p[5])
    elif p[1] == 'while':
        p[0] = WhileBlock(p[3], p[5])
    elif p[1] == 'print':
        p[0] = Print(p[3])
    elif len(p) > 2 and p[2] == '=':
        p[0] = VariableAssignment(p[1], p[3])
    else:
        p[0] = BlockStatements(p[1])


def p_prop_fun_call(p):
    '''prop : SBMLVAR LPAREN inParams RPAREN
            | SBMLVAR LPAREN RPAREN'''
    if len(p) > 4:
        p[0] = FunctionCall(p[1], p[3])
    else:
        p[0] = FunctionCall(p[1])


def p_prop_fun_in_params(p):
    '''inParams : prop COMMA inParams
               | prop'''
    if len(p) > 2:
        p[0] = Params(p[1], p[3])
    else:
        p[0] = Params(p[1], None)


def p_prop_integer(p):
    'prop : INTEGER'
    p[0] = Integer(p[1])


def p_prop_real(p):
    'prop : REAL'
    p[0] = Real(p[1])


def p_prop_string(p):
    'prop : STRING'
    p[0] = String(p[1])


def p_prop_variable(p):
    'prop : SBMLVAR '
    p[0] = Variable(p[1])


def p_expr_uminus(p):
    'prop : MINUS prop %prec UMINUS'
    p[0] = UnaryMinus(p[2])


def p_prop_operations(p):
    '''prop : prop POWER prop
            | prop TIMES prop
            | prop DIVIDE prop
            | prop INTDIVIDE prop
            | prop MODULUS prop
            | prop PLUS prop
            | prop MINUS prop
            | prop INSIDE prop
            | prop CONS prop'''
    p[0] = Operations(p[1], p[2], p[3])


def p_prop_bool_operations(p):
    '''prop : NEGATION prop
            | prop CONJUNCTION prop
            | prop DISJUNCTION prop
            | prop LESSTHAN prop
            | prop GREATEREQUAL prop
            | prop GREATERTHAN prop
            | prop NOTEQUAL prop
            | prop LESSEQUAL prop
            | prop EQUALTO prop'''
    if len(p) > 3:
        p[0] = Bool_Operations(p[1], p[2], p[3])
    else:
        p[0] = Bool_Operations(p[2], p[1])


def p_prop_bool(p):
    'prop : TRUE'
    p[0] = AST_True()


def p_prop_false(p):
    'prop : FALSE'
    p[0] = AST_False()


def p_prop_parenthetical(p):
    '''prop : LPAREN tup_prop RPAREN
            | LSQRBRCS tup_prop RSQRBRCS
            | LSQRBRCS RSQRBRCS
            | LPAREN prop RPAREN
            | LSQRBRCS prop RSQRBRCS '''
    if len(p) > 3:
        p[0] = Paren(p[1], p[2])
    else:
        p[0] = GetEmptyList()


def p_prop_list_index(p):
    '''prop : LSQRBRCS tup_prop RSQRBRCS list_ind
            | LSQRBRCS prop RSQRBRCS list_ind
            | SBMLVAR list_ind
            | STRING list_ind'''
    if len(p) > 3:
        p[0] = GetListIndElements(Paren(p[1], p[2]), p[4])
    else:
        p[0] = GetListIndElements(p[1], p[2])


def p_prop_list_ind(p):
    '''list_ind : LSQRBRCS tup_prop RSQRBRCS list_ind
                | LSQRBRCS tup_prop RSQRBRCS
                | LSQRBRCS prop RSQRBRCS list_ind
                | LSQRBRCS prop RSQRBRCS'''
    if len(p) > 4:
        p[0] = GetListInd(Paren(p[1], p[2]), p[4])
    else:
        p[0] = GetListInd(Paren(p[1], p[2]))


def p_prop_tup_ind(p):
    '''tup_ind : HASH prop
                | HASH prop tup_ind'''
    if len(p) > 3:
        p[0] = GetTupleInd(p[2], p[3])
    else:
        p[0] = GetTupleInd(p[2])


def p_prop_tuple_index(p):
    '''prop : tup_ind LPAREN tup_prop RPAREN
            | tup_ind LPAREN prop RPAREN'''
    p[0] = TupleInd(p[1], p[3])


def p_prop_tuple_element(p):
    '''tup_prop : prop COMMA tup_prop_tail
                | prop COMMA'''
    if len(p)>3:
        val = TupleListEle(p[1], p[3])
        if val == "Syntax Error":
            p_error(p)
        else:
            p[0] = val
    else:
        val = TupleListEle(p[1], None)
        if val == "Syntax Error":
            p_error(p)
        else:
            p[0] = val


def p_prop_tuple_tail(p):
    '''tup_prop_tail : prop COMMA tup_prop_tail
                     | prop'''
    if len(p)>3:
        val = TupleListEle(p[1], p[3])
        if val == "Syntax Error":
            p_error(p)
        else:
            p[0] = val
    else:
        val = TupleListEle(p[1], None)
        if val == "Syntax Error":
            p_error(p)
        else:
            p[0] = val


class SyntaxException(Exception):
    def _init_(self, value):
        self.value = value

    def _str_(self):
        return repr(self.value)


def p_error(p):
    raise SyntaxError(p)


class Node:
    def __init__(self):
        self.parent = None
        self.paren = False
        self.square_paren = False
        self.nested = False

    def parentCount(self):
        count = 0
        current = self.parent
        while current is not None:
            count += 1
            current = current.parent
        return count


class GetEmptyList(Node):
    def __init__(self):
        super().__init__()
        self.val = []
        self.square_paren = True

    def eval(self):
        # return self.val
        if self.parent and self.parent.square_paren:
            return [[]]
        else:
            return self.val

    def __str__(self):
        res = "\t" * self.parentCount() + "Empty List"
        return res


class Paren(Node):
    def __init__(self, braces, val):
        super().__init__()
        self.braces = braces
        self.val = val
        self.square_paren = True
        self.val.parent = self
        self.val.parent = self

        if braces == '(':
            self.val.paren = True
        else:
            self.val.square_paren = True

    def eval(self):
        if self.braces == '(':
            if self.parent and self.parent.paren:
                self.nested = True
            return self.val.eval()
        else:
            if self.parent and self.parent.square_paren:
                self.nested = True
            out = []
            eval_val = self.val.eval()

            if self.val.nested:
                # if eval_val.
                out += eval_val,
            elif type(eval_val) is list:
                out += eval_val
            else:
                out += eval_val,

            return out

    def __str__(self):
        res = "\t" * self.parentCount() + "Paren"
        return res


class TupleListEle(Node):
    def __init__(self, val_1, val_2):
        super().__init__()
        self.val_1 = val_1
        self.val_2 = val_2
        self.val_1.parent = self
        if val_2:
            self.val_2.parent = self

    def eval(self):
        if self.paren or self.square_paren:
            tup_val = self.val_1.eval()
            if self.paren:
                out = self.getTupVal(tup_val)
            elif self.square_paren:
                out = self.getListVal(tup_val)
            return out
        else:
            return "Syntax Error"

    def getTupVal(self, tup_val):
        out = ()
        if self.paren:
            self.val_1.paren = True

        if self.val_1.nested:
            out += (tup_val,)
        elif type(tup_val) is tuple:
            out += tup_val
        else:
            out += tup_val,

        if self.val_2:
            if self.paren:
                self.val_2.paren = True
            tup_val = self.val_2.eval()

            if self.val_2.nested:
                out += (tup_val,)
            elif type(tup_val) is tuple:
                out += tup_val
            else:
                out += tup_val,

        return out

    def getListVal(self, tup_val):
        out = []
        if self.square_paren:
            self.val_1.square_paren = True

        if self.val_1.nested:
            out += [tup_val]
        elif type(tup_val) is list:
            out += tup_val
        else:
            out += tup_val,

        if self.val_2:
            if self.square_paren:
                self.val_2.square_paren = True

            tup_val = self.val_2.eval()
            if self.val_2.nested:
                out += [tup_val]
            elif type(tup_val) is list:
                out += tup_val
            else:
                out += tup_val,

        return out

    def __str__(self):
        if self.paren:
            res = "\t" * self.parentCount() + "Tuple"
        else:
            res = "\t" * self.parentCount() + "List"
        res += "\n" + str(self.val_1)
        res += "\n" + str(self.val_2)
        return res


class GetTupleInd(Node):
    def __init__(self, num, multi_ind = None):
        super().__init__()
        self.number = num
        self.multi_ind = multi_ind
        if self.multi_ind:
            self.multi_ind.parent = self

    def eval(self):
        out = []
        out += [self.number]
        if self.multi_ind:
            out += self.multi_ind.eval()
        return out

    def __str__(self):
        res = "\t" * self.parentCount() + "GetTupleInd"
        return res


class GetListInd(Node):
    def __init__(self, num, multi_ind = None):
        super().__init__()
        self.number = num
        self.multi_ind = multi_ind
        if self.multi_ind:
            self.multi_ind.parent = self

    def eval(self):
        out = []
        val = self.number.eval()
        if type(val) is not list:
            out += [val]
        elif len(val) > 1:
            raise SyntaxError
        else:
            out += val
        if self.multi_ind:
            out += self.multi_ind.eval()
        return out

    def __str__(self):
        res = "\t" * self.parentCount() + "GetListInd"
        return res


class TupleInd(Node):
    def __init__(self, ind, tup):
        super().__init__()
        self.index = ind
        self.elements = tup
        self.paren = True
        self.elements.paren = True
        self.elements.parent = self

    def eval(self):
        out = self.elements.eval()
        lis = self.index.eval()
        for item in lis:
            out = out[item.eval()-1]
        return out

    def __str__(self):
        res = "\t" * self.parentCount() + "Tuple Index"
        return res


class GetListIndElements(Node):
    def __init__(self, lis, ind):
        super().__init__()
        self.index = ind
        self.elements = lis
        if type(lis) is not str:
            self.elements.square_paren = True
            self.elements.parent = self

    def eval(self, change_val = None):
        val = None
        if type(self.elements) is str:
            val = variable_dict.get(self.elements)
            if val is not None:
                out = val
            else:
                out = self.elements
        else:
            out = self.elements.eval()
        ind_lis = self.index.eval()
        for item in ind_lis[:-1]:
            out = out[item]
        if change_val is not None:
            out[ind_lis[-1]] = change_val
        else:
            out = out[ind_lis[-1]]
        return out

    def __str__(self):
        res = "\t" * self.parentCount() + "Tuple Index"
        return res


class Integer(Node):
    def __init__(self, val):
        super().__init__()
        self.value = int(val)

    def eval(self):
        return self.value

    def __str__(self):
        res = "\t" * self.parentCount() + "Integer"
        return res


class Real(Node):
    def __init__(self, val):
        super().__init__()
        self.value = float(val)

    def eval(self):
        return self.value

    def __str__(self):
        res = "\t" * self.parentCount() + "Float"
        return res


class String(Node):
    def __init__(self, val):
        super().__init__()
        self.value = str(val)

    def eval(self):
        return self.value

    def __str__(self):
        res = "\t" * self.parentCount() + "String"
        return res


class Variable(Node):
    def __init__(self, val):
        super().__init__()
        self.value = str(val)

    def eval(self):
        return variable_dict.get(self.name())

    def name(self):
        return self.value

    def __str__(self):
        res = "\t" * self.parentCount() + "Variable"
        return res


class UnaryMinus(Node):
    def __init__(self, val):
        super().__init__()
        self.value = val

    def eval(self):
        return -(self.value.eval())

    def __str__(self):
        res = "\t" * self.parentCount() + "UMINUS"
        return res


class Operations(Node):
    def __init__(self, left, oper, right):
        super().__init__()
        self.left = left
        self.right = right
        self.oper = oper
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        if self.oper == '**' :
            return self.left.eval() ** self.right.eval()
        elif self.oper == '*' :
            return self.left.eval() * self.right.eval()
        elif self.oper == '/' :
            return self.left.eval() / self.right.eval()
        elif self.oper == 'div':
            return self.left.eval() // self.right.eval()
        elif self.oper == 'mod':
            return self.left.eval() % self.right.eval()
        elif self.oper == '+':
            return self.left.eval() + self.right.eval()
        elif self.oper == '-':
            return self.left.eval() - self.right.eval()
        elif self.oper == 'in':
            return self.left.eval() in self.right.eval()
        elif self.oper == '::':
            return [self.left.eval()] + self.right.eval()

    def __str__(self):
        res = "\t" * self.parentCount() + self.oper
        res += "\n" + str(self.left)
        res += "\n" + str(self.right)
        return res


class Bool_Operations(Node):
    def __init__(self, left, oper, right = None):
        super().__init__()
        self.left = left
        self.right = right
        self.oper = oper
        self.left.parent = self
        if self.right:
            self.right.parent = self

    def eval(self):
        left_val = self.left.eval()
        if self.right:
            right_val = self.right.eval()
        if self.oper == 'not':
            return not left_val
        elif self.oper == 'andalso' :
            return left_val and right_val
        elif self.oper == 'orelse' :
            return left_val or right_val
        elif self.oper == '<':
            return left_val < right_val
        elif self.oper == '==':
            return left_val == right_val
        elif self.oper == '<=':
            return left_val <= right_val
        elif self.oper == '<>':
            return left_val !=  right_val
        elif self.oper == '>=':
            return left_val >= right_val
        elif self.oper == '>':
            return left_val > right_val

    def __str__(self):
        res = "\t" * self.parentCount() + self.oper
        res += "\n" + str(self.left)
        if self.right:
            res += "\n" + str(self.right)
        return res


class VariableAssignment(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.right.parent = self

    def eval(self):
        if type(self.left) is Variable:
            key = self.left.name()
            val = self.right.eval()
            variable_dict.update({key: val})
        else:
            self.left.eval(self.right.eval())
        return

    def __str__(self):
        res = "\t" * self.parentCount() + "Variable"
        res += "\n" + str(self.left)
        res += "\n" + str(self.right)
        return res


class Print(Node):
    def __init__(self, exp):
        super().__init__()
        self.exp = exp
        self.exp.parent = self

    def eval(self):
        if type(self.exp) is Variable:
            print(str(self.exp.eval()))
        else:
            print(self.exp.eval())
        return

    def __str__(self):
        res = "\t" * self.parentCount() + "Print"
        res += "\n" + str(self.exp)
        return res


class MultiStatements(Node):
    def __init__(self, exp, multiExp = None):
        super().__init__()
        self.exp = exp
        self.multiExp = multiExp
        self.exp.parent = self
        if self.multiExp:
            self.multiExp.parent = self

    def eval(self):
        self.exp.eval()
        if self.multiExp:
            self.multiExp.eval()
        return

    def __str__(self):
        res = "\t" * self.parentCount() + "MultiStatements"
        res += "\n" + str(self.exp)
        return res


class BlockStatements(Node):
    def __init__(self, exp):
        super().__init__()
        self.exp = exp
        if self.exp:
            self.exp.parent = self

    def eval(self):
        if self.exp:
            self.exp.eval()
        return

    def __str__(self):
        res = "\t" * self.parentCount() + "BlockStatements"
        res += "\n" + str(self.exp)
        return res


class FunctionDef(Node):
    def __init__(self, funName, inParams, funBlock, outParams = None):
        super().__init__()
        self.funName = funName
        self.inParams = inParams
        self.funBlock = funBlock
        self.outParams = outParams

    def eval(self):
        global variable_dict
        if self.funBlock:
            self.funBlock.eval()
        return

    def __str__(self):
        res = "\t" * self.parentCount() + "FunctionDef"
        res += "\n" + str(self.funName)
        return res


class FunctionCall(Node):
    def __init__(self, funName, inParams = None):
        super().__init__()
        self.funName = funName
        self.inParams = inParams

    def eval(self):

        global variable_dict

        funBlock = functions_Name_dict.get(self.funName)
        funParamsDict = {}

        if funBlock.inParams or self.inParams:
            inParams = self.inParams.eval()
            funInParams = funBlock.inParams.eval()

            n = len(inParams)
            if n != len(funInParams):
                raise SyntaxError

            for i in range(n):
                funParamsDict.update({funInParams[i]: inParams[i]})

        funVariableStack.append(variable_dict)
        variable_dict = funParamsDict
        funBlock.eval()
        out = None
        if funBlock.outParams:
            out = funBlock.outParams.eval()
        variable_dict = funVariableStack.pop()

        return out

    def __str__(self):
        res = "\t" * self.parentCount() + "FunctionCall"
        res += "\n" + str(self.funName)
        return res


class MainBlock(Node):
    def __init__(self, prop_list):
        super().__init__()
        self.prop_list = prop_list

    def eval(self):
        for prop in  self.prop_list:
            if type(prop) is FunctionDef:
                functions_Name_dict.update({prop.funName: prop})
            elif type(prop) is FunctionCall:
                functions_Name_dict.get(prop.funName).eval()
            elif prop:
                prop.eval()
        return

    def __str__(self):
        res = "\t" * self.parentCount() + "Main Block"
        res += "\n" + str(self.prop_list)
        return res


class Params(Node):
    def __init__(self, param1, param2):
        super().__init__()
        self.param1 = param1
        self.param2 = param2

    def eval(self):
        out = []
        if type(self.param1) is str:
            out.append(self.param1)
        else:
            val1 = self.param1.eval()
            if type(val1) is list:
                if type(self.param1) is not Params:
                    out = out + [val1.copy()]
                else:
                    out = out + val1
            else:
                out.append(val1)

        if self.param2:
            if type(self.param2) is str:
                out.append(self.param2)
            else:
                val2 = self.param2.eval()
                if type(val2) is list:
                    if type(self.param2) is not Params:
                        out = out + [val2.copy()]
                    else:
                        out = out + val2
                else:
                    out.append(val2)
        return out


class IfBlock(Node):
    def __init__(self, exp_1, exp_2, exp_3 = None):
        super().__init__()
        self.exp_1 = exp_1
        self.exp_2 = exp_2
        self.exp_3 = exp_3
        self.exp_1.parent = self
        if self.exp_2:
            self.exp_2.parent = self
        if self.exp_3:
            self.exp_3.parent = self

    def eval(self):
        val = None
        if self.exp_3 is not None:
            if self.exp_1.eval():
                if self.exp_2 is not None:
                    self.exp_2.eval()
            else:
                self.exp_3.eval()
        elif self.exp_1.eval():
            if self.exp_2 is not None:
                self.exp_2.eval()
        return

    def __str__(self):
        res = "\t" * self.parentCount() + "IfBlock"
        res += "\n" + str(self.exp_1) + str(self.exp_2)
        return res


class WhileBlock(Node):
    def __init__(self, exp_1, exp_2):
        super().__init__()
        self.exp_1 = exp_1
        self.exp_2 = exp_2
        self.exp_1.parent = self
        if self.exp_2:
            self.exp_2.parent = self

    def eval(self):
        while self.exp_1.eval():
            if self.exp_2:
                self.exp_2.eval()
            else:
                return
        return

    def __str__(self):
        res = "\t" * self.parentCount() + "While Block"
        res += "\n" + str(self.exp_1) + str(self.exp_2)
        return res


class AST_True(Node):
    def __init__(self):
        super().__init__()
        self.value = True

    def eval(self):
        return self.value

    def __str__(self):
        res = "\t" * self.parentCount() + "True"
        return res


class AST_False(Node):
    def __init__(self):
        super().__init__()
        self.value = False

    def eval(self):
        return self.value

    def __str__(self):
        res = "\t" * self.parentCount() + "False"
        return res


import ply.yacc as yacc
import ply.lex as lex

lexer = lex.lex()
parser = yacc.yacc()


def parse(inp):
    result = parser.parse(inp)
    return result



# def main():
#     error_count = 0
#     pass_count = 0
#     for i in range(1, 12):
#         file_name = sys.argv[1]  + str(i) + ".txt"
#         with open(file_name, 'r') as file:
#             data = file.read().replace('\n', '')
#             try:
#                 result = parser.parse(data, debug=0)
#                 if result is not None:
#                     result.eval()
#                     pass_count += 1
#             except SyntaxError as e:
#                 error_count += 1
#                 print("SYNTAX ERROR --- ")
#             except Exception as e:
#                 error_count += 1
#                 print("SEMANTIC ERROR --- ")
#
#     print("Total test cases passed : " + str(pass_count))
#     print("Total errors : " + str(error_count))
#
#
# if __name__ == "__main__":
#     main()






def main():
    while True:
        print("Enter data: ")
        data = input()
        result = parser.parse(data, debug=0)
        if result is not None:
            result.eval()
        # try:
        #     result = parser.parse(data, debug=0)
        #     if result is not None:
        #         result.eval()
        # except:
        #     raise ec
            # print("error")
        # except SyntaxError as e:
        #     print("SYNTAX ERROR --- ")
        # except Exception as e:
        #     print("SEMANTIC ERROR --- ")
        print(" ")


if __name__ == "__main__":
    main()






