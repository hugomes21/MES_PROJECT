from dataclasses import dataclass
from typing import List

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

@dataclass
class Return(Stmt):
    expr: Expr

@dataclass
class Print(Stmt):
    expr: Expr

# RAIZ DO PROGRAMA
@dataclass
class Program:
    body: List[Stmt]


# EXEMPLOS DE USO
programa1 = Program([
    Assign("x", IntLit(3)),
    Assign("y", IntLit(0)),
    While(
        condition=BinOp(">", Var("x"), IntLit(0)),
        body=[
            Assign("y", BinOp("+", Var("y"), Var("x"))),
            Assign("x", BinOp("-", Var("x"), IntLit(1))),
            Print(Var("y"))
        ]
    ),
    If(
        condition=BinOp("==", Var("y"), IntLit(6)),
        then_branch=[Assign("result", IntLit(1))],
        else_branch=[Assign("result", IntLit(0))]
    ),
    Return(Var("result"))
])

programa2 = Program([
    Assign("sum", IntLit(0)),
    For(
        var="i",
        start=IntLit(1),
        end=IntLit(4),
        body=[
            Assign("sum", BinOp("+", Var("sum"), Var("i"))),
            Print(Var("sum"))
        ]
    ),
    If(
        condition=BoolLit(True),
        then_branch=[Assign("z", IntLit(5))],
        else_branch=[Assign("z", IntLit(5))]  # code smell
    ),
    Return(Var("sum"))
])

programa3 = Program([
    FunctionDef(
        name="check_and_add",
        params=["a", "b"],
        body=[
            If(
                condition=BinOp("&&", BinOp(">", Var("a"), IntLit(0)), BinOp(">", Var("b"), IntLit(0))),
                then_branch=[Assign("r", BinOp("+", Var("a"), Var("b")))],
                else_branch=[Assign("r", IntLit(0))]
            ),
            Return(Var("r"))
        ]
    ),
    Assign("x", FunctionCall("check_and_add", [IntLit(2), IntLit(3)])),
    Print(Var("x")),
    Return(Var("x"))
])