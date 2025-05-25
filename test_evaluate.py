from Lang import *
from evaluate import *
from contextlib import redirect_stdout

# Test suites para programa1 a programa3 (como exigido pelo enunciado para runTestSuite)
testSuite1 = [ ([], 1) ]
testSuite2 = [ ([], 6) ]
testSuite3 = [ ([], 5) ]
testPrintSuite = [ ([], 42) ]

# Programas mutados
programa1_mut = Program([
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
        condition=BinOp("!=", Var("y"), IntLit(6)),  # <--- MUDADO
        then_branch=[Assign("result", IntLit(1))],
        else_branch=[Assign("result", IntLit(0))]
    ),
    Return(Var("result"))
])

programa2_mut = Program([
    Assign("sum", IntLit(0)),
    For(
        var="i",
        start=IntLit(1),
        end=IntLit(4),
        body=[
            Assign("sum", BinOp("-", Var("sum"), Var("i"))),  # <--- MUDADO
            Print(Var("sum"))
        ]
    ),
    If(
        condition=BoolLit(True),
        then_branch=[Assign("z", IntLit(5))],
        else_branch=[Assign("z", IntLit(5))]
    ),
    Return(Var("sum"))
])

programa3_mut = Program([
    FunctionDef(
        name="check_and_add",
        params=["a", "b"],
        body=[
            If(
                condition=BinOp("&&", BinOp(">", Var("a"), IntLit(0)), BinOp(">", Var("b"), IntLit(0))),
                then_branch=[Assign("r", BinOp("*", Var("a"), Var("b")))],  # <--- MUDADO
                else_branch=[Assign("r", IntLit(0))]
            ),
            Return(Var("r"))
        ]
    ),
    Assign("x", FunctionCall("check_and_add", [IntLit(2), IntLit(3)])),
    Print(Var("x")),
    Return(Var("x"))
])


# Programa com instrução Print
programa_com_print = Program([
    Assign("x", IntLit(42)),
    Print(Var("x")),
    Return(Var("x"))
])

# Aplicar mutação aleatória ao programa1
def testar_mutacoes():
    programas = [
        ("programa1", programa1, testSuite1),
        ("programa2", programa2, testSuite2),
        ("programa3", programa3, testSuite3)
    ]

    for nome, prog, suite in programas:
        mutado = mutate(prog)
        print(f"\nMutando {nome}...")
        print(mutado)
        passou = runTestSuite(mutado, suite)
        print(f"{nome} mutado → passou tests? {passou}")


def test_all_with_evaluate():
    print("======================== Testar evaluate() ========================")
    for i in range(1, 15):
        prog = globals().get(f"programa{i}")
        if not prog: continue
        try:
            result = evaluate(prog, [])
            print(f"Programa {i}: resultado = {result}")
        except Exception as e:
            print(f"Programa {i}: erro → {e}")

def test_all_with_runTest():
    print("\n========================  Testar runTest() ========================")
    for i in range(1, 15):
        prog = globals().get(f"programa{i}")
        if not prog:
            continue
        try:
            ok = runTest(prog, ([], evaluate(prog, [])))
            print(f"Programa {i}: passou = {ok}")
        except Exception as e:
            print(f"Programa {i}: erro → {e}")

def test_instrumentation_manual():
    instr = instrumentation(programa1)
    print("Programa 1 instrumentado:")
    print(instr)

def test_instrumentedTestSuite_verbose():
    instrumented = instrumentation(programa1)
    for inputs, expected in testSuite1:
        output = StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = output

        try:
            result = evaluate(instrumented, inputs)
        except:
            result = None
        finally:
            sys.stdout = sys_stdout_backup

        trace = output.getvalue().strip().splitlines()
        print("Trace da execução:")
        for line in trace:
            print("  Instr:", line)

        print("Resultado esperado:", expected)
        print("Resultado obtido:", result)
        print("Teste passou:", result == expected)


def main():
    with open("resultado_evaluate.txt", "w", encoding="utf-8") as f:
        with redirect_stdout(f):
            test_all_with_evaluate()
            test_all_with_runTest()

            print("\n========================  Testar runTestSuite() para os 3 programas escolhidos ========================")
            print("Programa 1:", runTestSuite(programa1, testSuite1))
            print("Programa 2:", runTestSuite(programa2, testSuite2))
            print("Programa 3:", runTestSuite(programa3, testSuite3))

            print("\n========================  Testar runTestSuite() para os 3 programas mutados ========================")
            print("Programa 1 Mutado:", runTestSuite(programa1_mut, testSuite1))
            print("Programa 2 Mutado:", runTestSuite(programa2_mut, testSuite2))
            print("Programa 3 Mutado:", runTestSuite(programa3_mut, testSuite3))

            print("\n========================  Testar programa com Print ========================")
            print("Programa Print:", runTestSuite(programa_com_print, testPrintSuite))

            print("\n========================  Testar mutações aleatoriamente ========================")
            testar_mutacoes()

            print("\n========================  Testar instrumentation manualmente ========================")
            test_instrumentation_manual()

            print("\n========================  Testar instrumentedTestSuite com trace ========================")
            test_instrumentedTestSuite_verbose()

            print("\n========================  Testar instrumentedTestSuite ========================")
            result = instrumentedTestSuite(programa1, testSuite1)
            print("instrumentedTestSuite para programa1:", result)

if __name__ == "__main__":
    main()

