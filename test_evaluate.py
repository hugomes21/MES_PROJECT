from Lang import *
from evaluate import *
from contextlib import redirect_stdout

# Test suites para programa1 a programa3 (como exigido pelo enunciado para runTestSuite)
testSuite1 = [ ([("x", 10)], 15) ]  # y = x + 5 → 15
testSuite2 = [ ([], 4) ]           # max = b → 4
testSuite3 = [ ([], 10) ]          # sum = 1+2+3+4 → 10

# Programas mutados
programa1_mut = Program([
    Assign("x", IntLit(10)),
    Assign("y", BinOp("-", Var("x"), IntLit(5)))
])
programa2_mut = Program([
    Assign("a", IntLit(3)),
    Assign("b", IntLit(4)),
    If(
        condition=BinOp("<", Var("a"), Var("b")),
        then_branch=[Assign("max", Var("a"))],
        else_branch=[Assign("max", Var("b"))]
    )
])
programa3_mut = Program([
    Assign("sum", IntLit(0)),
    For(
        var="i",
        start=IntLit(1),
        end=IntLit(5),
        body=[
            Assign("sum", BinOp("-", Var("sum"), Var("i")))
        ]
    )
])

# Programa com instrução Print
programa_com_print = Program([
    Assign("x", IntLit(42)),
    Print(Var("x")),
    Return(Var("x"))
])

# Teste para programa com Print
testPrintSuite = [ ([], 42) ]

# Aplicar mutação aleatória ao programa1
mutated_programa1 = mutate(programa1)

def test_all_with_evaluate():
    print("=== Testar evaluate() para programa1 a programa14 ===")
    for i in range(1, 15):
        prog = globals().get(f"programa{i}")
        if not prog:
            continue
        try:
            result = evaluate(prog, [])
            print(f"Programa {i}: resultado = {result}")
        except Exception as e:
            print(f"Programa {i}: erro → {e}")

def test_all_with_runTest():
    print("\n=== Testar runTest() para programa1 a programa14 ===")
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
    print("\n=== Testar instrumentation manualmente ===")
    instr = instrumentation(programa1)
    print("Programa 1 instrumentado:")
    print(instr)

def test_instrumentedTestSuite_verbose():
    print("\n=== Testar instrumentedTestSuite com trace ===")
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

            print("\n=== Testar runTestSuite() para os 3 programas escolhidos ===")
            print("Programa 1:", runTestSuite(programa1, testSuite1))
            print("Programa 2:", runTestSuite(programa2, testSuite2))
            print("Programa 3:", runTestSuite(programa3, testSuite3))

            print("\n=== Testar runTestSuite() para os 3 programas mutados ===")
            print("Programa 1 Mutado:", runTestSuite(programa1_mut, testSuite1))
            print("Programa 2 Mutado:", runTestSuite(programa2_mut, testSuite2))
            print("Programa 3 Mutado:", runTestSuite(programa3_mut, testSuite3))

            print("\n=== Testar programa com Print ===")
            print("Programa Print:", runTestSuite(programa_com_print, testPrintSuite))

            print("\n=== Testar programa1 mutado aleatoriamente ===")
            print("Programa 1 Mutado Aleatoriamente:", runTest(mutated_programa1, testSuite1[0]))

            test_instrumentation_manual()
            test_instrumentedTestSuite_verbose()

            print("\n=== Testar instrumentedTestSuite ===")
            result = instrumentedTestSuite(programa1, testSuite1)
            print("instrumentedTestSuite para programa1:", result)

if __name__ == "__main__":
    main()

