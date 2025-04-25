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
    Assign("x", IntLit(10)),  # x = 10
    Assign("y", BinOp("+", Var("x"), IntLit(5))),  # y = x + 5
    Return(Var("y"))  # Retorna o valor final de y
])

programa2 = Program([
    Assign("a", IntLit(3)),  # a = 3
    Assign("b", IntLit(4)),  # b = 4
    If(
        condition=BinOp(">", Var("a"), Var("b")),  # if a > b
        then_branch=[Assign("max", Var("a"))],  # max = a
        else_branch=[Assign("max", Var("b"))]  # else max = b
    ),
    Return(Var("max"))  # Retorna apenas o valor final relevante
])

programa3 = Program([
    Assign("sum", IntLit(0)),  # sum = 0
    For(
        var="i",
        start=IntLit(1),  # for i in range(1, 5)
        end=IntLit(5),
        body=[
            Assign("sum", BinOp("+", Var("sum"), Var("i")))  # sum += i
        ]
    ),
    Return(Var("sum"))  # Retorna o valor final da soma
])

programa4 = Program([
    Assign("x", IntLit(10)),  # x = 10
    Assign("y", IntLit(0)),  # y = 0
    While(
        condition=BinOp(">", Var("x"), IntLit(0)),  # while x > 0
        body=[
            Assign("y", BinOp("+", Var("y"), Var("x"))),  # y += x
            Assign("x", BinOp("-", Var("x"), IntLit(1)))  # x -= 1
        ]
    ),
    Return(Var("y"))  # Retorna o valor acumulado de y
])

programa5 = Program([
    FunctionDef(
        name="add",
        params=["a", "b"],
        body=[
            Assign("result", BinOp("+", Var("a"), Var("b"))),  # result = a + b
            Return(Var("result"))  # return result
        ]
    ),
    Assign("z", FunctionCall("add", [IntLit(5), IntLit(7)])),  # z = add(5, 7)
    Return(Var("z"))  # Retorna o resultado da função
])

programa6 = Program([
    Assign("a", IntLit(1)),  # a = 1
    Assign("b", IntLit(2)),  # b = 2
    Assign("c", BinOp("*", Var("a"), Var("b"))),  # c = a * b
    Return(Var("c"))  # Retorna o valor de c
])

programa7 = Program([
    Assign("x", BoolLit(True)),  # x = true
    Assign("y", BoolLit(False)),  # y = false
    If(
        condition=BinOp("&&", Var("x"), UnaryOp("not", Var("y"))),  # if x && not y
        then_branch=[Assign("result", IntLit(1))],  # result = 1
        else_branch=[Assign("result", IntLit(0))]  # else result = 0
    ),
    Return(Var("result"))  # Retorna o resultado do if
])

programa8 = Program([
    Assign("a", BinOp("+", IntLit(0), IntLit(3))),  # → 3
    Assign("b", BinOp("*", IntLit(1), IntLit(5))),  # → 5
    Assign("c", BinOp("==", BoolLit(True), BoolLit(True))),  # → True
    Assign("d", BinOp("||", BoolLit(False), BoolLit(True))),  # → True
    Assign("e", BinOp("+", Var("a"), IntLit(0))),  # → a
    Assign("f", BinOp("*", Var("b"), IntLit(1))),  # → b
    Return(Var("f"))  # Retorna o valor de f
])

programa9 = Program([
    If(
        condition=BoolLit(True),
        then_branch=[Assign("x", IntLit(1))],
        else_branch=[Assign("x", IntLit(2))]  # → elimina o if
    ),
    If(
        condition=BinOp("==", Var("x"), BoolLit(True)),  # → x
        then_branch=[Assign("y", IntLit(1))],
        else_branch=[Assign("y", IntLit(0))]
    ),
    If(
        condition=Var("cond"),
        then_branch=[Assign("z", IntLit(5))],
        else_branch=[Assign("z", IntLit(5))]  # → code smell
    ),
    Return(Var("y"))  # Retorna o valor de y
])

programa10 = Program([
    Assign("a", BinOp("+", IntLit(2), IntLit(3))),  # → 5
    Assign("b", BinOp("*", BinOp("+", IntLit(0), IntLit(4)), IntLit(1))),  # → 4
    Assign("c", BinOp("*", BinOp("*", IntLit(1), Var("b")), IntLit(0))),  # → 0
    Assign("d", BinOp("==", BinOp("!=", BoolLit(True), BoolLit(True)), BoolLit(False))),  # → True
    Return(Var("d"))  # Retorna o valor de d
])

programa11 = Program([
    Assign("x", IntLit(1)),
    For(
        var="i",
        start=IntLit(0),
        end=IntLit(0),  # loop nunca corre
        body=[Assign("x", BinOp("+", Var("x"), IntLit(1)))]
    ),
    If(
        condition=BoolLit(False),
        then_branch=[Assign("y", IntLit(10))],
        else_branch=[Assign("y", IntLit(20))]  # → y = 20
    ),
    Return(Var("y"))  # Retorna o valor de y
])

programa12 = Program([
    Assign("flag", BinOp("==", BoolLit(True), BoolLit(False))),  # → False
    Assign("check", BinOp("&&", BoolLit(True), BoolLit(False))),  # → False
    Assign("value", BinOp("+", BinOp("*", IntLit(0), IntLit(7)), IntLit(10))),  # → 10
    Return(Var("value"))  # Retorna o valor de value
])

programa13 = Program([
    If(
        condition=Var("x"),
        then_branch=[Assign("z", IntLit(5))],
        else_branch=[Assign("z", IntLit(5))]  # → code smell: branches iguais
    ),
    If(
        condition=BoolLit(True),
        then_branch=[Assign("a", BinOp("+", IntLit(1), IntLit(1)))],  # → a = 2
        else_branch=[Assign("a", IntLit(999))]  # nunca executado
    ),
    Return(Var("a"))  # Retorna o valor de a
])

programa14 = Program([
    FunctionDef(
        name="mult_by_1",
        params=["n"],
        body=[
            Assign("result", BinOp("*", Var("n"), IntLit(1))),  # → n
            Return(Var("result"))
        ]
    ),
    Assign("out", FunctionCall("mult_by_1", [IntLit(42)])),
    Return(Var("out"))  # Retorna o valor de out
])

if __name__ == "__main__":
    print("Programa 1:", programa1)
    print("Programa 2:", programa2)
    print("Programa 3:", programa3)
    print("Programa 4:", programa4)
    print("Programa 5:", programa5)
    print("Programa 6:", programa6)
    print("Programa 7:", programa7)
    print("Programa 8:", programa8)
    print("Programa 9:", programa9)
    print("Programa 10:", programa10)
    print("Programa 11:", programa11)
    print("Programa 12:", programa12)
    print("Programa 13:", programa13)
    print("Programa 14:", programa14)
    