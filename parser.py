from parsita import TextParsers, lit, reg, opt, rep, rep1, eof
from Lang import *

# Helper to remove indentation (strip whitespace)
def wsp(p):
    return p << opt(reg(r'[ \t]*'))

class LangParser(TextParsers):
    number = reg(r'-?\d+').map(lambda x: IntLit(int(x)))
    boolean = (lit('true').result(BoolLit(True)) | lit('false').result(BoolLit(False)))
    identifier = reg(r'[a-zA-Z_]\w*')

    var = identifier.map(Var)

    lparen = lit('(')
    rparen = lit(')')

    # Forward declaration
    def lazy_expr(): return LangParser.expr

    atom = number | boolean | var | (lparen >> lazy_expr << rparen)

    @staticmethod
    def bin_expr(term_parser, ops):
        def parser():
            return term_parser & rep(wsp(ops) & term_parser)
        return parser().map(LangParser.fold_binop)

    @staticmethod
    def fold_binop(first_and_rest):
        first, rest = first_and_rest
        result = first
        for (op, rhs) in rest:
            result = BinOp(op, result, rhs)
        return result

    mul_div = bin_expr(atom, lit('*') | lit('/'))
    add_sub = bin_expr(mul_div, lit('+') | lit('-'))
    comparisons = bin_expr(add_sub, lit('==') | lit('!=') | lit('<') | lit('>'))
    expr = comparisons

    # Statements
    assignment = (identifier << lit('=')) & expr << lit('\n')
    assignment = assignment.map(lambda pair: Assign(pair[0], pair[1]))

    if_stmt = (
        lit('if') >> expr << lit(':') << lit('\n') &
        rep1(wsp(reg(r'.+')) << lit('\n')) &
        lit('else:') << lit('\n') &
        rep1(wsp(reg(r'.+')) << lit('\n'))
    ).map(lambda t: If(t[0], [Assign('todo_then', IntLit(0))], [Assign('todo_else', IntLit(0))]))  # Placeholder parsing

    while_stmt = (
        lit('while') >> expr << lit(':') << lit('\n') &
        rep1(wsp(reg(r'.+')) << lit('\n'))
    ).map(lambda t: While(t[0], [Assign('todo_while', IntLit(0))]))

    for_stmt = (
        lit('for') >> identifier << lit('in') << lit('range(') & expr << lit(',') & expr << lit('):') << lit('\n') &
        rep1(wsp(reg(r'.+')) << lit('\n'))
    ).map(lambda t: For(t[0], t[1], t[2], [Assign('todo_for', IntLit(0))]))

    stmt = assignment | if_stmt | while_stmt | for_stmt
    stmts = rep(stmt)

    program = stmts << eof
    program = program.map(lambda lst: Program(lst))

def parse_code(code: str) -> Program:
    result = LangParser.program.parse(code)
    if result.status:
        return result.value
    else:
        raise SyntaxError("Parsing failed:\n" + result.expecting)

# -------- Testes --------
valid_programs = [
    """
x = 10
y = x + 5
""",
    """
a = 3
b = 4
if a > b:
    max = a
else:
    max = b
""",
    """
sum = 0
for i in range(1, 5):
    sum = sum + i
"""
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
    for i, code in enumerate(valid_programs):
        try:
            ast = parse_code(code)
            print(f"Valid program {i+1} parsed successfully:")
            print(ast)
            print()
        except SyntaxError as e:
            print(f"Valid program {i+1} failed to parse:\n{e}\n")

    for i, code in enumerate(invalid_programs):
        try:
            ast = parse_code(code)
            print(f"Invalid program {i+1} should not parse, but got:\n{ast}\n")
        except SyntaxError:
            print(f"Invalid program {i+1} correctly failed to parse.\n")
