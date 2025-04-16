from lark import Lark, Transformer, v_args
from Lang import *

grammar = r"""
    start: stmt+

    stmt: IDENTIFIER "=" expr "\n"

    ?expr: expr "==" expr   -> eq
         | expr "!=" expr   -> neq
         | expr "<" expr    -> lt
         | expr ">" expr    -> gt
         | expr "+" expr    -> add
         | expr "-" expr    -> sub
         | expr "*" expr    -> mul
         | expr "/" expr    -> div
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

    def stmt(self, args): # args[0] é o nome da variável e args[1] é a expressão
        if len(args) != 2:
            raise ValueError("Invalid assignment statement")
        if not isinstance(args[0], str):
            raise ValueError("Invalid variable name")
        if not isinstance(args[1], Expr):
            raise ValueError("Invalid expression")
        return Assign(args[0], args[1])

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