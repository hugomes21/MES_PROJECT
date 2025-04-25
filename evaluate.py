from typing import List, Tuple, Dict, Union
from Lang import *

# 1.5 Software Testing

Inputs = List[Tuple[str, int]]

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


def eval_expr(expr: Expr, env: Dict[str, Union[int, bool]]) -> Union[int, bool]:
    if isinstance(expr, IntLit):
        return expr.value
    elif isinstance(expr, BoolLit):
        return expr.value
    elif isinstance(expr, Var):
        return env[expr.name]
    elif isinstance(expr, BinOp):
        l = eval_expr(expr.left, env)
        r = eval_expr(expr.right, env)
        if expr.op == "+": return l + r
        if expr.op == "-": return l - r
        if expr.op == "*": return l * r
        if expr.op == "/": return l // r
        if expr.op == "==": return l == r
        if expr.op == "!=": return l != r
        if expr.op == "<": return l < r
        if expr.op == ">": return l > r
        if expr.op == "&&": return l and r
        if expr.op == "||": return l or r
    elif isinstance(expr, UnaryOp):
        v = eval_expr(expr.expr, env)
        if expr.op == "not": return not v
        if expr.op == "-": return -v
    elif isinstance(expr, FunctionCall):
        raise NotImplementedError("Function calls not yet supported")
    else:
        raise Exception(f"Unsupported expression: {expr}")


def eval_stmt(stmt: Stmt, env: Dict[str, Union[int, bool]]):
    if isinstance(stmt, Assign):
        env[stmt.var] = eval_expr(stmt.expr, env)
    elif isinstance(stmt, If):
        cond = eval_expr(stmt.condition, env)
        branch = stmt.then_branch if cond else stmt.else_branch
        for s in branch:
            eval_stmt(s, env)
    elif isinstance(stmt, While):
        while eval_expr(stmt.condition, env):
            for s in stmt.body:
                eval_stmt(s, env)
    elif isinstance(stmt, For):
        start = eval_expr(stmt.start, env)
        end = eval_expr(stmt.end, env)
        for i in range(start, end):
            env[stmt.var] = i
            for s in stmt.body:
                eval_stmt(s, env)
    elif isinstance(stmt, Return):
        raise ReturnException(eval_expr(stmt.expr, env))
    elif isinstance(stmt, FunctionDef):
        raise NotImplementedError("Function definitions not yet supported")


def evaluate(ast: Program, inputs: Inputs) -> int:
    env = {var: val for var, val in inputs}
    try:
        for stmt in ast.body:
            eval_stmt(stmt, env)
    except ReturnException as ret:
        return ret.value

    if "result" in env:
        return env["result"]
    else:
        raise Exception("No return or 'result' variable found.")


def runTest(ast: Program, testCase: Tuple[Inputs, int]) -> bool:
    inputs, expected = testCase
    try:
        result = evaluate(ast, inputs)
        return result == expected
    except:
        return False


def runTestSuite(ast: Program, testCases: List[Tuple[Inputs, int]]) -> bool:
    return all(runTest(ast, case) for case in testCases)

