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
    Assign("y", IntLit(0)),
    Assign("temp", BinOp("+", IntLit(0), IntLit(3))),  # → 3
    Assign("useless", BinOp("*", IntLit(1), IntLit(1))),  # → 1
    While(
        condition=BinOp("==", BinOp(">", Var("x"), IntLit(0)), BoolLit(True)),  # → apenas (x > 0)
        body=[
            Assign("y", BinOp("+", Var("y"), BinOp("*", Var("x"), IntLit(1)))),  # → y + x
            Assign("x", BinOp("-", Var("x"), IntLit(0))),  # → x (não altera)
            Assign("x", BinOp("-", Var("x"), IntLit(1)))
        ]
    ),
    If(
        condition=BoolLit(True),  # → if sempre executado
        then_branch=[
            If(
                condition=BinOp("==", Var("y"), IntLit(6)),
                then_branch=[Assign("result", IntLit(1))],
                else_branch=[Assign("result", IntLit(0))]
            )
        ],
        else_branch=[
            Assign("result", IntLit(999))
        ]
    ),
    Return(Var("result"))
])


programa2 = Program([
    Assign("sum", IntLit(0)),
    Assign("zero", BinOp("+", IntLit(0), IntLit(0))),  # → 0
    For(
        var="i",
        start=IntLit(1),
        end=IntLit(4),
        body=[
            Assign("sum", BinOp("+", Var("sum"), BinOp("*", IntLit(1), Var("i")))),  # → sum + i
            Assign("dummy", BinOp("*", Var("i"), IntLit(0)))  # → 0
        ]
    ),
    If(
        condition=BinOp("==", BoolLit(True), BoolLit(True)),  # → True
        then_branch=[
            Assign("z", IntLit(5))
        ],
        else_branch=[
            Assign("z", IntLit(5))  # branches iguais
        ]
    ),
    Return(Var("sum"))
])


programa3 = Program([
    FunctionDef(
        name="check_and_add",
        params=["a", "b"],
        body=[
            If(
                condition=BinOp("==", BinOp(">", Var("a"), IntLit(0)), BoolLit(True)),  # → apenas a > 0
                then_branch=[
                    If(
                        condition=BinOp("==", BinOp(">", Var("b"), IntLit(0)), BoolLit(True)),  # → b > 0
                        then_branch=[
                            Assign("r", BinOp("+", Var("a"), BinOp("+", Var("b"), IntLit(0))))  # → a + b
                        ],
                        else_branch=[Assign("r", IntLit(0))]
                    )
                ],
                else_branch=[
                    Assign("r", IntLit(0))
                ]
            ),
            Return(Var("r"))
        ]
    ),
    Assign("temp", BinOp("*", IntLit(1), IntLit(1))),  # → 1
    Assign("x", FunctionCall("check_and_add", [Var("a"), Var("b")])),
    Assign("x", BinOp("*", Var("x"), IntLit(1))),  # → x
    Return(Var("x"))
])
