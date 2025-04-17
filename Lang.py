from dataclasses import dataclass
from typing import List, Union, Optional

# 1.1 Language AST (Abstract Syntax Tree)
# EXPRESSÕES

@dataclass
class Expr:
    pass

@dataclass
class Var(Expr):
    name: str

@dataclass
class IntLit(Expr):
    value: int

@dataclass
class BoolLit(Expr):
    value: bool

@dataclass
class BinOp(Expr):
    op: str  # '+', '-', '*', '/', '==', '&&', '||', '<', etc.
    left: Expr
    right: Expr

@dataclass
class UnaryOp(Expr):
    op: str  # 'not', '-' (negativo)
    expr: Expr

# INSTRUÇÕES

@dataclass
class Stmt:
    pass

@dataclass
class Assign(Stmt):
    var: str
    expr: Expr

@dataclass
class If(Stmt):
    condition: Expr
    then_branch: List[Stmt]
    else_branch: List[Stmt]

@dataclass
class While(Stmt):
    condition: Expr
    body: List[Stmt]

@dataclass
class For(Stmt):
    var: str
    start: Expr
    end: Expr
    body: List[Stmt]

@dataclass
class Seq(Stmt):
    stmts: List[Stmt]

# FUNÇÕES
@dataclass
class FunctionDef(Stmt):
    name: str
    params: List[str]
    body: List[Stmt]

@dataclass
class FunctionCall(Expr):
    name: str
    args: List[Expr]

# RAIZ DO PROGRAMA

@dataclass
class Program:
    body: List[Stmt]


# EXEMPLOS DE USO
programa1 = Program([
    Assign("x", IntLit(10)), # x = 10
    Assign("y", BinOp("+", Var("x"), IntLit(5))) # y = x + 5
])

programa2 = Program([
    Assign("a", IntLit(3)), # a = 3
    Assign("b", IntLit(4)), # b = 4
    If(
        condition=BinOp(">", Var("a"), Var("b")), # if a > b
        then_branch=[Assign("max", Var("a"))], # max = a
        else_branch=[Assign("max", Var("b"))] # else max = b
    )
])

programa3 = Program([
    Assign("sum", IntLit(0)), # sum = 0
    For(
        var="i", 
        start=IntLit(1), # for i in range(1, 5)
        end=IntLit(5),
        body=[
            Assign("sum", BinOp("+", Var("sum"), Var("i"))) # sum += i
        ]
    )
])

programa4 = Program([
    Assign("x", IntLit(10)),  # x = 10
    Assign("y", IntLit(0)),   # y = 0
    While(
        condition=BinOp(">", Var("x"), IntLit(0)),  # while x > 0
        body=[
            Assign("y", BinOp("+", Var("y"), Var("x"))),  # y += x
            Assign("x", BinOp("-", Var("x"), IntLit(1)))  # x -= 1
        ]
    )
])
 
programa5 = Program([
    FunctionDef(
        name="add",
        params=["a", "b"],
        body=[
            Assign("result", BinOp("+", Var("a"), Var("b"))),  # result = a + b
            Assign("return", Var("result"))                   # return result
        ]
    ),
    Assign("z", FunctionCall("add", [IntLit(5), IntLit(7)]))  # z = add(5, 7)
])

programa6 = Program([
    Seq([
        Assign("a", IntLit(1)),  # a = 1
        Assign("b", IntLit(2)),  # b = 2
        Assign("c", BinOp("*", Var("a"), Var("b")))  # c = a * b
    ])
])

programa7 = Program([
    Assign("x", BoolLit(True)),  # x = true
    Assign("y", BoolLit(False)), # y = false
    If(
        condition=BinOp("&&", Var("x"), UnaryOp("not", Var("y"))),  # if x && not y
        then_branch=[Assign("result", IntLit(1))],  # result = 1
        else_branch=[Assign("result", IntLit(0))]  # else result = 0
    )
])

# 1.3 Pretty Printing

def indent(lines, level=1):
    return ["    " * level + line for line in lines]

def pretty_expr(expr: Expr) -> str:
    if isinstance(expr, Var):
        return expr.name
    elif isinstance(expr, IntLit):
        return str(expr.value)
    elif isinstance(expr, BoolLit):
        return str(expr.value).lower()
    elif isinstance(expr, BinOp):
        return f"({pretty_expr(expr.left)} {expr.op} {pretty_expr(expr.right)})"
    elif isinstance(expr, UnaryOp):
        return f"({expr.op} {pretty_expr(expr.expr)})"
    elif isinstance(expr, FunctionCall):
        args = ", ".join(pretty_expr(a) for a in expr.args)
        return f"{expr.name}({args})"
    else:
        return "???"

def pretty_stmt(stmt: Stmt, level=0) -> List[str]:
    if isinstance(stmt, Assign):
        return [f"{stmt.var} = {pretty_expr(stmt.expr)}"]
    elif isinstance(stmt, If):
        cond = pretty_expr(stmt.condition)
        then_lines = sum([pretty_stmt(s, level + 1) for s in stmt.then_branch], [])
        else_lines = sum([pretty_stmt(s, level + 1) for s in stmt.else_branch], [])
        return [f"if {cond}:"] \
            + indent(then_lines, level + 1) \
            + [f"else:"] \
            + indent(else_lines, level + 1)
    elif isinstance(stmt, While):
        cond = pretty_expr(stmt.condition)
        body = sum([pretty_stmt(s, level + 1) for s in stmt.body], [])
        return [f"while {cond}:"] \
            + indent(body, level + 1)
    elif isinstance(stmt, For):
        start = pretty_expr(stmt.start)
        end = pretty_expr(stmt.end)
        body = sum([pretty_stmt(s, level + 1) for s in stmt.body], [])
        return [f"for {stmt.var} in range({start}, {end}):"] \
            + indent(body, level + 1)
    elif isinstance(stmt, FunctionDef):
        header = f"def {stmt.name}({', '.join(stmt.params)}):"
        body = sum([pretty_stmt(s, level + 1) for s in stmt.body], [])
        return [header] + indent(body, level + 1)
    elif isinstance(stmt, Seq):
        return sum([pretty_stmt(s, level) for s in stmt.stmts], [])
    else:
        return [f"# unknown statement {stmt}"]

def pretty_program(prog: Program) -> str:
    lines = sum([pretty_stmt(s) for s in prog.body], [])
    return "\n".join(line.lstrip() for line in lines) + "\n"

# Injetar __str__ no Program
Program.__str__ = lambda self: pretty_program(self)


# PONTO DE ENTRADA
if __name__ == "__main__":
    print("Programa 1:", programa1)
    print("Programa 2:", programa2)
    print("Programa 3:", programa3)
    print("Programa 4:", programa4)
    print("Programa 5:", programa5)
    print("Programa 6:", programa6)
    print("Programa 7:", programa7)