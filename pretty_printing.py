from parser import *

# 1.3 Pretty Printing

def indent(lines, level=1):
    return [("    " * level + line) if line.strip() else line for line in lines]


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
        if expr.op == "not":
            return f"(not {pretty_expr(expr.expr)})"
        else:
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
    
    elif isinstance(stmt, Print):
        return [f"print({pretty_expr(stmt.expr)})"]
    
    elif isinstance(stmt, Return):
        return [f"return {pretty_expr(stmt.expr)}"]
    
    else:
        return [f"# unknown statement {stmt}"]

def pretty_program(prog: Program) -> str:
    lines = sum([pretty_stmt(s, level=0) for s in prog.body], [])
    return "\n".join(lines) + "\n"

# Injetar __str__ no Program
Program.__str__ = lambda self: pretty_program(self)