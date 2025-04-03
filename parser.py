from parsita import Parser, lit, reg, opt, rep, rep1, eof, Success, Failure
from Lang import *

# Helper to remove indentation (strip whitespace)
def wsp(p):
    return opt(reg(r'[ \t]*')) >> p << opt(reg(r'[ \t]*'))


class LangParser(Parser):
    number = wsp(reg(r'-?\d+')) >> (lambda x: IntLit(int(x)))
    boolean = (wsp(lit('true')) >> (lambda _: BoolLit(True))) | (lit('false') >> (lambda _: BoolLit(False)))
    identifier = reg(r'[a-zA-Z_]\w*')

    var = identifier >> Var

    lparen = lit('(')
    rparen = lit(')')

    # Forward declaration
    def lazy_expr(): return LangParser.expr

    atom = number | boolean | var | (lparen >> lazy_expr << rparen)

    @staticmethod
    def bin_expr(term_parser, ops):
        def parser():
            return term_parser & rep(wsp(ops) & term_parser)
        return parser() >> LangParser.fold_binop

    @staticmethod
    def fold_binop(first_and_rest):
        first, rest = first_and_rest
        result = first
        for (op, rhs) in rest:
            result = BinOp(op, result, rhs)
        return result

# Define expressions after the class is fully defined
LangParser.mul_div = LangParser.bin_expr(LangParser.atom, wsp(lit('*')) | wsp(lit('/')))
LangParser.add_sub = LangParser.bin_expr(LangParser.mul_div, wsp(lit('+')) | wsp(lit('-')))
LangParser.comparisons = LangParser.bin_expr(LangParser.add_sub, wsp(lit('==')) | wsp(lit('!=')) | wsp(lit('<')) | wsp(lit('>')))
LangParser.expr = LangParser.comparisons

# Statements
LangParser.assignment = (LangParser.identifier << wsp(lit('='))) & LangParser.expr << wsp(lit('\n'))
LangParser.assignment = LangParser.assignment >> (lambda pair: Assign(pair[0], pair[1]))

LangParser.if_stmt = (
    wsp(lit('if')) >> LangParser.expr << wsp(lit(':')) << wsp(lit('\n')) &
    rep1(LangParser.stmt) &
    wsp(lit('else:')) << wsp(lit('\n')) &
    rep1(LangParser.stmt)
) >> (lambda t: If(t[0], t[1], t[2]))

LangParser.while_stmt = (
    wsp(lit('while')) >> LangParser.expr << wsp(lit(':')) << wsp(lit('\n')) &
    rep1(LangParser.stmt)
) >> (lambda t: While(t[0], t[1]))

LangParser.for_stmt = (
    wsp(lit('for')) >> LangParser.identifier << wsp(lit('in')) << wsp(lit('range(')) &
    LangParser.expr << wsp(lit(',')) & LangParser.expr << wsp(lit('):')) << wsp(lit('\n')) &
    rep1(LangParser.stmt)
) >> (lambda t: For(t[0], t[1], t[2], t[3]))

LangParser.stmt = LangParser.assignment | LangParser.if_stmt | LangParser.while_stmt | LangParser.for_stmt
LangParser.stmts = rep(LangParser.stmt)

LangParser.program = opt(rep(wsp(lit('\n')))) >> LangParser.stmts << eof
LangParser.program = LangParser.program >> (lambda lst: Program(lst))

def parse_code(code: str) -> Program:
    result = LangParser.program.parse(code)
    if isinstance(result, Success):
        return result.value
    else:
        raise SyntaxError(f"Parsing failed:\n{result.explanation}")

from Lang import programa1, programa2, programa3, programa4, programa5, programa6, programa7

# -------- Testes --------
valid_programs = [
    ("""
x = 10
y = x + 5
""", programa1),
    ("""
a = 3
b = 4
if a > b:
    max = a
else:
    max = b
""", programa2),
    ("""
sum = 0
for i in range(1, 5):
    sum = sum + i
""", programa3),
    ("""
x = 10
y = 0
while x > 0:
    y = y + x
    x = x - 1
""", programa4),
    ("""
def add(a, b):
    result = a + b
    return result

z = add(5, 7)
""", programa5),
    ("""
a = 1
b = 2
c = a * b
""", programa6),
    ("""
x = true
y = false
if x && not y:
    result = 1
else:
    result = 0
""", programa7),
]

invalid_programs = [
    """
x == 10
""",
    """
if x > 3
    y = 4
""",
    """
for i in range(1 5):
    x = x + 1
"""
]

if __name__ == "__main__":
    # Testar programas válidos
    for i, (code, expected_ast) in enumerate(valid_programs):
        try:
            ast = parse_code(code)
            assert ast == expected_ast, f"AST mismatch for valid program {i+1}"
            print(f"Valid program {i+1} parsed successfully and matches expected AST.")
        except SyntaxError as e:
            print(f"Valid program {i+1} failed to parse:\n{e}\n")
        except AssertionError as e:
            print(e)

    # Testar programas inválidos
    for i, code in enumerate(invalid_programs):
        try:
            ast = parse_code(code)
            print(f"Invalid program {i+1} should not parse, but got:\n{ast}\n")
        except SyntaxError:
            print(f"Invalid program {i+1} correctly failed to parse.\n")
