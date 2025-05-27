from Lang import *
from collections import Counter


# 1.4 Optimization and Refactoring
# Otimizações 
def simplify_expr(expr: Expr) -> Expr:
    if isinstance(expr, BinOp):
        left = simplify_expr(expr.left)
        right = simplify_expr(expr.right)

        # Soma com 0
        if expr.op == "+":
            if isinstance(left, IntLit) and left.value == 0: return right
            if isinstance(right, IntLit) and right.value == 0: return left

        # Subtração de 0
        if expr.op == "-":
            if isinstance(left, IntLit) and left.value == 0: return UnaryOp("-", right)
            if isinstance(right, IntLit) and right.value == 0: return left
        
        # Multiplicação por 1 ou 0
        if expr.op == "*":
            if isinstance(left, IntLit):
                if left.value == 1: return right
                if left.value == 0: return IntLit(0)
            if isinstance(right, IntLit):
                if right.value == 1: return left
                if right.value == 0: return IntLit(0)

        # Divisão por 1
        if expr.op == "/":
            if isinstance(right, IntLit) and right.value == 1: return left
            if isinstance(left, IntLit) and left.value == 0: return IntLit(0)
        
        # Divisão por 0
        if expr.op == "/":
            if isinstance(right, IntLit) and right.value == 0:
                raise ZeroDivisionError("Divisão por zero")
            if isinstance(left, IntLit) and left.value == 0: return IntLit(0)

        # Constante folding
        if isinstance(left, IntLit) and isinstance(right, IntLit):
            if expr.op == "+": return IntLit(left.value + right.value)
            elif expr.op == "-": return IntLit(left.value - right.value)
            elif expr.op == "*": return IntLit(left.value * right.value)
            elif expr.op == "/": return IntLit(left.value // right.value) if right.value != 0 else expr

        # Simplificação de expressões booleanas
        if expr.op == "&&":
            if isinstance(left, BoolLit): return right if left.value else BoolLit(False)
            if isinstance(right, BoolLit): return left if right.value else BoolLit(False)
        if expr.op == "||":
            if isinstance(left, BoolLit): return BoolLit(True) if left.value else right
            if isinstance(right, BoolLit): return BoolLit(True) if right.value else left

        return BinOp(expr.op, left, right)

    elif isinstance(expr, UnaryOp):
        inner = simplify_expr(expr.expr)
        if expr.op == "not" and isinstance(inner, BoolLit):
            return BoolLit(not inner.value)
        return UnaryOp(expr.op, inner)

    else:
        return expr

def simplify_stmt(stmt: Stmt) -> Stmt:
    if isinstance(stmt, Assign):
        return Assign(stmt.var, simplify_expr(stmt.expr))
    elif isinstance(stmt, If):
        return If(
            condition=simplify_expr(stmt.condition),
            then_branch=[simplify_stmt(s) for s in stmt.then_branch],
            else_branch=[simplify_stmt(s) for s in stmt.else_branch]
        )
    elif isinstance(stmt, While):
        return While(
            condition=simplify_expr(stmt.condition),
            body=[simplify_stmt(s) for s in stmt.body]
        )
    elif isinstance(stmt, For):
        return For(
            stmt.var,
            simplify_expr(stmt.start),
            simplify_expr(stmt.end),
            [simplify_stmt(s) for s in stmt.body]
        )
    elif isinstance(stmt, FunctionDef):
        return FunctionDef(
            stmt.name,
            stmt.params,
            [simplify_stmt(s) for s in stmt.body]
        )
    elif isinstance(stmt, Return):
        return Return(simplify_expr(stmt.expr))
    else:
        return stmt
    
# Refatorações
def refactor_expr(expr: Expr) -> Expr:
    if isinstance(expr, BinOp):
        left = refactor_expr(expr.left)
        right = refactor_expr(expr.right)

        # x == True  →  x
        if expr.op == "==" and isinstance(right, BoolLit):
            if right.value:
                return left
            else:
                return UnaryOp("not", left)
        return BinOp(expr.op, left, right)

    elif isinstance(expr, UnaryOp):
        return UnaryOp(expr.op, refactor_expr(expr.expr))

    elif isinstance(expr, FunctionCall):
        return FunctionCall(expr.name, [refactor_expr(arg) for arg in expr.args])

    else:
        return expr


def refactor_stmt(stmt: Stmt) -> Stmt:
    if isinstance(stmt, Assign):
        return Assign(stmt.var, refactor_expr(stmt.expr))
    elif isinstance(stmt, If):
        cond = refactor_expr(stmt.condition)

        then_branch = [refactor_stmt(s) for s in stmt.then_branch]
        else_branch = [refactor_stmt(s) for s in stmt.else_branch]

        # if True: then x else y  →  apenas x
        if isinstance(cond, BoolLit):
            return then_branch if cond.value else else_branch

        return If(cond, then_branch, else_branch)

    elif isinstance(stmt, While):
        return While(
            refactor_expr(stmt.condition),
            [refactor_stmt(s) for s in stmt.body]
        )

    elif isinstance(stmt, For):
        return For(
            stmt.var,
            refactor_expr(stmt.start),
            refactor_expr(stmt.end),
            [refactor_stmt(s) for s in stmt.body]
        )

    elif isinstance(stmt, FunctionDef):
        return FunctionDef(
            stmt.name,
            stmt.params,
            [refactor_stmt(s) for s in stmt.body]
        )

    elif isinstance(stmt, Return):
        return Return(refactor_expr(stmt.expr))

    else:
        return stmt

def refactor(prog: Program) -> Program:
    stmts = []
    for s in prog.body:
        refactored = refactor_stmt(s)
        if isinstance(refactored, list):
            stmts.extend(refactored)
        else:
            stmts.append(refactored)
    return Program(stmts)

def names(prog: Program) -> list[str]:
    result = set()

    def visit_stmt(stmt: Stmt):
        if isinstance(stmt, Assign):
            result.add(stmt.var)
        elif isinstance(stmt, FunctionDef):
            result.add(stmt.name)
            result.update(stmt.params)
            for s in stmt.body:
                visit_stmt(s)
        elif isinstance(stmt, If):
            for s in stmt.then_branch + stmt.else_branch:
                visit_stmt(s)
        elif isinstance(stmt, While):
            for s in stmt.body:
                visit_stmt(s)
        elif isinstance(stmt, For):
            result.add(stmt.var)
            for s in stmt.body:
                visit_stmt(s)
        elif isinstance(stmt, Return):
            pass  # não declara nomes

    for stmt in prog.body:
        visit_stmt(stmt)

    return list(sorted(result))

def instructions(prog: Program) -> dict[str, int]:
    counter = Counter()

    def visit_stmt(stmt: Stmt):
        counter[type(stmt).__name__] += 1
        if isinstance(stmt, FunctionDef):
            for s in stmt.body:
                visit_stmt(s)
        elif isinstance(stmt, If):
            for s in stmt.then_branch + stmt.else_branch:
                visit_stmt(s)
        elif isinstance(stmt, While):
            for s in stmt.body:
                visit_stmt(s)
        elif isinstance(stmt, For):
            for s in stmt.body:
                visit_stmt(s)

    for stmt in prog.body:
        visit_stmt(stmt)

    return dict(counter)

def detect_smells(prog: Program) -> dict[str, int]:
    smells = Counter()

    def visit_expr(expr: Expr):
        if isinstance(expr, BinOp):
            if expr.op == "==" and isinstance(expr.right, BoolLit):
                smells["comparação redundante com booleano"] += 1
            visit_expr(expr.left)
            visit_expr(expr.right)
        elif isinstance(expr, UnaryOp):
            visit_expr(expr.expr)
        elif isinstance(expr, FunctionCall):
            for arg in expr.args:
                visit_expr(arg)

    def visit_stmt(stmt: Stmt):
        # Atribuição redundante x = x
        if isinstance(stmt, Assign):
            if isinstance(stmt.expr, Var) and stmt.var == stmt.expr.name:
                smells["atribuição redundante (x = x)"] += 1
            visit_expr(stmt.expr)

        elif isinstance(stmt, If):
            if stmt.then_branch == stmt.else_branch:
                smells["branches iguais em if"] += 1
            visit_expr(stmt.condition)
            for s in stmt.then_branch + stmt.else_branch:
                visit_stmt(s)

        elif isinstance(stmt, While):
            if isinstance(stmt.condition, BoolLit) and stmt.condition.value:
                smells["while True pode causar loop infinito"] += 1
            visit_expr(stmt.condition)
            for s in stmt.body:
                visit_stmt(s)

        elif isinstance(stmt, For):
            visit_expr(stmt.start)
            visit_expr(stmt.end)
            for s in stmt.body:
                visit_stmt(s)

        elif isinstance(stmt, FunctionDef):
            for i, s in enumerate(stmt.body):
                visit_stmt(s)
                # Código morto após return
                if isinstance(s, Return) and i < len(stmt.body) - 1:
                    smells["código morto após return"] += 1

        elif isinstance(stmt, Return):
            visit_expr(stmt.expr)

    for stmt in prog.body:
        visit_stmt(stmt)

    return dict(smells)

def opt(prog: Program) -> Program:
    return Program([simplify_stmt(stmt) for stmt in prog.body])
