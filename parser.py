from lark import Lark, Transformer, Token
from lark.indenter import Indenter
from Lang import *

grammar = r"""
%import common.CNAME -> NAME
%import common.WS_INLINE
%import common.SH_COMMENT
%ignore WS_INLINE
%ignore SH_COMMENT
%declare _INDENT _DEDENT

start: stmt*

stmt: assign_stmt
    | if_stmt
    | for_stmt
    | while_stmt
    | funcdef_stmt
    | return_stmt

assign_stmt: IDENTIFIER "=" expr _NL
return_stmt: "return" expr _NL

funcdef_stmt: "def" IDENTIFIER "(" parameters? ")" ":" _NL _INDENT stmt+ _DEDENT

if_stmt: "if" expr ":" _NL _INDENT stmt+ _DEDENT "else" ":" _NL _INDENT stmt+ _DEDENT

for_stmt: "for" IDENTIFIER "in" "range" "(" expr "," expr ")" ":" _NL _INDENT stmt+ _DEDENT

while_stmt: "while" expr ":" _NL _INDENT stmt+ _DEDENT

parameters: IDENTIFIER ("," IDENTIFIER)*

?expr: expr "==" expr   -> eq
        | expr "!=" expr   -> neq
        | expr "<" expr    -> lt
        | expr ">" expr    -> gt
        | expr "+" expr    -> add
        | expr "-" expr    -> sub
        | expr "*" expr    -> mul
        | expr "/" expr    -> div
        | expr "&&" expr  -> and_
        | expr "||" expr  -> or_
        | "(" "not" expr ")"   -> not_
        | IDENTIFIER "(" [expr ("," expr)*] ")" -> funccall
        | NUMBER           -> number
        | IDENTIFIER       -> var
        | BOOLEAN          -> boolean
        | "(" expr ")"

_NL: (/\r?\n[\t ]*/ | SH_COMMENT)+
BOOLEAN.10: "true" | "false"
IDENTIFIER: /[a-zA-Z_]\w*/
NUMBER: /-?\d+/
"""

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8

class ASTTransformer(Transformer):
    def start(self, stmts):
        return Program(stmts)

    def number(self, n): # n[0] é o número
        return IntLit(int(n[0]))

    def boolean(self, b): # b[0] é o booleano
        return BoolLit(b[0] == "true")

    def var(self, name): # name[0] é o nome da variável
        return Var(str(name[0]))

    def add(self, args): # args[0] e args[1] são os operandos
        return BinOp("+", args[0], args[1])

    def sub(self, args):
        return BinOp("-", args[0], args[1])

    def mul(self, args):
        return BinOp("*", args[0], args[1])

    def div(self, args):
        return BinOp("/", args[0], args[1])

    def eq(self, args):
        return BinOp("==", args[0], args[1])

    def neq(self, args):
        return BinOp("!=", args[0], args[1])

    def lt(self, args):
        return BinOp("<", args[0], args[1])

    def gt(self, args):
        return BinOp(">", args[0], args[1])
    
    def and_(self, args):
        return BinOp("&&", args[0], args[1])
    
    def or_(self, args):
        return BinOp("||", args[0], args[1])
    
    def not_(self, args):
        return UnaryOp("not", args[0])

    def stmt(self, args):
        return args[0]    
    
    def assign_stmt(self, args):
        return Assign(str(args[0]), args[1])
    
    def return_stmt(self, args):
        return Return(args[0])
    
    def parameters(self, args):
        return [str(p) for p in args]

    def _filter_newlines(self, stmts):
        # Remove tokens _NL das listas de statements
        return [s for s in stmts if not (isinstance(s, Token) and s.type == "_NL")]


    def if_stmt(self, args):
        cond = args[0]
        stmts = self._filter_newlines(args[1:])
        half = len(stmts) // 2
        then_branch = stmts[:half]
        else_branch = stmts[half:]
        return If(cond, then_branch, else_branch)
    
    def for_stmt(self, args):
        var = str(args[0])
        start = args[1]
        end = args[2]
        body = self._filter_newlines(args[3:])
        return For(var, start, end, body)
    
    def while_stmt(self, args):
        cond = args[0]
        body = self._filter_newlines(args[1:])
        return While(cond, body)
    
    def funccall(self, args):
        name = str(args[0])
        params = args[1:]
        return FunctionCall(name, params)

    def funcdef_stmt(self, args):
        name = str(args[0])
        if isinstance(args[1], list):
            params = [str(p) for p in args[1]]
            body = self._filter_newlines(args[2:])
        elif isinstance(args[1], Token):
            params = [str(args[1])]
            body = self._filter_newlines(args[2:])
        else:
            params = []
            body = self._filter_newlines(args[1:])
        return FunctionDef(name, params, body)

parser = Lark(grammar, parser='lalr', transformer=ASTTransformer(), postlex=TreeIndenter())

def parse_code(code: str) -> Program:
    return parser.parse(code.strip() + "\n")