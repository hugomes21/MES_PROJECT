from typing import List, Tuple, Dict, Union
from Lang import *
import random, sys
from io import StringIO

# 1.5 Software Testing

Inputs = List[Tuple[str, int]]

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

# 1. Evaluation
def eval_expr(expr: Expr, env: Dict[str, Union[int, bool]], func_env: dict) -> Union[int, bool]:
    if isinstance(expr, IntLit):
        return expr.value
    elif isinstance(expr, BoolLit):
        return expr.value
    elif isinstance(expr, Var):
        return env[expr.name]
    elif isinstance(expr, BinOp):
        l = eval_expr(expr.left, env, func_env)
        r = eval_expr(expr.right, env, func_env)
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
        v = eval_expr(expr.expr, env, func_env)
        if expr.op == "not": return not v
        if expr.op == "-": return -v
    elif isinstance(expr, FunctionCall):
        func_def = func_env.get(expr.name)
        if not func_def:
            raise Exception(f"Função '{expr.name}' não definida")

        if len(func_def.params) != len(expr.args):
            raise Exception(f"Número de argumentos incorreto em '{expr.name}'")

        new_env = {}  # Ambiente local para a função

        for param, arg_expr in zip(func_def.params, expr.args):
            new_env[param] = eval_expr(arg_expr, env, func_env)

        try:
            for stmt in func_def.body:
                eval_stmt(stmt, new_env, func_env)
        except ReturnException as ret:
            return ret.value

        raise Exception(f"Função '{expr.name}' não retornou valor")


def eval_stmt(stmt: Stmt, env: Dict[str, Union[int, bool]], func_env: dict):
    if isinstance(stmt, Assign):
        env[stmt.var] = eval_expr(stmt.expr, env, func_env)
    
    elif isinstance(stmt, If):
        cond = eval_expr(stmt.condition, env, func_env)
        branch = stmt.then_branch if cond else stmt.else_branch
        for s in branch:
            eval_stmt(s, env, func_env)
    
    elif isinstance(stmt, While):
        while eval_expr(stmt.condition, env, func_env):
            for s in stmt.body:
                eval_stmt(s, env, func_env)
    
    elif isinstance(stmt, For):
        start = eval_expr(stmt.start, env, func_env)
        end = eval_expr(stmt.end, env, func_env)
        for i in range(start, end):
            env[stmt.var] = i
            for s in stmt.body:
                eval_stmt(s, env, func_env)
   
    elif isinstance(stmt, FunctionDef):
        func_env[stmt.name] = stmt

    elif isinstance(stmt, Return):
        raise ReturnException(eval_expr(stmt.expr, env, func_env))

    elif isinstance(stmt, Print):
        val = eval_expr(stmt.expr, env, func_env)
        if isinstance(stmt.expr, IntLit):
            print(f"Instr: {val}")
        else:
            print(val)


    elif isinstance(stmt, FunctionDef):
        raise NotImplementedError("Function definitions not yet supported")

def evaluate(ast: Program, inputs: Inputs) -> int:
    env = {var: val for var, val in inputs}
    func_env = {} # Novo ambiente para funções
    
    try:
        for stmt in ast.body:
            eval_stmt(stmt, env, func_env)
    except ReturnException as ret:
        return ret.value

    if "result" in env:
        return env["result"]
    else:
        raise Exception("No return or 'result' variable found.")

# 2. Test 
def runTest(ast: Program, testCase: Tuple[Inputs, int]) -> bool:
    inputs, expected = testCase
    try:
        result = evaluate(ast, inputs)
        return result == expected
    except:
        return False

# 3. Test Suite
def runTestSuite(ast: Program, testCases: List[Tuple[Inputs, int]]) -> bool:
    return all(runTest(ast, case) for case in testCases)

# 5. Mutation Testing
def mutate_expr(expr: Expr) -> Expr:
    if isinstance(expr, BinOp):
        mutations = []
        if expr.op == "+":
            mutations.append(lambda: BinOp("-", expr.left, expr.right))
        if expr.op == "*":
            mutations.append(lambda: BinOp("/", expr.left, expr.right))
        if expr.op == "&&":
            mutations.append(lambda: BinOp("||", expr.left, expr.right))
        if expr.op == "||":
            mutations.append(lambda: BinOp("&&", expr.left, expr.right))
        if expr.op == "==":
            mutations.append(lambda: BinOp("!=", expr.left, expr.right))
        if expr.op == ">":
            mutations.append(lambda: BinOp("<=", expr.left, expr.right))
        if expr.op == "<":
            mutations.append(lambda: BinOp(">=", expr.left, expr.right))


        # Constante folding inverso (ex: 0 + x → x - 1)
        if isinstance(expr.left, IntLit):
            mutations.append(lambda: BinOp(expr.op, IntLit(expr.left.value + 1), expr.right))
        if isinstance(expr.right, IntLit):
            mutations.append(lambda: BinOp(expr.op, expr.left, IntLit(expr.right.value + 1)))

        if mutations:
            return random.choice(mutations)()

        # Recurse nas subexpressões
        return BinOp(expr.op, mutate_expr(expr.left), mutate_expr(expr.right))

    elif isinstance(expr, UnaryOp):
        return UnaryOp(expr.op, mutate_expr(expr.expr))

    elif isinstance(expr, FunctionCall):
        return FunctionCall(expr.name, [mutate_expr(arg) for arg in expr.args])

    else:
        return expr

def mutate_stmt(stmt: Stmt) -> Stmt:
    if isinstance(stmt, Assign):
        return Assign(stmt.var, mutate_expr(stmt.expr))
    elif isinstance(stmt, If):
        return If(
            mutate_expr(stmt.condition),
            [mutate_stmt(s) for s in stmt.then_branch],
            [mutate_stmt(s) for s in stmt.else_branch]
        )
    elif isinstance(stmt, While):
        return While(
            mutate_expr(stmt.condition),
            [mutate_stmt(s) for s in stmt.body]
        )
    elif isinstance(stmt, For):
        return For(
            stmt.var,
            mutate_expr(stmt.start),
            mutate_expr(stmt.end),
            [mutate_stmt(s) for s in stmt.body]
        )
    elif isinstance(stmt, FunctionDef):
        return FunctionDef(
            stmt.name,
            stmt.params,
            [mutate_stmt(s) for s in stmt.body]
        )
    elif isinstance(stmt, Return):
        return Return(mutate_expr(stmt.expr))
    elif isinstance(stmt, Print):
        return Print(mutate_expr(stmt.expr))
    else:
        return stmt

def mutate(program: Program) -> Program:
    # Aplica mutação a apenas uma instrução aleatória
    body = program.body[:]
    if not body:
        return program

    idx = random.randrange(len(body))
    body[idx] = mutate_stmt(body[idx])
    return Program(body)

# 8. Instrumentation
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
            print(line)

        if result != expected:
            all_passed = False

    return all_passed

# Extra : Spectrum Based Fault Localization
def collect_spectrum_data(program, test_suite):
    results = []
    instrumented_program = instrumentation(program)
    for inputs, expected in test_suite:
        output = StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = output
        try:
            result = evaluate(instrumented_program, inputs)
            passed = (result == expected)
        except:
            passed = False
        finally:
            sys.stdout = sys_stdout_backup

        trace = output.getvalue().strip().splitlines()
        instr_ids = []
        for line in trace:
            if line.startswith("Instr: "):
                try:
                    instr_id = int(line.replace("Instr: ", "").strip())
                    instr_ids.append(instr_id)
                except ValueError:
                    pass
        # ← colocar aqui, não dentro do loop anterior!
        results.append((instr_ids, passed))
    return results

def compute_ochiai(spectrum_data):
    from collections import defaultdict
    total_fail = sum(1 for _, passed in spectrum_data if not passed)
    instr_stats = defaultdict(lambda: {"pass": 0, "fail": 0})
    
    for instrs, passed in spectrum_data:
        for instr_id in instrs:
            if passed:
                instr_stats[instr_id]["pass"] += 1
            else:
                instr_stats[instr_id]["fail"] += 1

    scores = {}
    for instr_id, counts in instr_stats.items():
        f = counts["fail"]
        p = counts["pass"]
        if total_fail == 0 or (f + p) == 0:
            score = 0.0
        else:
            denom = ((f + p) * total_fail) ** 0.5
            score = f / denom
        scores[instr_id] = score
    return sorted(scores.items(), key=lambda x: -x[1])


def spectrum_based_fault_localization(program, test_suite):
    spectrum_data = collect_spectrum_data(program, test_suite)
    ochiai_scores = compute_ochiai(spectrum_data)
    return ochiai_scores
