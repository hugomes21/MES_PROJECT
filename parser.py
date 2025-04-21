from lark import Lark, Transformer, v_args
from Lang import *

grammar = r"""
    start: stmt+

    stmt: assign_stmt | if_stmt | for_stmt | while_stmt | funcdef_stmt

    assign_stmt: IDENTIFIER "=" expr "\n"

    if_stmt: "if" expr ":" "\n" stmt+ "else" ":" "\n" stmt+

    for_stmt: "for" IDENTIFIER "in" "range" "(" expr "," expr ")" ":" "\n" stmt+

    while_stmt: "while" expr ":" "\n" stmt+

    funcdef_stmt: "def" IDENTIFIER "(" [IDENTIFIER ("," IDENTIFIER)*] ")" ":" "\n" stmt+

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
    def number(self, n): # n[0] é o número
        return IntLit(int(n[0]))

    def boolean(self, b): # b[0] é o booleano
        return BoolLit(b[0] == "true")

    def var(self, name): # name[0] é o nome da variável
        return Var(name[0])

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
        return Assign(args[0], args[1])
    
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
        params = []
        body_start = 1
        if isinstance(args[1], list):
            params = [str(p) for p in args[1]]
            body_start = 2
        elif isinstance(args[1], str):
            params = [args[1]]
            body_start = 2
        elif isinstance(args[1], Stmt):
            params = []
            body_start = 1
        else:
            params = []
        body = args[body_start:]
        return FunctionDef(name, params, body)

    def start(self, stmts): # stmts é uma lista de declarações
        if not isinstance(stmts, list):
            raise ValueError("Invalid program")
        return Program(stmts)

parser = Lark(grammar, parser='lalr', transformer=ASTTransformer())

def parse_code(code: str) -> Program:
    return parser.parse(code)

if __name__ == "__main__":
    # Exemplos válidos (mais complexos)
    valid_programs = [
        ("x = 10\ny = 20\nz = x * y + (x - y) / 2\n", "Programa válido 1"),
        ("a = 5\nb = a * (a + 2)\nc = b == 35\nd = c != false\n", "Programa válido 2"),
        ("flag = true\nresult = flag == false\nother = (result != true) + 1\n", "Programa válido 3"),
        ("n1 = 7\nn2 = 3\nsum = n1 + n2\nprod = sum * (n1 - n2)\n", "Programa válido 4"),
        ("x = 1\ny = 2\nz = 3\nw = (x + y + z) * (x - y - z)\n", "Programa válido 5"),
        ("a = 10\nb = 2\nc = a / b\nis_small = c < 10\n", "Programa válido 6"),
    ]

    for code, description in valid_programs:
        try:
            ast = parse_code(code)
            print(f"✅ {description} parseado com sucesso:\n{ast}\n")
        except Exception as e:
            print(f"❌ {description} falhou inesperadamente: {e}\n")

    # Exemplos inválidos (mais complexos)
    invalid_programs = [
        ("x = 10\ny =\nz = x + y\n", "Programa inválido 1"),
        ("a = 5\nb = * 2\n", "Programa inválido 2"),
        ("flag = true\nresult = flag ==\n", "Programa inválido 3"),
        ("x = (10 + 2\n", "Programa inválido 4"),
        ("y = 3 +\n", "Programa inválido 5"),
    ]

    for code, description in invalid_programs:
        try:
            ast = parse_code(code)
            print(f"❌ {description} deveria falhar mas foi parseado:\n{ast}\n")
        except Exception as e:
            print(f"✅ {description} corretamente rejeitado: {e}\n")