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
            Return(Var("result"))               # return result
        ]
    ),
    Assign("z", FunctionCall("add", [IntLit(5), IntLit(7)]))  # z = add(5, 7)
])

programa6 = Program([
        Assign("a", IntLit(1)),  # a = 1
        Assign("b", IntLit(2)),  # b = 2
        Assign("c", BinOp("*", Var("a"), Var("b")))  # c = a * b

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

if __name__ == "__main__":
    print("Programa 1:", programa1)
    print("Programa 2:", programa2)
    print("Programa 3:", programa3)
    print("Programa 4:", programa4)
    print("Programa 5:", programa5)
    print("Programa 6:", programa6)
    print("Programa 7:", programa7)