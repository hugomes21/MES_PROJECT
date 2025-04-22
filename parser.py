from lark import Lark, Transformer, Token
from Lang import *

grammar = r"""
start: stmt*

stmt: assign_stmt
    | if_stmt
    | for_stmt
    | while_stmt
    | funcdef_stmt
    | return_stmt

assign_stmt: IDENTIFIER "=" expr NEWLINE
return_stmt: "return" expr NEWLINE

funcdef_stmt: "def" IDENTIFIER "(" parameters? ")" ":" NEWLINE stmt+

if_stmt: "if" expr ":" NEWLINE stmt+ "else" ":" NEWLINE stmt+

for_stmt: "for" IDENTIFIER "in" "range" "(" expr "," expr ")" ":" NEWLINE stmt+

while_stmt: "while" expr ":" NEWLINE stmt+

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
        | BOOLEAN          -> boolean
        | IDENTIFIER       -> var
        | "(" expr ")"

BOOLEAN: "true" | "false"
IDENTIFIER: /[a-zA-Z_]\w*/
NUMBER: /-?\d+/

%import common.NEWLINE
%import common.WS_INLINE
%ignore WS_INLINE
"""

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

    
    def if_stmt(self, args):
        cond = args[0]
        then_branch = args[1:1+len(args[1:])//2]
        else_branch = args[1+len(args[1:])//2:]
        return If(cond, then_branch, else_branch)
    
    def for_stmt(self, args):
        var = args[0]   # variável for
        start = args[1] # valor inicial
        end = args[2]   # valor final
        body = args[3:] # corpo do loop
        return For(var, start, end, body)
    
    def while_stmt(self, args):
        cond = args[0]
        body = args[1:]
        return While(cond, body)
    
    def funccall(self, args):
        name = args[0]
        params = args[1:]
        return FunctionCall(name, params)

    def funcdef_stmt(self, args):
        name = args[0]
        if isinstance(args[1], list):
            params = [str(p) for p in args[1]]
            body = args[2:]
        elif isinstance(args[1], Token):
            params = [str(args[1])]
            body = args[2:]
        else:
            params = []
            body = args[1:]
        return FunctionDef(name, params, body)

parser = Lark(grammar, parser='lalr', transformer=ASTTransformer())

def parse_code(code: str) -> Program:
    # NÃO remova a indentação!
    clean_code = code.strip() + "\n"
    return parser.parse(clean_code)

