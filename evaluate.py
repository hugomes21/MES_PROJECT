from typing import List, Tuple, Dict, Union
from Lang import *
import random
from io import StringIO
import sys

# 1.5 Software Testing

Inputs = List[Tuple[str, int]]

@dataclass
class Print(Stmt):
    expr: Expr

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
    
    elif isinstance(stmt, Print):
        print(eval_expr(stmt.expr, env))
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

def mutate(program: Program) -> Program:
    mutated_body = []
    for stmt in program.body:
        if isinstance(stmt, Assign) and isinstance(stmt.expr, BinOp):
            # Mudar operador '+' para '-' com 50% de probabilidade
            if stmt.expr.op == "+" and random.random() < 0.5:
                mutated_expr = BinOp("-", stmt.expr.left, stmt.expr.right)
                mutated_body.append(Assign(stmt.var, mutated_expr))
                continue
        mutated_body.append(stmt)
    return Program(mutated_body)

def instrumentation(ast: Program) -> Program:
    def instrument_stmt(stmt: Stmt, count: int) -> Tuple[List[Stmt], int]:
        marker = Print(IntLit(count))
        if isinstance(stmt, If):
            then_instr, count = instrument_block(stmt.then_branch, count + 1)
            else_instr, count = instrument_block(stmt.else_branch, count + 1)
            return [marker, If(stmt.condition, then_instr, else_instr)], count
        elif isinstance(stmt, While):
            body_instr, count = instrument_block(stmt.body, count + 1)
            return [marker, While(stmt.condition, body_instr)], count
        elif isinstance(stmt, For):
            body_instr, count = instrument_block(stmt.body, count + 1)
            return [marker, For(stmt.var, stmt.start, stmt.end, body_instr)], count
        elif isinstance(stmt, FunctionDef):
            body_instr, count = instrument_block(stmt.body, count + 1)
            return [marker, FunctionDef(stmt.name, stmt.params, body_instr)], count
        else:
            return [marker, stmt], count

    def instrument_block(stmts: List[Stmt], count: int) -> Tuple[List[Stmt], int]:
        result = []
        for stmt in stmts:
            new_stmts, count = instrument_stmt(stmt, count + 1)
            result.extend(new_stmts)
        return result, count

    new_body, _ = instrument_block(ast.body, 0)
    return Program(new_body)

def instrumentedTestSuite(ast: Program, testCases: List[Tuple[Inputs, int]]) -> bool:
    instrumented_ast = instrumentation(ast)
    all_passed = True

    for inputs, expected in testCases:
        output = StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = output

        try:
            result = evaluate(instrumented_ast, inputs)
        except:
            result = None
        finally:
            sys.stdout = sys_stdout_backup

        trace = output.getvalue().strip().splitlines()
        print("Execução instrumentada:")
        for line in trace:
            print("  Instr:", line)

        if result != expected:
            all_passed = False

    return all_passed
